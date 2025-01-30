"""
########################################################################
The cornE12FF2022.py module contains a function to setup and run pyfao56
for the (fully irrigated) E12 plot in a 2022 corn field study at the
Limited Irrigation Research Farm (LIRF) in Greeley, Colorado. Routines
related to the SoilProfile classes were also tested.

The cornE12FF2022.py module contains the following:
    run - function to setup and run pyfao56 for the E12 plot in a 2022
          corn field study in Greeley, Colorado.

11/30/2022 Scripts developed for running pyfao56 for 2022 corn data
########################################################################
"""

import pyfao56 as fao
import pyfao56.custom as custom
import os

def run():
    """Setup and run pyfao56 for a 2022 corn field study"""

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters from parameters file
    par_file = os.path.join(module_dir, 'E12FF2022.par')
    par = fao.Parameters()
    par.loadfile(par_file)

    #Specify the model weather data from weather file
    wth_file = os.path.join(module_dir, 'LIRF.wth')
    wth = fao.Weather(wth_file)

    #Specify the irrigation schedule from irrigation file
    irr_file = os.path.join(module_dir, 'E12FF2022.irr')
    irr = fao.Irrigation(irr_file)

    #Use ExampleSoil class to customload soil profile information
    depths = [15, 45, 75, 105, 135, 165, 215]
    thetaFC = [0.29, 0.24, 0.182, 0.158, 0.120, 0.108, 0.144]
    thetaIN = [0.26, 0.22, 0.172, 0.158, 0.120, 0.108, 0.144]
    thetaWP = [thetaFC[0] / 2, thetaFC[1] / 2, thetaFC[2] / 2,
               thetaFC[3] / 2, thetaFC[4] / 2, thetaFC[5] / 2,
               thetaFC[6] / 2]
    sol = custom.ExampleSoil()
    sol.customload(depths,thetaFC,thetaWP,thetaIN)
    sol.savefile(os.path.join(module_dir, 'E12FF2022.sol'))

    #Specify Kcb from overhead canopy images via an update file
    upd_file = os.path.join(module_dir, 'E12FF2022.upd')
    upd = fao.Update(upd_file)

    #Running the model without Update or SoilProfile classes
    mdl = fao.Model('2022-129', '2022-299', par, wth, irr=irr,
                    cons_p=True)
    mdl.run()
    print(mdl)
    mdl.savefile(os.path.join(module_dir,'E12FF2022_default.out'))
    mdl.savesums(os.path.join(module_dir,'E12FF2022_default.sum'))

    #Running the model with SoilProfile class
    mdl_sol = fao.Model('2022-129', '2022-299', par, wth, irr=irr,
                        sol=sol, cons_p=True)
    mdl_sol.run()
    print(mdl_sol)
    mdl_sol.savefile(os.path.join(module_dir,'E12FF2022_Soil.out'))
    mdl_sol.savesums(os.path.join(module_dir,'E12FF2022_Soil.sum'))

    #Running the model with Update class
    mdl_kcb = fao.Model('2022-129', '2022-299', par, wth, irr=irr,
                        upd=upd, cons_p=True)
    mdl_kcb.run()
    print(mdl_kcb)
    mdl_kcb.savefile(os.path.join(module_dir,'E12FF2022_CCKcb.out'))
    mdl_kcb.savesums(os.path.join(module_dir,'E12FF2022_CCKcb.sum'))

    #Running the model with Update and SoilProfile classes
    mdl_all = fao.Model('2022-129', '2022-299', par, wth, irr=irr,
                        sol=sol, upd=upd, cons_p=True)
    mdl_all.run()
    print(mdl_all)
    mdl_all.savefile(os.path.join(module_dir,'E12FF2022.out'))
    mdl_all.savesums(os.path.join(module_dir,'E12FF2022.sum'))

if __name__ == '__main__':
    run()
