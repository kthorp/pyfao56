"""
########################################################################
The updateKcb.py module contains a function to setup and run pyfao56
with basal crop coefficient (Kcb) updates for Zone 12-11 in a 2019
cotton field study at Maricopa, Arizona. The Kcb was estimated from
fractional cover measurements based on weekly imagery from a small
unoccupied aircraft system (sUAS).

The updateKcb.py module contains the following:
    run - function to setup and run pyfao56 with Kcb updating for Zone
    12-11 in the 2019 cotton field study at Maricopa, Arizona

12/02/2021 Scripts developed for running pyfao56 for 2019 cotton data
########################################################################
"""

import pyfao56 as fao
import os

def run():
    """Setup and run pyfao56 with Kcb updating"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2019 Cotton')
    par.Kcbmid = 1.225
    par.Lini = 35
    par.Ldev = 50
    par.Lmid = 46
    par.Lend = 39
    par.hini = 0.05
    par.hmax = 1.20
    par.thetaFC = 0.2125
    par.thetaWP = 0.1019
    par.theta0  = 0.1850
    par.Zrini = 0.82
    par.Zrmax = 1.40
    par.pbase = 0.65
    par.Ze = 0.06
    par.REW = 4.0
    par.savefile(os.path.join(module_dir,'cotton2019.par'))
    par.loadfile(os.path.join(module_dir,'cotton2019.par'))

    #Specify the weather data
    wth = fao.Weather(comment = '2019 Cotton')
    wth.loadfile(os.path.join(module_dir,'cotton2019.wth'))
    wth.savefile(os.path.join(module_dir,'cotton2019.wth'))
    wth.loadfile(os.path.join(module_dir,'cotton2019.wth'))

    #Specify the irrigation schedule (2019 F13B4 Zone 12-11)
    irr = fao.Irrigation(comment = '2019 Cotton')
    irr.addevent(2019, 109, 20.4, 1.00)
    irr.addevent(2019, 112, 10.2, 1.00)
    irr.addevent(2019, 114, 10.2, 1.00)
    irr.addevent(2019, 116, 10.2, 1.00)
    irr.addevent(2019, 119, 10.2, 1.00)
    irr.addevent(2019, 122, 10.2, 1.00)
    irr.addevent(2019, 130, 10.2, 1.00)
    irr.addevent(2019, 136, 20.2, 1.00)
    irr.addevent(2019, 143, 15.2, 1.00)
    irr.addevent(2019, 150, 20.2, 1.00)
    irr.addevent(2019, 158, 22.8, 1.00)
    irr.addevent(2019, 164, 21.3, 1.00)
    irr.addevent(2019, 165, 21.3, 1.00)
    irr.addevent(2019, 171, 22.0, 1.00)
    irr.addevent(2019, 172, 20.2, 1.00)
    irr.addevent(2019, 178, 31.5, 1.00)
    irr.addevent(2019, 179, 21.0, 1.00)
    irr.addevent(2019, 184, 25.2, 1.00)
    irr.addevent(2019, 186, 25.2, 1.00)
    irr.addevent(2019, 191,  9.1, 1.00)
    irr.addevent(2019, 192, 33.8, 1.00)
    irr.addevent(2019, 193, 18.1, 1.00)
    irr.addevent(2019, 199, 38.6, 1.00)
    irr.addevent(2019, 200, 38.6, 1.00)
    irr.addevent(2019, 206, 35.5, 1.00)
    irr.addevent(2019, 207, 23.7, 1.00)
    irr.addevent(2019, 213, 26.8, 1.00)
    irr.addevent(2019, 214, 26.8, 1.00)
    irr.addevent(2019, 220, 32.9, 1.00)
    irr.addevent(2019, 221, 21.9, 1.00)
    irr.addevent(2019, 227, 30.2, 1.00)
    irr.addevent(2019, 228, 30.2, 1.00)
    irr.addevent(2019, 234, 38.9, 1.00)
    irr.addevent(2019, 235, 26.0, 1.00)
    irr.addevent(2019, 241, 33.9, 1.00)
    irr.addevent(2019, 242, 33.9, 1.00)
    irr.addevent(2019, 248, 28.3, 1.00)
    irr.addevent(2019, 249, 28.3, 1.00)
    irr.savefile(os.path.join(module_dir,'cotton2019.irr'))
    irr.loadfile(os.path.join(module_dir,'cotton2019.irr'))

    #Specify the updates for Kcb and fc
    upd = fao.Update(comment = '2019 Cotton')
    upd.loadfile(os.path.join(module_dir,'cotton2019.upd'))
    upd.savefile(os.path.join(module_dir,'cotton2019.upd'))
    upd.loadfile(os.path.join(module_dir,'cotton2019.upd'))

    #Run the model
    mdl = fao.Model('2019-108','2019-274', par, wth, irr=irr,
                    upd=upd, comment = '2019 Cotton')
    mdl.run()
    print(mdl)
    mdl.savefile(os.path.join(module_dir,'cotton2019.out'))
    mdl.savesums(os.path.join(module_dir,'cotton2019.sum'))

if __name__ == '__main__':
    run()
