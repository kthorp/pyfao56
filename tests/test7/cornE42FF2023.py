"""
########################################################################
The cornE42FF2023.py module contains a function to setup and run pyfao56
for the (fully irrigated) E42 plot in a 2023 corn field study at the
Limited Irrigation Research Farm (LIRF) in Greeley, Colorado.
Specifically, this module tests the Visualization class in pyfao56.

The cornE42FF2023.py module contains the following:
    run - function to setup and run pyfao56 for the E42 plot in a 2023
          corn field study in Greeley, Colorado.

08/29/2023 Scripts developed for running pyfao56 for 2023 corn data
########################################################################
"""

import pyfao56 as fao
import pyfao56.tools as tools
import os
import numpy as np

def run():
    """Setup and run pyfao56 for a 2023 corn field study"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters from parameters file
    par_file = os.path.join(module_dir, 'E42FF2023.par')
    par = fao.Parameters()
    par.loadfile(par_file)

    #Specify the model weather data from weather file
    wth_file = os.path.join(module_dir, 'LIRFWeather2023.wth')
    wth = fao.Weather(wth_file)

    #Specify the irrigation schedule from irrigation file
    irr_file = os.path.join(module_dir, 'E42FF2023.irr')
    irr = fao.Irrigation(irr_file)

    #Specify the soil profile data from soil file
    sol_file = os.path.join(module_dir, 'E42FF2023.sol')
    sol = fao.SoilProfile(sol_file)

    #Specify Kcb from overhead canopy images via an update file
    upd_file = os.path.join(module_dir, 'E42FF2023.upd')
    upd = fao.Update(upd_file)

    #Run the model with Update and SoilProfile classes
    mdl = fao.Model('2023-122', '2023-305', par, wth, irr=irr,
                    sol=sol, upd=upd, cons_p=True)
    mdl.run()
    print(mdl)
    mdl.savefile(os.path.join(module_dir,'E42FF2023.out'))
    mdl.savesums(os.path.join(module_dir,'E42FF2023.sum'))

    #Analyze measured soil water data
    #Need to update soil water data with remainder of 2023 season.
    sws = tools.SoilWaterSeries(filepath='E42FF2023.sws',
                                par=par,sol=sol)
    for key in sorted(sws.swdata.keys()):
        print('Computing soil water depletion for {:s}'.format(key))
        sws.swdata[key].getZr(mdl)
        sws.swdata[key].computeDr()
        sws.swdata[key].computeKs(mdl)
    sws.savefile(os.path.join(module_dir,'E42FF2023.sws'))

    #Plot measured and simulated data
    vis = tools.Visualization(mdl, sws=sws, dayline=True)
    pngpath = os.path.join(module_dir, 'E42FF2023_Dr.png')
    vis.plot_Dr(drmax=True,raw=True,events=True,obs=True,ks=True,
                dp=True,title='2023 Corn E42FF Dr',
                filepath=pngpath)
    pngpath = os.path.join(module_dir, 'E42FF2023_ET.png')
    vis.plot_ET(title='2023 Corn E42FF ET', show=True, filepath=pngpath)
    pngpath = os.path.join(module_dir, 'E42FF2023_Kc.png')
    vis.plot_Kc(title='2023 Corn E42FF Kc', show=True, filepath=pngpath)

    #Compute fit statistics
    sDr = []
    mDr = []
    sDrmax = []
    mDrmax = []
    for key in sorted(sws.swdata.keys()):
        sDr.append(mdl.odata.loc[key,'Dr'])
        mDr.append(sws.swdata[key].mDr)
        sDrmax.append(mdl.odata.loc[key,'Drmax'])
        mDrmax.append(sws.swdata[key].mDrmax)
    statsDr = tools.Statistics(sDr,mDr,comment='Dr')
    statsDrmax = tools.Statistics(sDrmax,mDrmax,comment='Drmax')
    print(statsDr)
    statsDr.savefile(os.path.join(module_dir,'E42FF2023_Dr.fit'))
    print(statsDrmax)
    statsDrmax.savefile(os.path.join(module_dir,'E42FF2023_Drmax.fit'))
    data = np.array((sDr,mDr,sDrmax,mDrmax)).transpose()
    np.savetxt('E42FF2023_fitdata.csv',data,delimiter=',')

if __name__ == '__main__':
    run()
