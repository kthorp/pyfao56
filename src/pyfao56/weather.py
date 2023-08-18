"""
########################################################################
The weather.py module contains the Weather class, which provides I/O
tools for defining weather input data, as required for FAO-56
calculations.

The weather.py module contains the following:
    Weather - A class for managing weather data for FAO-56 calculations

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
08/03/2022 Added an input variable for measured vapor pressure
########################################################################
"""

import pandas as pd
from pyfao56 import refet
import datetime

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
    label : str, optional
        Provide a string to customize plot/unit information and
        other metadata for output file (default = None).
    wdata : DataFrame
        Weather data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Srad','Tmax','Tmin','Vapr','Tdew','RHmax','RHmin',
                   'Wndsp','Rain','ETref','MorP']
            Srad  - Incoming solar radiation (MJ/m2)
            Tmax  - Daily maximum air temperature (deg C)
            Tmin  - Daily minimum air temperature (deg C)
            Vapr  - Daily average vapor pressure (kPa)
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

    def __init__(self,filepath=None,label=None):
        """Initialize the Weather class attributes.

        If filepath is provided, weather data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        label : str, optional
            Provide a string to customize plot/unit information and
            other metadata for output file (default = None).
        """

        self.rfcrp = 'S'
        self.z     = float('NaN')
        self.lat   = float('NaN')
        self.wndht = float('NaN')
        self.cnames = ['Srad','Tmax','Tmin','Vapr','Tdew','RHmax',
                       'RHmin','Wndsp','Rain','ETref','MorP']
        self.wdata = pd.DataFrame(columns=self.cnames)
        self.timestamp = datetime.datetime.now().strftime('"%Y-%m-%d '
                                                         '%H:%M:%S"')
        if label is None:
            self.label = 'File Creation Timestamp: ' + self.timestamp
            self.customlabel = False
        else:
            self.label = 'File Creation Timestamp: ' + self.timestamp \
                         + '\n' + label
            self.customlabel = True
        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the Weather class variables as a string."""

        fmts = {'Srad':'{:6.2f}'.format,'Tmax':'{:6.2f}'.format,
                'Tmin':'{:6.2f}'.format,'Tdew':'{:6.2f}'.format,
                'Vapr':'{:6.2f}'.format,'RHmax':'{:6.2f}'.format,
                'RHmin':'{:6.2f}'.format,'Wndsp':'{:6.2f}'.format,
                'Rain':'{:6.2f}'.format,'ETref':'{:6.2f}'.format,
                'MorP':'{:>5s}'.format}
        ast='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Weather Data\n'
             '{:s}\n'
             '{:s}\n'
             '{:>12s} Reference crop - Short (\'S\') or Tall (\'T\')\n'
             '{:12.7f} Weather station elevation (z) (m)\n'
             '{:12.7f} Weather station latitude (decimal degrees)\n'
             '{:12.7f} Wind speed measurement height (m)\n\n'
             'Daily weather data:\n'
             'Year-DOY'
             ).format(ast,self.label,ast,self.rfcrp,self.z,self.lat,
                      self.wndht)
        for cname in self.cnames:
            s += '{:>7s}'.format(cname)
        s += '\n'
        if not self.wdata.empty:
            s += self.wdata.to_string(header=False,na_rep='   NaN',
                                      formatters=fmts)
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
            print('The filepath for weather data is not found.')
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
# ----------------------------Note to Kelly-----------------------------
# I have made changes to improve flexibility and incorporate line
# identifiers for standardized-yet-flexible file loading. These changes
# allow users to customize the I/O files while maintaining the desired
# functionality.

# Overview:
# The loadfile function reads a weather data file and extracts relevant
# information. It uses asterisk lines as file identifiers to locate the
# timestamp and the user-defined label for the file (if provided).

# Customized Label:
# The function supports a user-defined label for the weather data file.
# The standard label format is:
#   self.label = 'File Creation Timestamp: ' + self.timestamp + '\n' +
#                user_supplied_label_string
# The function is designed to work with labels of any length. In testing,
# it successfully handled labels like None, '2023 LIRF Weather Data' and
# '2023 \nLIRF \n Weather \n Data'.

# Error Handling:
# The function raises an error if someone tries to load a file where the
# label consists of 72 asterisks, indicating an invalid file format.

# Step-by-Step Explanation:
# 1. The function attempts to open the file specified by the filepath.
# 2. If the file opens successfully, then it reads the file contents and
#    stores them in the lines variable.
# 3. It searches for lines in the file that consist of 72 asterisks
#    and keeps track of the line numbers where they are found.
#    - If no asterisk lines are found, it raises a ValueError.
#    - If > two asterisk lines are found, it raises a ValueError.
#    - If exactly two asterisk lines are found, it extracts information
#      from the lines in between.
# 4. The function retrieves the timestamp from start_line + 3,
#    specifically from character positions 26 to 45. The timestamp is
#    stored in the timestamp attribute of the class.
# 5. If there is only one line between the timestamp line and the end_line,
#    the function creates a label containing only the file creation
#    timestamp. Otherwise, it follows the standard label format to
#    create a label from the lines between the timestamp line and the
#    end_line.
# 6. The function extracts weather data from specific lines after the
#    end_line and assigns the values to the corresponding attributes.
#    It creates an empty DataFrame named wdata with column names
#    specified by the cnames attribute. It then iterates over the lines
#    starting from end_line + 8, processes each line to extract data,
#    and adds it to the wdata DataFrame.

# Please remove these comments when merging.
# ------------------------------Best, Josh------------------------------

# 1.
        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for weather data is not found.')
        else:
            ast = '*' * 72
# 2.
            lines = f.readlines()
            f.close()

# 3.
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
# 4.
            if not end_line == 3: #added later to preserve v1.1 file formats
                self.timestamp = str(lines[start_line+3][26:45])
# 5.
                if start_line+4 == end_line:
                    if not self.customlabel:
                        self.label = 'File Creation Timestamp: "'\
                                     + self.timestamp + '"'
                else:
                    label = lines[start_line+4:end_line]
                    label[-1] = label[-1].rstrip()
                    self.label = 'File Creation Timestamp: "'\
                                 + self.timestamp + '"' + '\n' + \
                                 ''.join(label)
# 6.
            self.rfcrp = lines[end_line+1][:12].strip()
            self.z = float(lines[end_line+2][:12])
            self.lat = float(lines[end_line+3][:12])
            self.wndht = float(lines[end_line+4][:12])
            self.wdata = pd.DataFrame(columns=self.cnames)
            for line in lines[end_line+8:]:
                line = line.strip().split()
                year = line[0][:4]
                doy = line[0][-3:]
                key = '{:04d}-{:03d}'.format(int(year),int(doy))
                data = list()
                for i in list(range(1,11)):
                    data.append(float(line[i]))
                data.append(line[11].strip())
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
                                self.wdata.loc[index,'Vapr'],
                                self.wdata.loc[index,'Tdew'],
                                self.wdata.loc[index,'RHmax'],
                                self.wdata.loc[index,'RHmin'],
                                self.wdata.loc[index,'Wndsp'],
                                self.wndht)
        return ETref
