"""
########################################################################
The cotton2018.py module from test04 and test09 has been modified to
provide a test of the blue green water routine.

The cotton2018.py module contains the following:
    run - function to setup and run a calibrated pyfao56 model for
          irrigation plots in a 2018 cotton field study at Maricopa

02/07/2022 Scripts developed for running pyfao56 for 2018 cotton data
02/22/2024 Script modified to test the autoirrigation routine.
02/12/2025 Measured soil water content data added to analysis.
03/05/2025 Expanded the analysis to include all plots in the 2018 study
04/22/2025 Finalized optimization of DUL and root depth parameters
02/09/2026 Modified the autoirrigation script to test blue green water
########################################################################
"""

import pyfao56 as fao
import pyfao56.custom as custom
import pyfao56.tools as tools
import os
import time
import sys
import numpy as np
import pandas as pd
import geojson

def run(plot='p06-1'):
    """Setup and run pyfao56 for a 2018 cotton field study"""

    start = time.time()

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2018 Cotton')
    par.Kcmini = 0.35 #FAO-56 Table 12
    par.Kcmmid = 1.18 #FAO-56 Table 12 with adjustments
    par.Kcmend = 0.62 #FAO-56 Table 12 with adjustments
    par.Kcbini = 0.15 #FAO-56 Table 17
    par.Kcbmid = 1.13 #FAO-56 Table 17 with adjustments
    par.Kcbend = 0.52 #FAO-56 Table 17 with adjustments
    par.Lini = 32 #Hunsaker et al. (2005) with adjustments
    par.Ldev = 47 #Hunsaker et al. (2005) with adjustments
    par.Lmid = 37 #Hunsaker et al. (2005) with adjustments
    par.Lend = 35 #Hunsaker et al. (2005) with adjustments
    par.hini = 0.05 #Assumed
    par.hmax = 1.20 #Measured
    par.thetaFC = 0.2050
    par.thetaWP = 0.0980
    par.theta0  = 0.1515
    par.Zrini = 0.18 #Adjusted to eliminate early-season stress
    par.Zrmax = 1.2 #This one optimized below.
    par.pbase = 0.65 #FAO-56 Table 22
    par.Ze = 0.05 #Adjusted to reduce early-season Dr
    par.REW = 4.0 #Adjusted to reduce early-season Dr
    par.savefile(os.path.join(module_dir,'cotton2018.par'))

    #Specify the weather data
    #wth = custom.AzmetMaricopa(comment = '2018 Cotton')
    #wth.customload('2018-108','2018-303')
    #wth.savefile(os.path.join(module_dir,'cotton2018.wth'))
    wth = fao.Weather(comment = '2018 Cotton')
    wth.loadfile(os.path.join(module_dir,'cotton2018.wth'))

    #Specify the full-season irrigation schedule
    irrsched = pd.read_csv(os.path.join(module_dir,'irrigation.csv'))
    irrfull = fao.Irrigation(comment = '2018 Cotton, ' + plot)
    for index, row in irrsched.iterrows():
        irrfull.addevent(int(row['Year']),int(row['DOY']),
                         float(row[plot]),1.0)
    irrfull.savefile(os.path.join(module_dir,'cotton2018_full.irr'))

    #Specify layered soil profile
    watlim = pd.read_csv(os.path.join(module_dir,'waterlimits.csv'))
    watlim = watlim.set_index('PlotID')
    sol = fao.SoilProfile(comment = '2018 Cotton, ' + plot)
    for depth in [40,80,120,160,200]:
        dul = watlim.loc[plot,'SDUL'+'{:03d}'.format(depth)]
        ll  = watlim.loc[plot,'SLLL'+'{:03d}'.format(depth)]
        sol.sdata.loc[depth-20] = [dul,ll,dul]
        sol.sdata.loc[depth]    = [dul,ll,dul]
    sol.savefile(os.path.join(module_dir,'cotton2018.sol'))
    sol.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sol'))

    #Obtain measured soil water content data
    with open(os.path.join(module_dir,'neutronswc.geojson'),'r') as f:
        swcdata = geojson.load(f)
    sws = tools.SoilWaterSeries(par=par,sol=sol)
    for feature in swcdata['features']:
        if feature['properties'].get('tb_label') == plot[1:]:
            swld = feature['properties']['SWLD']
            for key in swld.keys():
                #Assign measurements (made in morning on reported date)
                #to the end of time step on previous day
                mdate = key[0:4] + '-{:03d}'.format(int(key[4:7])-1)
                mvswc = dict()
                for key2 in swld[key].keys():
                    mvswc.update({int(key2)+10:swld[key][key2]})
                swp = sws.SoilWaterProfile(mdate,mvswc,par=par,sol=sol)
                sws.addprofile(mdate,swp)
    sws.savefile(os.path.join(module_dir,'cotton2018.sws'))
    sws.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sws'))

    #Update with optimized DUL and root depth from multiobjective opt
    moofile = 'pyfao56_PostMortem.csv'
    optdul = pd.read_csv(os.path.join(module_dir,moofile))
    optdul = optdul.set_index('Plot')
    for depth in [20,40,60,80,100,120,140,160,180,200]:
        dul = optdul.loc[plot,'DUL'+'{:03d}'.format(depth)]
        sol.sdata.loc[depth,'thetaFC'] = dul
    sol.savefile(os.path.join(module_dir,'cotton2018.sol'))
    sol.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sol'))

    par.Zrmax = optdul.loc[plot,'Zrmax']
    par.savefile(os.path.join(module_dir,'cotton2018.par'))
    par.savefile(os.path.join(module_dir,'cotton2018'+plot+'.par'))

    #Adjust theta0 to first neutron SWC measurement per depth
    for depth in [20,40,60,80,100,120,140,160,180,200]:
        #dul = 0.0
        #for mdate in sws.swdata.keys():
        #    if depth in sws.swdata[mdate].mvswc.keys():
        #        dul = max(sws.swdata[mdate].mvswc[depth],dul)
        dul = sol.sdata.loc[depth,'thetaFC']
        ll = sol.sdata.loc[depth,'thetaWP']
        theta0 = sws.swdata['2018-123'].mvswc[depth]
        sol.sdata.loc[depth] = [dul,ll,theta0]
    sol.savefile(os.path.join(module_dir,'cotton2018.sol'))
    sol.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sol'))
    sws.updatesol(sol)
    sws.updatepar(par)

    #Instantiate Model class
    mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        irr=irrfull, K_adj=True)

    #Run the model
    mdl.run()
    #print(mdl)
    mdl.savefile(os.path.join(module_dir,'cotton2018.out'))
    mdl.savesums(os.path.join(module_dir,'cotton2018.sum'))

    #Instantiate BlueGreen class
    res_bg = tools.BlueGreen(mdl, cg=0.5, cb=0.5,
                             comment = 'initial test')

    #Run the blue green partitioning
    res_bg.run()

    #Print output
    print(res_bg)

    #Save BG results
    res_bg.savefile()

    # Plot color-coded fluxes
    res_bg.plot(var='ETa', filename='example_bg.png')

    end=time.time()
    #print('Elapsed time = {:f} s'.format(end-start))

if __name__ == '__main__':
    run('p06-1')
