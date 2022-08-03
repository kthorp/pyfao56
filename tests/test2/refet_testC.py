"""
########################################################################
The refet_testC.py module contains a function to compare the hourly
short crop reference evapotranspiration (ETo) and hourly tall crop
reference evapotranspiration (ETr) calculations from the pyfao56
refet.py module with ETo and ETr computed by Ref-ET software (University
of Idaho) based on weather data from the Arizona Meteorological Network
(AZMET) station at Maricopa, Arizona for 2003 through 2020.

The refet_testC.py module contains the following:
    run - function to compute the root mean squared error (RMSE) between
    hourly reference ET from pyfao56 and that from Ref-ET software

08/01/2022 Scripts developed for comparing ET from pyfao56 and Ref-ET
########################################################################
"""

import os
import datetime
import urllib3
import math
import pandas as pd
import numpy as np
from pyfao56 import refet

def run(start='2003-001',end='2020-366'):
    """Compare hourly ETo and ETr from pyfao56 and Ref-ET software

    Parameters
    ----------
    start : str
        Start year and doy ('yyyy-ddd')
    end   : str
        End year and doy ('yyyy-ddd')
    """

    #Get the installation directory for the package
    pdir = os.path.dirname(os.path.abspath(__file__))

    #Load hourly AZMET data into an array
    today = datetime.datetime.today()
    azmet = []
    for year in range(1987,int(today.strftime('%Y'))+1):
        print('Retrieving {:4d} data...'.format(year))
        year2 = ('{:4d}'.format(year))[2:4]
        client = urllib3.PoolManager()
        url = 'http://ag.arizona.edu/azmet/data/06'+year2+'rh.txt'
        page = client.request('GET',url,retries=9999)
        weatherdata = page.data.decode('utf-8').split('\n')[:-1]
        for line in weatherdata:
            if line in ['']: continue
            if line[:14] == '89,365,24,18.1': continue
            line = line.rstrip().split(',')
            item = list()
            if int(line[0]) < 100:
                item.append(float(line[0])+1900) #year [0]
            else:
                item.append(float(line[0])) #year [0]
            item.append(float(line[1])) #doy [1]
            item.append(float(line[2])) #hour [2]
            if 0.0 <= float(line[6]) <= 10.0:
                item.append(float(line[6])) #srad [3]
            else:
                item.append(float('NaN'))
            if -55.0 <= float(line[3]) <= 55.0:
                item.append(float(line[3])) #tavg [4]
            else:
                item.append(float('NaN'))
            if item[0] >= 2003:
                if -50.0 <= float(line[17]) <= 50.0:
                    item.append(float(line[17])) #tdew [5]
                else:
                    item.append(float('NaN'))
            else:
                tavg = float(line[3]) #Avg temperature
                havg = float(line[4]) #Avg relative humidity
                #From https://cals.arizona.edu/azmet/dewpoint.html
                B = math.log(havg/100.0)+((17.27*tavg)/(237.3+tavg))
                B = B/17.27
                D = (237.3*B)/(1-B)
                if -50.0 <= D <= 50.0:
                    item.append(D) #tdew[5]
                else:
                    item.append(float('NaN'))
            if 0.0 <= float(line[4]) <= 100.0:
                item.append(float(line[4])) #rhum [6]
            else:
                item.append(float('NaN'))
            if 0.0 <= float(line[10]) <= 30.0:
                item.append(float(line[10])) #wndsp [7]
            else:
                item.append(float('NaN'))
            if 0.0 <= float(line[7]) <= 200.0:
                item.append(float(line[7])) #rain [8]
            else:
                item.append(float('NaN'))
            azmet.append(item)
    azmet = np.array(azmet)
    nanrows = azmet[np.isnan(azmet).any(axis=1)]
    for item in nanrows:
        mykey = '{:04d}-{:03d}-{:02d}'.format(int(item[0]),
                                              int(item[1]),
                                              int(item[2]))
        print('Warning: Questionable weather data: ' + mykey)
    if len(nanrows) > 0:
        result = input('Continue (Y/N)?')
        if result not in ['Y']:
            return
    #print(azmet)

    #Lots of missing hourly data prior to 2003.
    #For 2003 to present, only 2008d107 has missing hourly data.
    #Replace 2008d107 missing data with data from 2008d106
    for i, row in enumerate(azmet):
        if int(row[0])==2008 and int(row[1])==107:
            if math.isnan(row[3]):
                azmet[i] = azmet[i-24]
                azmet[i,1] = 107.

    #Compute hourly ASCE Standardized Reference ET
    #Define Maricopa weather station parameters
    z     = 361.000     #Weather station elevation (z) (m)
    lat   = 33.068941   #Weather station latitude (deg)
    lon   = -111.972244 #Weather station longitude (deg)
    lzn   = 105.0000    #Longitude at center of local time zone (deg)
    wndht = 3.00000     #Wind speed measurement height (m)
    fcdo  = 1.0         #Initial cloudiness for ETo
    fcdr  = 1.0         #Initial cloudiness for ETr
    etos=[]
    etrs=[]
    for row in azmet:
        eto, fcdo = refet.ascehourly('S',z,lat,lon,lzn,
                                     row[1], #doy
                                     row[2]-.5, #sct
                                     row[3], #israd
                                     row[4], #tavg
                                     float('NaN'), #vapr
                                     row[5], #tdew
                                     row[6], #rhum
                                     float('NaN'), #tmin
                                     row[7], #wndsp
                                     wndht, #wndht
                                     1.0, #tl
                                     'D', #csreq
                                     fcdo) #fcdpt
        etos.append(eto)
        etr, fcdr = refet.ascehourly('T',z,lat,lon,lzn,
                                     row[1], #doy
                                     row[2]-.5, #sct
                                     row[3], #israd
                                     row[4], #tavg
                                     float('NaN'), #vapr
                                     row[5], #tdew
                                     row[6], #rhum
                                     float('NaN'), #tmin
                                     row[7], #wndsp
                                     wndht, #wndht
                                     1.0, #tl
                                     'D', #csreq
                                     fcdr) #fcdpt
        etrs.append(etr)
    n = len(etos)
    etos = np.array(etos)
    etos = np.reshape(etos,(n,1))
    n = len(etrs)
    etrs = np.array(etrs)
    etrs = np.reshape(etrs,(n,1))
    azmet = np.concatenate((azmet,etos,etrs),axis=1)
    azmet = pd.DataFrame(azmet,columns=['Year','DOY','Hour','Srad',
                                        'Tavg','Tdew','Rhum','Wndsp',
                                        'Rain','ETo','ETr'])
    azmet.insert(0,'Date','')
    azmet['Date'] = azmet.apply(lambda row : makedate(row), axis=1)
    azmet.drop_duplicates(subset='Date',keep='first',inplace=True)
    azmet.set_index('Date',inplace=True)

    #Order the results by date and write to a file
    f = open(os.path.join(pdir,'AZMET_Maricopa_hourlyEToETr.txt'),'w')
    f.write('Year DOY Hr   Srad   Tavg   Tdew   Rhum  Wndsp')
    f.write('   Rain    ETo    ETr\r\n') #REF-ET requires Windows EOL
    startDate = datetime.datetime.strptime(start, '%Y-%j')
    endDate   = datetime.datetime.strptime(end, '%Y-%j')
    tdelta = datetime.timedelta(days=1)
    tcurrent = startDate
    while tcurrent <= endDate:
        for hr in list(range(1,25)):
            mykey = tcurrent.strftime('%Y-%j')
            mykey = mykey + '-{:02d}'.format(hr)
            s='{:04d} '.format(int(azmet.loc[mykey,'Year']))
            s+='{:03d} '.format(int(azmet.loc[mykey,'DOY']))
            s+='{:02d} '.format(int(azmet.loc[mykey,'Hour']))
            s+='{:6.2f} '.format(azmet.loc[mykey,'Srad'])
            s+='{:6.2f} '.format(azmet.loc[mykey,'Tavg'])
            s+='{:6.2f} '.format(azmet.loc[mykey,'Tdew'])
            s+='{:6.2f} '.format(azmet.loc[mykey,'Rhum'])
            s+='{:6.2f} '.format(azmet.loc[mykey,'Wndsp'])
            s+='{:6.2f} '.format(azmet.loc[mykey,'Rain'])
            s+='{:6.2f} '.format(azmet.loc[mykey,'ETo'])
            s+='{:6.2f}'.format(azmet.loc[mykey,'ETr'])
            f.write(s+'\r\n')
            print(s)
        tcurrent = tcurrent + tdelta
    f.close()

    #Load reference ET data (ETo and ETr) from Ref-ET output file
    f = open(os.path.join(pdir,'AZMET_Maricopa_hourlyEToETr.out'),'r')
    lines = f.readlines()
    f.close()
    RefET = []
    for line in lines[77:157879]:
        line = line.strip().split()
        mon = int(line[0])
        dom = int(line[1])
        year = int(line[2])
        hour = int(int(line[4])/100)
        ETr = float(line[10])
        ETo = float(line[11])
        date = '{:02d}-{:02d}-{:04d}'.format(mon,dom,year)
        date = datetime.datetime.strptime(date,'%m-%d-%Y')
        mykey = date.strftime('%Y-%j')+'-{:02d}'.format(hour)
        RefET.append({'Date':mykey,'ETr':ETr,'ETo':ETo})
    RefET = pd.DataFrame(RefET)
    RefET.drop_duplicates(subset='Date',keep='first',inplace=True)
    RefET.set_index('Date',inplace=True)

    #Compare ETo and ETr from pyfao56 and Ref-ET and compute RMSE
    tcurrent = startDate
    refetETo = []
    pyfaoETo = []
    refetETr = []
    pyfaoETr = []
    while tcurrent <= endDate:
        for hr in list(range(1,25)):
            mykey = tcurrent.strftime('%Y-%j')+'-{:02d}'.format(hr)
            pyfaoETo.append(azmet.loc[mykey,'ETo'])
            refetETo.append(RefET.loc[mykey,'ETo'])
            pyfaoETr.append(azmet.loc[mykey,'ETr'])
            refetETr.append(RefET.loc[mykey,'ETr'])
        tcurrent = tcurrent + tdelta

    refetETo = np.array(refetETo)
    pyfaoETo = np.array(pyfaoETo)
    refetETr = np.array(refetETr)
    pyfaoETr = np.array(pyfaoETr)
    conc = np.concatenate(([refetETo],[pyfaoETo],
                           [refetETr],[pyfaoETr]),axis=0)
    np.savetxt("outputC.csv",conc.transpose(),delimiter=',')

    rmseETo = np.sqrt(np.mean((refetETo-pyfaoETo)**2))
    rmseETr = np.sqrt(np.mean((refetETr-pyfaoETr)**2))

    s  = 'The RMSE between pyfao56 ETo and Ref-ET ETo is ' #0.057 mm
    s += '{:6.3f} mm.'.format(rmseETo)
    print(s)
    s  = 'The RMSE between pyfao56 ETr and Ref-ET ETr is ' #0.070 mm
    s += '{:6.3f} mm.'.format(rmseETr)
    print(s)

def makedate(row):
    year = int(row['Year'])
    doy = int(row['DOY'])
    hour = int(row['Hour'])
    date = '{:04d}-{:03d}-{:02d}'.format(year,doy,hour)
    return date

if __name__ == '__main__':
    run()
