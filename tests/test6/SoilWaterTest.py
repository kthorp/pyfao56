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
    # Use soil water content file to initialize SoilWater class
    swc_file = os.path.join(module_dir, 'E12FF2022.vswc')
    # Initialize without a model
    print('Testing initialization with smc file but no model...\n')
    wtr0 = SoilWater(None, swc_file)
    print(wtr0, '\n')
    # Initialize with default model
    print('Testing initialization with smc file & default model...\n')
    wtr1 = SoilWater(mdl, swc_file)
    print(wtr1, '\n')
    # Initialize with stratified soil model
    print('Testing initialization with smc file & stratified soil '
          'model...\n')
    wtr2 = SoilWater(mdl_sol, swc_file)
    print(wtr2, '\n')
    # Initialize empty class
    print('Testing empty class initialization...\n')
    wtr3 = SoilWater()
    print(wtr3, '\n')

    # Test the savefile function
    swc_file2 = os.path.join(module_dir, 'E12FF2022_NEW.vswc')
    swd_file  = os.path.join(module_dir, 'E12FF2022.vswd')
    rzsw_file = os.path.join(module_dir, 'E12FF2022.rzsw')
    print('Testing savefile function...\n')
    wtr2.savefile(swc_path=swc_file2, swd_path=swd_file,
                  rzsw_path=rzsw_file)
    if os.path.exists(swc_file2):
        print(f"The {swc_file2} was successfully saved.\n")
    else:
        print(f"The {swc_file2} was not saved. \n")
    print('Testing savefile function error message...\n')
    wtr2.savefile()

    # Test the loadfile function
    # Testing using the swc method
    print('Loading soil water content file...\n')
    wtr3.loadfile(swc_path=swc_file2)
    print(wtr3, '\n')
    # Testing using the swd method
    print('Loading soil water deficit file...\n')
    wtr3 = SoilWater()
    wtr3.loadfile(swd_path=swd_file)
    print(wtr3, '\n')
    # Testing using the swrz method
    print('Loading soil water root zone file...\n')
    wtr3 = SoilWater()
    wtr3.loadfile(rzsw_path=rzsw_file)
    print(wtr3, '\n')
    # Testing using all three methods
    print('Loading soil water data...\n')
    wtr3 = SoilWater()
    wtr3.loadfile(swc_path=swc_file2, swd_path=swd_file,
                  rzsw_path=rzsw_file)
    print(wtr3, '\n')

    # I have an example customload function, but it depends on openpyxl,
    # and I don't want to have to make that a pyfao56 dependency. So I
    # am skipping testing the customload function

    # Testing compute functions
    print('Testing the compute_swd_from_swc function...\n')
    wtr = SoilWater(mdl=mdl_sol)
    wtr.loadfile(swc_file2)
    wtr.compute_swd_from_swc()
    print(wtr, '\n')
    print('Testing the compute_root_zone_sw function...\n')
    wtr.compute_root_zone_sw()
    print(wtr, '\n')

if __name__ == '__main__':
    run()