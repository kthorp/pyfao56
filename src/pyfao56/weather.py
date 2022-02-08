"""
########################################################################
The weather.py module contains the Weather class, which provides I/O
tools for defining weather input data, as required for FAO-56
calculations.

The weather.py module contains the following:
    Weather - A class for managing weather data for FAO-56 calculations

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

import pandas as pd
from pyfao56 import refet

class Weather:
    """A class for managing weather data for FAO-56 calculations.

    Attributes
    ----------
    rfcrp : str
        Type of reference crop  - Short ('S') or Tall ('T')
    z : float
        Weather station elevation (z) (m)
    lat : float
        Weather station latitude (decimal degrees)
    wndht : float
        Weather station wind speed measurement height (m)
    cnames : list
        Column names for wdata
    wdata : DataFrame
        Weather data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Srad','Tmax','Tmin','Tdew','RHmax','RHmin',
                   'Wndsp','Rain','ETref','MorP']
            Srad  - Incoming solar radiation (MJ/m2)
            Tmax  - Daily maximum air temperature (deg C)
            Tmin  - Daily minimum air temperature (deg C)
            Tdew  - Daily average dew point temperature (deg C)
            RHmax - Daily maximum relative humidity (%)
            RHmin - Daily minimum relative humidity (%)
            Wndsp - Daily average wind speed (m/s)
            Rain  - Daily precipitation (mm)
            ETref - Daily reference ET (mm)
            MorP  - Measured ('M') or Predicted ('P') data

    Methods
    -------
    savefile(filepath='pyfao56.wth')
        Save the weather data to a file
    loadfile(filepath='pyfao56.wth')
        Load the weather data from a file
    customload()
        Users can override for custom weather loading, for example from
        meteorological network webpages
    compute_etref(index)
        Compute ASCE standardized reference ET for the weather data at
        index in self.wdata
    """

    def __init__(self,filepath=None):
        """Initialize the Weather class attributes.

        If filepath is provided, weather data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        """

        self.rfcrp = 'S'
        self.z     = float('NaN')
        self.lat   = float('NaN')
        self.wndht = float('NaN')
        self.cnames = ['Srad','Tmax','Tmin','Tdew','RHmax','RHmin',
                       'Wndsp','Rain','ETref','MorP']
        self.wdata = pd.DataFrame(columns=self.cnames)

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the Weather class variables as a string."""

        fmts = {'Srad':'{:6.2f}'.format,'Tmax':'{:6.2f}'.format,
                'Tmin':'{:6.2f}'.format,'Tdew':'{:6.2f}'.format,
                'RHmax':'{:6.2f}'.format,'RHmin':'{:6.2f}'.format,
                'Wndsp':'{:6.2f}'.format,'Rain':'{:6.2f}'.format,
                'ETref':'{:6.2f}'.format,'MorP':'{:>5s}'.format }
        ast='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 in Python\n'
             'Weather Data\n'
             '{:s}\n'
             '{:>12s} Reference crop - Short (\'S\') or Tall (\'T\')\n'
             '{:12.7f} Weather station elevation (z) (m)\n'
             '{:12.7f} Weather station latitude (decimal degrees)\n'
             '{:12.7f} Wind speed measurement height (m)\n\n'
             'Daily weather data:\n'
             'Year-DOY'
             ).format(ast,ast,self.rfcrp,self.z,self.lat,self.wndht)
        for cname in self.cnames:
            s += '{:>7s}'.format(cname)
        s += '\n'
        s += self.wdata.to_string(header=False,formatters=fmts)
        return s

    def savefile(self,filepath='pyfao56.wth'):
        """Save pyfao56 weather data to a file.

        Parameters
        ----------
        filepath : str, optional
           Any valid filepath string (default = 'pyfao56.wth')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print("The filepath for weather data is not found.")
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.wth'):
        """Load pyfao56 weather data from a file.

        Parameters
        ----------
        filepath : str, optional
           Any valid filepath string (default = 'pyfao56.wth')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print("The filepath for weather data is not found.")
        else:
            lines = f.readlines()
            f.close()
            self.rfcrp = lines[4][:12].strip()
            self.z = float(lines[5][:12])
            self.lat = float(lines[6][:12])
            self.wndht = float(lines[7][:12])
            self.wdata = pd.DataFrame(columns=self.cnames)
            data = []
            for line in lines[11:]:
                line = line.strip().split()
                year = line[0][:4]
                doy = line[0][-3:]
                key = '{:04d}-{:03d}'.format(int(year),int(doy))
                data[:] = []
                for i in list(range(1,10)):
                    data.append(float(line[i]))
                data.append(line[10].strip())
                self.wdata.loc[key] = data

    def customload(self):
        """Override this function to customize loading weather data."""

        pass

    def compute_etref(self,index):
        """Compute ASCE standardized reference ET for data at index.

        Parameters
        ----------
        index : str
            The Year-DOY ('yyyy-ddd') index of self.wdata

        Returns
        -------
        ETref : float
            Daily standardized reference evapotranspiration for the
            short or tall reference crop (mm)
        """

        ETref = refet.ascedaily(self.rfcrp,
                                self.z,
                                self.lat,
                                float(index[-3:]),#DOY
                                self.wdata.loc[index,'Srad'],
                                self.wdata.loc[index,'Tmax'],
                                self.wdata.loc[index,'Tmin'],
                                self.wdata.loc[index,'Tdew'],
                                self.wdata.loc[index,'RHmax'],
                                self.wdata.loc[index,'RHmin'],
                                self.wdata.loc[index,'Wndsp'],
                                self.wndht)
        return ETref
