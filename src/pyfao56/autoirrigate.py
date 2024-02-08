"""
########################################################################
The autoirrigate.py module contains the AutoIrrigate class, which
provides I/O tools for defining input parameters for scheduling
irrigation automatically in pyfao56.

The autoirrigate.py module contains the following:
    AutoIrrigate - A class for managing input parameters for automatic
        irrigation calculations

12/08/2023 Initial Python framework established for auto irrigation
02/08/2024 Further development of definitions with Fared Farag
########################################################################
"""

import datetime

class AutoIrrigate:
    """A class for managing input parameters for FAO-56 calculations

    Attributes
    ----------

    Whether or not to consider autoirrigation
    alre : boolean
        Autoirrigate only after last reported irrigation event
    idow : list
        Autoirrigate only on specified days of the week
    idoy : list
        Autoirrigate only on specified days of the year
    fpdep : float
        Threshold forcasted precipitation depth (mm)
    fpday : int
        Number of days to consider forecasted precipitation (days)
    fpact : str
        'none' - Do not autoirrigate
        'reduce' - Deduct forecasted precip from irrigation amounts

    Irrigation Triggering
    cmad : float
        Constant maximum allowable depletion (cm3/cm3)
    vmad : list
        Variable maximum allowable depletion (cm3/cm3)
    cksc : float
        Constant critical transpiration reduction factor, Ks (0-1)
    vksc : list
        Variable critical transpiration reduction factor, Ks (0-1)
    dsli : int
        Days since last irrigation event (days)
    dsle : int
        Days since last watering event, including precipitation (days)
    evnt : int
        Depth of water to be considered a watering event (mm)

    Irrigation Amount
    icon : float
        Constant irrigation amount (mm)
    imin : float
        Minimum irrigation amount (mm)
    imax : float
        Maximum irrigation amount (mm)
    itdr : float
        Target root-zone depletion following irrigation (mm)
    itfdr : float
        Target root-zone fractional depletion following irrigation (mm)
    ietr : boolean
        Replace (ETcadj-Rain) since last irrigation from past X number of days (days)
    ieff : float
        Irrigation application efficiency (%)

    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class

    Methods
    -------
    savefile(filepath='pyfao56.ati')
        Save the autoirrigate parameters to a file
    loadfile(filepath='pyfao56.ati')
        Load the autoirrigate parameters from a file
    """

    def __init__(self, mad=0.4, irrEfficiency=1.0, comment=""):
        """Initialize the AutoIrrigate class attributes.

        Parameters
        ----------
        mad            : float, optional, default = 0.4
        irrEfficiency  : float, optional, default = 1.0
        comment        : str  , optional, default = ''
        """

        if mad < 0.0:
            raise ValueError("mad must be a positive number")
        if not 0.0 <= irrEfficiency <= 1.0:
            raise ValueError("irrEfficiency must be between 0.0 and 1.0")

        self.mad = float(mad)
        self.irrEfficiency = float(irrEfficiency)
        self.comment = "Comments: " + comment.strip()
        self.tmstmp = datetime.datetime.now()

    def __str__(self):
        """Represent the AutoIrrigate class variables as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'AutoIrrigate Data\n'
           'Timestamp: {:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:s}\n'
          ).format(ast,timestamp,ast,self.comment,ast)
        return s

    def savefile(self,filepath='pyfao56.ati'):
        """Save pyfao56 autoirrigate parameters to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.ati')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for autoirrigate data is not found.')
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.ati'):
        """Load pyfao56 autoirrigate parameters from a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.ati')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for autoirrigate data is not found.')
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
            for line in lines[endast+1:]:
                line = line.strip().split(',')[0].split()
                if line[1].lower() == 'kcbini':
                    self.Kcbini = float(line[0])
