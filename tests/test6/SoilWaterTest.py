"""
########################################################################
The SoilWaterTest.py module contains a function to setup and run pyfao56
for the (fully irrigated) E12 plot in a 2022 corn field study at the
Limited Irrigation Research Farm (LIRF) in Greeley, Colorado, while also
testing the SoilWater class for managing observed values.

The SoilWaterTest.py module contains the following:
    run - function to setup and run pyfao56 for the E12 plot in a 2022
          corn field study in Greeley, Colorado.

03/02/2023 Scripts developed for testing SoilWater class.
########################################################################
"""

import pyfao56 as fao
from pyfao56.tools import SoilWater
import os

def run():
    """Setup and run pyfao56 in a way that tests the SoilWater class of
    the tools subpackage.
    """

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

    #Run the default model
    mdl = fao.Model('2022-129', '2022-299', par, wth, irr, cons_p=True)
    mdl.run()
    mdl.savefile(os.path.join(module_dir,'E12FF2022.out'))

    #Specify soil profile information from soil profile file
    sol_file = os.path.join(module_dir, 'E12FF2022.sol')
    sol = fao.SoilProfile(sol_file)

    #Run the model with SoilProfile class
    mdl_sol = fao.Model('2022-129', '2022-299', par, wth, irr,
                        sol=sol, cons_p=True)
    mdl_sol.run()
    mdl_sol.savefile(os.path.join(module_dir,'E12FF2022_Soil.out'))

    print('Testing SoilWater class initialization...\n')
    # Initialize with a model only
    print('Testing initialization with just a model...\n')
    wtr = SoilWater(mdl=mdl)
    print(wtr)

    # Test the loadfile function
    swc_file = os.path.join(module_dir, 'E12FF2022.vswc')
    rzsw_file = os.path.join(module_dir, 'E12FF2022.rzsw')
    # Testing using the swc method
    print('\nLoading soil water content file...\n')
    wtr.loadfile(swc_path=swc_file)
    print(wtr, '\n')
    # Testing using the rzsw method
    print('Loading soil water root zone file...\n')
    wtr.loadfile(rzsw_path=rzsw_file)
    print(wtr, '\n')

    # Initialize without a model
    print('Testing initialization with swc file but no model...\n')
    wtr0 = SoilWater(swc_path=swc_file)
    print(wtr0, '\n')

    # Initialize with default model
    print('Testing initialization with swc file & default model...\n')
    wtr1 = SoilWater(mdl=mdl, swc_path=swc_file)
    wtr1.compute_root_zone_sw()
    print(wtr1, '\n')
    # Initialize with stratified soil model
    print('Testing initialization with swc file & stratified soil '
          'model...\n')
    wtr2 = SoilWater(mdl=mdl_sol, swc_path=swc_file)
    wtr2.compute_root_zone_sw()
    print(wtr2, '\n')

    # Test the savefile function
    swc_file2 = os.path.join(module_dir, 'E12FF2022_NEW.vswc')
    rzsw_file = os.path.join(module_dir, 'E12FF2022_NEW.rzsw')
    print('Testing savefile function...\n')
    wtr2.savefile(swc_path=swc_file2, rzsw_path=rzsw_file)
    if os.path.exists(swc_file2) & os.path.exists(rzsw_file):
        print(f"{swc_file2} and {rzsw_file} were successfully saved.\n")
    else:
        print(f"{swc_file2} and {rzsw_file} were NOT SAVED. \n")
    print('Testing savefile function error message...\n')
    wtr2.savefile()

    # Initialize empty class
    print('Testing empty class initialization...\n')
    wtr3 = SoilWater()
    wtr3.compute_root_zone_sw()
    print(wtr3, '\n')
    # Testing compute root zone method
    print('Computing root zone soil water from swc file...\n')
    wtr3.loadfile(swc_path=swc_file2)
    wtr3.compute_root_zone_sw()
    # Previous line results in an error message due to lack of a model
    print('Loading model & retrying now')
    wtr3.mdl = mdl_sol
    wtr3.compute_root_zone_sw()
    print(wtr3, '\n')

    # I have an example customload function, but it depends on openpyxl,
    # and I don't want to have to make that a pyfao56 dependency. So I
    # am skipping testing the customload function

if __name__ == '__main__':
    run()