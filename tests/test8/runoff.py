"""
########################################################################
The runoff.py module contains a function to setup and run pyfao56
for rainfed conditions in a 2015 hypothetical corn field in McLean
county, IL.  This is to demonstrate the runoff produced due to heavy
rainfall using the MOP70 runoff method.

The runoff.py module contains the following:
    run - function to setup and run pyfao56 for the rainfed conditions
    in a 2015 hypothetical corn field in McLean county, IL using the 
    MOP70 runoff method.
    plot - makes time series plots of water balance variables

01/22/2024 - Script developed for testing runoff by Dinesh Gulati
02/07/2024 - Edits for pyfao56 release
########################################################################
"""

import os
import matplotlib.pyplot as plt
import pyfao56 as fao

#function to plot and visualize different water balance components
def plot(results):
    fig = plt.figure(figsize=(16,9), dpi=250)
    ax1 = plt.subplot(311)
    plt.plot(results['DOY'],results['Ks'],color='green',ls='--',
             label='Ks')
    ax1.set_ylabel('Ks')
    ax1.set_xticks([])
    plt.legend()

    ax01  = ax1.twinx()
    plt.plot(results['DOY'],results['ETc'],color='coral',label='ETc')
    plt.plot(results['DOY'],results['ETcadj'],color='olive',
             label='ETc adj')
    ax01.set_ylabel('ETc & ETcadj (mm)')
    ax01.set_xticks([])
    plt.legend(loc='upper left',)

    ax2 = plt.subplot(312)
    ax2.set_ylabel('Rainfall & Runoff (mm)')
    ax2.set_xticks([])
    plt.bar(results['DOY'],results['Rain'],color='dodgerblue',alpha=0.6,
            label='Rainfall')
    plt.bar(results['DOY'],results['Runoff'],color='yellow',
            label='Runoff')
    plt.legend()

    ax3 = plt.subplot(313)
    ax3.set_ylim(results['TAW'].iloc[-1]+10,0)
    ax3.set_xlabel('DOY')
    ax3.set_xticks([])
    ax3.set_ylabel('TAW, RAW, Dr & DP (mm)')
    plt.plot(results['DOY'],results['TAW'],color='blue',label='TAW')
    plt.plot(results['DOY'],results['RAW'],color='darkslategrey',
             lw=2,label='RAW')
    plt.plot(results['DOY'],results['Dr'],color='red', alpha=0.7,
             label='Dr' )
    plt.bar(results['DOY'],results['DP'],color='goldenrod',
            label='Percolation')
    plt.legend()
    plt.savefig('results.png', bbox_inches='tight')
    return plt.show()

def run():
    """Setup and run pyfao56 for a 2015 Illinois corn field"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters in a Parameters object
    par = fao.Parameters()
    #crop parameters
    par.Kcbmid = 1.05
    par.Kcbend = 0.15
    par.Lini = 24
    par.Ldev = 32
    par.Lmid = 40
    par.Lend = 41
    par.hini = 0.01 # initial Plant height
    par.hmax = 2 # from FAO-56
    par.Zrini = 0.2
    par.Zrmax = 1.20 #from FAO-56 1.0-2.0
    par.pbase = 0.55 #from Table 22, FAO-56
    par.CN2 = 75
    #soil parameters
    #soil properties for the site were fetched from USDA-NRCS data
    #hosted at the web soil survey at centroid of McLean county, IL
    par.Ze = 0.1
    par.REW = 9 #8.0-11.0
    par.thetaFC = 0.290
    par.thetaWP = 0.068
    par.theta0 = 0.290 #Intial soil water considered at field capacity
    par_file = os.path.join(module_dir, 'par2015.par')
    par.savefile(par_file)

    #Specify the model weather data from weather file
    #Waether data for crop period was fetched from the GRIDMET dataset
    #at centroid of McLean county, IL
    wth = fao.Weather(comment='2015 McLean,IL weather data')
    wth_file = os.path.join(module_dir, 'met2015.wth')
    wth.loadfile(wth_file)
    wth.savefile(wth_file)
    wth.loadfile(wth_file)

    #Run the model
    #start date- Agricultural handbook no. 628
    #end date- based on GDD
    mdl_mop70 = fao.Model('2015-118','2015-254', par, wth, roff=True,
                comment = '2015 Corn with MOP70 runoff method')

    mdl_mop70.run()
    mdl_mop70.savefile(os.path.join(module_dir,'model_MOP70.out'))
    results_mop70 = mdl_mop70.odata.T.drop_duplicates().T.round(3)
    plot(results_mop70)

if __name__ == '__main__':
    run()
