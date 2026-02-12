"""
########################################################################
The autoirrigate.py module contains the AutoIrrigate class, which
provides I/O tools for defining conditions for scheduling irrigation
automatically in pyfao56.

The autoirrigation methodology is described and tested in the following
documentation:
Thorp, K. R., DeJonge, K. C., Kukal, M. S., 2025. The pyfao56 automatic
irrigation scheduling algorithm. Agricultural Water Management 322,
110013. https://doi.org/10.1016/j.agwat.2025.110013

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
                   'mad','madDr','ksc','dsli','dsle','evnt','ifix',
                   'itdr','itfdr','ietrd','ietri','ietre','ettyp',
                   'iper','ieff','imin','imax','fw']
            Variables to determine if autoirrigation occurs or not:
            start - Autoirrigate only on start date or later
                    (str, 'yyyy-ddd')
            end   - Autoirrigate only on end date or earlier
                    (str, 'yyyy-ddd')
            alre  - Autoirrigate only after last reported irrigation
                    event (boolean)
            idow  - Autoirrigate only on specified days of the week
                    (str, '0123456')
                    (0:sun, 1:mon, 2:tue, 3:wed, 4:thu, 5:fri, 6:sat)
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
                    depletion (fDr) >= mad
            madDr - Management allowed depletion (float, mm)
                    Autoirrigate if root-zone soil water depletion (Dr)
                    >= madDr
            ksc   - Critical value for transpiration reduction factor Ks
                    (float, 0-1, 1:full transpiration, 0:no trans.)
                    Autoirrigate if Ks <= ksc
            dsli  - Days since last irrigation event
                    (float, days)
                    Autoirrigate if days since last irrigation >= dsli
            dsle  - Days since last watering event, considering both
                    eff. precip and eff. irrigation (float, days)
                    Autoirrigate if days since last watering event
                    >= dsle
            evnt  - Minimum depth of effective precipitation and
                    effective irrigation to be considered a watering
                    event (float, mm)

            The default autoirrigation amount is root-zone soil water
            depletion (Dr, mm). Variables to alter this irrigation
            amount are as follows:

            ifix  - Apply a fixed autoirrigation amount (float, mm)
            itdr  - Target a specfic root-zone soil water depletion (Dr)
                    following autoirrigation (float, mm)
            itfdr - Target a specific fractional root-zone soil water
                    depletion following autoirrigation (float, mm/mm)
            ietrd - Replace ET minus effective precipitation from the
                    past given number of days (float, days)
            ietri - Replace ET minus effective precipitation since the
                    last irrigation event (boolean)
            ietre - Replace ET minus effective precipitation since the
                    last watering event (boolean)
            ettyp - Specify type of ET to replace
                    'ETa'  - Replace ETa less precip
                    'ETcm' - Replace ETcm less precip
                    'ETc'  - Replace ETc less precip
            iper  - Adjust the autoirrigation amount by a fixed
                    percentage (float, %)
            ieff  - Consider an application efficiency for
                    autoirrigation (float, %)
            imin  - Limit autoirrigation to >= minimum amount (float,mm)
            imax  - Limit autoirrigation to <= maximum amount (float,mm)

            fw    - Fraction of soil surface wetted (FAO-56 Table 20)

    Methods
    -------
    savefile(filepath='pyfao56.ati')
        Save the autoirrigate parameters to a file
    loadfile(filepath='pyfao56.ati')
        Load the autoirrigate parameters from a file
    addset(start,end,alre=True,idow='0123456',fpdep=25.,fpday=0,
           fpact='proceed',mad=NaN,madDr=NaN,ksc=NaN,dsli=NaN,dsle=NaN,
           evnt=10.,ifix=NaN,itdr=NaN,itfdr=NaN,ietrd=NaN,ietri=NaN,
           ietre=NaN,ettyp='ETa',iper=100.,ieff=100.,imin=NaN,imax=NaN,
           fw=1.)
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
                       'ifix','itdr','itfdr','ietrd','ietri','ietre',
                       'ettyp','iper','ieff','imin','imax','fw']
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
                'evnt' :'{:6.2f}'.format,'ifix' :'{:6.2f}'.format,
                'itdr' :'{:6.2f}'.format,'itfdr':'{:6.3f}'.format,
                'ietrd':'{:6.0f}'.format,'ietri':'{!s:>5}'.format,
                'ietre':'{!s:>5}'.format,'ettyp':'{!s:>6}'.format,
                'iper' :'{:6.2f}'.format,'ieff' :'{:6.2f}'.format,
                'imin' :'{:6.2f}'.format,'imax' :'{:6.2f}'.format,
                'fw'   :'{:6.2f}'.format}
        fmthead = ['  {:>8s}','  {:>8s}','  {:>5s}','  {:>7s}',
                    ' {:>6s}', ' {:>6s}','  {:>7s}', ' {:>6s}',
                    ' {:>6s}', ' {:>6s}', ' {:>6s}', ' {:>6s}',
                    ' {:>6s}', ' {:>6s}', ' {:>6s}', ' {:>6s}',
                    ' {:>6s}','  {:>5s}','  {:>5s}','  {:>6s}',
                    ' {:>6s}', ' {:>6s}', ' {:>6s}', ' {:>6s}',
                    ' {:>6s}']
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
                data.append(float(line[14]))  #ifix
                data.append(float(line[15]))  #itdr
                data.append(float(line[16]))  #itfdr
                data.append(float(line[17]))  #ietrd
                data.append(line[18]=='True') #ietri
                data.append(line[19]=='True') #ietre
                data.append(line[20].strip()) #ettyp
                data.append(float(line[21]))  #iper
                data.append(float(line[22]))  #ieff
                data.append(float(line[23]))  #imax
                data.append(float(line[24]))  #imin
                data.append(float(line[25]))  #fw
                self.aidata.loc[i] = data

    def addset(self,start,end,alre=True,idow='0123456',fpdep=25.,
               fpday=0,fpact='proceed',mad=float('NaN'),
               madDr=float('NaN'),ksc=float('NaN'),dsli=float('NaN'),
               dsle=float('NaN'),evnt=10.,ifix=float('NaN'),
               itdr=float('NaN'),itfdr=float('NaN'),ietrd=float('NaN'),
               ietri=False,ietre=False,ettyp='ETa',iper=100.,ieff=100.,
               imin=0.,imax=float('NaN'),fw=1.):
        """Add a set of autoirrigation parameters to aidata

        Default parameter values are given below. Users should update
        the parameters with values for their desired autoirrigation
        conditions.

        Parameters
        ----------
        See AutoIrrigate class docstring for parameter definitions.
        start : str, start year and doy for parameter set ('yyyy-ddd')
        end   : str, end year and doy for parameter set ('yyy-ddd')
        alre  : boolean, optional, default=True
        idow  : str    , optional, default='0123456'
        fpdep : float  , optional, default=25.
        fpday : float  , optional, default=0
        fpact : str    , optional, default='proceed'
        mad   : float  , optional, default=NaN
        madDr : float  , optional, default=NaN
        ksc   : float  , optional, default=NaN
        dsli  : float  , optional, default=NaN
        dsle  : float  , optional, default=NaN
        evnt  : float  , optional, default=10.
        ifix  : float  , optional, default=NaN
        itdr  : float  , optional, default=NaN
        itfdr : float  , optional, default=NaN
        ietrd : float  , optional, default=NaN
        ietri : boolean, optional, default=False
        ietre : boolean, optional, default=False
        ettyp : string , optional, default='ETa'
        iper  : float  , optional, default=100.
        ieff  : float  , optional, default=100.
        imin  : float  , optional, default=0.
        imax  : float  , optional, default=NaN
        fw    : float  , optional, default=1.
        """

        i = len(self.aidata)
        data = [str(start),str(end),bool(alre),str(idow),float(fpdep),
                float(fpday),str(fpact),float(mad),float(madDr),
                float(ksc),float(dsli),float(dsle),float(evnt),
                float(ifix),float(itdr),float(itfdr),float(ietrd),
                bool(ietri),bool(ietre),str(ettyp),float(iper),
                float(ieff),float(imin),float(imax),float(fw)]
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
