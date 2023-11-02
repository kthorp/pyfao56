"""
########################################################################
The cotton2022.py module contains a function to setup and run pyfao56
for plot 10-2 in a 2022 cotton field study at Maricopa, Arizona. The
SoilWaterSeries class was also tested to assess measured soil water
content data for root zone soil water depletion.

The cotton2022.py module contains the following:
    run - function to setup and run pyfao56 for the plot 10-2 in a 2022
    cotton field study at Maricopa, Arizona and to compute root zone
    soil water depletion from measured soil water content.

08/28/2023 Scripts developed for running pyfao56 for 2022 cotton data
########################################################################
"""

import pyfao56 as fao
import pyfao56.custom as custom
import pyfao56.tools as tools
import os
import numpy as np

def run():
    """Setup and run pyfao56 for a 2022 cotton field study"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2022 Cotton, plot 10-2')
    par.Kcbmid = 1.225
    par.Lini = 35
    par.Ldev = 50
    par.Lmid = 46
    par.Lend = 39
    par.hini = 0.05
    par.hmax = 1.20
    par.thetaFC = 0.2060
    par.thetaWP = 0.0980
    par.theta0  = 0.0580
    par.Zrini = 0.20
    par.Zrmax = 1.50
    par.pbase = 0.65
    par.Ze = 0.06
    par.REW = 4.0
    par.savefile(os.path.join(module_dir,'cotton2022p10-2.par'))

    #Specify the weather data
    #wth = custom.AzmetMaricopa(comment = '2022 Cotton')
    #wth.customload('2022-111','2022-304')
    #wth.savefile(os.path.join(module_dir,'cotton2022.wth'))
    wth = fao.Weather()
    wth.loadfile(os.path.join(module_dir,'cotton2022.wth'))

    #Specify the irrigation schedule for plot 10-2
    irr = fao.Irrigation(comment = '2022 Cotton, plot 10-2')
    irr.addevent(2022, 112, 30.4, 1.0)
    irr.addevent(2022, 116, 30.4, 1.0)
    irr.addevent(2022, 119, 30.4, 1.0)
    irr.addevent(2022, 122, 10.2, 1.0)
    irr.addevent(2022, 124, 20.2, 1.0)
    irr.addevent(2022, 126, 20.2, 1.0)
    irr.addevent(2022, 132, 30.4, 1.0)
    irr.addevent(2022, 137, 12.8, 1.0)
    irr.addevent(2022, 140, 19.2, 1.0)
    irr.addevent(2022, 144, 15.0, 1.0)
    irr.addevent(2022, 147, 15.0, 1.0)
    irr.addevent(2022, 153, 19.0, 1.0)
    irr.addevent(2022, 154, 19.0, 1.0)
    irr.addevent(2022, 158, 20.2, 1.0)
    irr.addevent(2022, 161, 29.9, 1.0)
    irr.addevent(2022, 165, 27.3, 1.0)
    irr.addevent(2022, 168, 37.3, 1.0)
    irr.addevent(2022, 173, 28.0, 1.0)
    irr.addevent(2022, 175, 28.0, 1.0)
    irr.addevent(2022, 180, 25.2, 1.0)
    irr.addevent(2022, 182, 32.8, 1.0)
    irr.addevent(2022, 188, 32.5, 1.0)
    irr.addevent(2022, 189, 32.5, 1.0)
    irr.addevent(2022, 193, 40.2, 1.0)
    irr.addevent(2022, 196, 23.2, 1.0)
    irr.addevent(2022, 201, 43.9, 1.0)
    irr.addevent(2022, 203, 30.3, 1.0)
    irr.addevent(2022, 207, 32.4, 1.0)
    irr.addevent(2022, 210, 32.4, 1.0)
    irr.addevent(2022, 214, 34.0, 1.0)
    irr.addevent(2022, 217, 21.7, 1.0)
    irr.addevent(2022, 222, 31.8, 1.0)
    irr.addevent(2022, 224, 31.8, 1.0)
    irr.addevent(2022, 228, 32.5, 1.0)
    irr.addevent(2022, 231, 32.5, 1.0)
    irr.addevent(2022, 235, 22.1, 1.0)
    irr.addevent(2022, 238, 33.1, 1.0)
    irr.addevent(2022, 242, 35.4, 1.0)
    irr.addevent(2022, 245, 35.4, 1.0)
    irr.addevent(2022, 249, 35.0, 1.0)
    irr.addevent(2022, 252, 35.0, 1.0)
    irr.savefile(os.path.join(module_dir,'cotton2022p10-2.irr'))

    #Specify layered soil profile
    sol = fao.SoilProfile(filepath='./cotton2022p10-2.sol')

    #Run the model
    mdl = fao.Model('2022-111','2022-304', par, wth, irr=irr, sol=sol,
                    comment = '2022 Cotton, plot 10-2')
    mdl.run()
    print(mdl)
    mdl.savefile(os.path.join(module_dir,'cotton2022p10-2.out'))
    mdl.savesums(os.path.join(module_dir,'cotton2022p10-2.sum'))

    #Analyze measured soil water data
    sws = tools.SoilWaterSeries(filepath='./cotton2022p10-2.sws',
                                par=par,sol=sol)
    for key in sorted(sws.swdata.keys()):
        print('Computing soil water depletion for {:s}'.format(key))
        sws.swdata[key].getZr(mdl)
        sws.swdata[key].computeDr()
        sws.swdata[key].computeKs(mdl)
    sws.savefile(os.path.join(module_dir,'cotton2022p10-2.sws'))

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
    statsDr.savefile(os.path.join(module_dir,'cotton2022p10-2_Dr.fit'))
    print(statsDrmax)
    statsDrmax.savefile(os.path.join(module_dir,
                                     'cotton2022p10-2_Drmax.fit'))
    data = np.array((sDr,mDr,sDrmax,mDrmax)).transpose()
    np.savetxt('cotton2022p10-2_fitdata.csv',data,delimiter=',')

    #Plot measured and simulated data
    vis = tools.Visualization(mdl, sws=sws, dayline=True)
    pngpath = os.path.join(module_dir, 'cotton2022p10-2_Dr.png')
    vis.plot_Dr(drmax=True,raw=True,events=True,obs=True,ks=True,
                dp=True,title='2022 Cotton p10-2 Dr',
                filepath=pngpath)
    pngpath = os.path.join(module_dir, 'cotton2022p10-2_ET.png')
    vis.plot_ET(title='2023 Cotton p10-2 ET',show=True,filepath=pngpath)
    pngpath = os.path.join(module_dir, 'cotton2022p10-2_Kc.png')
    vis.plot_Kc(title='2023 Cotton p10-2 Kc',show=True,filepath=pngpath)

if __name__ == '__main__':
    run()
