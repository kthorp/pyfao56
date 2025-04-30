"""
########################################################################
The cotton2018.py module from test4 has been modified to provide tests
of the autoirrigation routines.

The cotton2018.py module contains the following:
    run - function to setup and run pyfao56 for irrigation treatments in
          a 2018 cotton field study at Maricopa, Arizona

02/07/2022 Scripts developed for running pyfao56 for 2018 cotton data
02/22/2024 Script modified to test the autoirrigation routine.
02/12/2025 Measured soil water content data added to analysis.
03/05/2025 Expanded the analysis to include all plots in the 2018 study
04/22/2025 Finalized optimization of DUL and root depth parameters
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

def run(case=0, plot='p06-1'):
    """Setup and run pyfao56 for a 2018 cotton field study"""

    start = time.time()

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2018 Cotton')
    par.Kcmini = 0.35 #FAO-56 Table 12
    par.Kcmmid = 1.18 #FAO-56 Table 12 plus adjustments
    par.Kcmend = 0.62 #FAO-56 Table 12 plus adjustments
    par.Kcbini = 0.15 #FAO-56 Table 17
    par.Kcbmid = 1.13 #FAO-56 Table 17 plus adjustments
    par.Kcbend = 0.52 #FAO-56 Table 17 plus adjustments
    par.Lini = 32 #Hunsaker et al. (2005) plus adjustments
    par.Ldev = 47 #Hunsaker et al. (2005) plus adjustments
    par.Lmid = 37 #Hunsaker et al. (2005) plus adjustments
    par.Lend = 35 #Hunsaker et al. (2005) plus adjustments
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

    #Specify the first half of the irrigation schedule
    irrhalf = fao.Irrigation(comment = '2018 Cotton, ' + plot)
    for index, row in irrsched.iterrows():
        if int(row['DOY']) < 188:
            irrhalf.addevent(int(row['Year']),int(row['DOY']),
                             float(row[plot]),1.0)
    irrhalf.savefile(os.path.join(module_dir,'cotton2018_half.irr'))

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
                #Assign measurements (made in the morning on reported date)
                #to the end of time step on previous day
                mdate = key[0:4] + '-{:03d}'.format(int(key[4:7])-1)
                mvswc = dict()
                for key2 in swld[key].keys():
                    mvswc.update({int(key2)+10:swld[key][key2]})
                swp = sws.SoilWaterProfile(mdate,mvswc,par=par,sol=sol)
                sws.addprofile(mdate,swp)
    sws.savefile(os.path.join(module_dir,'cotton2018.sws'))
    sws.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sws'))

    #Update with optimized DUL and root depth from multiobjective optimization
    optdul = pd.read_csv(os.path.join(module_dir,'pyfao56_PostMortem.csv'))
    optdul = optdul.set_index('Plot')
    for depth in [20,40,60,80,100,120,140,160,180,200]:
        dul = optdul.loc[plot,'DUL'+'{:03d}'.format(depth)]
        sol.sdata.loc[depth,'thetaFC'] = dul
    sol.savefile(os.path.join(module_dir,'cotton2018.sol'))
    sol.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sol'))

    par.Zrmax = optdul.loc[plot,'Zrmax']
    par.savefile(os.path.join(module_dir,'cotton2018.par'))

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

    #Instantiate AutoIrrigate class
    airr = fao.AutoIrrigate()

    #Case 0: Actual irrigation record, No autoirrigation
    if case==0:
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        irr=irrfull, K_adj=True)
    #Case 1: Minimal autoirrigation input case
    #        Autoirrigate yesterday's Dr every day from start to end
    elif case==1:
        airr.addset('2018-108','2018-250')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 2: Mixing half-season record and autoirrigation
    #        alre is 'True' by default
    #        Actual irrigation record for first half season
    #        Then autoirrigate yesterday's Dr in last half season
    elif case==2:
        airr.addset('2018-108','2018-250')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        irr=irrhalf, autoirr=airr, K_adj=True)
    #Case 3: Full season autoirrigate with mad = 0.4
    elif case==3:
        airr.addset('2018-108','2018-250',mad=0.4)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 4: Autoirrigate with mad = 0.4 only on Tuesday and Friday
    elif case==4:
        airr.addset('2018-108','2018-250',mad=0.4,idow='25')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 5: Autoirrigate with mad = 0.3, but cancel autoirrigation
    #        if 25 mm rain coming in the next three days
    elif case==5:
        airr.addset('2018-108','2018-250',mad=0.3,fpdep=25.,fpday=3,
                    fpact='cancel')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 6: Autoirrigate with mad = 0.3, but if 25 mm rain coming in
    #        the next three days, reduce irrigation by rain amount.
    elif case==6:
        airr.addset('2018-108','2018-250',mad=0.3,fpdep=25.,fpday=3,
                    fpact='reduce')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 7: Autoirrigate based on Dr, not fractional Dr.
    #        Notice lack of irrigation until June when root zone
    #        increases enough to have 40 mm of storage.
    elif case==7:
        airr.addset('2018-108','2018-250',madDr=40.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 8: Fix problem with early season irrigation in Case 7.
    elif case==8:
        airr.addset('2018-108','2018-120',madDr=10.)
        airr.addset('2018-121','2018-150',madDr=20.)
        airr.addset('2018-150','2018-250',madDr=40.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 9: Autoirrigate when Ks > 0.6.
    #        There is timestep issue with this method.
    elif case==9:
        airr.addset('2018-108','2018-250',ksc=0.6)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 10: Autoirrigate every 6 days
    elif case==10:
        airr.addset('2018-108','2018-250',dsli=6)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 11: Autoirrigate every 4 days or sooner with mad=0.3
    #         Early season mad driven, Late season dsli driven
    elif case==11:
        airr.addset('2018-108','2018-250',dsli=4)
        airr.addset('2018-108','2018-250',mad=0.3)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 12: Autoirrigate every 5 days after watering event > 14 mm
    elif case==12:
        airr.addset('2018-108','2018-250',dsle=5,evnt=14.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 13: Autoirrigate 20 mm constant rate every 4 days
    elif case==13:
        airr.addset('2018-108','2018-250',dsli=4,icon=20.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 14: Autoirrigate with mad=0.5 targeting 15 mm Dr deficit
    #         #Mostly nonsensible scheduling in the early season
    elif case==14:
        airr.addset('2018-108','2018-250',mad=0.5,itdr=15.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 15: Autoirrigate with mad=0.5 targeting 0.1 fDr deficit
    #         Somewhat more sensible than Case 14.
    elif case==15:
        airr.addset('2018-108','2018-250',mad=0.5,itfdr=0.1)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 16: Autoirrigate every 5 days with 5-day ET replacement
    #         less precipitation. Default ET is ETa.
    elif case==16:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5,ettyp='ETa')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 17: Autoirrigate with mad=0.4 and replace ET less
    #         precipitation since last irrigation event. Default ET is
    #         ETa.
    elif case==17:
        airr.addset('2018-108','2018-250',mad=0.4,ietri=True)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 18: Autoirrigate with mad=0.4 and replace ET less
    #         precipitation since last watering event > 14 mm.
    #         Default ET is ETa.
    elif case==18:
        airr.addset('2018-108','2018-250',mad=0.4,evnt=14,ietre=True)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 19: Autoirrigate every 5 days with 5-day ET replacement
    #         less precipitation. Use ETc instead of ETa.
    elif case==19:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5,ettyp='ETc')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 20: Autoirrigate with mad=0.45 and apply 90% of Dr
    elif case==20:
        airr.addset('2018-108','2018-250',mad=0.45,iper=90.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 21: Autoirrigate with mad=0.45 considering an application
    #         efficiency of 80%.
    elif case==21:
        airr.addset('2018-108','2018-250',mad=0.45,ieff=80.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 22: Autoirrigate with mad=0.3 considering a minimum
    #         application rate of 12 mm.
    elif case==22:
        airr.addset('2018-108','2018-250',mad=0.3,imin=12.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 23: Autoirrigate with mad=0.3 considering a minimum
    #         application rate of 12 mm and maximum rate of 24 mm.
    elif case==23:
        airr.addset('2018-108','2018-250',mad=0.3,imin=12.,imax=24.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 24: Autoirrigate with mad=0.4 and specify fw for the
    #         irrigation method at 0.5
    elif case==24:
        airr.addset('2018-108','2018-250',mad=0.4,fw=0.5)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    else:
        print("No case for input value.")
        return

    #Test save and load methods
    airr.savefile(os.path.join(module_dir,'cotton2018.ati'))
    airr.loadfile(os.path.join(module_dir,'cotton2018.ati'))

    #Run the model
    mdl.run()
    #print(mdl)
    mdl.savefile(os.path.join(module_dir,'cotton2018.out'))
    mdl.savesums(os.path.join(module_dir,'cotton2018.sum'))

    if case==0:

        #Analyze measured soil water data
        for key in sorted(sws.swdata.keys()):
            #print('Computing soil water depletion for {:s}'.format(key))
            sws.swdata[key].getZr(mdl)
            sws.swdata[key].computeDr()
            sws.swdata[key].computeKs(mdl)
        sws.savefile(os.path.join(module_dir,'cotton2018.sws'))
        sws.savefile(os.path.join(module_dir,'cotton2018'+plot+'.sws'))

        #Compute fit statistics
        sDr = list()
        mDr = list()
        for key in sorted(sws.swdata.keys()):
            sDr.append(mdl.odata.loc[key,'Dr'])
            mDr.append(sws.swdata[key].mDr)
        statsDr = tools.Statistics(sDr,mDr,comment='Dr')
        #print(statsDr)
        filename='cotton2018case0'+plot+'.fit'
        statsDr.savefile(os.path.join(module_dir,filename))
        print(plot,statsDr.stats['rmse'],statsDr.stats['nse'],statsDr.stats['kge'])

    #Plot measured and simulated data
    vis = tools.Visualization(mdl, sws=sws, dayline=True)
    filename='cotton2018case{:d}'.format(case)+plot+'_Dr.png'
    pngpath = os.path.join(module_dir, filename)
    vis.plot_Dr(drmax=False,raw=False,events=True,obs=True,ks=True,
                dpro=True,filepath=pngpath,show=False)
    #filename='cotton2018_'+plot+'_ET.png'
    #pngpath = os.path.join(module_dir, filename)
    #vis.plot_ET(show=True,filepath=pngpath)
    #filename='cotton2018_'+plot+'_Kc.png'
    #pngpath = os.path.join(module_dir, filename)
    #vis.plot_Kc(show=True,filepath=pngpath)

    end=time.time()
    #print('Elapsed time = {:f} s'.format(end-start))

if __name__ == '__main__':
    case = int(sys.argv[1])
    plots = ['p01-1','p01-2','p01-3','p01-4',
             'p02-1','p02-2','p02-3','p02-4',
             'p03-1','p03-2','p03-3','p03-4',
             'p04-1','p04-2','p04-3','p04-4',
             'p05-1','p05-2','p05-3','p05-4',
             'p06-1','p06-2','p06-3','p06-4',
             'p07-1','p07-2','p07-3','p07-4',
             'p08-1','p08-2','p08-3','p08-4',
             'p09-1','p09-2','p09-3','p09-4',
             'p10-1','p10-2','p10-3','p10-4',
             'p11-1','p11-2','p11-3','p11-4',
             'p12-1','p12-2','p12-3','p12-4',
             'p13-1','p13-2','p13-3','p13-4',
             'p14-1','p14-2','p14-3','p14-4',
             'p15-1','p15-2','p15-3','p15-4',
             'p16-1','p16-2','p16-3','p16-4']
    if case==0:
        for plot in plots:
            run(case,plot)
    else:
        run(case,'p06-1')
