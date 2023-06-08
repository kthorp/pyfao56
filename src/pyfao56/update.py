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
    label : str, optional
        Provide a string to customize plot/unit information and
        other metadata for output file (default = None).
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

    def __init__(self,filepath=None,label=None):
        """Initialize the Update class attributes.

        If filepath is provided, update data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
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
        self.udata = pd.DataFrame(columns=['Kcb','h','fc'])

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the Update class variables as a string."""

        pd.options.display.float_format = '{:6.4f}'.format
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'Update Data\n'
           '{:s}\n'
           '{:s}\n'
           'Year-DOY    Kcb      h     fc\n'
          ).format(ast,self.label,ast)
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

            self.udata = pd.DataFrame(columns=['Kcb','h','fc'])
            for line in lines[end_line+2:]:
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
