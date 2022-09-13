"""
This file is meant to demonstrate a method of using the SoilWater class.
"""

# Loading in the SoilWater Class
#   - change this once pyfao56 includes new SoilWater class
from pyfao56_LIRF_features.src.pyfao56.soil_water import SoilWater
from datetime import datetime

# # Creating a formatted date to add to the end of saved files:
date = datetime.today().strftime('%m_%d_%Y')
# # Specify the output folder (using absolute path):
output_folder_path = input('Input Absolute path to output folder:')+'/'

# # Making Saved File Name
file_name = f'{output_folder_path}SWC_{date}.sh2o'

# # Testing the string, savefile, and loadfile functions of the
# reworked soil water class
# # Setting Inputs
depths = [0.15, 0.30, 0.60, 0.90, 1.20, 1.50, 2.00]
bounds = [(0, 0.15), (0.15, 0.45), (0.45, 0.75),
          (0.75, 1.05), (1.05, 1.35), (1.35, 1.65),
          (1.65, 2.15)]
thetaFC = [0.29, 0.24, 0.182, 0.158, 0.120, 0.108, 0.144]
thetaIN = [0.083, 0.058, 0.039, 0.033, 0.012, 0.005, 0.014]
thetaWP = [thetaFC[0] / 2, thetaFC[1] / 2, thetaFC[2] / 2,
           thetaFC[3] / 2, thetaFC[4] / 2, thetaFC[5] / 2,
           thetaFC[6] / 2]

# # Instantiating the Class
swc = SoilWater(depths=depths, theta_fc=thetaFC, theta_ini=thetaIN,
                theta_wp=thetaWP, layer_boundaries=bounds)

# # Printing the string to check formatting
print(f'First SWC String:\n{swc.__str__()}\n')

# # Saving data frame to a file in the output folder
swc.savefile(filepath=file_name)

# # Loading file saved above to a new class instantiation of SoilWater,
# # then printing string to make sure load worked properly.
second_swc = SoilWater(filepath=file_name)
print(f'Second SWC String:\n{second_swc}\n')

# # Saving second_swc data just to compare to first saved file:
second_swc.savefile(filepath=f'{output_folder_path}TestCOMP_SWC_{date}'
                             f'.sh2o')
