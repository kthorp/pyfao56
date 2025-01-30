"""
########################################################################
The cotton2018.py module from test4 has been modified to provide tests
of using tabular data from FAO-56 tables and automated adjustment of
crop coefficients based on weather data inputs.

The cotton2018.py module contains the following:
    run - function to setup and run pyfao56 for the 100%-100% irrigation
    treatment in a 2018 cotton field study at Maricopa, Arizona

02/07/2022 Scripts developed for running pyfao56 for 2018 cotton data
01/29/2025 Script modified to test tabular data from FAO-56 tables
########################################################################
"""

import pyfao56 as fao
import pyfao56.tools as tools
import pyfao56.custom as custom
import os
import time
import sys

def run():
    """Setup and run pyfao56 for a 2018 cotton field study"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Search FAO56 tables
    tables = tools.FAO56Tables()
    t11_cotton = tables.search11("cotton")
    print(t11_cotton) #Use table row index #93 for "desert usa"
    t12_cotton = tables.search12("CoTtOn") #case insensitive
    print(t12_cotton) #Use table row index #55
    t17_cotton = tables.search17("cotton")
    print(t17_cotton) #Use table row index #54
    t22_cotton = tables.search22("cotton")
    print(t22_cotton) #Use table row index #48

    #Specify the model parameters
    par = fao.Parameters(comment = '2018 Cotton')
    par.setfrom11(93)
    par.setfrom12(55)
    par.setfrom17(54)
    par.setfrom22(48)

    par.thetaFC = 0.2050
    par.thetaWP = 0.0980
    par.theta0  = 0.1515
    par.Zrini = 0.20
    par.Ze = 0.06
    par.REW = 4.0
    par.savefile(os.path.join(module_dir,'cotton2018.par'))
    print(par)

    #Specify the weather data
    #wth = custom.AzmetMaricopa(comment = '2018 Cotton')
    #wth.customload('2018-001','2018-365')
    #wth.savefile(os.path.join(module_dir,'cotton2018.wth'))
    wth = fao.Weather()
    wth.loadfile(os.path.join(module_dir,'cotton2018.wth'))

    #Specify the full irrigation schedule for the 100%-100% treatment
    irr = fao.Irrigation()
    irr.loadfile(os.path.join(module_dir,'cotton2018.irr'))

    #Run the model
    mdl = fao.Model('2018-108','2018-365',par, wth, irr=irr, K_adj=True)
    mdl.run()
    #print(mdl)
    mdl.savefile(os.path.join(module_dir,'cotton2018.out'))
    mdl.savesums(os.path.join(module_dir,'cotton2018.sum'))

if __name__ == '__main__':
    run()
