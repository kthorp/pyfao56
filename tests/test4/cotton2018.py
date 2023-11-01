"""
########################################################################
The cotton2018.py module contains a function to setup and run pyfao56
for the 100%-100% and the 60-60% irrigation treatments in a 2018 cotton
field study at Maricopa, Arizona. Simulation output was used in the
first SoftwareX manuscript for pyfao56.

The cotton2018.py module contains the following:
    run - function to setup and run pyfao56 for the 100%-100% and the
    60-60% in a 2018 cotton field study at Maricopa, Arizona

02/07/2022 Scripts developed for running pyfao56 for 2018 cotton data
########################################################################
"""

import pyfao56 as fao
import pyfao56.custom as custom
import os

def run():
    """Setup and run pyfao56 for a 2018 cotton field study"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2018 Cotton')
    par.Kcbmid = 1.225
    par.Lini = 35
    par.Ldev = 50
    par.Lmid = 46
    par.Lend = 39
    par.hini = 0.05
    par.hmax = 1.20
    par.thetaFC = 0.2050
    par.thetaWP = 0.0980
    par.theta0  = 0.1515
    par.Zrini = 0.20
    par.Zrmax = 1.40
    par.pbase = 0.65
    par.Ze = 0.06
    par.REW = 4.0
    par.savefile(os.path.join(module_dir,'cotton2018.par'))

    #Specify the weather data
    wth = custom.AzmetMaricopa(comment = '2018 Cotton')
    wth.customload('2018-108','2018-303')
    wth.savefile(os.path.join(module_dir,'cotton2018.wth'))

    #Specify the irrigation schedule for the 60%-60% treatment
    irr060 = fao.Irrigation(comment = '2018 Cotton, 60%-60% ' + 
                            'irrigation treatment')
    irr060.addevent(2018, 110, 20.4, 1.0)
    irr060.addevent(2018, 114, 20.4, 1.0)
    irr060.addevent(2018, 117, 20.4, 1.0)
    irr060.addevent(2018, 120,  5.1, 1.0)
    irr060.addevent(2018, 127, 20.4, 1.0)
    irr060.addevent(2018, 136, 20.2, 1.0)
    irr060.addevent(2018, 143, 20.4, 1.0)
    irr060.addevent(2018, 150, 15.3, 1.0)
    irr060.addevent(2018, 157, 12.8, 1.0)
    irr060.addevent(2018, 158,  7.6, 1.0)
    irr060.addevent(2018, 164, 25.3, 1.0)
    irr060.addevent(2018, 165, 15.2, 1.0)
    irr060.addevent(2018, 171, 33.0, 1.0)
    irr060.addevent(2018, 172, 15.3, 1.0)
    irr060.addevent(2018, 178, 20.4, 1.0)
    irr060.addevent(2018, 179, 20.4, 1.0)
    irr060.addevent(2018, 186, 33.0, 1.0)
    irr060.addevent(2018, 187, 20.4, 1.0)
    irr060.addevent(2018, 192, 15.3, 1.0)
    irr060.addevent(2018, 193, 20.4, 1.0)
    irr060.addevent(2018, 194,  5.1, 1.0)
    irr060.addevent(2018, 200, 27.9, 1.0)
    irr060.addevent(2018, 201, 15.3, 1.0)
    irr060.addevent(2018, 206, 20.4, 1.0)
    irr060.addevent(2018, 207, 15.3, 1.0)
    irr060.addevent(2018, 213, 20.4, 1.0)
    irr060.addevent(2018, 214, 20.4, 1.0)
    irr060.addevent(2018, 220, 15.3, 1.0)
    irr060.addevent(2018, 221, 15.3, 1.0)
    irr060.addevent(2018, 229, 10.2, 1.0)
    irr060.addevent(2018, 234, 15.3, 1.0)
    irr060.addevent(2018, 235, 10.2, 1.0)
    irr060.addevent(2018, 242, 15.3, 1.0)
    irr060.addevent(2018, 243, 15.3, 1.0)
    irr060.addevent(2018, 248, 15.3, 1.0)
    irr060.addevent(2018, 250, 15.3, 1.0)
    irr060.savefile(os.path.join(module_dir,'cotton2018_060.irr'))

    #Specify the irrigation schedule for the 100%-100% treatment
    irr100 = fao.Irrigation(comment = '2018 Cotton, 100%-100% ' +
                            'irrigation treatment')
    irr100.addevent(2018, 110, 20.4, 1.0)
    irr100.addevent(2018, 114, 20.4, 1.0)
    irr100.addevent(2018, 117, 20.4, 1.0)
    irr100.addevent(2018, 120,  5.1, 1.0)
    irr100.addevent(2018, 127, 20.4, 1.0)
    irr100.addevent(2018, 136, 20.2, 1.0)
    irr100.addevent(2018, 143, 20.4, 1.0)
    irr100.addevent(2018, 150, 25.5, 1.0)
    irr100.addevent(2018, 157, 21.2, 1.0)
    irr100.addevent(2018, 158, 12.7, 1.0)
    irr100.addevent(2018, 164, 28.7, 1.0)
    irr100.addevent(2018, 165, 25.3, 1.0)
    irr100.addevent(2018, 171, 41.4, 1.0)
    irr100.addevent(2018, 172, 25.5, 1.0)
    irr100.addevent(2018, 178, 34.0, 1.0)
    irr100.addevent(2018, 179, 34.0, 1.0)
    irr100.addevent(2018, 186, 41.4, 1.0)
    irr100.addevent(2018, 187, 34.0, 1.0)
    irr100.addevent(2018, 192, 25.5, 1.0)
    irr100.addevent(2018, 193, 34.0, 1.0)
    irr100.addevent(2018, 194,  8.5, 1.0)
    irr100.addevent(2018, 200, 32.9, 1.0)
    irr100.addevent(2018, 201, 25.5, 1.0)
    irr100.addevent(2018, 206, 34.0, 1.0)
    irr100.addevent(2018, 207, 25.5, 1.0)
    irr100.addevent(2018, 213, 34.0, 1.0)
    irr100.addevent(2018, 214, 34.0, 1.0)
    irr100.addevent(2018, 220, 25.5, 1.0)
    irr100.addevent(2018, 221, 25.5, 1.0)
    irr100.addevent(2018, 229, 17.0, 1.0)
    irr100.addevent(2018, 234, 25.5, 1.0)
    irr100.addevent(2018, 235, 17.0, 1.0)
    irr100.addevent(2018, 242, 25.5, 1.0)
    irr100.addevent(2018, 243, 25.5, 1.0)
    irr100.addevent(2018, 248, 25.5, 1.0)
    irr100.addevent(2018, 250, 25.5, 1.0)
    irr100.savefile(os.path.join(module_dir,'cotton2018_100.irr'))

    #Specify the irrigation schedule for the 120%-120% treatment
    irr120 = fao.Irrigation(comment = '2018 Cotton, 120%-120% ' +
                            'irrigation treatment')
    irr120.addevent(2018, 110, 20.4, 1.0)
    irr120.addevent(2018, 114, 20.4, 1.0)
    irr120.addevent(2018, 117, 20.4, 1.0)
    irr120.addevent(2018, 120,  5.1, 1.0)
    irr120.addevent(2018, 127, 20.4, 1.0)
    irr120.addevent(2018, 136, 20.2, 1.0)
    irr120.addevent(2018, 143, 20.4, 1.0)
    irr120.addevent(2018, 150, 30.6, 1.0)
    irr120.addevent(2018, 157, 25.5, 1.0)
    irr120.addevent(2018, 158, 15.2, 1.0)
    irr120.addevent(2018, 164, 30.4, 1.0)
    irr120.addevent(2018, 165, 30.4, 1.0)
    irr120.addevent(2018, 171, 45.7, 1.0)
    irr120.addevent(2018, 172, 30.6, 1.0)
    irr120.addevent(2018, 178, 40.8, 1.0)
    irr120.addevent(2018, 179, 40.8, 1.0)
    irr120.addevent(2018, 186, 45.7, 1.0)
    irr120.addevent(2018, 187, 40.8, 1.0)
    irr120.addevent(2018, 192, 30.6, 1.0)
    irr120.addevent(2018, 193, 40.8, 1.0)
    irr120.addevent(2018, 194, 10.2, 1.0)
    irr120.addevent(2018, 200, 35.5, 1.0)
    irr120.addevent(2018, 201, 30.6, 1.0)
    irr120.addevent(2018, 206, 40.8, 1.0)
    irr120.addevent(2018, 207, 30.6, 1.0)
    irr120.addevent(2018, 213, 40.8, 1.0)
    irr120.addevent(2018, 214, 40.8, 1.0)
    irr120.addevent(2018, 220, 30.6, 1.0)
    irr120.addevent(2018, 221, 30.6, 1.0)
    irr120.addevent(2018, 229, 20.4, 1.0)
    irr120.addevent(2018, 234, 30.6, 1.0)
    irr120.addevent(2018, 235, 20.4, 1.0)
    irr120.addevent(2018, 242, 30.6, 1.0)
    irr120.addevent(2018, 243, 30.6, 1.0)
    irr120.addevent(2018, 248, 30.6, 1.0)
    irr120.addevent(2018, 250, 30.6, 1.0)
    irr120.savefile(os.path.join(module_dir,'cotton2018_120.irr'))

    #Run the 60%-60% model
    mdl060 = fao.Model('2018-108','2018-303', par, wth, irr=irr060,
                       comment = '2018 Cotton, 60%-60% ' +
                            'irrigation treatment')
    mdl060.run()
    print(mdl060)
    mdl060.savefile(os.path.join(module_dir,'cotton2018_060.out'))
    mdl060.savesums(os.path.join(module_dir,'cotton2018_060.sum'))

    #Run the 100%-100% model
    mdl100 = fao.Model('2018-108','2018-303', par, wth, irr=irr100,
                       comment = '2018 Cotton, 100%-100% ' + 
                            'irrigation treatment')
    mdl100.run()
    print(mdl100)
    mdl100.savefile(os.path.join(module_dir,'cotton2018_100.out'))
    mdl100.savesums(os.path.join(module_dir,'cotton2018_100.sum'))

    #Run the 120%-120% model
    mdl120 = fao.Model('2018-108','2018-303', par, wth, irr=irr120,
                       comment = '2018 Cotton, 120%-120% ' +
                            'irrigation treatment')
    mdl120.run()
    print(mdl120)
    mdl120.savefile(os.path.join(module_dir,'cotton2018_120.out'))
    mdl120.savesums(os.path.join(module_dir,'cotton2018_120.sum'))

if __name__ == '__main__':
    run()
