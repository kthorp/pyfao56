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
    cnames : list
        Column names for sdata
    label : str, optional
        Provide a string to customize plot/unit information and
        other metadata for output file (default = None).
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

    def __init__(self, filepath=None, label=None):
        """Initialize the SoilProfile class attributes.

        If filepath is provided, soil data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None).
        label : str, optional
            Provide a string to customize plot/unit information and
            other metadata for output file (default = None).
        """

        self.timestamp = datetime.datetime.now().strftime('"%Y-%m-%d '
                                                          '%H:%M:%S"')
        if label is None:
            self.label = 'File Creation Timestamp: ' + self.timestamp
            self.customlabel = False
        else:
            self.label = 'File Creation Timestamp: ' + self.timestamp \
                         + '\n' + label
            self.customlabel = True
        self.cnames = ['thetaFC', 'thetaWP', 'theta0']
        self.sdata = pd.DataFrame(columns=self.cnames)

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilProfile class as a string"""

        fmts = {'__index__':'{:5d}'.format,
                'thetaFC'  :'{:7.3f}'.format,
                'thetaWP'  :'{:7.3f}'.format,
                'theta0'   :'{:7.3f}'.format}
        ast ='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Soil Profile Data\n'
             '{:s}\n'
             '{:s}\n'
             'Depth').format(ast,self.label,ast)
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
            start_line = None
            end_line = None
            for i, line in enumerate(lines):
                if line.strip() == ast:
                    if start_line is None:
                        start_line = i
                    elif end_line is None:
                        end_line = i
                    else:
                        raise ValueError('Invalid file format. Too many'
                                         ' asterisk identifier lines '
                                         'found.')
            if start_line is None or end_line is None:
                raise ValueError("Invalid file format. Asterisk "
                                 "identifiers not found.")
            if not end_line == 3:
                self.timestamp = str(lines[start_line + 3][26:45])
                if start_line + 4 == end_line:
                    if not self.customlabel:
                        self.label = 'File Creation Timestamp: "' \
                                     + self.timestamp + '"'
                else:
                    label = lines[start_line + 4:end_line]
                    label[-1] = label[-1].rstrip()
                    self.label = 'File Creation Timestamp: "' \
                                 + self.timestamp + '"' + '\n' + \
                                 ''.join(label)

            for line in lines[end_line+2:]:
                line = line.strip().split()
                depth = int(line[0])
                data = list()
                for i in list(range(1, 4)):
                    data.append(float(line[i]))
                self.sdata.loc[depth] = data

    def customload(self):
        """Override this function to customize loading soil data."""

        pass
