"""
########################################################################
The irrigation.py module contains the Irrigation class, which provides
I/O tools for defining the irrigation management schedule, as required
for FAO-56 calculations.

The irrigation.py module contains the following:
    Irrigation - A class for managing irrigation data for FAO-56
        calculations

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

import pandas as pd

class Irrigation:
    """A class for managing irrigation data for FAO-56 calculations

    Attributes
    ----------
    idata : DataFrame
        Irrigation data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Depth','fw']
            Depth - Irrigation depth (mm)
            fw - fraction of soil surface wetted (FAO-56 Table 20)

    Methods
    -------
    savefile(filepath='pyfao56.irr')
        Save irrigation data to a file
    loadfile(filepath='pyfao56.irr')
        Load irrigation data from a file
    addevent(year,doy,depth,fw)
        Add an irrigation event to self.idata
    """

    def __init__(self,filepath=None):
        """Initialize the Irrigation class attributes.

        If filepath is provided, irrigation data is loaded from the file

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        """

        self.idata = pd.DataFrame(columns=['Depth','fw'])

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the Irrigation class variables as a string."""

        pd.options.display.float_format = '{:6.2f}'.format
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 in Python\n'
           'Irrigation Data\n'
           '{:s}\n'
           'Year-DOY  Depth     fw\n'
          ).format(ast,ast)
        s += self.idata.to_string(header=False)
        return s

    def savefile(self,filepath='pyfao56.irr'):
        """Save pyfao56 irrigation data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.irr')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print("The filepath for irrigation data is not found.")
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.irr'):
        """Load pyfao56 irrigation data from a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.irr')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print("The filepath for irrigation data is not found.")
        else:
            lines = f.readlines()
            f.close()
            self.idata = pd.DataFrame(columns=['Depth','fw'])
            for line in lines[5:]:
                line = line.strip().split()
                year = line[0][:4]
                doy = line[0][-3:]
                key = '{:04d}-{:03d}'.format(int(year),int(doy))
                self.idata.loc[key] = [float(line[1]),float(line[2])]

    def addevent(self, year, doy, depth, fw):
        """Add an irrigation event to self.idata

        Parameters
        ----------
        year  : int
            The 4-digit year of the irrigation event
        doy   : int
            The day of year of the irrigation event
        depth : float
            The depth of irrigation (mm)
        fw    : float
            Fraction of soil surface wetted (FAO-56 Table 20)
        """

        key = '{:04d}-{:03d}'.format(year,doy)
        self.idata.loc[key] = [depth,fw]
