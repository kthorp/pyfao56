"""
########################################################################
The soil_water.py module contains the SoilWaterSeries class, which
provides I/O tools for processing measured volumetric soil water content
(SWC, cm3/cm3) data in the pyfao56 environment. The SoilWaterSeries
class manages SWC data collected at one location over time (e.g., at one
access tube over a growing season). A subclass called SoilWaterProfile
handles data storage and computations for one soil water profile
measurement event (i.e., measurements of the soil water profile on a
single date). The SoilWaterProfile class computes root zone soil water
metrics, especially the root zone soil water depletion (SWD, mm), given
estimates of root depth.

The soil_water.py module contains the following:
    SoilWaterSeries - A class for managing measured SWC profile series
    SoilWaterProfile - A class for managing a single SWC profile

10/17/2022 SWC Python functions developed by Josh Brekel, USDA-ARS
03/07/2023 SoilWater functions developed by Josh Brekel, USDA-ARS
08/23/2023 Major overhaul for pyfao56 1.2 release
########################################################################
"""

import pandas as pd
import datetime

class SoilWaterSeries:
    """A class for managing a series of measured soil water content data

    Attributes
    ----------
    par : pyfao56 Parameters object, optional
        Provides the parameter data (e.g., thetaFC, Zrmax)
        (default = None)
    sol : pyfao56 SoilProfile object, optional
        Provides layered soil profile data (e.g., thetaFC)
        (default = None)
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class
    swdata : dict
        Container for SoilWaterProfile objects
        key - measurement date as string ('yyyy-ddd')
        value - SoilWaterProfile object

    Methods
    -------
    savefile(filepath='pyfao56.sws')
        Save soil water series data to a file
    loadfile(filepath='pyfao56.sws')
        Load soil water series data from a file
    addprofile(mdate,swp)
        Add a SoilWaterProfile object to self.swdata
    customload()
        Override this function to customize loading measured volumetric
        soil water content data.
    summarize()
        Summarize the series of root zone soil water metrics
    """

    def __init__(self,filepath=None,par=None,sol=None,comment=''):
        """Initialize the SoilWaterSeries class attributes.

        If filepath is provided, soil water data is loaded from the file

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None)
        par : pyfao56 Parameters object, optional
            Provides the parameter data (e.g., thetaFC, Zrmax)
            (default = None)
        sol : pyfao56 SoilProfile object, optional
            Provides layered soil profile data (e.g., thetaFC)
            (default = None)
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """

        self.par = par
        self.sol = sol
        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp = datetime.datetime.now()
        self.swdata = {}

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilWaterSeries class data as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        ast='*'*72
        s=('{:s}\n'
           'pyfao56: FAO-56 Evapotranspiration in Python\n'
           'Measured Soil Water Data\n'
           'Timestamp: {:s}\n'
           '{:s}\n'
           '{:s}\n'
           '{:s}\n'
          ).format(ast,timestamp,ast,self.comment,ast)
        if len(self.swdata) > 0:
            s += 'Year-DOY  n'
            key0 = list(self.swdata.keys())[0]
            n = len(self.swdata[key0].mvswc)
            for i in range(n):
                s += ' D{:02d}'.format(i+1)
            for i in range(n):
                s += ' SWC{:02d}'.format(i+1)
            s += '    Zr      mDr   mDrmax   mfDr mfDrmax mSWCr mSWCrmax'
            s += '    mKs\n'
            for key in sorted(self.swdata.keys()):
                s += self.swdata[key].__str__() + '\n'
        return s

    def savefile(self,filepath='pyfao56.sws'):
        """Save pyfao56 soil water series data to a file.

        The function saves a file with standard pyfao56-styled header.
        Each data line contains the following info:
        1. SWC measurement date as string ('yyyy-ddd')
        2. The number, x, of SWC measurement depths as integer
        3. x bottom depths of SWC measurement layers as integer (cm)
        4. x SWC measurements as integer (cm3/cm3, same order as depths)
        5. Estimate of Zr on the measurement date
        6. mDr (mm)
        7. mDrmax (mm)
        8. mfDr (mm/mm)
        9. mfDrmax (mm/mm)
        10. mSWCr (cm3/cm3)
        11. mSWCrmax (cm3/cm3)
        12. mKs (0.0-1.0)

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.sws')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for soil water data is not found.')
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.sws'):
        """Load measured soil water content data from a file

        The function expects a file with standard pyfao56-styled header.
        Each data line contains the following info:
        1. SWC measurement date as string ('yyyy-ddd')
        2. The number, x, of SWC measurement depths as integer
        3. x bottom depths of SWC measurement layers as integer (cm)
        4. x SWC measurements as integer (cm3/cm3, same order as depths)
        5. Optionally, an estimate of Zr on the measurement date
        6. Optionally, other values, which are not loaded.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.sws')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for soil water data is not found.')
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
            self.swdata.clear()
            for line in lines[endast+2:]:
                line = line.strip().split()
                mdate = line[0]
                numdpths = int(line[1])
                mvswc = dict()
                for i in list(range(numdpths)):
                    dpth = int(line[2+i])
                    swc = float(line[2+i+numdpths])
                    mvswc.update({dpth:swc})
                try:
                    Zr = float(line[2+numdpths*2+1])
                except:
                    Zr = float('NaN')
                swp = self.SoilWaterProfile(mdate,
                                            mvswc,
                                            par = self.par,
                                            sol = self.sol,
                                            Zr = Zr)
                self.addprofile(mdate,swp)

    def addprofile(self,mdate,swp):
        """Add a SoilWaterProfile object to self.swdata

        Parameters
        ----------
        mdate : str
            Measurement date as string ('yyyy-ddd')
        swp : SoilWaterProfile object
            Measured soil water profile data on mdate
        """

        self.swdata.update({mdate:swp})

    def customload(self):
        """Override this function to customize loading measured
        vol. soil water content data into SoilWaterProfile objects.
        """

        pass

    def summarize(self):
        """Summarize the series of root zone soil water metrics

        Returns
        -------
        summary : DataFrame
            Summary of series of root zone soil water metrics
        """

        cols = ['Year-DOY','mDr','mDrmax','mfDr','mfDrmax',
                'mSWCr','mSWCrmax','mKs']
        summary = pd.DataFrame(columns = cols)
        summary = summary.set_index('Year-DOY')
        for key in sorted(self.swdata.keys()):
            summary.loc[key,'mDr'] = self.swdata[key].mDr
            summary.loc[key,'mDrmax'] = self.swdata[key].mDrmax
            summary.loc[key,'mfDr'] = self.swdata[key].mfDr
            summary.loc[key,'mfDrmax'] = self.swdata[key].mfDrmax
            summary.loc[key,'mSWCr'] = self.swdata[key].mSWCr
            summary.loc[key,'mSWCrmax'] = self.swdata[key].mSWCrmax
            summary.loc[key,'mKs'] = self.swdata[key].mKs
        return summary

    class SoilWaterProfile:
        """Manage a single soil water content measurement profile

        Attributes
        ----------

        mdate : str
            Year and day of year of the measurement ('yyyy-ddd')
        mvswc : dict
            Measured volumetric soil water content (SWC, cm3/cm3)
            key - Bottom depth of measurement layer as integer (cm)
            value - Measured volumetric SWC as float (cm3/cm3)
        par : pyfao56 Parameters class, optional
            Provides the parameter data (e.g., thetaFC, Zrmax)
            (default = None)
        sol : pyfao56 SoilProfile class, optional
            Provides layered soil profile data (e.g., thetaFC)
            (default = None)
        Zr : float, optional
            Root depth on SWC measurement date (m) (default = NaN)
        mDr : float
            Measured soil water depletion for root zone (mm)
        mDrmax : float
            Measured soil water depletion for maximum root zone (mm)
        mfDr : float
            Measured fractional depletion for root zone (mm/mm)
        mfDrmax : float
            Measured fractional depletion for maximum root zone (mm/mm)
        mSWCr : float
            Measured soil water content for root zone (cm3/cm3)
        mSWCrmax : float
            Measured soil water content for maximum root zone (cm3/cm3)
        mKs : float
            Measured transpiration reduction factor (Ks, 0.0-1.0)

        Methods
        -------
        getZr(model)
            Get Zr on measurement date from model simulation output
        computeDr(negdep=True)
            Compute root zone soil water status metrics from mvswc
        computeKs(model)
            Estimate Ks from measured Dr, TAW, and RAW
        """

        def __init__(self, mdate, mvswc, par = None, sol = None,
                     Zr=float('NaN')):
            """
            Initialize the SoilWaterProfile class attributes.

            Parameters
            ----------
            mdate : str
                Year and day of year of measurement ('yyyy-ddd')
            mvswc : dict
                Measured volumetric soil water content (SWC, cm3/cm3)
                key - Bottom depth of measurement layer as integer (cm)
                value - Measured volumetric SWC as float (cm3/cm3)
            par : pyfao56 Parameters class, optional
                Provides the parameter data (e.g., thetaFC, Zrmax)
                (default = None)
            sol : pyfao56 SoilProfile class, optional
                Provides layered soil profile data (e.g., thetaFC)
                (default = None)
            Zr : float, optional
                Root depth on SWC measurement date (m) (default = NaN)
            """

            self.mdate = mdate
            self.mvswc = mvswc
            self.par = par
            self.sol = sol
            self.Zr = Zr
            self.mDr = float('NaN')
            self.mDrmax = float('NaN')
            self.mfDr = float('NaN')
            self.mfDrmax = float('NaN')
            self.mSWCr = float('NaN')
            self.mSWCrmax = float('NaN')
            self.mKs = float('NaN')

        def __str__(self):
            """Represent the SoilWaterProfile class as a string"""

            s = ('{:8s} '
                 '{:2d} '
                ).format(self.mdate,len(self.mvswc.keys()))
            for key in sorted(self.mvswc.keys()):
                s += '{:3d} '.format(key)
            for key in sorted(self.mvswc.keys()):
                s += '{:5.3f} '.format(self.mvswc[key])
            s += ('{:5.3f} {:8.3f} {:8.3f} {:6.3f} {:7.3f} '
                  '{:5.3f} {:8.3f} {:6.3f}'
                 ).format(self.Zr,self.mDr,self.mDrmax,self.mfDr,
                          self.mfDrmax,self.mSWCr,self.mSWCrmax,
                          self.mKs)
            return s

        def getZr(self, mdl):
            """Get Zr from model simulation on the measurement date

            Parameters
            ----------
            mdl : pyfao56 Model object
                Provides a Model instance with an odata DataFrame
            """

            self.Zr = mdl.odata.loc[self.mdate,'Zr']

        def computeDr(self, negdep = True):
            """Compute root zone soil water status metrics

            Parameters
            ----------
            negdep : boolean, optional
                Allow negative depletion or not (default = True)
            """

            #Root zone is evaluated in 10^-5 meter increments
            #Set root zone depth variables in 10^-5 meter units
            rzmax = int(self.par.Zrmax * 100000.) #10^-5 meters
            rz = int(self.Zr * 100000.) #10^-5 meters

            #Initialize other variables
            swc_dpths = list(self.mvswc.keys())
            if self.sol is not None:
                sol_dpths = list(self.sol.sdata.index.values) #cm
                thetaFC = self.sol.sdata['thetaFC'].to_dict()
                thetaWP = self.sol.sdata['thetaWP'].to_dict()
            elif self.par is not None:
                sol_dpth = int(self.par.Zrmax*100.) #cm
                sol_dpths = [sol_dpth] #cm
                thetaFC = {sol_dpth:self.par.thetaFC}
                thetaWP = {sol_dpth:self.par.thetaWP}
            else:
                raise Exception("No soil profile data available.")
            FCr = 0.
            FCrmax = 0.
            WPr = 0.
            WPrmax = 0.
            SWCr = 0.
            SWCrmax = 0.

            #Iterate the max root zone depth in 10^-5 m increments
            inc_dpth = 0.01 #mm
            for inc in list(range(1, rzmax + 1)):
                #Find soil profile layer depth that contains inc
                sol_dpth = [dpth for (idx, dpth) in enumerate(sol_dpths)
                            if inc <= dpth * 1000][0] #10^-5 meters
                #Find SWC measurement bottom depth that contains inc
                swc_dpth = [dpth for (idx, dpth) in enumerate(swc_dpths)
                            if inc <= dpth * 1000][0] #10^-5 meters
                #Compute incremental values
                FCinc  = thetaFC[sol_dpth] * inc_dpth #mm
                WPinc  = thetaWP[sol_dpth] * inc_dpth #mm
                SWCinc = self.mvswc[swc_dpth] * inc_dpth #mm
                if not negdep and SWCinc > FCinc:
                    SWCinc = FCinc #no negative depletion

                #Accumulate
                FCrmax  += FCinc #mm
                WPrmax  += WPinc #mm
                SWCrmax += SWCinc #mm
                if inc < rz:
                    FCr  += FCinc #mm
                    WPr  += WPinc #mm
                    SWCr += SWCinc #mm

            #Finalize water status metrics
            self.mDr = FCr - SWCr #mm
            self.mDrmax = FCrmax - SWCrmax #mm
            self.mfDr = (FCr - SWCr) / (FCr - WPr) #mm/mm
            self.mfDrmax = (FCrmax-SWCrmax)/(FCrmax-WPrmax) #mm/mm
            self.mSWCr = SWCr / (rz * inc_dpth) #cm3/cm3
            self.mSWCrmax = SWCrmax / (rzmax * inc_dpth) #cm3/cm3

        def computeKs(self, mdl):
            """Estimate Ks from measured Dr, TAW, and RAW

            Parameters
            ----------
            mdl : pyfao56 Model object
                Provides a Model instance with an odata DataFrame
            """

            TAW = mdl.odata.loc[self.mdate,'TAW']
            RAW = mdl.odata.loc[self.mdate,'RAW']
            Ks = (TAW - self.mDr) / (TAW - RAW) #FAO-56 Eq. 84
            self.mKs = sorted([0.0,Ks,1.0])[1]
