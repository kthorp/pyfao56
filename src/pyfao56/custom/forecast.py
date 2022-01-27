"""
########################################################################
The forecast.py module contains the Forecast class, which is used to
retrieve seven-day weather forecasts from the National Digital Forecast
Database (NDFD). It uses the REST approach, which was more robust than
the SOAP method, in terms of server responsiveness. Data is retrieved
for computation of ASCE Standardized Reference Evapotranspiration,
including wind speed (m/s) and minimum, maximum, and dew point air
temperatures (degrees C). Solar radiation forecasts are not provided by
NDFD.

#https://graphical.weather.gov/xml/rest.php
#https://graphical.weather.gov/xml/docs/elementInputNames.php

xx/xx/2019 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""
import datetime
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import numpy as np

class Forecast():
    """A class for obtaining weather forecasts from the NDFD

    Obtains weather forecast data from the National Digital Forecast
    Database (NDFD). Given latitude and longitude, the class methods will
    obtain and store a seven-day weather forecast from today forward,
    including wind speed and minimum, maximum, and dew point air
    temperature.

    Attributes
    ----------
    latitude : float
        Site latitude (decimal degrees)
    longitude : float
        Site longitude (decimal degrees)
    forecast : DataFrame
        Weather forecast data from NDFD as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Tmax','Tmin','Tdew','Wndsp']
            Tmax  - Daily maximum air temperature (deg C)
            Tmin  - Daily minimum air temperature (deg C)
            Tdew  - Daily average dew point temperature (deg C)
            Wndsp - Daily average wind speed (m/s)

    Methods
    -------
    getforecast()
        Request and process weather forecast data from NDFD and update
        the self.forecast DataFrame.
    """

    def __init__(self, latitude, longitude):
        """Initialize the Forecast class attributes

        Parameters
        ----------
        latitude : float
            Site latitude (decimal degrees)
        longitude : float
            Site longitude (decimal degrees)
        """

        self.latitude = latitude
        self.longitude = longitude
        self._initialize()

    def __str__(self):
        """Represent the Forecast class variables as a string."""
        pd.options.display.float_format = '{:6.2f}'.format
        s = ('Latitude: {:12.7f}\n'
             'Longitude: {:12.7f}\n\n'
             'NDFD weather forecast data for year-doy:\n'
             ).format(self.latitude, self.longitude)
        s += self.forecast.to_string()
        return s

    def _initialize(self):
        """Initialize the self.forecast DataFrame."""
        init = []
        keys = []
        cols = ['Tmax','Tmin','Tdew','Wndsp']
        today = datetime.datetime.today()
        NaN = float('NaN')
        for i in list(range(-1,10)):
            day = today + datetime.timedelta(days=i)
            keys.append(day.strftime('%Y-%j'))
            init.append([NaN,NaN,NaN,NaN])
        self.forecast = pd.DataFrame(init,index=keys,columns=cols)

    def getforecast(self):
        """Request and process weather forecast data from NDFD."""

        #Submit the request to NDFD.
        request = {}
        request.update({'lat':self.latitude})
        request.update({'lon':self.longitude})
        request.update({'product':'time-series'})
        request.update({'begin':''})
        request.update({'end':''})
        request.update({'Unit':'m'})
        request.update({'maxt':'maxt'})
        request.update({'mint':'mint'})
        request.update({'dew':'dew'})
        request.update({'wspd':'wspd'})
        url = 'https://graphical.weather.gov/xml/sample_products/'
        url+= 'browser_interface/ndfdXMLclient.php'
        r = requests.get(url,params=request)

        #Process the resulting XML string from NDFD.
        tree = ET.fromstring(r.text)
        data = tree.find('data')
        pars = data.find('parameters')

        items = {'Tmax' :['temperature','maximum'  ,'start-valid-time'],
                 'Tmin' :['temperature','minimum'  ,'end-valid-time'  ],
                 'Tdew' :['temperature','dew point','start-valid-time'],
                 'Wndsp':['wind-speed' ,'sustained','start-valid-time']}

        self._initialize()
        times = []
        values = []
        dayvals = []
        today = datetime.datetime.today()
        for item in items.keys():
            values[:] = []
            tag = items[item][0]
            att = items[item][1]
            node1 = pars.find("./"+tag+"[@type='"+att+"']")
            for child in node1:
                if child.tag == 'value':
                    values.append(float(child.text))
            tl = node1.attrib['time-layout']
            times[:] = []
            node2 = data.find(".//layout-key[.='"+tl+"']..")
            for child2 in node2:
                if child2.tag == items[item][2]:
                    times.append(child2.text)
            for i in list(range(-1,10)):
                day = today + datetime.timedelta(days=i)
                key1 = day.strftime('%Y-%j')
                dayvals[:] = []
                for j in list(range(len(times))):
                    Ymd='%Y-%m-%d'
                    date = datetime.datetime.strptime(times[j][:10],Ymd)
                    key2 = date.strftime('%Y-%j')
                    if key1 == key2:
                        dayvals.append(values[j])
                if len(dayvals) > 0:
                    mean = np.mean(np.array(dayvals))
                    self.forecast.loc[key1,item] = mean
