"""
This file is meant to demonstrate both of the methods of initializing
the pyfao56 SoilProfile class. The file thereby demonstrates the
input/output functionality of the SoilProfile class.

The pyfao56 user has two choices when initializing SoilProfile:
    1) provide a text file with data to populate the sdata class
        attribute
    2) write custom code to override the customload class method to
        populate the sdata class attribute programmatically.

Section 1:
I first import some packages / classes that will be used. The first part
of this section is there to make the script execute properly using my
forked repository of pyfao56. Once the updated SoilProfile class is
added to pyfao56 itself, this section can simply import SoilProfile
from fao.SoilProfile.

Section 2:
Then, I define filepath and output folder-related variables. Different
users should alter these variables to fit their machines.

Section 3:
Once the output variables are defined, I create a child class of
SoilProfile. The child class (called example_soil) overrides the
customload class method from SoilProfile.

Section 4:
After the customload function is defined, I move on to defining the
variables that will serve as parameters in the customload function.
These are just some example parameters used to demonstrate data from a
potential soil profile.

Section 5:
I initialize a SoilProfile class (via my example_soil child class) that
uses the customload class method created in Section 3 above.
Once the sdata attribute is populated via the customload method, I
print it just to visually confirm that it looks as expected.
I then test the savefile method of the class by saving the sdata
attribute to a file. The filepath used is a filepath created in Section
2 above.

Section 6:
I initialize a different instance of a SoilProfile class (not using the
child class this time) and provide the path to the file saved from
Section 5.
Once the class is initialized, I print sdata from the second class
instantiation to visually confirm that it looks as expected.
Finally, I save the second instance's sdata attribute to a different
file for comparison to the previously saved file.
"""

# # **************************** SECTION 1 ****************************
# Loading in the SoilProfile Class
# Cut the next 25ish lines once pyfao56 includes the SoilProfile class!
import sys
import os
myCurrentDir = os.getcwd()
sys.path.append(myCurrentDir)
from pathlib import Path
path = Path(myCurrentDir)
parentDir = str(path.parent.absolute())
aPath = Path(parentDir)
grandparentDir = str(aPath.parent.absolute())
bPath = Path(grandparentDir)
greatgrandparentDir = str(bPath.parent.absolute())
sys.path.append(parentDir)
sys.path.append(grandparentDir)
sys.path.append(greatgrandparentDir)
try:
    from pyfao56_LIRF_features.src.pyfao56.soil_profile import \
        SoilProfile
except ModuleNotFoundError:
    print(f'Opps! Something went wrong with importing SoilProfile.\n'
          f'Here is the current directory: {myCurrentDir}\n'
          f'Here is the parent directory: {parentDir}\n'
          f'Here is the grandparent directory: {grandparentDir}\n'
          f'Here is the great-grandparent directory: '
          f'{greatgrandparentDir}\n'
          f'Here is the system path: {sys.path}')

# Once pyfao56 includes newly revised SoilProfile class, use the two
#   lines below instead
# import pyfao56 as fao
# SoilProfile = fao.SoilProfile
from datetime import datetime
import pandas as pd


# # **************************** SECTION 2 ****************************
# Creating a formatted date to add to the end of saved files:
date = datetime.today().strftime('%m_%d_%Y')
# Path to the Example_Output Folder (specific to your machine)
# !!!!!!!!!!!!!!!!!!!!!!!!Change the next line!!!!!!!!!!!!!!!!!!!!!!!!
output_folder = "***INSERT PATH INFO***/tests/test5/Example_Output/"
# Names of the Output files - names will be unique to the day
output_file = f'{output_folder}First_Ex_Soil_Output{date}.sol'
second_output_file = f'{output_folder}Second_Ex_Soil_Output{date}.sol'


