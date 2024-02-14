"""
########################################################################
The autoirrigate.py module contains the AutoIrrigate class, which
provides I/O tools for defining conditions for scheduling irrigation
automatically in pyfao56.

The autoirrigate.py module contains the following:
    AutoIrrigate - A class for managing multiple sets of conditions for
                   automatic irrigation

12/08/2023 Initial Python framework established for auto irrigation
02/08/2024 Further development, ideas from Kendall DeJonge & Fared Farag
02/14/2024 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

import pandas as pd
import datetime

class AutoIrrigate:
    """A class for managing multiple sets of autoirrigation conditions

    Attributes
    ----------
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class
    aidata : DataFrame
        AutoIrrigate data with mixed data types
        index - counter as int
        columns - ['start','end','alre','idow','fpdep','fpday','fpact',
                   'mad','madDr','ksc','dsli','dsle','evnt','icon',
                   'iper','itdr','itfdr','ietrd','ietri','ietre','ieff',
                   'imin','imax']
            Variables to determine if autoirrigation occurs or not:
            start - Autoirrigate only on start date or later
                    (str, 'yyyy-ddd')
            end   - Autoirrigate only on end date or earlier
                    (str, 'yyyy-ddd')
            alre  - Autoirrigate only after last reported irrigation
                    event (boolean)
            idow  - Autoirrigate only on specified days of the week
                    (str, '1234567')
                    (1:sun, 2:mon, 3:tue, 4:wed, 5:thu, 6:fri, 7:sat)
            fpdep - Threshold for forcasted precipitation depth
                    (float, mm)
            fpday : Number of days to consider forecasted precipitation
                    (float, days)
            fpact : Action if forecasted precip is above threshold
                    'proceed' - Proceed to autoirrigate anyway if needed
                    'cancel'  - Do not autoirrigate
                    'reduce'  - Deduct forecasted precip from
                                autoirrigation amount
            mad   - Management allowed depletion (float, mm/mm)
                    Autoirrigate if fractional root-zone soil water
                    depletion (fDr) > mad
            madDr - Management allowed depletion (float, mm)
                    Autoirrigate if root-zone soil water depletion (Dr)
                    > madDr
            ksc   - Critical value for transpiration reduction factor Ks
                    (float, 0-1, 1:full transpiration, 0:no trans.)
                    Autoirrigate if Ks < ksc
            dsli  - Critical days since last irrigation event
                    (float, days)
                    Autoirrigate if days since last irrigation > dsli
            dsle  - Days since last watering event, including
                    precipitation (float, days)
                    Autoirrigate if days since last watering event >dsle
            evnt  - Minimum depth to be considered a watering event
                    (float, mm)

            The default autoirrigation amount is root-zone soil water
            depletion (Dr, mm). Variables to alter this irrigation
            amount are as follows:

            icon  - Apply a constant autoirrigation amount (float, mm)
            iper  - Apply a percentage of root-zone soil water depletion
                    (Dr) (float, %)
            itdr  - Target a specfic root-zone soil water depletion (Dr)
                    following autoirrigation (float, mm)
            itfdr - Target a specific fractional root-zone soil water
                    depletion following autoirrigation (float, mm/mm)
            ietrd - Replace ETcadj minus precipitation from the past
                    given number of days (float, days)
            ietri - Replace ETcadj minus precipitation since the last
                    irrigation event (boolean)
            ierte - Replace ETcadj minus precipitation since the last
                    watering event (boolean)
            ieff  - Consider an application efficiency for
                    autoirrigation (float, %)
            imin  - Limit autoirrigation to > minimum amount (float, mm)
            imax  - Limit autoirrigation to < maximum amount (float, mm)

    Methods
    -------
    savefile(filepath='pyfao56.ati')
        Save the autoirrigate parameters to a file
    loadfile(filepath='pyfao56.ati')
        Load the autoirrigate parameters from a file
    addset(start='yyyy-ddd',end='yyyy-ddd',alre=True,idow='1234567',
           fpdep=25.,fpday=3,fpact='proceed',mad=0.5,madDr=NaN,ksc=NaN,
           dsli=NaN,dsle=NaN,evnt=6.,icon=NaN,iper=100.,itdr=NaN,
           itfdr=NaN,ietrd=NaN,ietri=NaN,ietre=NaN,ieff=100.,imin=NaN,
           imax=NaN)
        Add a set of autoirrigation parameters to self.aidata
    removeset(index)
        Remove a set of autoirrigation parameters from self.aidata
    customload()
        Override this function to customize loading of autoirrigation
        conditions
    """

    def __init__(self,filepath=None,comment=''):
        """Initialize the AutoIrrigate class attributes.

        If filepath is provided, data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """

        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp = datetime.datetime.now()
        self.cnames = ['start','end','alre','idow','fpdep','fpday',
                       'fpact','mad','madDr','ksc','dsli','dsle','evnt',
                       'icon','iper','itdr','itfdr','ietrd','ietri',
                       'ietre','ieff','imin','imax']
        self.aidata = pd.DataFrame(columns=self.cnames)

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the AutoIrrigate class variables as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        fmts = {'start':'{:>8s}'.format ,'end'  :'{:>8s}'.format ,
                'alre' :'{!s:>5}'.format,'idow' :'{:>7s}'.format ,
                'fpdep':'{:6.2f}'.format,'fpday':'{:6.0f}'.format,
                'fpact':'{:>7s}'.format ,'mad'  :'{:6.3f}'.format,
                'madDr':'{:6.2f}'.format,'ksc'  :'{:6.3f}'.format,
                'dsli' :'{:6.0f}'.format,'dsle' :'{:6.0f}'.format,
                'evnt' :'{:6.2f}'.format,'icon' :'{:6.2f}'.format,
                'iper' :'{:6.2f}'.format,'itdr' :'{:6.2f}'.format,
                'itfdr':'{:6.3f}'.format,'ietrd':'{:6.0f}'.format,
                'ietri':'{!s:>5}'.format,'ietre':'{!s:>5}'.format,
                'ieff' :'{:6.2f}'.format,'imin' :'{:6.2f}'.format,
                'imax' :'{:6.2f}'.format}
        fmthead = ['  {:>8s}','  {:>8s}','  {:>5s}','  {:>7s}',
                    ' {:>6s}', ' {:>6s}','  {:>7s}', ' {:>6s}',
                    ' {:>6s}', ' {:>6s}', ' {:>6s}', ' {:>6s}',
                    ' {:>6s}', ' {:>6s}', ' {:>6s}', ' {:>6s}',
                    ' {:>6s}', ' {:>6s}','  {:>5s}','  {:>5s}',
                    ' {:>6s}', ' {:>6s}', ' {:>6s}']
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'AutoIrrigate Data\n'
           'Timestamp: {:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:s}\n'
          ).format(ast,timestamp,ast,self.comment,ast)
        s += ' '*len(str(self.aidata.shape[0]))
        for i, cname in enumerate(self.cnames):
            s += fmthead[i].format(cname)
        s += '\n'
        if not self.aidata.empty:
            s += self.aidata.to_string(header=False,na_rep='   NaN',
                                       formatters=fmts)
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
            self.aidata = pd.DataFrame(columns=self.cnames)
            for i, line in enumerate(lines[endast+2:]):
                line = line.strip().split()
                data = list()
                data.append(line[1])          #start
                data.append(line[2])          #end
                data.append(line[3]=='True')  #alre
                data.append(line[4])          #idow
                data.append(float(line[5]))   #fpdep
                data.append(float(line[6]))   #fpday
                data.append(line[7])          #fpact
                data.append(float(line[8]))   #mad
                data.append(float(line[9]))   #madDr
                data.append(float(line[10]))  #ksc
                data.append(float(line[11]))  #dsli
                data.append(float(line[12]))  #dsle
                data.append(float(line[13]))  #evnt
                data.append(float(line[14]))  #icon
                data.append(float(line[15]))  #iper
                data.append(float(line[16]))  #itdr
                data.append(float(line[17]))  #itfdr
                data.append(float(line[18]))  #ietrd
                data.append(line[19]=='True') #ietri
                data.append(line[20]=='True') #ietre
                data.append(float(line[21]))  #ieff
                data.append(float(line[22]))  #imax
                data.append(float(line[23]))  #imin
                self.aidata.loc[i] = data

    def addset(self,start='yyyy-ddd',end='yyyy-ddd',alre=True,
               idow='1234567',fpdep=25.,fpday=3,fpact='proceed',mad=0.5,
               madDr=float('NaN'),ksc=float('NaN'),dsli=float('NaN'),
               dsle=float('NaN'),evnt=10.,icon=float('NaN'),iper=100.,
               itdr=float('NaN'),itfdr=float('NaN'),ietrd=float('NaN'),
               ietri=False,ietre=False,ieff=100.,imin=0.,
               imax=float('NaN')):
        """Add a set of autoirrigation parameters to aidata

        Default parameter values are given below. Users should update
        the parameters with values for their desired autoirrigation
        conditions.

        Parameters
        ----------
        See AutoIrrigate class docstring for parameter definitions.
        start : str    , optional, default='yyyy-ddd'
        end   : str    , optional, default='yyyy-ddd'
        alre  : boolean, optional, default=True
        idow  : str    , optional, default='1234567'
        fpdep : float  , optional, default=25.
        fpday : float  , optional, default=3
        fpact : str    , optional, default='proceed'
        mad   : float  , optional, default=0.5
        madDr : float  , optional, default=NaN
        ksc   : float  , optional, default=NaN
        dsli  : float  , optional, default=NaN
        dsle  : float  , optional, default=NaN
        evnt  : float  , optional, default=10.
        icon  : float  , optional, default=NaN
        iper  : float  , optional, default=100.
        itdr  : float  , optional, default=NaN
        itfdr : float  , optional, default=NaN
        ietrd : float  , optional, default=NaN
        ietri : boolean, optional, default=False
        ietre : boolean, optional, default=False
        ieff  : float  , optional, default=100.
        imin  : float  , optional, default=0.
        imax  : float  , optional, default=NaN
        """

        i = len(self.aidata)
        data = [str(start),str(end),bool(alre),str(idow),float(fpdep),
                float(fpday),str(fpact),float(mad),float(madDr),
                float(ksc),float(dsli),float(dsle),float(evnt),
                float(icon),float(iper),float(itdr),float(itfdr),
                float(ietrd),bool(ietri),bool(ietre),float(ieff),
                float(imin),float(imax)]
        self.aidata.loc[i] = data

    def removeset(self,index):
        """Remove a set of autoirrigation parameters from aidata

        Parameters
        ----------
        index : int
            Index of the set of autoirrigation data to be removed
        """

        self.aidata.drop(index)

    def customload(self):
        """Override function to customize loading autoirrigate data."""

        pass
