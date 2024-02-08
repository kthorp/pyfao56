"""
########################################################################
The autoirrigate.py module contains the AutoIrrigate class, which
provides I/O tools for defining input parameters for scheduling
irrigation automatically in pyfao56.

The autoirrigate.py module contains the following:
    AutoIrrigate - A class for managing input parameters for automatic
        irrigation calculations

12/08/2023 Initial Python framework established for auto irrigation
########################################################################
"""

import datetime

class AutoIrrigate:
    """A class for managing input parameters for FAO-56 calculations

    Attributes
    ----------
    mad : float
        maximum allowable depletion
    irrEfficiency : float
        irrigation efficiency (between 0 and 1)
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class

    Methods
    -------
    savefile(filepath='pyfao56.par')
        Save the parameter data to a file
    loadfile(filepath='pyfao56.par')
        Load the parameter data from a file
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

    def run():
        pass

    def __str__(self):
        """Represent the Parameter class variables as a string."""

        self.tmstmp = datetime.datetime.now()

        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'Parameter Data\n'
           'Timestamp: {:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:9.4f} Kcbini, Kcb Initial (FAO-56 Table 17)\n'
           '{:9.4f} Kcbmid, Kcb Mid (FAO-56 Table 17)\n'
           '{:9.4f} Kcbend, Kcb End (FAO-56 Table 17)\n'
           '{:9d} Lini, Length Stage Initial (days) (FAO-56 Table 11)\n'
           '{:9d} Ldev, Length Stage Development (days) '
           '(FAO-56 Table 11)\n'
           '{:9d} Lmid, Length Stage Mid (days) (FAO-56 Table 11)\n'
           '{:9d} Lend, Length Stage End (days) (FAO-56 Table 11)\n'
           '{:9.4f} hini, Plant Height Initial (m)\n'
           '{:9.4f} hmax, Plant Height Maximum (m) (FAO-56 Table 12)\n'
           '{:9.4f} thetaFC, Vol. Soil Water Content, Field Capacity '
           '(cm3/cm3)\n'
           '{:9.4f} thetaWP, Vol. Soil Water Content, Wilting Point '
           '(cm3/cm3)\n'
           '{:9.4f} theta0, Vol. Soil Water Content, Initial '
           '(cm3/cm3)\n'
           '{:9.4f} Zrini, Rooting Depth Initial (m)\n'
           '{:9.4f} Zrmax, Rooting Depth Maximum (m) '
           '(FAO-56 Table 22)\n'
           '{:9.4f} pbase, Depletion Fraction (p) (FAO-56 Table 22)\n'
           '{:9.4f} Ze, Depth of surface evaporation layer (m) '
           '(FAO-56 Table 19 and Page 144)\n'
           '{:9.4f} REW, Total depth Stage 1 evaporation (mm) '
           '(FAO-56 Table 19)\n'
          ).format(ast,timestamp,ast,self.comment,ast,self.Kcbini,
                   self.Kcbmid,self.Kcbend,self.Lini,self.Ldev,
                   self.Lmid,self.Lend,self.hini,self.hmax,self.thetaFC,
                   self.thetaWP,self.theta0,self.Zrini,self.Zrmax,
                   self.pbase,self.Ze,self.REW)
        return s

    def savefile(self,filepath='pyfao56.par'):

        """Save pyfao56 parameters to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.par')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for parameter data is not found.')
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.par'):
        """Load pyfao56 parameters from a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.par')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for parameter data is not found.')
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
                elif line[1].lower() == 'kcbmid':
                    self.Kcbmid = float(line[0])
                elif line[1].lower() == 'kcbend':
                    self.Kcbend = float(line[0])
                elif line[1].lower() == 'lini':
                    self.Lini = int(line[0])
                elif line[1].lower() == 'ldev':
                    self.Ldev = int(line[0])
                elif line[1].lower() == 'lmid':
                    self.Lmid = int(line[0])
                elif line[1].lower() == 'lend':
                    self.Lend = int(line[0])
                elif line[1].lower() == 'hini':
                    self.hini = float(line[0])
                elif line[1].lower() == 'hmax':
                    self.hmax = float(line[0])
                elif line[1].lower() == 'thetafc':
                    self.thetaFC = float(line[0])
                elif line[1].lower() == 'thetawp':
                    self.thetaWP = float(line[0])
                elif line[1].lower() == 'theta0':
                    self.theta0 = float(line[0])
                elif line[1].lower() == 'zrini':
                    self.Zrini = float(line[0])
                elif line[1].lower() == 'zrmax':
                    self.Zrmax = float(line[0])
                elif line[1].lower() == 'pbase':
                    self.pbase = float(line[0])
                elif line[1].lower() == 'ze':
                    self.Ze = float(line[0])
                elif line[1].lower() == 'rew':
                    self.REW = float(line[0])
