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
12/13/2023 Added irrigation efficiency term for each irrigation event
########################################################################
"""

import pandas as pd
import datetime

class Irrigation:
    """A class for managing irrigation data for FAO-56 calculations

    Attributes
    ----------
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class
    idata : DataFrame
        Irrigation data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Depth','fw','ieff']
            Depth - Irrigation depth (mm)
            fw - fraction of soil surface wetted (FAO-56 Table 20)
            ieff - Irrigation application efficiency (%)

    Methods
    -------
    savefile(filepath='pyfao56.irr')
        Save irrigation data to a file
    loadfile(filepath='pyfao56.irr')
        Load irrigation data from a file
    addevent(year,doy,depth,fw,ieff)
        Add an irrigation event to self.idata
    customload()
        Users can override for custom loading of irrigation data.
    """

    def __init__(self,filepath=None,comment=''):
        """Initialize the Irrigation class attributes.

        If filepath is provided, irrigation data is loaded from the file

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """

        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp = datetime.datetime.now()
        self.idata = pd.DataFrame(columns=['Depth','fw','ieff'])

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the Irrigation class variables as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        fmts = {'Depth':'{:6.2f}'.format,'fw':'{:6.2f}'.format,
                'ieff':'{:6.1f}'.format}
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'Irrigation Data\n'
           'Timestamp: {:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:s}\n'
           'Year-DOY  Depth     fw IrrEff\n'
          ).format(ast,timestamp,ast,self.comment,ast)
        if not self.idata.empty:
            s += self.idata.to_string(header=False,formatters=fmts)
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
            print('The filepath for irrigation data is not found.')
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
            print('The filepath for irrigation data is not found.')
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
            self.idata = pd.DataFrame(columns=['Depth','fw','ieff'])
            for line in lines[endast+2:]:
                line = line.strip().split()
                year = line[0][:4]
                doy = line[0][-3:]
                key = '{:04d}-{:03d}'.format(int(year),int(doy))
                data = list()
                data.append(float(line[1]))
                data.append(float(line[2]))
                if len(line) == 3: #v1.2.1 and prior - no efficiency
                    data.append(100.0)
                else:
                    data.append(float(line[3]))
                self.idata.loc[key] = data

    def addevent(self, year, doy, depth, fw, ieff=100.0):
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
        ieff  : float, optional
            Irrigation application efficiency (%)
            (default = 100.0)
        """

        key = '{:04d}-{:03d}'.format(year,doy)
        self.idata.loc[key] = [depth,fw,ieff]

    def customload(self):
        """Override this function to customize loading irrigation
        data."""

        pass
