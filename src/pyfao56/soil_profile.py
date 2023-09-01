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
09/27/2022 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

import pandas as pd
import datetime

class SoilProfile:
    """A class for managing layered soil profile data in pyfao56.

    Attributes
    ----------
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class
    cnames : list
        Column names for sdata
    sdata : DataFrame
        Soil profile data as float
        index = Bottom depth of the layer as integer (cm)
        columns = ['thetaFC', 'thetaWP', 'theta0']
            thetaFC - Volumetric Soil Water Content, Field Capacity
                      (cm3/cm3)
            thetaWP - Volumetric Soil Water Content, Wilting Point
                      (cm3/cm3)
            theta0  - Volumetric Soil Water Content, Initial
                      (cm3/cm3)

    Methods
    -------
    savefile(filepath='pyfao56.sol')
        Save the soil profile data to a file
    loadfile(filepath='pyfao56.sol')
        Load soil profile data from a file
    customload()
        Users can override for custom loading of soil data.
    """

    def __init__(self, filepath=None, comment=''):
        """Initialize the SoilProfile class attributes.

        If filepath is provided, soil data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None).
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """

        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp = datetime.datetime.now()
        self.cnames = ['thetaFC', 'thetaWP', 'theta0']
        self.sdata = pd.DataFrame(columns=self.cnames)

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilProfile class as a string"""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        fmts = {'__index__':'{:5d}'.format,
                'thetaFC'  :'{:7.3f}'.format,
                'thetaWP'  :'{:7.3f}'.format,
                'theta0'   :'{:7.3f}'.format}
        ast ='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Soil Profile Data\n'
             'Timestamp: {:s}\n'
             '{:s}\n'
             '{:s}\n'
             '{:s}\n'
             'Depth').format(ast,timestamp,ast,self.comment,ast)
        for cname in self.cnames:
            s += '{:>8s}'.format(cname)
        s += '\n'
        if not self.sdata.empty:
            s += self.sdata.to_string(header=False,
                                      na_rep='    NaN',
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
            print('The filepath for soil profile data is not found.')
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
            print('The filepath for soil profile data is not found.')
        else:
            lines = f.readlines()
            f.close()
            ast = '*' * 72
            a = [i for i,line in enumerate(lines) if line.strip()==ast]
            endast = a[-1] 
            if endast == 3: #v1.1.0 and prior - no timestamps & metadata
                self.comment = 'Comments: '
            else:
                self.comment = ''.join(lines[5:endast]).strip()
            if endast >= 4:
                ts = lines[3].strip().split('stamp:')[1].strip()
                ts = datetime.datetime.strptime(ts,'%m/%d/%Y %H:%M:%S')
                self.tmstmp = ts
            for line in lines[endast+2:]:
                line = line.strip().split()
                depth = int(line[0])
                data = list()
                for i in list(range(1, 4)):
                    data.append(float(line[i]))
                self.sdata.loc[depth] = data

    def customload(self):
        """Override this function to customize loading soil data."""

        pass
