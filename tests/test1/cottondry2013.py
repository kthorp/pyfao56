"""
########################################################################
The cottondry2013.py module contains a function to setup and run pyfao56
for the water-limited treatment in a 2013 cotton field study at
Maricopa, Arizona.  The savefile and loadfile routines for Parameters,
Weather, and Irrigation classes are also tested.

The cottondry2013.py module contains the following:
    run - function to setup and run pyfao56 for the water-limited
    treatment in a 2013 cotton field study at Maricopa, Arizona

11/30/2021 Scripts developed for running pyfao56 for 2013 cotton data
########################################################################
"""

import pyfao56 as fao
import os

def run():
    """Setup and run pyfao56 for a 2013 cotton field study"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2013 Cotton Dry')
    par.Kcbmid = 1.20
    par.Kcbend = 0.573
    par.Lini = 31
    par.Ldev = 52
    par.Lmid = 50
    par.Lend = 21
    par.hini = 0.05
    par.hmax = 1.20
    par.thetaFC = 0.225
    par.thetaWP = 0.100
    par.theta0 = 0.100
    par.Zrini = 0.60
    par.Zrmax = 1.70
    par.pbase = 0.65
    par.Ze = 0.11429
    par.REW = 9.0
    par.savefile(os.path.join(module_dir,'cotton2013.par'))
    par.loadfile(os.path.join(module_dir,'cotton2013.par'))

    #Specify the weather data
    wth = fao.Weather(comment = '2013 Cotton Dry')
    wth.loadfile(os.path.join(module_dir,'cotton2013.wth'))
    wth.savefile(os.path.join(module_dir,'cotton2013.wth'))
    wth.loadfile(os.path.join(module_dir,'cotton2013.wth'))

    #Specify the irrigation schedule
    irr = fao.Irrigation(comment = '2013 Cotton Dry')
    irr.addevent(2013, 115, 33.0, 0.5)
    irr.addevent(2013, 120,108.0, 0.5)
    irr.addevent(2013, 145, 16.2, 0.2)
    irr.addevent(2013, 146, 16.2, 0.2)
    irr.addevent(2013, 151, 16.2, 0.2)
    irr.addevent(2013, 159, 16.2, 0.2)
    irr.addevent(2013, 160, 16.2, 0.2)
    irr.addevent(2013, 165, 16.2, 0.2)
    irr.addevent(2013, 166, 16.2, 0.2)
    irr.addevent(2013, 167, 16.2, 0.2)
    irr.addevent(2013, 172, 16.2, 0.2)
    irr.addevent(2013, 173, 16.2, 0.2)
    irr.addevent(2013, 174, 16.2, 0.2)
    irr.addevent(2013, 179, 16.2, 0.2)
    irr.addevent(2013, 180, 16.2, 0.2)
    irr.addevent(2013, 181, 16.2, 0.2)
    irr.addevent(2013, 182, 16.2, 0.2)
    irr.addevent(2013, 186, 10.1, 0.2)
    irr.addevent(2013, 187, 10.1, 0.2)
    irr.addevent(2013, 188, 10.1, 0.2)
    irr.addevent(2013, 193, 10.1, 0.2)
    irr.addevent(2013, 194, 10.1, 0.2)
    irr.addevent(2013, 195, 10.1, 0.2)
    irr.addevent(2013, 200, 10.1, 0.2)
    irr.addevent(2013, 201, 10.1, 0.2)
    irr.addevent(2013, 202, 10.1, 0.2)
    irr.addevent(2013, 203, 10.1, 0.2)
    irr.addevent(2013, 207, 20.3, 0.2)
    irr.addevent(2013, 208, 10.1, 0.2)
    irr.addevent(2013, 209, 10.1, 0.2)
    irr.addevent(2013, 210, 10.1, 0.2)
    irr.addevent(2013, 214, 20.3, 0.2)
    irr.addevent(2013, 215, 20.3, 0.2)
    irr.addevent(2013, 216, 10.1, 0.2)
    irr.addevent(2013, 217, 10.1, 0.2)
    irr.addevent(2013, 221, 10.1, 0.2)
    irr.addevent(2013, 222, 10.1, 0.2)
    irr.addevent(2013, 223, 10.1, 0.2)
    irr.addevent(2013, 228, 10.1, 0.2)
    irr.addevent(2013, 229, 10.1, 0.2)
    irr.addevent(2013, 230, 10.1, 0.2)
    irr.addevent(2013, 231, 10.1, 0.2)
    irr.addevent(2013, 233,  4.1, 0.2)
    irr.addevent(2013, 235, 12.2, 0.2)
    irr.addevent(2013, 236, 12.2, 0.2)
    irr.addevent(2013, 237, 12.2, 0.2)
    irr.addevent(2013, 238, 12.2, 0.2)
    irr.addevent(2013, 241,  4.1, 0.2)
    irr.addevent(2013, 243, 10.1, 0.2)
    irr.addevent(2013, 244, 10.1, 0.2)
    irr.addevent(2013, 245, 10.1, 0.2)
    irr.savefile(os.path.join(module_dir,'cottondry2013.irr'))
    irr.loadfile(os.path.join(module_dir,'cottondry2013.irr'))

    #Run the model
    mdl = fao.Model('2013-113','2013-312', par, wth, irr=irr,
                    comment = '2013 Cotton Dry')
    mdl.run()
    print(mdl)
    mdl.savefile(os.path.join(module_dir,'cottondry2013.out'))
    mdl.savesums(os.path.join(module_dir,'cottondry2013.sum'))

if __name__ == '__main__':
    run()