# # **************************** SECTION 3 ****************************
# Creating a Customload method in a child class to SoilProfile
# Normally, this would be in its own module, separate from a script.
# It is in this script just to demonstrate functionality.
class example_soil(SoilProfile):
    """A class for loading soil profile data.

    Inherits attributes and methods from pyfao56 SoilProfile. Overrides
    the SoilProfile customload function to allow soil profile data to be
    loaded from four lists.

    Attributes
    ----------
    cnames : list
        Column names for sdata
    sdata : DataFrame
        Soil profile data as float
        index = Bottom depth of the layer in centimeters (int)
        columns = ['thetaFC', 'thetaWP', 'thetaIN']
            thetaFC - volumetric soil water content (cm^3/cm^3) of the
                      assumed soil layer's field capacity
            thetaWP - volumetric soil water content (cm^3/cm^3) of the
                      soil layer's assumed permanent wilting point
            thetaIN - initial volumetric soil water content (cm^3/cm^3)
                      measurement of the assumed soil layer

    Methods
    -------
    savefile(filepath='pyfao56.sol')
        Save the soil profile data to a file
    loadfile(filepath='pyfao56.sol')
        Load soil profile data from a file
    customload(bottom_depths, fc, wp, ini)
        Loads soil profile information from four ordered lists.
    """

    def customload(self, bottom_depths, fc, wp, ini):
        """Loads soil profile information from four ordered lists.

        Parameters
        ----------
        bottom_depths : list
            A list of the bottom depths (cm, int) of assumed soil
            layers. Order the list from the shallowest layer to the
            deepest layer.
        fc : list
            A list of field capacities (cm^3/cm^3) of assumed soil
            layers. Order the list from the shallowest layer to the
            deepest layer.
        wp : list
            A list of wilting points (cm^3/cm^3) of assumed soil layers.
            Order the list from the shallowest layer to the deepest
            layer.
        ini : list
            A list of initial volumetric soil water content (cm^3/cm^3)
            measurements of assumed soil layers. Order the list from the
            shallowest layer to the deepest layer.
        ***Note on parameters: all lists should created such that data
        is ordered from the top (shallow part) of the soil profile to
        the bottom (deep part) of the soil profile. For example, the
        FieldCapacity of the third layer down should be the third entry
        in the fc list.
        """

        soil_data_dict = {self.cnames[0]: fc,
                          self.cnames[1]: wp,
                          self.cnames[2]: ini}
        self.sdata = pd.DataFrame.from_dict(soil_data_dict,
                                            dtype='float64')
        self.sdata.index = bottom_depths
        self.sdata.index.astype('int32', copy=False)


# # **************************** SECTION 4 ****************************
# Defining example inputs to use in the example_soil customload method:
depths = [15, 45, 75, 105, 135, 165, 215]
thetaFC = [0.29, 0.24, 0.182, 0.158, 0.120, 0.108, 0.144]
thetaIN = [0.083, 0.058, 0.039, 0.033, 0.012, 0.005, 0.014]
thetaWP = [thetaFC[0] / 2, thetaFC[1] / 2, thetaFC[2] / 2,
           thetaFC[3] / 2, thetaFC[4] / 2, thetaFC[5] / 2,
           thetaFC[6] / 2]


# # **************************** SECTION 5 ****************************
# Instantiating the first example class
first_soil_class = example_soil()

# Feeding Section 4 inputs into the customload function
# from example_soil
first_soil_class.customload(bottom_depths=depths, fc=thetaFC,
                            wp=thetaWP, ini=thetaIN)

# Printing the sdata DataFrame from our example class.
print(f'First Class Instance - Testing "CustomLoad" '
      f'Initialization Method: \n'
      f'{first_soil_class.sdata}\n')

# Testing the savefile function
first_soil_class.savefile(filepath=output_file)


# # **************************** SECTION 6 ****************************
# Testing the loadfile function by instantiating another class:
second_soil_class = SoilProfile(filepath=output_file)

# Printing the sdata DataFrame from our example class.
print(f'Second Class Instance - Testing "Input File" Initialization '
      f'Method: \n'
      f'{second_soil_class.sdata}\n')

# Saving the Second sdata DataFrame for comparison to the first file
second_soil_class.savefile(filepath=second_output_file)
