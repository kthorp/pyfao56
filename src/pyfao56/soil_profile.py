# Notes for Kelly

# TODO: I (Josh) am not super confident in my formatting abilities. I think it is worthwhile for you to (quickly)double
#  check my __str__ method.

# Should we consider a different file extension for the soil files? .sol seems to be used by Adobe Flash Player
# (https://file.org/extension/sol). So, I think there is a chance that a user's OS might try to open it as an
# Adobe file. I am not sure how that all works, but I know PyCharm offered to download a plugin for handling that sort
# of file extension.

"""
########################################################################
The soil_profile.py module contains the SoilProfile class, which
provides I/O tools for defining soil properties stratified by soil
layer. Layered soil properties can be used (optionally) in the model
class to simulate the water balance, assuming the user has data to
define the soil properties by layer. Alternatively, users can define
soil properties using three parameters in the Parameters class (theta0,
thetaFC, and thetaWP), but this method assumes a single homogenous soil
layer.
The soil_profile.py module contains the following:
    SoilProfile - A class for managing soil properties stratified
       by soil layer
08/10/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
09/21/2022 Finalized updates for inclusion in the pyfao56 Python package
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
    customload()
        Override this function to customize loading soil data.
    """

    def __init__(self, filepath=None):
        """Initialize the SoilProfile class attributes.
        If filepath is provided, soil data is loaded from the file.
        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None).
        """

        self.cnames = ['thetaFC', 'thetaWP', 'thetaIN']
        self.sdata = pd.DataFrame(columns=self.cnames)

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilProfile class as a string"""

        ast = '*' * 72
        # Returning string for the sdata dataframe
        fmts = ['{:9.5f}'.format] * 3
        s = (f'{ast}\n'
             f'pyfao56: FAO-56 in Python\n'
             f'Soil Profile Information\n'
             f'{ast}\n'
             f'Soil Characteristics Organized by Layer:\n'
             f'Depth ')
        for cname in self.cnames:
            s += f'{cname:<10}'
        s += f'\n'
        s += self.sdata.to_string(header=False,
                                  index_names=False,
                                  na_rep='      NaN',
                                  formatters=fmts)
        return s

    def savefile(self, filepath='pyfao56.sol'):
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
            print("The filepath for soil profile data is not found.")
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
            print("The filepath for soil profile data is not found.")
        else:
            lines = f.readlines()
            f.close()
            for line in lines[6:]:
                line = line.strip().split()
                depth = int(line[0])
                data = list()
                for i in list(range(1, 4)):
                    data.append((float(line[i])))
                # data.append(line[10].strip())
                self.sdata.loc[depth] = data

    def customload(self):
        """Override this function to customize loading soil data."""

        pass