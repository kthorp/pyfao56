"""
########################################################################
The model.py module contains the Model class, which defines the
equations for daily soil water balance calculations based on the FAO-56
dual crop coefficient method for evapotranspiration (ET) estimation.

The FAO-56 method is described in the following documentation:
Allen, R. G., Pereira, L. S., Raes, D., Smith, M., 1998.  FAO Irrigation
and Drainage Paper No. 56. Crop Evapotranspiration: Guidelines for
Computing Crop Water Requirements. Food and Agriculture Organization of
the United Nations, Rome Italy.

http://www.fao.org/3/x0490e/x0490e00.htm

The model.py module contains the following:
    Model - A class for managing FAO-56 soil water balance computations.

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
10/27/2022 Incorporated Fort Collins ARS stratified soil layers approach
11/30/2022 Incorporated Fort Collins ARS water balance approach
08/17/2023 Improved logic for case of missing rhmin data
10/31/2023 Added AquaCrop Ks option
11/01/2023 Added reports of the cumulative seasonal water balance
########################################################################
"""

import pandas as pd
import datetime
import math

class Model:
    """A class for managing FAO-56 soil water balance computations.

    Manages computations based on FAO-56 methods for evapotranspiration
    and soil water balance calculations (Allen et al., 1998).

    Attributes
    ----------
    startDate : datetime
        Simulation start date in datetime format
    endDate : datetime
        Simulation end date in datetime format
    par : pyfao56 Parameters class
        Provides the parameter data for simulations
    wth : pyfao56 Weather class
        Provides the weather data for simulations
    irr : pyfao56 Irrigation class, optional
        Provides the irrigation data for simulations
        (default = None)
    sol : pyfao56 SoilProfile class, optional
        Provides data for modeling with stratified soil layers
        (default = None)
    upd : pyfao56 Update class, optional
        Provides data and methods for state variable updating
        (default = None)
    cons_p : boolean, optional
        If False, p follows FAO-56; if True, p is constant (=pbase)
        (default = False)
    aq_Ks : boolean, optional
        If False, Ks follows FAO-56; if True, Ks via AquaCrop equation
        (default = False)
    comment : str, optional
        User-defined file descriptions or metadata (default = '')
    tmstmp : datetime
        Time stamp for the class
    ModelState : class
        Contains parameters and model states for a single timestep
    cnames : list
        Column names for odata
    odata : DataFrame
        Model output data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Year','DOY','DOW','Date','ETref','tKcb','Kcb','h',
                   'Kcmax','fc','fw','few','De','Kr','Ke','E','DPe',
                   'Kc','ETc','TAW','TAWrmax','TAWb','Zr','p','RAW',
                   'Ks','Kcadj','ETcadj','T','DP','Dinc','Dr','fDr',
                   'Drmax','fDrmax','Db','fDb','Irrig','Rain','Year',
                   'DOY','DOW','Date']
            Year    - 4-digit year (yyyy)
            DOY     - Day of year (ddd)
            DOW     - Day of week
            Date    - Month/Day/Year (mm/dd/yy)
            ETref   - Daily reference evapotranspiration (mm)
            tKcb    - Basal crop coefficient, trapezoidal from FAO-56
            Kcb     - Basal crop coefficient, considering updates
            h       - Plant height (m)
            Kcmax   - Upper limit crop coefficient, FAO-56 Eq. 72
            fc      - Canopy cover fraction, FAO-56 Eq. 76
            fw      - Fraction soil surface wetted, FAO-56 Table 20
            few     - Exposed & wetted soil fraction, FAO-56 Eq. 75
            De      - Cumulative depth of evaporation, FAO-56 Eqs. 77&78
            Kr      - Evaporation reduction coefficient, FAO-56 Eq. 74
            Ke      - Evaporation coefficient, FAO-56 Eq. 71
            E       - Soil water evaporation (mm), FAO-56 Eq. 69
            DPe     - Percolation under exposed soil (mm), FAO-56 Eq. 79
            Kc      - Crop coefficient, FAO-56 Eq. 69
            ETc     - Non-stressed crop ET (mm), FAO-56 Eq. 69
            TAW     - Total available water (mm), FAO-56 Eq. 82
            TAWrmax - Total available water for max root depth (mm)
            TAWb    - Total available water in bottom layer (mm)
            Zr      - Root depth (m), FAO-56 page 279
            p       - Fraction depleted TAW, FAO-56 p162 and Table 22
            RAW     - Readily available water (mm), FAO-56 Equation 83
            Ks      - Transpiration reduction factor, FAO-56 Eq. 84
            Kcadj   - Adjusted crop coefficient, FA0-56 Eq. 80
            ETcadj  - Adjusted crop ET (mm), FAO-56 Eq. 80
            T       - Adjusted crop transpiration (mm)
            DP      - Deep percolation (mm), FAO-56 Eq. 88
            Dinc    - Depletion increment due to root growth (mm)
            Dr      - Soil water depletion (mm), FAO-56 Eqs. 85 & 86
            fDr     - Fractional root zone soil water depletion (mm/mm)
            Drmax   - Soil water depletion for max root depth (mm)
            fDrmax  - Fractional depletion for max root depth (mm/mm)
            Db      - Soil water depletion in the bottom layer (mm)
            fDb     - Fractional depletion in the bottom layer (mm/mm)
            Irrig   - Depth of irrigation (mm)
            Rain    - Depth of precipitation (mm)
            Year    - 4-digit year (yyyy)
            DOY     - Day of year (ddd)
            DOW     - Day of week
            Date    - Month/Day/Year (mm/dd/yy)
    swbdata : dict
        Container for cumulative seasonal water balance data
        keys - ['ETref','ETc','ETcadj','E','T','DP','Irrig','Rain',
                'Dr_ini','Dr_end','Drmax_ini','Drmax_end']
        value - Cumulative water balance data in mm

    Methods
    -------
    savefile(filepath='pyfao56.out')
        Save pyfao56 output data to a file
    savesums(filepath='pyfao56.sum')
        Save seasonal water balance data to a file
    run()
        Conduct the FAO-56 calculations from startDate to endDate
    """

    def __init__(self, start, end, par, wth, irr=None, sol=None,
                 upd=None, cons_p=False, aq_Ks=False, comment=''):
        """Initialize the Model class attributes.

        Parameters
        ----------
        start : str
            Simulation start year and doy ('yyyy-ddd')
        end : str
            Simulation end year and doy ('yyyy-ddd')
        par : pyfao56 Parameters object
            Provides the parameter data for simulations
        wth : pyfao56 Weather object
            Provides the weather data for simulations
        irr : pyfao56 Irrigation object, optional
            Provides the irrigation data for simulations
            (default = None)
        sol : pyfao56 SoilProfile object, optional
            Provides data for modeling with stratified soil layers
            (default = None)
        upd : pyfao56 Update object, optional
            Provides data and methods for state variable updating
            (default = None)
        cons_p : boolean, optional
            If False, p follows FAO-56; if True, p is constant (=pbase)
            (default = False)
        aq_Ks : boolean, optional
            If False, Ks follows FAO-56; if True, Ks via AquaCrop Eqn
            (default = False)
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """

        self.startDate = datetime.datetime.strptime(start, '%Y-%j')
        self.endDate   = datetime.datetime.strptime(end, '%Y-%j')
        self.par = par
        self.wth = wth
        self.irr = irr
        self.sol = sol
        self.upd = upd
        self.cons_p = cons_p
        self.aq_Ks = aq_Ks
        self.comment = 'Comments: ' + comment.strip()
        self.tmstmp = datetime.datetime.now()
        self.cnames = ['Year','DOY','DOW','Date','ETref','tKcb','Kcb',
                       'h','Kcmax','fc','fw','few','De','Kr','Ke','E',
                       'DPe','Kc','ETc','TAW','TAWrmax','TAWb','Zr','p',
                       'RAW','Ks','Kcadj','ETcadj','T','DP','Dinc','Dr',
                       'fDr','Drmax','fDrmax','Db','fDb','Irrig','Rain',
                       'Year','DOY','DOW','Date']
        self.odata = pd.DataFrame(columns=self.cnames)

    def __str__(self):
        """Represent the Model class variables as a string."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        sdate = self.startDate.strftime('%m/%d/%Y')
        edate = self.endDate.strftime('%m/%d/%Y')
        if self.sol is None:
            solmthd = 'D - Default FAO-56 homogenous soil bucket ' \
                      'approach'
        else:
            solmthd = 'L - Fort Collins ARS stratified soil layers ' \
                      'approach'
        fmts = {'Year':'{:4s}'.format,'DOY':'{:3s}'.format,
                'DOW':'{:3s}'.format,'Date':'{:8s}'.format,
                'ETref':'{:6.3f}'.format,'tKcb':'{:5.3f}'.format,
                'Kcb':'{:5.3f}'.format,'h':'{:5.3f}'.format,
                'Kcmax':'{:5.3f}'.format,'fc':'{:5.3f}'.format,
                'fw':'{:5.3f}'.format,'few':'{:5.3f}'.format,
                'De':'{:7.3f}'.format,'Kr':'{:5.3f}'.format,
                'Ke':'{:5.3f}'.format,'E':'{:6.3f}'.format,
                'DPe':'{:7.3f}'.format,'Kc':'{:5.3f}'.format,
                'ETc':'{:6.3f}'.format,'TAW':'{:7.3f}'.format,
                'TAWrmax':'{:7.3f}'.format,'TAWb':'{:7.3f}'.format,
                'Zr':'{:5.3f}'.format,'p':'{:5.3f}'.format,
                'RAW':'{:7.3f}'.format,'Ks':'{:5.3f}'.format,
                'Kcadj':'{:5.3f}'.format,'ETcadj':'{:6.3f}'.format,
                'T':'{:6.3f}'.format,'DP':'{:7.3f}'.format,
                'Dinc':'{:7.3f}'.format,'Dr':'{:7.3f}'.format,
                'fDr':'{:7.3f}'.format,'Drmax':'{:7.3f}'.format,
                'fDrmax':'{:7.3f}'.format,'Db':'{:7.3f}'.format,
                'fDb':'{:7.3f}'.format,'Irrig':'{:7.3f}'.format,
                'Rain':'{:7.3f}'.format}
        ast='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Output Data\n'
             'Timestamp: {:s}\n'
             'Simulation start date: {:s}\n'
             'Simulation end date: {:s}\n'
             'Soil method: {:s}\n'
             '{:s}\n'
             '{:s}\n'
             '{:s}\n'
             'Year-DOY  Year  DOY  DOW      Date  ETref  tKcb   Kcb'
             '     h Kcmax    fc    fw   few      De    Kr    Ke      E'
             '     DPe    Kc    ETc     TAW TAWrmax    TAWb    Zr     p'
             '     RAW    Ks Kcadj ETcadj      T      DP    Dinc'
             '      Dr     fDr   Drmax  fDrmax      Db     fDb'
             '   Irrig    Rain  Year  DOY  DOW      Date\n'
             ).format(ast,
                      timestamp,
                      sdate,
                      edate,
                      solmthd,
                      ast,
                      self.comment,
                      ast)
        if not self.odata.empty:
            s += self.odata.to_string(header=False,formatters=fmts)
        return s

    def savefile(self,filepath='pyfao56.out'):
        """Save pyfao56 output data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.out')

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

    def savesums(self, filepath='pyfao56.sum'):
        """Save a summary file with cumulative water balance values.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.sum')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        sdate = self.startDate.strftime('%m/%d/%Y')
        edate = self.endDate.strftime('%m/%d/%Y')

        ast = '*'*72
        s = ('{:s}\n'
            'pyfao56: FAO-56 Evapotranspiration in Python\n'
            'Seasonal Water Balance Summary\n'
            'Timestamp: {:s}\n'
            'Simulation start date: {:s}\n'
            'Simulation end date: {:s}\n'
            'All values expressed in mm.\n'
            '{:s}\n'
            '{:s}\n'
            '{:s}\n'
            ).format(ast,timestamp,sdate,edate,ast,self.comment,ast)
        if not self.odata.empty:
            keys = ['ETref','ETc','ETcadj','E','T','DP','Irrig','Rain',
                    'Dr_ini','Dr_end','Drmax_ini','Drmax_end']
            for key in keys:
                s += '{:8.3f} : {:s}\n'.format(self.swbdata[key],key)

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for summary data is not found.')
        else:
            f.write(s)
            f.close()

    class ModelState:
        """Contain parameters and states for a single timestep."""

        pass

    def run(self):
        """Initialize model, conduct simulations, update self.odata"""

        tcurrent = self.startDate
        tdelta = datetime.timedelta(days=1)

        #Initialize model state
        io = self.ModelState()
        io.i = 0
        io.Kcbini  = self.par.Kcbini
        io.Kcbmid  = self.par.Kcbmid
        io.Kcbend  = self.par.Kcbend
        io.Lini    = self.par.Lini
        io.Ldev    = self.par.Ldev
        io.Lmid    = self.par.Lmid
        io.Lend    = self.par.Lend
        io.hini    = self.par.hini
        io.hmax    = self.par.hmax
        io.thetaFC = self.par.thetaFC
        io.thetaWP = self.par.thetaWP
        io.theta0  = self.par.theta0
        io.Zrini   = self.par.Zrini
        io.Zrmax   = self.par.Zrmax
        io.pbase   = self.par.pbase
        io.Ze      = self.par.Ze
        io.REW     = self.par.REW
        #Total evaporable water (TEW, mm) - FAO-56 Equation 73
        io.TEW = 1000. * (io.thetaFC - 0.50 * io.thetaWP) * io.Ze
        #Initial depth of evaporation (De, mm) - FAO-56 page 153
        io.De = 1000. * (io.thetaFC - 0.50 * io.thetaWP) * io.Ze
        if self.sol is None:
            io.solmthd = 'D' #Default homogeneous soil from Parameters
            #Initial root zone depletion (Dr, mm) - FAO-56 Equation 87
            io.Dr = 1000. * (io.thetaFC - io.theta0) * io.Zrini
            #Initial soil depletion for max root depth (Drmax, mm)
            io.Drmax = 1000. * (io.thetaFC - io.theta0) * io.Zrmax
            #Initial root zone total available water (TAW, mm)
            io.TAW = 1000. * (io.thetaFC - io.thetaWP) * io.Zrini
            #By default, FAO-56 doesn't consider the following variables
            io.TAWrmax = -99.999
            io.Db = -99.999
            io.TAWb = -99.999
        else:
            io.solmthd = 'L' #Layered soil profile from SoilProfile
            io.lyr_dpths = list(self.sol.sdata.index)
            io.lyr_thFC  = list(self.sol.sdata['thetaFC'])
            io.lyr_thWP  = list(self.sol.sdata['thetaWP'])
            io.lyr_th0   = list(self.sol.sdata['theta0'])
            io.Dr = 0.
            io.Drmax = 0.
            io.TAW = 0.
            io.TAWrmax = 0.
            #Iterate down the soil profile in 1 mm increments
            for dpthmm in list(range(1, (io.lyr_dpths[-1] * 10 + 1))):
                #Find soil layer index that contains dpthmm
                lyr_idx = [idx for (idx, dpth) in
                          enumerate(io.lyr_dpths) if dpthmm<=dpth*10][0]
                #Initial root zone depletion (Dr, mm)
                if dpthmm <= io.Zrini * 1000.: #mm
                    diff = (io.lyr_thFC[lyr_idx] - io.lyr_th0[lyr_idx])
                    io.Dr += diff #mm
                #Initial depletion for max root depth (Drmax, mm)
                if dpthmm <= io.Zrmax * 1000.: #mm
                    diff = (io.lyr_thFC[lyr_idx] - io.lyr_th0[lyr_idx])
                    io.Drmax += diff #mm
                #Initial root zone total available water (TAW, mm)
                if dpthmm <= io.Zrini * 1000.: #mm
                    diff = (io.lyr_thFC[lyr_idx] - io.lyr_thWP[lyr_idx])
                    io.TAW += diff #mm
                #Total available water for max root depth (TAWrmax, mm)
                if dpthmm <= io.Zrmax * 1000.: #mm
                    diff = (io.lyr_thFC[lyr_idx] - io.lyr_thWP[lyr_idx])
                    io.TAWrmax += diff #mm
            #Initial depletion in the bottom layer (Db, mm)
            io.Db = io.Drmax - io.Dr
            #Initial total available water in bottom layer (TAWb, mm)
            io.TAWb = io.TAWrmax - io.TAW
        io.h = io.hini
        io.Zr = io.Zrini
        io.fw = 1.0
        io.wndht = self.wth.wndht
        io.rfcrp = self.wth.rfcrp
        io.cons_p = self.cons_p
        io.aq_Ks = self.aq_Ks
        self.odata = pd.DataFrame(columns=self.cnames)

        while tcurrent <= self.endDate:
            mykey = tcurrent.strftime('%Y-%j')

            #Update ModelState object
            io.ETref = self.wth.wdata.loc[mykey,'ETref']
            if math.isnan(io.ETref):
                io.ETref = self.wth.compute_etref(mykey)
            io.rain = self.wth.wdata.loc[mykey,'Rain']
            io.wndsp = self.wth.wdata.loc[mykey,'Wndsp']
            if math.isnan(io.wndsp):
                io.wndsp = 2.0
            io.rhmin = self.wth.wdata.loc[mykey,'RHmin']
            if math.isnan(io.rhmin):
                tmax = self.wth.wdata.loc[mykey,'Tmax']
                tmin = self.wth.wdata.loc[mykey,'Tmin']
                tdew = self.wth.wdata.loc[mykey,'Tdew']
                if math.isnan(tdew):
                    tdew = tmin
                #ASCE (2005) Eqs. 7 and 8
                emax = 0.6108*math.exp((17.27*tmax)/
                                       (tmax+237.3))
                ea   = 0.6108*math.exp((17.27*tdew)/
                                       (tdew+237.3))
                io.rhmin = ea/emax*100.
            if math.isnan(io.rhmin):
                io.rhmin = 45.
            io.idep = 0.0
            if self.irr is not None:
                if mykey in self.irr.idata.index:
                    io.idep = self.irr.idata.loc[mykey,'Depth']
                    io.fw = self.irr.idata.loc[mykey,'fw']

            #Obtain updates for Kcb, h, and fc, if available
            io.updKcb = float('NaN')
            io.updh = float('NaN')
            io.updfc = float('NaN')
            if self.upd is not None:
                io.updKcb = self.upd.getdata(mykey,'Kcb')
                io.updh = self.upd.getdata(mykey,'h')
                io.updfc = self.upd.getdata(mykey,'fc')

            #Advance timestep
            self._advance(io)

            #Append results to self.odata
            year = tcurrent.strftime('%Y')
            doy = tcurrent.strftime('%j') #Day of Year
            dow = tcurrent.strftime('%a') #Day of Week
            dat = tcurrent.strftime('%m/%d/%y') #Date mm/dd/yy
            data = [year, doy, dow, dat, io.ETref, io.tKcb, io.Kcb,
                    io.h, io.Kcmax, io.fc, io.fw, io.few, io.De, io.Kr,
                    io.Ke, io.E, io.DPe, io.Kc, io.ETc, io.TAW,
                    io.TAWrmax, io.TAWb, io.Zr, io.p, io.RAW, io.Ks,
                    io.Kcadj, io.ETcadj, io.T, io.DP, io.Dinc, io.Dr,
                    io.fDr, io.Drmax, io.fDrmax, io.Db, io.fDb, io.idep,
                    io.rain, year, doy, dow, dat]
            self.odata.loc[mykey] = data

            tcurrent = tcurrent + tdelta
            io.i+=1

        #Save seasonal water balance data to self.swbdata dictionary
        sdoy = self.startDate.strftime("%Y-%j")
        edoy = self.endDate.strftime("%Y-%j")
        self.swbdata = {'ETref'    :sum(self.odata['ETref']),
                        'ETc'      :sum(self.odata['ETc']),
                        'ETcadj'   :sum(self.odata['ETcadj']),
                        'E'        :sum(self.odata['E']),
                        'T'        :sum(self.odata['T']),
                        'DP'       :sum(self.odata['DP']),
                        'Irrig'    :sum(self.odata['Irrig']),
                        'Rain'     :sum(self.odata['Rain']),
                        'Dr_ini'   :self.odata.loc[sdoy,'Dr'],
                        'Dr_end'   :self.odata.loc[edoy,'Dr'],
                        'Drmax_ini':self.odata.loc[sdoy,'Drmax'],
                        'Drmax_end':self.odata.loc[edoy,'Drmax']}

    def _advance(self, io):
        """Advance the model by one daily timestep.

        Parameters
        ----------
        io : ModelState object
        """

        #Basal crop coefficient (Kcb)
        #From FAO-56 Tables 11 and 17
        s1 = io.Lini
        s2 = s1 + io.Ldev
        s3 = s2 + io.Lmid
        s4 = s3 + io.Lend
        if 0<=io.i<=s1:
            io.tKcb = io.Kcbini
            io.Kcb = io.Kcbini
        elif s1<io.i<=s2:
            io.tKcb += (io.Kcbmid-io.Kcbini)/(s2-s1)
            io.Kcb += (io.Kcbmid-io.Kcbini)/(s2-s1)
        elif s2<io.i<=s3:
            io.tKcb = io.Kcbmid
            io.Kcb = io.Kcbmid
        elif s3<io.i<=s4:
            io.tKcb += (io.Kcbmid-io.Kcbend)/(s3-s4)
            io.Kcb += (io.Kcbmid-io.Kcbend)/(s3-s4)
        elif s4<io.i:
            io.tKcb = io.Kcbend
            io.Kcb = io.Kcbend
        #Overwrite Kcb if updates are available
        if io.updKcb > 0: io.Kcb = io.updKcb

        #Plant height (h, m)
        io.h = max([io.hini+(io.hmax-io.hini)*(io.Kcb-io.Kcbini)/
                    (io.Kcbmid-io.Kcbini),0.001,io.h])
        #Overwrite h if updates are available
        if io.updh > 0: io.h = io.updh

        #Root depth (Zr, m) - FAO-56 page 279
        io.Zr = max([io.Zrini + (io.Zrmax-io.Zrini)*(io.tKcb-io.Kcbini)/
                     (io.Kcbmid-io.Kcbini),0.001,io.Zr])

        #Upper limit crop coefficient (Kcmax) - FAO-56 Eq. 72
        u2 = io.wndsp * (4.87/math.log(67.8*io.wndht-5.42))
        u2 = sorted([1.0,u2,6.0])[1]
        rhmin = sorted([20.0,io.rhmin,80.])[1]
        if io.rfcrp == 'S':
            io.Kcmax = max([1.2+(0.04*(u2-2.0)-0.004*(rhmin-45.0))*
                            (io.h/3.0)**.3, io.Kcb+0.05])
        elif io.rfcrp == 'T':
            io.Kcmax = max([1.0, io.Kcb + 0.05])

        #Canopy cover fraction (fc, 0.0-0.99) - FAO-56 Eq. 76
        io.fc = sorted([0.0,((io.Kcb-io.Kcbini)/(io.Kcmax-io.Kcbini))**
                        (1.0+0.5*io.h),0.99])[1]
        #Overwrite fc if updates are available
        if io.updfc > 0: io.fc = io.updfc

        #Fraction soil surface wetted (fw) - FAO-56 Table 20, page 149
        if io.idep > 0.0 and io.rain > 0.0:
            pass #fw=fw input
        elif io.idep > 0.0 and io.rain <= 0.0:
            pass #fw=fw input
        elif io.idep <= 0.0 and io.rain >= 3.0:
            io.fw = 1.0
        else:
            pass #fw = previous fw

        #Exposed & wetted soil fraction (few, 0.01-1.0) - FAO-56 Eq. 75
        io.few = sorted([0.01,min([1.0-io.fc, io.fw]),1.0])[1]

        #Evaporation reduction coefficient (Kr, 0-1) - FAO-56 Eq. 74
        io.Kr = sorted([0.0,(io.TEW-io.De)/(io.TEW-io.REW),1.0])[1]

        #Evaporation coefficient (Ke) - FAO-56 Eq. 71
        io.Ke = min([io.Kr*(io.Kcmax-io.Kcb), io.few*io.Kcmax])

        #Soil water evaporation (E, mm) - FAO-56 Eq. 69
        io.E = io.Ke * io.ETref

        #Deep percolation under exposed soil (DPe, mm) - FAO-56 Eq. 79
        runoff = 0.0
        io.DPe = max([io.rain - runoff + io.idep/io.fw - io.De,0.0])

        #Cumulative depth of evaporation (De, mm) - FAO-56 Eqs. 77 & 78
        De = io.De-(io.rain-runoff)-io.idep/io.fw+io.E/io.few+io.DPe
        io.De = sorted([0.0,De,io.TEW])[1]

        #Crop coefficient (Kc) - FAO-56 Eq. 69
        io.Kc = io.Ke + io.Kcb

        #Non-stressed crop evapotranspiration (ETc, mm) - FAO-56 Eq. 69
        io.ETc = io.Kc * io.ETref

        if io.solmthd == 'D':
            # Total available water (TAW, mm) - FAO-56 Eq. 82
            io.TAW = 1000.0 * (io.thetaFC - io.thetaWP) * io.Zr
        elif io.solmthd == 'L':
            io.TAW = 0.
            #Iterate down the soil profile in 1 mm increments
            for dpthmm in list(range(1, (io.lyr_dpths[-1] * 10 + 1))):
                #Find soil layer index that contains dpthmm
                lyr_idx = [idx for (idx, dpth) in
                          enumerate(io.lyr_dpths) if dpthmm<=dpth*10][0]
                #Total available water (TAW, mm)
                if dpthmm <= io.Zr * 1000.: #mm
                    diff = (io.lyr_thFC[lyr_idx] - io.lyr_thWP[lyr_idx])
                    io.TAW += diff #mm
            #Total available water in the bottom layer (TAWb, mm)
            io.TAWb_prev = io.TAWb
            io.TAWb = io.TAWrmax - io.TAW

        #Fraction depleted TAW (p, 0.1-0.8) - FAO-56 p162 and Table 22
        if io.cons_p is True:
            io.p = io.pbase
        else:
            io.p = sorted([0.1,io.pbase+0.04*(5.0-io.ETc),0.8])[1]

        #Readily available water (RAW, mm) - FAO-56 Equation 83
        io.RAW = io.p * io.TAW

        #Transpiration reduction factor (Ks, 0.0-1.0)
        if io.aq_Ks is True:
            #Ks method from AquaCrop
            rSWD = io.Dr/io.TAW
            Drel = (rSWD-io.p)/(1.0-io.p)
            sf = 1.5
            aqKs = 1.0-(math.exp(sf*Drel)-1.0)/(math.exp(sf)-1.0)
            io.Ks = sorted([0.0, aqKs, 1.0])[1]
        else:
            #FAO-56 Eq. 84
            io.Ks = sorted([0.0,(io.TAW-io.Dr)/(io.TAW-io.RAW),1.0])[1]

        #Adjusted crop coefficient (Kcadj) - FAO-56 Eq. 80
        io.Kcadj = io.Ks * io.Kcb + io.Ke

        #Adjusted crop evapotranspiration (ETcadj, mm) - FAO-56 Eq. 80
        io.ETcadj = io.Kcadj * io.ETref

        #Adjusted crop transpiration (T, mm)
        io.T = (io.Ks * io.Kcb) * io.ETref

        #Water balance methods
        if io.solmthd == 'D':
            #Deep percolation (DP, mm) - FAO-56 Eq. 88
            #Boundary layer is considered at the root zone depth (Zr)
            io.DP = max([io.rain-runoff+io.idep-io.ETcadj-io.Dr,0.0])

            #Root zone soil water depletion (Dr,mm) - FAO-56 Eqs.85 & 86
            Dr = io.Dr - (io.rain-runoff) - io.idep + io.ETcadj + io.DP
            io.Dr = sorted([0.0, Dr, io.TAW])[1]

            #Root zone soil water depletion fraction (fDr, mm/mm)
            io.fDr = 1.0 - ((io.TAW - io.Dr) / io.TAW)

            #By default, FAO-56 doesn't consider the following variables
            io.Dinc = -99.999
            io.Drmax = -99.999
            io.fDrmax = -99.999
            io.Db = -99.999
            io.fDb = -99.999

        elif io.solmthd == 'L':
            #Deep percolation (DP, mm)
            #Boundary layer is at the max root depth (Zrmax)
            io.DP = max([io.rain-runoff+io.idep-io.ETcadj-io.Drmax,0.0])

            #Depletion increment due to root growth (Dinc, mm)
            #Computed from Db based on the incremental change in TAWb
            if io.TAWb_prev > 0.0:
                io.Dinc = io.Db * (1.0 - (io.TAWb / io.TAWb_prev))
            else: #handle zero divide issue
                io.Dinc = 0.0

            #Root zone soil water depletion (Dr, mm)
            Dr = io.Dr - (io.rain-runoff)-io.idep+io.ETcadj+io.Dinc
            io.Dr = sorted([0.0, Dr, io.TAW])[1]

            #Root zone soil water depletion fraction (fDr, mm/mm)
            io.fDr = 1.0 - ((io.TAW - io.Dr) / io.TAW)

            #Soil water depletion at max root depth (Drmax, mm)
            Drmax = io.Drmax - (io.rain-runoff)-io.idep+io.ETcadj+io.DP
            io.Drmax = sorted([0.0, Drmax, io.TAWrmax])[1]

            #Soil water depletion fraction at Zrmax (fDrmax, mm/mm)
            io.fDrmax = 1.0 - ((io.TAWrmax - io.Drmax) / io.TAWrmax)

            #Soil water depletion in the bottom layer (Db, mm)
            Db = io.Drmax - io.Dr
            io.Db = sorted([0.0, Db, io.TAWb])[1]

            #Bottom layer soil water depletion fraction (fDb, mm/mm)
            if io.TAWb > 0.0:
                io.fDb = 1.0 - ((io.TAWb - io.Db) / io.TAWb)
            else:
                io.fDb = 0.0
