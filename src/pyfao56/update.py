"""
########################################################################
The update.py module contains the Update class, which provides I/O tools
for state variable updating during FAO-56 calculations.

The update.py module contains the following:
    Update - A class for managing state variable updates with FAO-56
        calculations

11/17/2021 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

import pandas as pd
import datetime

class Update:
    """A class for managing update data for FAO-56 calculations.

    At this time, update methods are available for the basal crop
    coefficient (Kcb), the plant height (h), and the crop cover (fc).

    Attributes
    ----------
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class
    udata : DataFrame
        Update data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Kcb','h','fc']
            Kcb - Basal crop coefficient (Kcb)
            h   - Plant height (h, m)
            fc  - Crop cover (fc, m)

    Methods
    -------
    savefile(filepath='pyfao56.upd')
        Save the update data to a file
    loadfile(filepath='pyfao56.upd')
        Load the update data from a file
    customload()
        Users can override for custom loading of update data
    getdata(index,var)
        Return a value from self.udata for model updating
    """

    def __init__(self,filepath=None,comment=''):
        """Initialize the Update class attributes.

        If filepath is provided, update data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """

        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp = datetime.datetime.now()
        self.udata = pd.DataFrame(columns=['Kcb','h','fc'])

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the Update class variables as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        pd.options.display.float_format = '{:6.4f}'.format
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'Update Data\n'
           'Timestamp: {:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:s}\n'
           'Year-DOY    Kcb      h     fc\n'
          ).format(ast,timestamp,ast,self.comment,ast)
        if not self.udata.empty:
            s += self.udata.to_string(header=False, na_rep='   NaN')
        return s

    def savefile(self,filepath='pyfao56.upd'):
        """Save pyfao56 update data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.upd')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for update data is not found.')
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.upd'):
        """Load pyfao56 update data from a file.

        Parameters
        ----------
        filepath : str, optional
           Any valid filepath string (default = 'pyfao56.upd')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for update data is not found.')
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
            self.udata = pd.DataFrame(columns=['Kcb','h','fc'])
            for line in lines[endast+2:]:
                line = line.strip().split()
                year = line[0][:4]
                doy = line[0][-3:]
                key = '{:04d}-{:03d}'.format(int(year),int(doy))
                self.udata.loc[key] = [float(line[1]),float(line[2]),
                                       float(line[3])]

    def customload(self):
        """Override this function to customize loading update data."""

        pass

    def getdata(self, index, var):
        """Obtain an update value for a variable, if available.

        Parameters
        ----------
        index : str
            A year-doy string (yyyy-ddd) as an index to self.udata
        var : str
            A column variable to return ('Kcb','h','fc')
        """

        try:
            return self.udata.loc[index,var]
        except:
            return float('NaN')
