"""
########################################################################
The refet_testA.py module contains a function to compare the daily short
crop reference evapotranspiration (ETo) calculation from the pyfao56
refet.py and refet2.py modules with ETo reported by the Arizona
Meteorological Network (AZMET) station at Maricopa, Arizona for 2003
through 2020.

The refet_testA.py module contains the following:
    run - function to compute the root mean squared error (RMSE) between
    daily ETo from pyfao56 and daily ETo from AZMET

11/30/2021 Scripts developed for comparing ETo from pyfao56 and AZMET
09/28/2026 Added functionality to make tests for refet2.py
########################################################################
"""

from pyfao56.custom import AzmetMaricopa
import datetime
import urllib3
import pandas as pd
import numpy as np

def run(start='2003-001',end='2020-366'):
    """Compare daily ETo from pyfao56 and AZMET

    Parameters
    ----------
    start : str
        Start year and doy ('yyyy-ddd')
    end   : str
        End year and doy ('yyyy-ddd')
    """

    #Initialize AzmetMaricopa class and load AZMET weather data
    wth = AzmetMaricopa()
    wth.customload(start,end)

    #Retrieve ETref as computed by AZMET (short crop reference ET, ETo)
    azmet = []
    for year in range(int(start[:4]),int(end[:4])+1):
        print('Retrieving {:4d} AZMET ETo data...'.format(year))
        year2 = ('{:4d}'.format(year))[2:4]
        client = urllib3.PoolManager()
        url = 'azmet.arizona.edu/azmet/data/06'+year2+'rd.txt'
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
            mydict.update({'ETref':float(line[25])})
            azmet.append(mydict)
    azmet = pd.DataFrame(azmet)
    azmet.drop_duplicates(subset='Date',keep='first',inplace=True)
    azmet.set_index('Date',inplace=True)

    startDate = datetime.datetime.strptime(start, '%Y-%j')
    endDate   = datetime.datetime.strptime(end, '%Y-%j')

    #Compare ETo from pyfao56 and AZMET and compute RMSE
    tcurrent = startDate
    tdelta = datetime.timedelta(days=1)
    azmetETo = []
    pyfaoETo = []
    pyfao2ETo = []
    while tcurrent <= endDate:
        mykey = tcurrent.strftime('%Y-%j')
        ETref = wth.compute_etref(mykey,algorithm='refet') #refet.py
        pyfaoETo.append(ETref)
        ETref = wth.compute_etref(mykey,algorithm='refet2') #refet2.py
        pyfao2ETo.append(ETref)
        ETref = azmet.loc[mykey,'ETref'] #AZMET ETref
        azmetETo.append(ETref)
        tcurrent = tcurrent + tdelta

    azmetETo = np.array(azmetETo)
    pyfaoETo = np.array(pyfaoETo)
    pyfao2ETo = np.array(pyfao2ETo)
    conc = np.concatenate(([azmetETo],[pyfaoETo],[pyfao2ETo]),axis=0)
    np.savetxt("outputA.csv",conc.transpose(),delimiter=',')

    rmse = np.sqrt(np.mean((azmetETo-pyfaoETo)**2))

    s  = 'The RMSE between refet.py ETo and AZMET ETo is ' #0.049 mm
    s += '{:6.3f} mm.'.format(rmse)
    print(s)

    rmse = np.sqrt(np.mean((azmetETo-pyfao2ETo)**2))

    s  = 'The RMSE between refet2.py ETo and AZMET ETo is ' #0.049 mm
    s += '{:6.3f} mm.'.format(rmse)
    print(s)

if __name__ == '__main__':
    run()
