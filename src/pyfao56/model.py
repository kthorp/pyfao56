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
    end : datetime
        Simulation end date in datetime format
    par : pyfao56 Parameters class
        Provides the parameter data for simulations
    wth : pyfao56 Weather class
        Provides the weather data for simulations
    irr : pyfao56 Irrigation class
        Provides the irrigation data for simulations
    upd : pyfao56 Updateclass, optional
        Provides data and methods for state variable updating
        (default = None)
    ModelState : class
        Contains parameters and model states for a single timestep
    cnames : list
        Column names for odata
    odata : DataFrame
        Model output data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Year','DOY','DOW','Date','ETref','Kcb','h','Kcmax',
                   'fc','fw','few','De','Kr','Ke','E','DPe','Kc','ETc',
                   'TAW','Zr','p','RAW','Ks','ETcadj','T','DP','Dr',
                   'PerDr','Irrig','Rain','Year','DOY','DOW','Date']
            Year   - 4-digit year (yyyy)
            DOY    - Day of year (ddd)
            DOW    - Day of week
            Date   - Month/Day/Year (mm/dd/yy)
            ETref  - Daily reference evapotranspiration (mm)
            Kcb    - Basal crop coefficient
            h      - Plant height (m)
            Kcmax  - Upper limit crop coefficient, FAO-56 Eq. 72
            fc     - Canopy cover fraction, FAO-56 Eq. 76
            fw     - Fraction soil surface wetted, FAO-56 Table 20
            few    - Exposed & wetted soil fraction, FAO-56 Eq. 75
            De     - Cumulative depth of evaporation, FAO-56 Eqs. 77&78
            Kr     - Evaporation reduction coefficient, FAO-56 Eq. 74
            Ke     - Evaporation coefficient, FAO-56 Eq. 71
            E      - Soil water evaporation (mm), FAO-56 Eq. 69
            DPe    - Percolation under exposed soil (mm), FAO-56 Eq. 79
            Kc     - Crop coefficient, FAO-56 Eq. 69
            ETc    - Non-stressed crop ET (mm), FAO-56 Eq. 69
            TAW    - Total available water (mm), FAO-56 Eq. 82
            Zr     - Root depth (m), FAO-56 page 279
            p      - Fraction depleted TAW, FAO-56 p162 and Table 22
            RAW    - Readily available water (mm), FAO-56 Equation 83
            Ks     - Transpiration reduction factor, FAO-56 Eq. 84
            ETcadj - Adjusted crop ET (mm), FAO-56 Eq. 80
            T      - Adjusted crop transpiration (mm)
            DP     - Deep percolation (mm), FAO-56 Eq. 88
            Dr     - Soil water depletion (mm), FAO-56 Eqs. 85 & 86
            PerDr  - Percent root zone soil water depletion (%)
            Irrig  - Depth of irrigation (mm)
            Rain   - Depth of precipitation (mm)
            Year   - 4-digit year (yyyy)
            DOY    - Day of year (ddd)
            DOW    - Day of week
            Date   - Month/Day/Year (mm/dd/yy)

    Methods
    -------
    run()
        Conduct the FAO-56 calculations from start to end
    """

    def __init__(self,start, end, par, wth, irr, upd=None):
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
        irr : pyfao56 Irrigation object
            Provides the irrigation data for simulations
        upd : pyfao56 Update object, optional
            Provides data and methods for state variable updating
            (default = None)
        """

        self.startDate = datetime.datetime.strptime(start, '%Y-%j')
        self.endDate   = datetime.datetime.strptime(end, '%Y-%j')
        self.par = par
        self.wth = wth
        self.irr = irr
        self.upd = upd
        self.cnames = ['Year','DOY','DOW','Date','ETref','Kcb','h',
                       'Kcmax','fc','fw','few','De','Kr','Ke','E','DPe',
                       'Kc','ETc','TAW','Zr','p','RAW','Ks','ETcadj',
                       'T','DP','Dr','PerDr','Irrig','Rain','Year',
                       'DOY','DOW','Date']
        self.odata = pd.DataFrame(columns=self.cnames)

    def __str__(self):
        """Represent the Model class variables as a string."""

        fmts = {'Year':'{:4s}'.format,'DOY':'{:3s}'.format,
                'DOW':'{:3s}'.format,'Date':'{:8s}'.format,
                'ETref':'{:6.3f}'.format,'Kcb':'{:5.3f}'.format,
                'h':'{:5.3f}'.format,'Kcmax':'{:5.3f}'.format,
                'fc':'{:5.3f}'.format,'fw':'{:5.3f}'.format,
                'few':'{:5.3f}'.format,'De':'{:7.3f}'.format,
                'Kr':'{:5.3f}'.format,'Ke':'{:5.3f}'.format,
                'E':'{:6.3f}'.format,'DPe':'{:7.3f}'.format,
                'Kc':'{:5.3f}'.format,'ETc':'{:6.3f}'.format,
                'TAW':'{:7.3f}'.format,'Zr':'{:5.3f}'.format,
                'p':'{:5.3f}'.format,'RAW':'{:7.3f}'.format,
                'Ks':'{:5.3f}'.format,'ETcadj':'{:6.3f}'.format,
                'T':'{:6.3f}'.format,'DP':'{:7.3f}'.format,
                'Dr':'{:7.3f}'.format,'PerDr':'{:7.3f}'.format,
                'Irrig':'{:7.3f}'.format,'Rain':'{:7.3f}'.format}
        ast='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 in Python\n'
             'Output Data\n'
             '{:s}\n'
             'Year-DOY  Year  DOY  DOW      Date  ETref   Kcb     h'
             ' Kcmax    fc    fw   few      De    Kr    Ke      E'
             '     DPe    Kc    ETc     TAW    Zr     p     RAW'
             '    Ks ETcadj      T      DP      Dr   PerDr   Irrig'
             '    Rain  Year  DOY  DOW      Date\n'
             ).format(ast,ast)
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
            print("The filepath for output data is not found.")
        else:
            f.write(self.__str__())
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
        io.TEW = 1000.0 * (io.thetaFC - 0.50 * io.thetaWP) * io.Ze
        #Initial depth of evaporation (De, mm) - FAO-56 page 153
        io.De = 1000.0 * (io.thetaFC - 0.50 * io.thetaWP) * io.Ze
        #Initial soil water depletion (Dr, mm) - FAO-56 Equation 87
        io.Dr = 1000.0 * (io.thetaFC - io.theta0) * io.Zrini
        io.h = io.hini
        io.Zr = io.Zrini
        io.fw = 1.0
        io.wndht = self.wth.wndht
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
                tdew = self.wth.wdata.loc[mykey,'Tmin']
                emax = 0.6108*math.exp((17.27*io.tmax)/
                                       (io.tmax+237.3))
                ea   = 0.6108*math.exp((17.27*io.tdew)/
                                       (io.tdew+237.3))
                io.rhmin = ea/emax*100.
            if math.isnan(io.rhmin):
                io.rhmin = 45.
            if mykey in self.irr.idata.index:
                io.idep = self.irr.idata.loc[mykey,'Depth']
                io.fw = self.irr.idata.loc[mykey,'fw']
            else:
                io.idep = 0.0

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
            data = [year,doy,dow,dat,io.ETref,io.Kcb,io.h,io.Kcmax,
                    io.fc,io.fw,io.few,io.De,io.Kr,io.Ke,io.E,io.DPe,
                    io.Kc,io.ETc,io.TAW,io.Zr,io.p,io.RAW,io.Ks,
                    io.ETcadj,io.T,io.DP,io.Dr,io.PerDr,io.idep,io.rain,
                    year,doy,dow,dat]
            self.odata.loc[mykey] = data

            tcurrent = tcurrent + tdelta
            io.i+=1

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
            io.Kcb=io.Kcbini
        elif s1<io.i<=s2:
            io.Kcb+=(io.Kcbmid-io.Kcbini)/(s2-s1)
        elif s2<io.i<=s3:
            io.Kcb=io.Kcbmid
        elif s3<io.i<=s4:
            io.Kcb += (io.Kcbmid-io.Kcbend)/(s3-s4)
        elif s4<io.i:
            io.Kcb=io.Kcbend
        if io.updKcb > 0: io.Kcb = io.updKcb

        #Plant height (h, m)
        io.h = max([io.hini+(io.hmax-io.hini)*(io.Kcb-io.Kcbini)/
                    (io.Kcbmid-io.Kcbini),0.001,io.h])
        if io.updh > 0: io.h = io.updh

        #Root depth (Zr, m) - FAO-56 page 279
        io.Zr = max([io.Zrini + (io.Zrmax-io.Zrini)*(io.Kcb-io.Kcbini)/
                     (io.Kcbmid-io.Kcbini),0.001,io.Zr])

        #Upper limit crop coefficient (Kcmax) - FAO-56 Eq. 72
        u2 = io.wndsp * (4.87/math.log(67.8*io.wndht-5.42))
        u2 = sorted([1.0,u2,6.0])[1]
        rhmin = sorted([20.0,io.rhmin,80.])[1]
        io.Kcmax = max([1.2+(0.04*(u2-2.0)-0.004*(rhmin-45.0))*
                        (io.h/3.0)**.3, io.Kcb+0.05])

        #Canopy cover fraction (fc, 0.0-0.99) - FAO-56 Eq. 76
        io.fc = sorted([0.0,((io.Kcb-io.Kcbini)/(io.Kcmax-io.Kcbini))**
                        (1.0+0.5*io.h),0.99])[1]
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

        #Total available water (TAW, mm) - FAO-56 Eq. 82
        io.TAW = 1000.0 * (io.thetaFC - io.thetaWP) * io.Zr

        #Fraction depleted TAW (p, 0.1-0.8) - FAO-56 p162 and Table 22
        io.p = sorted([0.1,io.pbase+0.04*(5.0-io.ETc),0.8])[1]

        #Readily available water (RAW, mm) - FAO-56 Equation 83
        io.RAW = io.p * io.TAW

        #Transpiration reduction factor (Ks, 0.0-1.0) - FAO-56 Eq. 84
        io.Ks = sorted([0.0, (io.TAW-io.Dr)/(io.TAW-io.RAW), 1.0])[1]

        #Adjusted crop evapotranspiration (ETcadj, mm) - FAO-56 Eq. 80
        io.ETcadj = (io.Ks * io.Kcb + io.Ke) * io.ETref

        #Adjusted crop transpiration (T, mm)
        io.T = (io.Ks * io.Kcb) * io.ETref

        #Deep percolation (DP, mm) - FAO-56 Eq. 88
        io.DP = max([io.rain-runoff+io.idep-io.ETcadj-io.Dr,0.0])

        #Root zone soil water depletion (Dr, mm) - FAO-56 Eqs. 85 & 86
        Dr = io.Dr - (io.rain - runoff) - io.idep + io.ETcadj + io.DP
        io.Dr = sorted([0.0, Dr, io.TAW])[1]

        #Percent root zone soil water depletion (PerDr, %)
        io.PerDr = (1.0-((io.TAW - io.Dr)/io.TAW))*100.0
