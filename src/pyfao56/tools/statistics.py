"""
########################################################################
The statistics.py module contains functions for computing fit statistics
between measured and simulated data, including
 1. Bias ('bias')
 2. Relative bias ('rbias')
 3. Percent bias ('pbias')
 4. Maximum error ('maxerr')
 5. Mean error ('meanerr')
 6. Mean absolute error ('mae')
 7. Sum of squared error ('sse')
 8. Pearson's correlation coefficient ('r')
 9. Coefficient of determination ('r2')
10. Root mean squared error ('rmse')
11. Relative root mean squared error ('rrmse')
12. Percent root mean squared error ('prmse')
13. Coefficient of residual mass ('crm')
14. Nash & Sutcliffe (1970) model efficiency ('nse')
15. Willmott (1981) index of agreement ('d')

11/01/2023 Initial Python script
########################################################################
"""

import numpy as np
import datetime

class Statistics:
    """A class for computing goodness-of-fit statistics

    Attributes
    ----------
    simulated : numpy array
        A 1d array of simulated data
    measured : numpy array
        A 1d array of measured data
    stats - dict
        Container for goodness-of-fit statistics
        keys - ['bias','rbias','pbias','maxerr','meanerr','mae','sse',
                'r','r2','rmse','rrmse','prmse','crm','nse','d']
        value - Computed value of the statistic

    Methods
    -------
    savefile(filepath='pyfao56.fit')
        Save goodness-of-fit statistics to a file
    """

    def __init__(self, simulated, measured, comment=''):
        """Initialize the Statistics class attributes.

        Parameters
        ----------
        simulated : list
            A list of simulated data
        measured : list
            A list of measured data
        """

        self.comment = 'Comments: ' + comment.strip()
        self.simulated = np.array(simulated).flatten()
        self.measured = np.array(measured).flatten()
        s = self.simulated
        m = self.measured
        self.stats = {}
        self.stats.update({'bias'   :self._bias(s,m)})
        self.stats.update({'rbias'  :self._rbias(s,m)})
        self.stats.update({'pbias'  :self._pbias(s,m)})
        self.stats.update({'maxerr' :self._maxerr(s,m)})
        self.stats.update({'meanerr':self._meanerr(s,m)})
        self.stats.update({'mae'    :self._mae(s,m)})
        self.stats.update({'sse'    :self._sse(s,m)})
        self.stats.update({'r'      :self._r(s,m)})
        self.stats.update({'r2'     :self._r2(s,m)})
        self.stats.update({'rmse'   :self._rmse(s,m)})
        self.stats.update({'rrmse'  :self._rrmse(s,m)})
        self.stats.update({'prmse'  :self._prmse(s,m)})
        self.stats.update({'crm'    :self._crm(s,m)})
        self.stats.update({'nse'    :self._nse(s,m)})
        self.stats.update({'d'      :self._d(s,m)})

    def __str__(self):
        """Represent the Statistics class variables as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        ast='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Goodness-of-fit Statistics\n'
             'Timestamp: {:s}\n'
             '{:s}\n'
             '{:s}\n'
             '{:s}\n'
             ).format(ast,
                      timestamp,
                      ast,
                      self.comment,
                      ast)
        keys = ['bias','rbias','pbias','maxerr','meanerr','mae','sse',
                'r','r2','rmse','rrmse','prmse','crm','nse','d']
        for key in keys:
            s += '{:s} : {:f}\n'.format(key, self.stats[key])
        return s

    def savefile(self,filepath='pyfao56.fit'):
        """Save goodness-of-fit statistics to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.fit')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for output data is not found.')
        else:
            f.write(self.__str__())
            f.close()

    def _bias(self,s,m):
        """Compute the bias."""
        return np.sum(s-m)

    def _rbias(self,s,m):
        """Compute the relative bias."""
        return np.sum(s-m)/np.mean(m)

    def _pbias(self,s,m):
        """Compute the percent bias."""
        return np.sum(s-m)/np.mean(m)*100.

    def _maxerr(self,s,m):
        """Compute maximum error."""
        return np.max(np.absolute(s-m))

    def _meanerr(self,s,m):
        """Compute the mean error."""
        return np.mean(s-m)

    def _mae(self,s,m):
        """Compute the mean absolute error."""
        return np.mean(np.absolute(s-m))

    def _sse(self,s,m):
        """Compute the sum of squared error."""
        return np.sum(np.square(s-m))

    def _r(self,s,m):
        """Compute the Pearson correlation coefficient (r)."""
        a = np.sum((s-np.mean(s))*(m-np.mean(m)))
        b = np.sum(np.square(s-np.mean(s)))
        c = np.sum(np.square(m-np.mean(m)))
        return a/np.sqrt(b*c)
        #return np.corrcoef(s,m)[0][1]

    def _r2(self,s,m):
        """Compute the coefficient of determination (r^2)."""
        a = np.sum((s-np.mean(s))*(m-np.mean(m)))
        b = np.sum(np.square(s-np.mean(s)))
        c = np.sum(np.square(m-np.mean(m)))
        return (a/np.sqrt(b*c))**2.0

    def _rmse(self,s,m):
        """Compute the root mean squared error."""
        return np.sqrt(np.mean(np.square(s-m)))

    def _rrmse(self,s,m):
        """Compute the relative root mean squared error."""
        return np.sqrt(np.mean(np.square(s-m)))/np.mean(m)

    def _prmse(self,s,m):
        """Compute the percent root mean squared error."""
        return np.sqrt(np.mean(np.square(s-m)))/np.mean(m)*100.

    def _crm(self,s,m):
        """Compute the coefficient of residual mass."""
        return (np.sum(s)-np.sum(m))/np.sum(m)

    def _nse(self,s,m):
        """Compute the Nash & Sutcliffe (1970) model efficiency."""
        a = np.sum(np.square(s-m))
        b = np.sum(np.square(m-np.mean(m)))
        return 1.0-a/b

    def _d(self,s,m):
        """Compute the Willmott (1981) index of agreement (d)."""
        a = np.sum(np.square(s-m))
        b = np.absolute(s-np.mean(m))
        c = np.absolute(m-np.mean(m))
        d = np.sum(np.square(b+c))
        return 1.0-a/d
