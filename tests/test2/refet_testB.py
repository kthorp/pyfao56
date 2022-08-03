"""
########################################################################
The refet_testB.py module contains a function to compare the daily short
crop reference evapotranspiration (ETo) and daily tall crop reference
evapotranspiration (ETr) calculations from the pyfao56 refet.py module
with ETo and ETr computed by Ref-ET software (University of Idaho) based
on weather data from the Arizona Meteorological Network (AZMET) station
at Maricopa, Arizona for 2003 through 2020.

The refet_testB.py module contains the following:
    run - function to compute the root mean squared error (RMSE) between
    daily reference ET from pyfao56 and that from Ref-ET software

12/02/2021 Scripts developed for comparing ET from pyfao56 and Ref-ET
########################################################################
"""

import os
from pyfao56.custom import AzmetMaricopa
import datetime
import urllib3
import pandas as pd
import numpy as np

def run(start='2003-001',end='2020-366'):
    """Compare daily ETo and ETr from pyfao56 and Ref-ET software

    Parameters
    ----------
    start : str
        Start year and doy ('yyyy-ddd')
    end   : str
        End year and doy ('yyyy-ddd')
    """

    #Get the installation directory for the package
    package_dir = os.path.dirname(os.path.abspath(__file__))

    #Initialize AzmetMaricopa classes for ETo and ETr, load AZMET data
    wthETo = AzmetMaricopa()
    wthETo.customload(start,end)
    wthETo.savefile(os.path.join(package_dir,'AZMET_Maricopa_ETo.wth'))
    wthETr = AzmetMaricopa()
    wthETr.customload(start,end,rfcrp='T')
    wthETr.savefile(os.path.join(package_dir,'AZMET_Maricopa_ETr.wth'))

    #Load reference ET data (ETo and ETr) from Ref-ET output file
    f = open(os.path.join(package_dir,'RefET.out'),'r')
    lines = f.readlines()
    f.close()
    refet = []
    for line in lines[75:6650]:
        line = line.strip().split()
        mon = int(line[0])
        dom = int(line[1])
        year = int(line[2])
        ETr = float(line[8])
        ETo = float(line[9])
        date = '{:02d}-{:02d}-{:04d}'.format(mon,dom,year)
        date = datetime.datetime.strptime(date,'%m-%d-%Y')
        mykey = date.strftime('%Y-%j')
        refet.append({'Date':mykey,'ETr':ETr,'ETo':ETo})
    refet = pd.DataFrame(refet)
    refet.drop_duplicates(subset='Date',keep='first',inplace=True)
    refet.set_index('Date',inplace=True)

    startDate = datetime.datetime.strptime(start, '%Y-%j')
    endDate   = datetime.datetime.strptime(end, '%Y-%j')

    #Compare ETo and ETr from pyfao56 and Ref-ET and compute RMSE
    tcurrent = startDate
    tdelta = datetime.timedelta(days=1)
    refetETo = []
    pyfaoETo = []
    refetETr = []
    pyfaoETr = []
    while tcurrent <= endDate:
        mykey = tcurrent.strftime('%Y-%j')
        ETref = wthETo.compute_etref(mykey) #pyfao56 ETo
        pyfaoETo.append(ETref)
        ETref = refet.loc[mykey,'ETo'] #Ref-ET ETo
        refetETo.append(ETref)
        ETref = wthETr.compute_etref(mykey) #pyfao56 ETr
        pyfaoETr.append(ETref)
        ETref = refet.loc[mykey,'ETr'] #Ref-ET ETr
        refetETr.append(ETref)
        tcurrent = tcurrent + tdelta

    refetETo = np.array(refetETo)
    pyfaoETo = np.array(pyfaoETo)
    refetETr = np.array(refetETr)
    pyfaoETr = np.array(pyfaoETr)
    conc = np.concatenate(([refetETo],[pyfaoETo],
                           [refetETr],[pyfaoETr]),axis=0)
    np.savetxt("outputB.csv",conc.transpose(),delimiter=',')

    rmseETo = np.sqrt(np.mean((refetETo-pyfaoETo)**2))
    rmseETr = np.sqrt(np.mean((refetETr-pyfaoETr)**2))

    s  = 'The RMSE between pyfao56 ETo and Ref-ET ETo is ' #0.070 mm
    s += '{:6.3f} mm.'.format(rmseETo)
    print(s)
    s  = 'The RMSE between pyfao56 ETr and Ref-ET ETr is ' #0.071 mm
    s += '{:6.3f} mm.'.format(rmseETr)
    print(s)

if __name__ == '__main__':
    run()
