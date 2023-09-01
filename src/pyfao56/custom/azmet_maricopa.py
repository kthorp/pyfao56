"""
########################################################################
The azmet_maricopa.py module contains the AzmetMaricopa class, which
inherits from the pyfao56 Weather class in weather.py. AzmetMaricopa
provides specific I/O functionality for obtaining required weather input
data from the Arizona Meteorological Network (AZMET) station in
Maricopa, Arizona.

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

from pyfao56 import Weather
import datetime
import urllib3
import math
import pandas as pd
from pyfao56.tools import Forecast

class AzmetMaricopa(Weather):
    """A class for obtaining weather data for Maricopa, Arizona

    Obtains and prepares weather data from the Arizona Meteorological
    Network (AZMET) station in Maricopa, Arizona. If necessary, obtains
    a 7-day weather forecast for Maricopa from the National Digital
    Forecast Database (NDFD) using the Forecast class in forecast.py.
    Computes ASCE Standardized Reference Evapotranspiration for the
    resulting data set. Checks for missing weather data. The class
    inherits from the pyfao56 Weather class.

    Attributes
    ----------
    rfcrp : str
        Type of reference crop  - Short ('S') or Tall ('T')
    z : float
        Weather station elevation (z) (m)
    lat : float
        Weather station latitude (decimal degrees)
    wndht : float
        Weather station wind speed measurement height (m)
    cnames : list
        Column names for wdata
    wdata : DataFrame
        Weather data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Srad','Tmax','Tmin','Tdew','RHmax','RHmin',
                   'Wndsp','Rain','ETref','MorP']
            Srad  - Incoming solar radiation (MJ/m2)
            Tmax  - Daily maximum air temperature (deg C)
            Tmin  - Daily minimum air temperature (deg C)
            Vapr  - Daily average vapor pressure (kPa)
            Tdew  - Daily average dew point temperature (deg C)
            RHmax - Daily maximum relative humidity (%)
            RHmin - Daily minimum relative humidity (%)
            Wndsp - Daily average wind speed (m/s)
            Rain  - Daily precipitation (mm)
            ETref - Daily reference ET (mm)
            MorP  - Measured ('M') or Predicted ('P') data

    Methods
    -------
    customload(start,end,usefc=True)
        Overridden method from the pyfao56 Weather class to provide
        customization for loading weather data from the Maricopa AZMET
        station and weather forecasts from the National Digital Forecast
        Database (NDFD).
    """

    def customload(self,start,end,rfcrp='S',usefc=True):
        """Prepare the wdata DataFrame with required weather data.

        Parameters
        ----------
        start : str
            Simulation start year and doy ('yyyy-ddd')
        end   : str
            Simulation end year and doy ('yyyy-ddd')
        rfcrp : str, optional
            Define the reference crop (default='S')
        usefc : bool, optional
            Use the 7-day NDFD weather forecast or not (default=True)
        """

        #Define Maricopa weather station parameters
        self.rfcrp = rfcrp   #Set the reference crop
        self.z     = 361.000 #Weather station elevation (z) (m)
        self.lat   = 33.0690 #Weather station latitude (deg)
        self.wndht = 3.00000 #Wind speed measurement height (m)

        #Retrieve AZMET weather history for Maricopa
        print('Retrieving AZMET weather history for Maricopa, AZ...')
        today = datetime.datetime.today()
        azmet = []
        for year in range(1987,int(today.strftime('%Y'))+1):
            print('Retrieving {:4d} data...'.format(year))
            year2 = ('{:4d}'.format(year))[2:4]
            client = urllib3.PoolManager()
            url = 'http://ag.arizona.edu/azmet/data/06'+year2+'rd.txt'
            page = client.request('GET',url,retries=9999)
            weatherdata = page.data.decode('utf-8').split('\n')[:-1]
            for line in weatherdata:
                if line in ['']: continue
                line = line.rstrip().split(',')
                lineyear = int(line[0])
                linedoy = int(line[1])
                if lineyear < 100: lineyear+=1900
                mykey = '{:04d}-{:03d}'.format(lineyear,linedoy)
                mydict = {}
                mydict.update({'Date':mykey})
                if 0.0 <= float(line[10]) <= 110.0:
                    mydict.update({'Srad':float(line[10])})
                if 0.0 <= float(line[3]) <= 55.0:
                    mydict.update({'Tmax':float(line[3])})
                if -15.0 <= float(line[4]) <= 40.0:
                    mydict.update({'Tmin':float(line[4])})
                mydict.update({'Vapr':float('NaN')})
                if year >= 2003:
                    if -50.0 <= float(line[27]) <= 50.0:
                        mydict.update({'Tdew':float(line[27])})
                else:
                    tavg = float(line[5]) #Avg daily temperature
                    havg = float(line[8]) #Avg relative humidity
                    #From https://cals.arizona.edu/azmet/dewpoint.html
                    B = math.log(havg/100.0)+((17.27*tavg)/(237.3+tavg))
                    B = B/17.27
                    D = (237.3*B)/(1-B)
                    if -50.0 <= D <= 50.0:
                        mydict.update({'Tdew':D})
                if 0.0 <= float(line[6]) <= 100.0:
                    mydict.update({'RHmax':float(line[6])})
                if 0.0 <= float(line[7]) <= 100.0:
                    mydict.update({'RHmin':float(line[7])})
                if 0.0 <= float(line[18]) <= 30.0:
                    mydict.update({'Wndsp':float(line[18])})
                if 0.0 <= float(line[11]) <= 200.0:
                    mydict.update({'Rain':float(line[11])})
                azmet.append(mydict)
        azmet = pd.DataFrame(azmet)
        lessvapr = azmet.drop('Vapr', axis=1)
        nanrows = lessvapr.isna().any(1).to_numpy().nonzero()[0]
        for item in nanrows:
            mykey = azmet.loc[item,'Date']
            print('Warning: Questionable weather data: ' + mykey)
        if len(nanrows) > 0:
            result = input('Continue (Y/N)?')
            if result not in ['Y']:
                return

        #Process AZMET data from requested start to end date
        startDate = datetime.datetime.strptime(start, '%Y-%j')
        endDate   = datetime.datetime.strptime(end, '%Y-%j')
        tdelta = datetime.timedelta(days=1)
        yesterday = today - tdelta
        tcurrent = startDate
        future = []
        wthdata = []
        needfuture = False
        print('Processing AZMET weather data...')
        while tcurrent <= endDate:
            mykey = tcurrent.strftime('%Y-%j')
            if tcurrent <= yesterday: #Get data for days prior to today
                daydata = azmet.loc[azmet['Date'] == mykey]
                daydata = daydata.to_dict('records')[0]
                daydata.update({'MorP':'M'})
                wthdata.append(daydata)
            else: #Predict future data as average of past data on a day
                needfuture = True
                future[:] = []
                for year in range(1987,int(tcurrent.strftime('%Y'))):
                    mon = int(tcurrent.strftime('%m')) #month
                    dom = int(tcurrent.strftime('%d')) #day of month
                    if mon==2 and dom==29: #leap day
                        if year%4: #not leapyear, use feb 28 data
                            feb28=tcurrent-tdelta
                        pastdate = feb28.replace(year=year)
                    else:
                        pastdate = tcurrent.replace(year=year)
                    pastkey = pastdate.strftime('%Y-%j')
                    daydata = azmet.loc[azmet['Date'] == pastkey]
                    daydata = daydata.to_dict('records')[0]
                    future.append(daydata)
                futmean = pd.DataFrame(future).drop('Date',1).mean(0)
                futmean = futmean.to_dict()
                futmean['Rain'] = 0.0
                futmean.update({'MorP':'P'})
                futmean.update({'Date':mykey})
                wthdata.append(futmean)
            tcurrent = tcurrent + tdelta
        self.wdata = pd.DataFrame(wthdata)
        self.wdata.drop_duplicates(subset='Date',keep='first',
                                   inplace=True)
        self.wdata.set_index('Date',inplace=True)
        self.wdata.index.name = None
        indx = len(self.wdata.columns)-1
        self.wdata.insert(indx,'ETref',float('NaN'))

        #If needed and wanted, update wdata with 7-day NDFD forecast
        if needfuture and usefc:
            fc = Forecast(33.069,-111.972,wndht=self.wndht)
            fc.getforecast()
            for i in list(range(-1,10)):
                day = today + datetime.timedelta(days=i)
                key = day.strftime('%Y-%j')
                for item in ['Tmax','Tmin','Tdew','Wndsp']:
                    val = fc.forecast.loc[key,item]
                    if not math.isnan(val):
                        self.wdata.loc[key,item] = val

        #Compute ASCE Standardized Reference ET
        for index, row in self.wdata.iterrows():
            etref = self.compute_etref(index)
            self.wdata.loc[index,'ETref'] = etref

        #Check for NaN
        lessvapr = self.wdata.drop('Vapr', axis=1)
        nanrows = lessvapr.isna().any(1).to_numpy().nonzero()[0]
        if len(nanrows) > 0:
            print('There were problems with the following records:')
            for item in nanrows:
                print(self.wdata.iloc[item])
        else:
            print('The weather data was loaded with no issue.')
