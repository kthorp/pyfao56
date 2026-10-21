"""
########################################################################
The aridity.py module contains the Aridity class, which provides tools
for analyzing and adjusting weather datasets for aridity, thereby
evaluating and improving their suitability for computation of
standardized reference evapotranspiration. The methodology follows
recommendations in Section 2.5 of FAO-56 (2025), pp. 36-51.

The aridity.py module contains the following:
    Aridity - A class for analyzing aridity in weather data

10/16/2026 Initial code developed by Kelly Thorp
########################################################################
"""

import pandas as pd
from pyfao56 import Weather
from pyfao56.custom import AzmetMaricopa
import matplotlib.pyplot as plt
import copy
import math

class Aridity(Weather):
    """A class for analyzing aridity in daily weather measurements.

    The class inherits from the pyfao56 Weather class.

    Attributes
    ----------
    daily : DataFrame
        Weather data from wdata DataFrame in Weather class as float
        index - datetime ('yyyy-mm-dd')
        columns - ['Srad','Sunhr','Rnet','Tmax','Tmin','Vapr','Tdew',
                   'RHmax','RHmin','RHavg','Wndsp','Rain','ETref']
            See Weather class for details.
    monthlymean : DataFrame
        Daily weather data resampled to monthly means
        index - datetime ('yyyy-mm-01')
        columns - ['Srad','Sunhr','Rnet','Tmax','Tmin','Vapr','Tdew',
                   'RHmax','RHmin','RHavg','Wndsp','Rain','ETref']
            See Weather class for details.
    monthlysum : DataFrame
        Daily weather data resampled to monthly sums
        index - datetime ('yyyy-mm-01')
        columns - ['Srad','Sunhr','Rnet','Tmax','Tmin','Vapr','Tdew',
                   'RHmax','RHmin','RHavg','Wndsp','Rain','ETref']
            See Weather class for details.
    yearlysum : DataFrame
        Daily weather data resampled to yearly sums
        index - datetime('yyyy-01-01')
        columns - ['Srad','Sunhr','Rnet','Tmax','Tmin','Vapr','Tdew',
                   'RHmax','RHmin','RHavg','Wndsp','Rain','ETref']
            See Weather class for details.
    AIcalc : dict
        Contains variables from UNEP Aridity Index computations
        Input, output, and intermediate variables are included:
            Tavg12 - Long-term monthly average temperature (deg C)
            I      - Annual heat index
            alpha  - Coefficient
            CEI    - Mean annual climatic evaporation index (mm)
            Pmean  - Mean annual precipitation (mm)
            AI     - Aridity Index
    AI : float
        UNEP Aridity Index, FAO-56 (2025), Box 2.4
    aT : float
        Subtractive correction factor for non-reference weather data
    climate : str
        Climate classification description
    needadj : Series
        Identifies weather records needing adjustment for aridity
        index - Year and day of year as string ('yyyy-ddd')
        value - boolean (True for adjustment needed)
    deltaT : Series
        Monthly deltaT computed from FAO-56 (2025) Eq. 2.12
        index - Year and day of year as string ('yyyy-ddd')
        value - deltaT as float
    analyzed : boolean
        Has the wdata DataFrame been analyzed for aridity
    adjusted : boolean
        Has the wdata DataFrame been adjusted for aridity

    Methods
    -------
    plot()
        Produce aridity plot as in Figures 2.4 and 2.5 in FAO-56 (2025)
    analyze()
        Compute the UNEP Aridity Index, FAO-56 (2025), Box 2.4
        Obtain aT correction factor for non-reference humidity, p. 40
        Determine needadj and deltaT, FAO-56 (2025) Eq. 2.12
    adjust(aT=None,bT=0.3,method='simple',plot=False,
           deltaT_trusted=None)
        Adjust the wdata DataFrame to account for aridity
    """

    def __init__(self, wth):
        """Initialize the Aridity class attributes

        Parameters
        ----------
        wth : pyfao56 Weather class
            Provides the weather data for aridity evaluation
        """

        self.__dict__.update(copy.deepcopy(wth.__dict__))
        self.daily = self.wdata.drop(columns=['MorP'])
        self.daily.index=pd.to_datetime(self.daily.index,format="%Y-%j")
        self.daily['Tavg'] = (self.daily['Tmax']+self.daily['Tmin'])/2.
        self.monthlymean = self.daily.resample('MS').mean()
        self.monthlysum = self.daily.resample('MS').sum()
        self.yearlysum = self.daily.resample('YS').sum()
        self.AIcalc = dict()
        self.AI = float('NaN')
        self.aT = float('NaN')
        self.climate = ''
        self.needadj = None
        self.deltaT = None
        self.analyzed = False
        self.adjusted = False

    def plot(self,title='', show=True, filepath=None):
        """Produce an FAO-56 (2025) aridity plot

        Parameters
        ----------
        title : str, optional
            Specify the title as the provided string
            (default = '')
        show : boolean, optional
            If True, the plot is displayed on the screen
            (default = True)
        filepath : str, optional
            Provide a filepath string to save the figure
            (default = None)
        """

        fig, ax = plt.subplots()
        precipETo = self.monthlysum['Rain']/self.monthlysum['ETref']
        TminTdew = self.monthlymean['Tmin']-self.monthlymean['Tdew']
        ax.scatter(precipETo,TminTdew,marker='x',color='k')
        ax.set_title(title, fontsize=12)
        ax.set_xlabel(r'Precipitation/ET$_{\mathrm{ref}}$')
        ax.set_ylabel(r'T$_{\mathrm{min}}$ - T$_{\mathrm{dew}}$')

        #Save and show the plot if requested
        if filepath is not None:
            plt.savefig(filepath)
        if show:
            plt.show()

    def analyze(self):
        """Analyze the weather data for aridity issues"""

        if self.analyzed:
            raise Exception ("Data have already been analyzed.")

        #Compute the UNEP Aridity Index, FAO-56 (2025) Box 2.4
        self.AIcalc.clear()

        #Tavg12 (list) : Mean monthly average air temperature (deg C)
        #FAO-56 (2025) Box 2.4
        group = self.monthlymean.index.month
        Tavg12 = self.monthlymean['Tavg'].groupby(group).mean()
        #FAO-56 (2025) Example 2.1
        #Tavg12[1] = 5.2
        #Tavg12[2] = 7.1
        #Tavg12[3] = 11.6
        #Tavg12[4] = 14.3
        #Tavg12[5] = 18.3
        #Tavg12[6] = 22.1
        #Tavg12[7] = 24.95
        #Tavg12[8] = 24.6
        #Tavg12[9] = 21.5
        #Tavg12[10] = 15.5
        #Tavg12[11] = 9.45
        #Tavg12[12] = 5.7
        self.AIcalc.update({'Tavg12':Tavg12})

        #I (float) : Annual heat index
        #FAO-56 (2025) Box 2.4
        I = ((Tavg12/5.0)**1.514).sum()
        self.AIcalc.update({'I':I})

        #alpha (float) : coefficient
        #FAO-56 (2025) Box 2.4
        alpha = 6.75e-7*I**3 - 7.71e-5*I**2 + 1.7912e-2*I+0.492
        self.AIcalc.update({'alpha':alpha})

        #CEI (float) : Mean annual climatic evaporation index (mm)
        #Thornthwaite (1948) and FAO-56 (2025) Box 2.4
        CEI = (16.*(10.*Tavg12/I)**alpha).sum()
        self.AIcalc.update({'CEI':CEI})

        #Pmean (float) : Mean annual precipitation (mm)
        #FAO-56 (2025) Box 2.4
        Pmean = self.yearlysum['Rain'].mean()
        #FAO-56 (2025) Example 2.1
        #Pmean = 22+18+31+46+47+43+24+34+34+30+22+29
        self.AIcalc.update({'Pmean':Pmean})

        #AI (float) : UNEP Aridity Index (unitless)
        #FAO-56 (2025) Box 2.4
        AI = Pmean / CEI
        self.AIcalc.update({'AI':AI})
        self.AI = AI

        #Get aT from FAO-56 (2025) page 40
        if AI < 0.05:
            self.aT = 5.0
            self.climate = 'Hyper-arid'
        elif AI < 0.20:
            self.aT = 2.5
            self.climate = 'Arid'
        elif AI < 0.50:
            self.aT = 1.5
            self.climate = 'Semiarid'
        elif AI < 0.65:
            self.aT = 0.5
            self.climate = 'Dry sub-humid'
        else:
            self.aT = 0.0
            self.climate = 'Moist sub-humid or Humid'

        #Analyze the data for aridity
        #FAO-56 (2025) Eq. 2.12 and Section 2.5.4
        deltaT = self.monthlymean['Tmin'] - self.monthlymean['Tdew']
        needadj = deltaT > self.aT
        #Provide adjustment months and deltaT with same index as wdata
        self.needadj = needadj.reindex(self.daily.index).ffill()
        self.deltaT = deltaT.reindex(self.daily.index).ffill()
        self.needadj.index = self.needadj.index.strftime('%Y-%j')
        self.deltaT.index = self.deltaT.index.strftime('%Y-%j')

        self.analyzed = True

    def adjust(self, aT=None, bT=0.3, method='simple', plot=False,
               deltaT_trusted=None):
        """Adjust weather data in wdata DataFrame to account for aridity

        Parameters
        ----------
        aT : float, optional
            Subtractive correction factor for non-reference weather data
            (default=None)
        bT : float, optional
            Fraction of of the aridity bias applied to air temperature
            (default=0.3)
        method : str, optional
            The weather data adjustment method (default='simple')
                'simple' - Uses FAO-56 (2025) Eqs. 2.6-2.7
                'trusted' - Uses FAO-56 (2025) Eqs. 2.7-2.11
                'notrusted' - Uses FAO-56 (2025) Eq. 2.7,2.12-2.15
        plot : boolean, optional
            Plot ETref before and after adjustment
        deltaT_trusted : Series
            deltaT (Tmin-Tdew) for trusted weather site with the same
            index and format as self.deltaT
        """

        if self.adjusted:
            raise Exception("Data have already been adjusted.")

        if not aT: aT=self.aT

        priorETref = self.wdata['ETref'].to_list()

        if method=='simple':
            #Adjust Tdew and other humidity variables
            #FAO-56 (2025) Eqs. 2.6-2.7 and Section 2.5.2
            for index, row in self.wdata.iterrows():
                tdew = self.wdata.loc[index,'Tmin'] - aT
                ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
                self.wdata.loc[index,'Vapr'] = ea
                self.wdata.loc[index,'Tdew'] = tdew
                self.wdata.loc[index,'RHmax'] = float('NaN')
                self.wdata.loc[index,'RHmin'] = float('NaN')
                self.wdata.loc[index,'RHavg'] = float('NaN')
        elif method=='trusted':
            #Adjust Tmax, Tmin, and Tdew and other humidity variables
            #FAO-56 (2025) Eqs. 2.7-2.11 and Section 2.5.4
            for index, row in self.wdata.iterrows():
                dTnref = self.deltaT.loc[index]
                dTref = deltaT_trusted.loc[index]
                dTpaired = dTnref - dTref
                if dTpaired > 2.5: #FAO-56 (2025) p. 43
                    self.wdata.loc[index,'Tmax']-=(bT*dTpaired)
                    self.wdata.loc[index,'Tmin']-=(bT*dTpaired)
                    self.wdata.loc[index,'Tdew']+=((1.-bT)*dTpaired)
                    tdew = self.wdata.loc[index,'Tdew']
                    ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
                    self.wdata.loc[index,'Vapr'] = ea
                    self.wdata.loc[index,'RHmax'] = float('NaN')
                    self.wdata.loc[index,'RHmin'] = float('NaN')
                    self.wdata.loc[index,'RHavg'] = float('NaN')
        elif method=='notrusted':
            #Adjust Tmax, Tmin, and Tdew and other humidity variables
            #FAO-56 (2025) Eqs. 2.7, 2.12-2.15 and Section 2.5.4
            for index, row in self.wdata.iterrows():
                if self.needadj.loc[index]:
                    adj1=bT*(self.deltaT.loc[index]-aT)
                    adj2=(1.-bT)*(self.deltaT.loc[index]-aT)
                    self.wdata.loc[index,'Tmax']-=adj1
                    self.wdata.loc[index,'Tmin']-=adj1
                    self.wdata.loc[index,'Tdew']+=adj2
                    tdew = self.wdata.loc[index,'Tdew']
                    ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
                    self.wdata.loc[index,'Vapr'] = ea
                    self.wdata.loc[index,'RHmax'] = float('NaN')
                    self.wdata.loc[index,'RHmin'] = float('NaN')
                    self.wdata.loc[index,'RHavg'] = float('NaN')
        else:
            raise ValueError("Aridity adjustment method not recognized")

        #Recompute ASCE Standardized Reference ET with new data
        for index, row in self.wdata.iterrows():
            etref = self.compute_etref(index)
            self.wdata.loc[index,'ETref'] = etref

        postETref = self.wdata['ETref'].to_list()

        #Plot ETref if requested
        if plot:
            fig, ax = plt.subplots()
            ax.scatter(priorETref,postETref,marker='x',color='k')
            title = 'Reference ET adjustment: ' + method + ' method'
            ax.set_title(title, fontsize=12)
            ax.set_xlabel(r'ET$_{\mathrm{ref}}$ pre adjustment')
            ax.set_ylabel(r'ET$_{\mathrm{ref}}$ post adjustment')
            upper = math.trunc(max(priorETref)) + 1
            ax.plot([0,upper],[0,upper]) #1:1 line
            ax.set_xlim(0,upper)
            ax.set_ylim(0,upper)
            plt.show()

        self.adjusted = True

if __name__ == '__main__':
    weather = AzmetMaricopa()
    weather.customload(start='1988-001',end='2025-365')
    weather.wdata.drop('1988-210', inplace=True)
    weather.wdata.drop('1997-243', inplace=True)

    #Humidity adjustments only via the simple method
    aridity = Aridity(weather)
    aridity.plot(title='Maricopa AZMET Station, 1988-2025')
    aridity.analyze()
    print('UNEP Aridity Index: {:5.3f}'.format(aridity.AI))
    print('Correction factor (aT): {:3.1f}'.format(aridity.aT))
    print('The climate classification is {:s}.'.format(aridity.climate))
    aridity.adjust(method='simple',plot=True)

    #Adjustments of Tmax, Tmin, and Tdew with no trusted site
    aridity2 = Aridity(weather)
    aridity2.analyze()
    aridity2.adjust(method='notrusted',plot=True)

    #Adjustments of Tmax, Tmin, and Tdew with a trusted site
    #Obtain deltaT for the trusted weather site and pass to adjust
    #trustsite = Aridity(wth)
    #trustsite.analyze()
    #aridity3 = Aridity(weather)
    #aridity3.analyze()
    #aridity3.adjust(method='trusted',deltaT_trusted=trustsite.deltaT)
