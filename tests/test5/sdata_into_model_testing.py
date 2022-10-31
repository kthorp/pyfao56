"""
This file serves two purposes. The primary purpose is to test the effort
to incorporate the SoilProfile class sdata attribute into the pyfao56
Model class. The secondary purpose is to provide a demonstration of how
to run the pyfao56 water balance model with the new SoilProfile class
included.

The file is split into three sections:
Section 1:
In section 1, the script imports the classes and packages needed to run
pyfao56. At the time of testing (10_04_2022), neither the SoilProfile
class nor the updated version of the Model class is part of the pyfao56
package. So, those classes need to be loaded separately, at least until
the new SoilProfile and Model classes are officially added to pyfao56.
Once these classes are added to the package, lines 38 to 74 can be cut.

Section 2:
In section 2, the script creates filepath variables that will be used to
run the model. The first set of variables are paths to input files
(parameter, weather, irrigation, and soil profile text files). The next
set of variables are there to create an output filepath that is specific
to the day that the script is run. The output of the model will be saved
to a text file based on the filepath created here.

Section 3:
In section 3, the script actually establishes and runs the pyfao56
model. It instantiates each class with the input files specified in
Section 2. It then run the model and saves the output to the output file
specified in Section 2.

"""

# # **************************** SECTION 1 ****************************
# Importing necessary packages
import os
import pyfao56 as fao
from datetime import datetime

# Loading in the SoilProfile and new Model Classes
# Cut the next 32ish lines once pyfao56 includes these new features!
import sys
from pathlib import Path
myCurrentDir = os.getcwd()
sys.path.append(myCurrentDir)
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
    print(f'Oops! Something went wrong with importing SoilProfile.\n'
          f'Here is the current directory: {myCurrentDir}\n'
          f'Here is the parent directory: {parentDir}\n'
          f'Here is the grandparent directory: {grandparentDir}\n'
          f'Here is the great-grandparent directory: '
          f'{greatgrandparentDir}\n'
          f'Here is the system path: {sys.path}\n')
try:
    from pyfao56_LIRF_features.src.pyfao56.model import Model
except ModuleNotFoundError:
    print(f'Oops! Something went wrong with importing Model.\n'
          f'Here is the current directory: {myCurrentDir}\n'
          f'Here is the parent directory: {parentDir}\n'
          f'Here is the grandparent directory: {grandparentDir}\n'
          f'Here is the great-grandparent directory: '
          f'{greatgrandparentDir}\n'
          f'Here is the system path: {sys.path}\n')


# # **************************** SECTION 2 ****************************
# Creating variables from relative paths to input files:
par_rel_path = r'sdata_into_model_input_files\Default_Parameters_File' \
               r'_LIRF_09_15_2022.par'
wth_rel_path = r'sdata_into_model_input_files\Default_Weather_File' \
               r'_LIRF_09_15_2022.wth'
irr_rel_path = r'sdata_into_model_input_files\Default_Irrigation_File' \
               r'_LIRF_09_15_2022.irr'
sol_rel_path = r'sdata_into_model_input_files\sdata_into_model_' \
               r'SoilProfile.sol'

# Creating a variable that saves the name of the current directory
dirname = os.path.dirname(__file__)

#Creating variables with the absolute paths of each input file
par_in_file = os.path.join(dirname, par_rel_path)
wth_in_file = os.path.join(dirname, wth_rel_path)
irr_in_file = os.path.join(dirname, irr_rel_path)
sol_in_file = os.path.join(dirname, sol_rel_path)

# Creating a formatted date to add to the end of saved files:
date = datetime.today().strftime('%m_%d_%Y')
# Specifying the folder for output to be saved to:
output_folder = os.path.join(dirname, 'Example_Output/')
# Name of the Output file - names will be unique to the day
model_output_file = f'{output_folder}sdata_into_model_test_{date}.out'


# # **************************** SECTION 3 ****************************
# Setting up the water balance model:
# Parameters class:
par = fao.Parameters()
par.loadfile(filepath=par_in_file)

# Weather class:
wth = fao.Weather(filepath=wth_in_file)

# Irrigation class:
irr = fao.Irrigation(filepath=irr_in_file)

# Soil Profile class:
sol = SoilProfile(filepath=sol_in_file)

# Model class:
mdl = Model(start='2022-129',
            end='2022-248',
            par=par,
            wth=wth,
            irr=irr,
            sol=sol,
            cons_p=True)
mdl.run()
mdl.savefile(filepath=model_output_file)

# Making sure Model updates didn't break default version of the model:
default_mdl = Model(start='2022-129',
                    end='2022-248',
                    par=par,
                    wth=wth,
                    irr=irr,
                    cons_p=True)
default_mdl.run()
default_mdl.savefile(filepath=f'{output_folder}default_model_'
                              f'test_{date}.out')
