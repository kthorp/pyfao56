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
########################################################################
"""

class Parameters:
    """A class for managing input parameters for FAO-56 calculations

    Attributes
    ----------
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

    Methods
    -------
    savefile(filepath='pyfao56.par')
        Save the parameter data to a file
    loadfile(filepath='pyfao56.par')
        Load the parameter data from a file
    """

    def __init__(self, Kcbini=0.15, Kcbmid=1.10, Kcbend=0.50, Lini=25,
                 Ldev=50, Lmid=50, Lend=25, hini=0.05, hmax=1.20,
                 thetaFC=0.250, thetaWP=0.100, theta0=0.100, Zrini=0.20,
                 Zrmax=1.40, pbase=0.50, Ze=0.10, REW=8.0):
        """Initialize the Parameters class attributes.

        Default parameter values are given below. Users should update
        the parameters with values for their specific crop and field
        conditions based on FAO-56 documentation.

        Parameters
        ----------
        See Parameters class docstring for parameter definitions.
        Kcbini  : float, default = 0.15
        Kcbmid  : float, default = 1.10
        Kcbend  : float, default = 0.50
        Lini    : int  , default = 25
        Ldev    : int  , default = 50
        Lmid    : int  , default = 50
        Lend    : int  , default = 25
        hini    : float, default = 0.05
        hmax    : float, default = 1.20
        thetaFC : float, default = 0.250
        thetaWP : float, default = 0.100
        theta0  : float, default = 0.100
        Zrini   : float, default = 0.20
        Zrmax   : float, default = 1.40
        pbase   : float, default = 0.50
        Ze      : float, default = 0.10
        REW     : float, default = 8.0
        """

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

    def __str__(self):
        """Represent the Parameter class variables as a string."""

        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'Parameter Data\n'
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
          ).format(ast,ast,self.Kcbini,self.Kcbmid,self.Kcbend,
                   self.Lini,self.Ldev,self.Lmid,self.Lend,self.hini,
                   self.hmax,self.thetaFC,self.thetaWP,self.theta0,
                   self.Zrini,self.Zrmax,self.pbase,self.Ze,self.REW)
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
            for line in lines[4:]: # Change this line when metadata is merged. Make it go from endline+1 to end of file
                line = line.strip().split()
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
