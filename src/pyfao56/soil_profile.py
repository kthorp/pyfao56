#TODO and notes to Josh

#Renamed the module as "soil_profile.py" and class as "SoilProfile"
#because the class pertains to defining soil properties and not so much
#about "soil water"

#Updated the module docstring.

#Need to simplify the __init__ function.  The user has two choices:
#1) provide a file with data to populate self.sdata
#or 2) write custom code to interact with the class to define self.sdata
#programmatically.  I have added a customload function that can be used
#for this.

#Simplify the input file...What is the minimum amount of data required
#from the user to make this work. Don't make them define extraneous
#parameters.

#Name the DataFrame sdata
#I wouldn't advise making a floating point variable as the index of the
#DataFrame (i.e., soil depth)
#Perhaps define the depth as an integer in centimeters?
#Probably layer top depth, layer bottom depth, and layer thickness
#do not all need to be defined by the user.
    #What is the minimum data?
        #Bottom layer depth (cm)
        #thetaFC (cm3/cm3)
        #thetaWP (cm3/cm3)
        #theta0 (cm3/cm3)
        #Keep units as cm3/cm3 as that's how I have it in Parameters class
    #Can the rest (thinkness and depths) be calculated as needed in model.py?
    #The primary question at this time is the optimum design for the
    #sdata DataFrame.  We can discuss what provides the data you need,
    #while keeping it simple and maintaining consistency with rest of 
    #pyfao56.

#Change default filenames to pyfao56.sol

#Need to modify __str__, savefile, and loadfile routines based on what
#we decide about the above points.

"""
########################################################################
The soil_profile.py module contains the SoilProfile class, which 
provides I/O tools for defining soil properties stratified by soil
layer. Layered soil properties can be used (optionally) in the model
class to simulate the water balance, assuming the user has data to
define the soil properties by layer. Alternatively, users can define
soil properties using three parameters in the Parameters class (theta0,
thetaFC, and thethaWP), but this method assumes a single homogenous soil
layer.

The soil_profile.py module contains the following:
    SoilProfile - A class for managing soil properties stratified
       by soil layer

08/10/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
09/16/2022 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

import pandas as pd

class SoilProfile:
    """A class for managing layered soil profile data in pyfao56.

    Attributes
    ----------
    cnames : list
        Column names for sdata
    sdata : DataFrame
        Soil profile data as float
        index = Bottom depth of the layer in centimeters (int)
        columns = ['Lr_Strt', 'Lr_End', 'Lr_Thck','thetaFC', 'thetaIN',
                   'thetaWP', 'FC_mm', 'IN_mm', 'WP_mm']
            Lr_Strt - depth (m) of the start of the assumed soil layer
            Lr_End  - depth (m) of the end of the assumed soil layer
            Lr_Thck - thickness, in meters, of the assumed soil layer
                      (calculated at class initialization)
            thetaFC - volumetric soil water content (m^3/m^3) of the
                      assumed soil layer's field capacity value
            thetaIN - initial volumetric soil water content (m^3/m^3)
                      measurement of the assumed soil layer
            thetaWP - volumetric soil water content (m^3/m^3) of the
                      soil layer's assumed permanent wilting point value
            FC_mm   - field capacity (mm) of the assumed soil layer
                      (calculated at class initialization)
            IN_mm   - initial soil water content (mm) of the assumed
                      soil layer (calculated at class initialization)
            WP_mm   - wilting point (mm) of the assumed soil layer
                      (calculated at class initialization)


    Methods
    -------
    savefile(filepath='pyfao56.sol')
        Save the soil profile data to a file
    loadfile(filepath='pyfao56.sol')
        Load soil profile data from a file
    """

    def __init__(self,filepath=None):
        """Initialize the SoilProfile class attributes.

        If filepath is provided, soil data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None).
        """

        self.cnames = ['Lr_Strt', 'Lr_End', 'Lr_Thck',
                       'thetaFC', 'theta0', 'thetaWP', 'FC_mm',
                       'IN_mm', 'WP_mm']
        self.sdata = pd.DataFrame(columns=self.cnames)
        
        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilProfile class as a string"""

        ast = '*' * 72
        # Returning string for the sdata dataframe
        fmts = ['{:9.5f}'.format] * 9
        s = (f'{ast}\n'
             f'pyfao56: FAO-56 in Python\n'
             f'Soil Water Information\n'
             f'{ast}\n'
             f'Soil Water Characteristics Organized by Layer:\n'
             f'Depth  ')
        for cname in self.cnames:
            s += f'{cname:<10}'
        s += f'\n'
        s += self.soil_water_profile.to_string(header=False,
                                               index_names=False,
                                               na_rep='      NaN',
                                               formatters=fmts)
        return s

    def savefile(self, filepath='pyfao56.sh2o'):
        """Save pyfao56 soil profile data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.sol')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """
        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print("The filepath for soil water data is not found.")
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.sol'):
        """Load pyfao56 soil profile data from a file.

        Parameters
        ----------
        filepath : str, optional
           Any valid filepath string (default = 'pyfao56.sol')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """
        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print("The filepath for soil water data is not found.")
        else:
            lines = f.readlines()
            f.close()
            self.soil_water_profile = pd.DataFrame(columns=self.cnames)
            self.soil_water_profile.index.name = 'Depth'
            for line in lines[6:]:
                line = line.strip().split()
                depth = line[0]
                data = list()
                for i in list(range(1, 10)):
                    data.append((float(line[i])))
                # data.append(line[10].strip())
                self.soil_water_profile.loc[depth] = data
            self.depths = list(self.soil_water_profile.index.values)
            self.theta_fc = list(self.soil_water_profile['thetaFC'])
            self.theta_ini = list(self.soil_water_profile['thetaIN'])
            self.theta_wp = list(self.soil_water_profile['thetaWP'])
    
    def customload(self):
        """Override this function to customize loading soil data."""
        
        pass
