"""
########################################################################
The SoilWaterTest.py module contains a function to setup and test the
SoilWater class for managing measured values from the E12 plot in a 2022
corn field study at the Limited Irrigation Research Farm (LIRF) in
Greeley, Colorado.

The SoilWaterTest.py module contains the following:
    run - function to test the SoilWater class for managing measured
          values from a 2022 corn field study in Greeley, Colorado.

03/02/2023 Script developed for testing SoilWater class.
########################################################################
"""

import pyfao56 as fao
from pyfao56.tools import SoilWater
import os

def run():
    """
    Test the pyfao56 tools SoilWater class for managing measured
    values from a 2022 corn field study in Greeley, Colorado.
    """

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    start = '2022-129'
    end   = '2022-299'

    #Specify the model parameters from parameters file
    par_file = os.path.join(module_dir, 'E12FF2022.par')
    par = fao.Parameters()
    par.loadfile(par_file)

    #Specify soil profile information from soil profile file
    sol_file = os.path.join(module_dir, 'E12FF2022.sol')
    sol = fao.SoilProfile(sol_file)

    # Initialize with Parameters only
    print('Test SoilWater initialization with a Parameters class...\n')
    wtr = SoilWater(par=par)
    # Initialize with SoilProfile only
    print('Test SoilWater initialization with a SoilProfile class...\n')
    wtr = SoilWater(sol=sol)

    # Test the loadfile function
    swc_file = os.path.join(module_dir, 'E12FF2022.vswc')
    rzsw_file = os.path.join(module_dir, 'E12FF2022.rzsw')
    # Testing using the swc method
    print('Loading soil water content file...\n')
    wtr.loadfile(swc_path=swc_file)
    # Testing using the rzsw method
    print('Loading soil water root zone file...\n')
    wtr.loadfile(rzsw_path=rzsw_file)
    print(wtr, '\n')

    # Initialize without classes
    print('Testing initialization with swc file but classes...\n')
    wtr0 = SoilWater(swc_path=swc_file)
    print(wtr0, '\n')

    # Initialize with Parameters class and swc file
    print('Testing compute RZSW with Parameters class...\n')
    wtr1 = SoilWater(par=par, swc_path=swc_file)
    wtr1.compute_root_zone_sw(start, end)
    print(wtr1, '\n')
    # Initialize with stratified soil profile
    print('Testing compute RZSW with Parameters & SoilProfile...\n')
    wtr2 = SoilWater(par=par, sol=sol, swc_path=swc_file)
    wtr2.compute_root_zone_sw(start, end)
    print(wtr2, '\n')

    # Test the savefile function
    swc_file2 = os.path.join(module_dir, 'E12FF2022_NEW.vswc')
    rzsw_file = os.path.join(module_dir, 'E12FF2022_NEW.rzsw')
    print('Testing savefile function...\n')
    wtr2.savefile(swc_path=swc_file2, rzsw_path=rzsw_file)
    if os.path.exists(swc_file2) & os.path.exists(rzsw_file):
        print(f"{swc_file2} and {rzsw_file} were successfully saved.\n")
    else:
        print(f"ERROR: SOIL WATER FILES NOT SAVED\n")
    print('Testing savefile function error message...\n')
    wtr2.savefile()
    print('\nSuccessfully tested SoilWater class.')

    # I have an example customload function, but it depends on openpyxl,
    # and I don't want to have to make that a pyfao56 dependency. So I
    # am skipping testing the customload function

if __name__ == '__main__':
    run()