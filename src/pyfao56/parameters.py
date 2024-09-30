"""
########################################################################
The parameters.py module contains the Parameters class, which provides
I/O tools for defining input parameters, as required for FAO-56
calculations.

The parameters.py module contains the following:
    Parameters - A class for managing input parameters for FAO-56
        calculations

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
12/12/2023 Added CN2 parameter for runoff method
09/30/2024 Added inputs for single crop coefficient computation
########################################################################
"""

import datetime

class Parameters:
    """A class for managing input parameters for FAO-56 calculations

    Attributes
    ----------
    Kcini : float
        Kc Initial (FAO-56 Table 12)
    Kcmid : float
        Kc Mid (FAO-56 Table 12)
    Kcend : float
        Kc End (FAO-56 Table 12)
    Kcbini : float
        Kcb Initial (FAO-56 Table 17)
    Kcbmid : float
        Kcb Mid (FAO-56 Table 17)
    Kcbend : float
        Kcb End (FAO-56 Table 17)
    Lini : int
        Length Stage Initial (days) (FAO-56 Table 11)
    Ldev : int
        Length Stage Development (days) (FAO-56 Table 11)
    Lmid : int
        Length Stage Mid (days) (FAO-56 Table 11)
    Lend : int
        Length Stage End (days) (FAO-56 Table 11)
    hini : float
        Plant Height Initial (m)
    hmax : float
        Plant Height Maximum (m) (FAO-56 Table 12)
    thetaFC : float
        Volumetric Soil Water Content, Field Capacity (cm3/cm3)
    thetaWP : float
        Volumetric Soil Water Content, Wilting Point (cm3/cm3)
    theta0 : float
        Volumetric Soil Water Content, Initial (cm3/cm3)
    Zrini : float
        Rooting Depth Initial (m)
    Zrmax : float
        Rooting Depth Maximum (m) (FAO-56 Table 22)
    pbase : float
        Depletion Fraction (p) (FAO-56 Table 22)
    Ze : float
        Depth of surface evaporation layer (m) (FAO-56 Table 19 & p144)
    REW : float
        Total depth Stage 1 evaporation (mm) (FAO-56 Table 19)
    CN2 : int
        Curve Number for AWC II (ASCE (2016), Table 14-3, p452)
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

    def __init__(self, Kcini=0.35, Kcmid=1.15, Kcend=0.60, Kcbini=0.15,
                 Kcbmid=1.10, Kcbend=0.50, Lini=25, Ldev=50, Lmid=50,
                 Lend=25, hini=0.010, hmax=1.20, thetaFC=0.250,
                 thetaWP=0.100, theta0=0.100, Zrini=0.20, Zrmax=1.40,
                 pbase=0.50, Ze=0.10, REW=8.0, CN2=70, comment=''):
        """Initialize the Parameters class attributes.

        Default parameter values are given below. Users should update
        the parameters with values for their specific crop and field
        conditions based on FAO-56 documentation.

        Parameters
        ----------
        See Parameters class docstring for parameter definitions.
        Kcini   : float, optional, default = 0.35
        Kcmid   : float, optional, default = 1.15
        Kcend   : float, optional, default = 0.60
        Kcbini  : float, optional, default = 0.15
        Kcbmid  : float, optional, default = 1.10
        Kcbend  : float, optional, default = 0.50
        Lini    : int  , optional, default = 25
        Ldev    : int  , optional, default = 50
        Lmid    : int  , optional, default = 50
        Lend    : int  , optional, default = 25
        hini    : float, optional, default = 0.010
        hmax    : float, optional, default = 1.20
        thetaFC : float, optional, default = 0.250
        thetaWP : float, optional, default = 0.100
        theta0  : float, optional, default = 0.100
        Zrini   : float, optional, default = 0.20
        Zrmax   : float, optional, default = 1.40
        pbase   : float, optional, default = 0.50
        Ze      : float, optional, default = 0.10
        REW     : float, optional, default = 8.0
        CN2     : int  , optional, default = 70
        comment : str  , optional, default = ''
        """

        self.Kcini  = Kcini
        self.Kcmid  = Kcmid
        self.Kcend  = Kcend
        self.Kcbini  = Kcbini
        self.Kcbmid  = Kcbmid
        self.Kcbend  = Kcbend
        self.Lini    = Lini
        self.Ldev    = Ldev
        self.Lmid    = Lmid
        self.Lend    = Lend
        self.hini    = hini
        self.hmax    = hmax
        self.thetaFC = thetaFC
        self.thetaWP = thetaWP
        self.theta0  = theta0
        self.Zrini   = Zrini
        self.Zrmax   = Zrmax
        self.pbase   = pbase
        self.Ze      = Ze
        self.REW     = REW
        self.CN2     = CN2
        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp  = datetime.datetime.now()

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
           '{:9.4f} Kcini, Kc Initial (FAO-56 Table 12)\n'
           '{:9.4f} Kcmid, Kc Mid (FAO-56 Table 12)\n'
           '{:9.4f} Kcend, Kc End (FAO-56 Table 12)\n'
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
           '{:9d} CN2, Curve Number for AWCII '
           '(ASCE (2016) Table 14-3 or SCS (1972))\n'
          ).format(ast,timestamp,ast,self.comment,ast,self.Kcini,
                   self.Kcmid,self.Kcend,self.Kcbini,self.Kcbmid,
                   self.Kcbend,self.Lini,self.Ldev,self.Lmid,
                   self.Lend,self.hini,self.hmax,self.thetaFC,
                   self.thetaWP,self.theta0,self.Zrini,self.Zrmax,
                   self.pbase,self.Ze,self.REW,self.CN2)
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
                if line[1].lower() == 'kcini':
                    self.Kcini = float(line[0])
                elif line[1].lower() == 'kcmid':
                    self.Kcmid = float(line[0])
                elif line[1].lower() == 'kcend':
                    self.Kcend = float(line[0])
                elif line[1].lower() == 'kcbini':
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
                elif line[1].lower() == 'CN2':
                    self.CN2 = int(line[0])
