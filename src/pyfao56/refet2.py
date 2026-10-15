"""
########################################################################
The refet2.py module contains the RefET2 class, which defines equations
for computing short-crop or tall-crop standardized reference
evapotranspiration for daily, hourly, or monthly time steps, following
the methods described in the 2025 revision of FAO-56 and the ASCE
Standardized Reference Evapotranspiration Equation. The short-crop
standardized reference evapotranspiration is equivalent to the FAO
Penman-Monteith ETo as described in FAO-56.

The 2025 revision of FAO-56 is cited as follows:
Pereira, L. S., Allen, R. G., Paredes, P., Lopez-Urrea, R., Raes, D.,
Smith, M., Kilic, A., Salman, M., 2025. FAO Irrigation and Drainage
Paper No. 56. Rev. 1. Crop Evapotranspiration: Guidelines for Computing
Crop Water Requirements, Second edition. Food and Agriculture
Organization of the United Nations, Rome, Italy.

The ASCE Standardized Reference Evapotranspiration Equation is cited as
follows:
ASCE Task Committee on Standardization of Reference Evapotranspiration
(Walter, I. A., Allen, R. G., Elliott, R., Itenfisu, D., Brown, P.,
Jensen, M. E.,Mecham, B., Howell, T. A., Snyder, R., Eching, S.,
Spofford, T., Hattendorf, M., Martin, D., Cuenca, R. H., Wright, J. L.)
, 2005. The ASCE Standardized Reference Evapotranspiration Equation.
American Society of Civil Engineers, Reston, VA.

The refet2.py module contains the following:
    RefET2 - A class for managing standardized reference
             evapotranspiration computations.

09/24/2026 Initial Python script by Kelly Thorp
########################################################################
"""

import math

class RefET2:
    """A class for managing standardized reference ET computations.

    Manages computations based on documentation provided in the 2025
    revision of FAO-56 (Pereira et al., 2025) and the ASCE Standardized
    Reference Evapotranspiration Equation (ASCE, 2005).

    Attributes
    ----------
    var : dict
        Contains variables from reference ET computations
        Input, output, and intermediate variables are included:
            albedo - Reflected solar (shortwave) radiation (fraction)
            b      - Used to calculate sc (radians)
            beta   - Sun angle at midpoint of period (radians)
            beta24 - Mean daily sun angle for daylight period (radians)
            csreq  - 'S' for simple Rso method; 'C' for complex method
            doy    - Day number of the year between 1 and 366
            dr     - Inverse relative distance Earth-Sun squared (-)
            ea     - Actual vapor pressure (kPa)
            emax   - Saturation vapor pressure at tmax (kPa)
            emin   - Saturation vapor pressure at tmin (kPa)
            es     - Saturation vapor pressure (kPa)
            etsz   - Standardized reference ET (mm)(d^-1 or h^-1)
            fcd    - Cloudiness function (-)
            fcdpt  - Cloudiness function from previous timestep (-)
            g      - Soil heat flux (MJ m^-2)(d^-1 or h^-1)
            kb     - Clearness index for direct beam radiation (-)
            kd     - Clearness index for diffuse radiation (-)
            kt     - Clearness coefficient for turbidity and haze (-)
            lat    - Latitude of the weather site (decimal degrees)
            latrad - Latitude of the weather site (radians)
            ldelta - Solar declination (radians)
            lon    - Longitude of the weather site (decimal degrees)
            lzn    - Longitude at center of local timezone (decimal deg)
            N      - Daylight hours (h)
            patm   - Mean atmospheric pressure at weather site (kPa)
            psycon - Psychrometric constant (kPa (deg C)^-1)
            pwat   - Precipitable water in the atmosphere (mm)
            ra     - Extraterrestrial radiation (MJ m^-2)(d^-1 or h^-1)
            ratio  - Ratio of rs and rso (-)
            rfcrp  - 'S' for short reference crop; 'T' for tall crop
            rhmax  - Daily maximum relative humidity (%)
            rhmin  - Daily minimum relative humidity (%)
            rhum   - Mean relative humidity (%)
            rn     - Net radiation (MJ m^-2)(d^-1 or h^-1)
            rnet   - Net radiation, input (MJ m^-2)(d^-1 or h^-1)
            rnl    - Net longwave radiation (MJ m^-2)(d^-1 or h^-1)
            rns    - Net shortwave radiation (MJ m^-2)(d^-1 or h^-1)
            rs     - Solar (shortwave) radiation (MJ m^-2)(d^-1 or h^-1)
            rso    - Clear sky solar radiation (MJ m^-2)(d^-1 or h^-1)
            sc     - Seasonal correction for solar time (h)
            sct    - Standard clock time at the midpoint of period (h)
            srad   - Solar radiation, input (MJ m^-2)(d^-1 or h^-1)
            sunhr  - Daily duration of sunshine (h)
            tavg   - Average of max and min air temperature (deg C)
            tdew   - Mean dew point temperature (deg C)
            tl     - Length of the calculation period (h)
            tmax   - Daily maximum air temperature (deg C)
            tmean  - Mean air temperature (deg C)
            tmin   - Daily minimum air temperature (deg C)
            u2     - Wind speed at standard 2 m height (m s^-1)
            Udelta - Slope of the saturation vapor pressure temperature
                     curve (kPa (deg C)^-1)
            vapr   - Mean vapor pressure (kPa)
            vpd    - Vapor pressure deficit (kPa)
            w1     - Solar time angle, beginning of period (radians)
            w2     - Solar time angle, end of period (radians)
            wmid   - Solar time angle at midpoint of period (radians)
            wndht  - Wind measurement height above ground surface (m)
            wndsp  - Mean wind speed, input (m s^-1)
            ws     - Sunset hour angle (radians)
            z      - Weather site elevation above mean sea level (m)

    Methods
    -------
    daily (z, lat, doy, tmax, tmin, rfcrp='S',
           srad=float('NaN'), sunhr=float('NaN'), rnet=float('NaN'),
           vapr=float('NaN'), tdew=float('NaN'), rhmax=float('NaN'),
           rhmin=float('NaN'), rhum=float('NaN'),
           wndsp=float('NaN'), wndht=2.0, csreq='S', kt=1.0)
        Compute daily standardized reference ET
    hourly (z, lat, lon, lzn, doy, sct, tmean, rfcrp='S',
            srad=float('NaN'), rnet=float('NaN'), vapr=float('NaN'),
            tdew=float('NaN'), rhum=float('NaN'), tmin=float('NaN'),
            wndsp=float('NaN'), wndht=2.0,
            tl=1.0, csreq='C', kt=1.0, fcdpt=0.65)
        Compute hourly standardized reference ET
    monthly (z, lat, doy, tmax, tmin, tpre, tnxt=float('NaN'),
             rfcrp='S', srad=float('NaN'), sunhr=float('NaN'),
             rnet=float('NaN'), vapr=float('NaN'), tdew=float('NaN'),
             rhmax=float('NaN'), rhmin=float('NaN'),
             rhum=float('NaN'), wndsp=float('NaN'), wndht=2.0,
             csreq='S', kt=1.0)
        Compute mean daily standardized reference ET for monthly periods
    """

    def __init__(self):
        """Initialize the RefET2 class attributes."""
        self.var = dict()

    def daily(self, z, lat, doy, tmax, tmin, rfcrp='S',
              srad=float('NaN'), sunhr=float('NaN'), rnet=float('NaN'),
              vapr=float('NaN'), tdew=float('NaN'), rhmax=float('NaN'),
              rhmin=float('NaN'), rhum=float('NaN'),
              wndsp=float('NaN'), wndht=2.0, csreq='S', kt=1.0):
        """Compute daily standardized reference evapotranspiration

        Parameters
        ----------
        z : float
            Weather site elevation above mean sea level (m)
        lat : float
            Latitude of the weather site (decimal degrees)
        doy : float
            Day number of the year between 1 and 366
        tmax : float
            Daily maximum air temperature (deg C)
        tmin : float
            Daily minimum air temperature (deg C)
        rfcrp : str, optional
            'S' for the short reference crop (0.12-m grass)(default='S')
            'T' for the tall reference crop (0.50-m alfalfa)
        srad : float, optional (but recommended)
            Solar (shortwave) radiation (MJ m^-2 d^-1) (default = NaN)
        sunhr : float, optional
            Daily duration of sunshine (h) (default = NaN)
        rnet : float, optional
            Daily net radiation (MJ m^-2 d^-1) (default = NaN)
        vapr : float, optional (but recommended)
            Daily mean vapor pressure (kPa) (default = NaN)
        tdew : float, optional (but recommended)
            Daily mean dew point temperature (deg C) (default = NaN)
        rhmax : float, optional
            Daily maximum relative humidity (%) (default = NaN)
        rhmin : float, optional
            Daily minimum relative humidity (%) (default = NaN)
        rhum : float, optional
            Daily mean relative humidity (%) (default = NaN)
        wndsp : float, optional  (but recommended)
            Daily mean wind speed (m s^-1) (default = NaN)
        wndht : float, optional (but recommended)
            Height of wind measurement above the ground surface (m)
            (default = 2.0)
        csreq : str, optional
            'S' for simple clear sky solar radiation method (Eq. 3.34)
            'C' for complex clear sky solar radation (Eqs. 3.35-3.39)
            (default = 'S')
        kt : float, optional
            Clearness coefficient for turbidity and haze (default = 1.0)

        Returns
        -------
        etsz  : float
            Daily standardized reference evapotranspiration for the
            short or tall reference crop (mm d^-1)
        """

        #Reset dictionary for storing variables
        self.var.clear()
        self.var.update({'z':z})
        self.var.update({'lat':lat})
        self.var.update({'doy':doy})
        self.var.update({'tmax':tmax})
        self.var.update({'tmin':tmin})
        self.var.update({'rfcrp':rfcrp})
        self.var.update({'srad':srad})
        self.var.update({'sunhr':sunhr})
        self.var.update({'rnet':rnet})
        self.var.update({'vapr':vapr})
        self.var.update({'tdew':tdew})
        self.var.update({'rhmax':rhmax})
        self.var.update({'rhmin':rhmin})
        self.var.update({'rhum':rhum})
        self.var.update({'wndsp':wndsp})
        self.var.update({'wndht':wndht})
        self.var.update({'csreq':csreq})
        self.var.update({'kt':kt})

        #patm (float) : Mean atmospheric pressure at weather site (kPa)
        #FAO-56 (2025) Eq. 3.1
        #ASCE (2005) Eq. 3
        patm = 101.3*((293.0-0.0065*z)/293.0)**5.26
        self.var.update({'patm':patm})

        #psycon (float) : Psychrometric constant (kPa (deg C)^-1)
        #FAO-56 (2025) Eq. 3.3
        #ASCE (2005) Eq. 4
        psycon = 0.000665*patm
        self.var.update({'psycon':psycon})

        #tavg (float) : Daily average air temperature (deg C)
        #FAO-56 (2025) Eq. 3.4
        #ASCE (2005) Eq. 2
        tavg = (tmax+tmin)/2.0
        self.var.update({'tavg':tavg})

        #Udelta (float) : Slope of the saturation vapor pressure
        #temperature curve (kPa (deg C)^-1)
        #FAO-56 (2025) Eq. 3.8
        #ASCE (2005) Eq. 5
        Udelta = 4098.0*(0.6108*math.exp(17.27*tavg/(tavg+237.3)))
        Udelta = Udelta/((tavg+237.3)**2.0)
        self.var.update({'Udelta':Udelta})

        #es (float) : Average saturation vapor pressure (kPa)
        #FAO-56 (2025) Eqs. 3.6 and 3.7
        #ASCE (2005) Eqs. 6 and 7
        emax = 0.6108*math.exp((17.27*tmax)/(tmax+237.3))
        emin = 0.6108*math.exp((17.27*tmin)/(tmin+237.3))
        es = (emax+emin)/2.0
        self.var.update({'emax':emax})
        self.var.update({'emin':emin})
        self.var.update({'es':es})

        #ea (float): Actual vapor pressure (kPa)
        #FAO-56 (2025) Box 3.1 provides example calculations
        #FAO-56 (2025) discusses preferred equations (page 74)
        #ASCE (2005) Table 3 provides preferred order for data sources
        if not math.isnan(vapr):
            #ASCE (2005) Table 3
            ea = vapr
        elif not math.isnan(tdew):
            #FAO-56 (2025) Eq. 3.9
            #ASCE (2005) Eq. 8
            ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
        elif not math.isnan(rhmax) and not math.isnan(rhmin):
            #FAO-56 (2025) Eq. 3.13
            #ASCE (2005) Eq. 11
            ea = (emin*rhmax/100. + emax*rhmin/100.)/2.0
        elif not math.isnan(rhmax):
            #FAO-56 (2025) Eq. 3.14
            #ASCE (2005) Eq. 12
            ea = emin*rhmax/100.
        elif not math.isnan(rhmin):
            #FAO-56 (2025) discourages this approach (page 74)
            #ASCE (2005) Eq. 13 with cautions related to RHmin integrity
            ea = emax*rhmin/100.
        elif not math.isnan(rhum):
            #FAO-56 (2025) Eq. 3.15
            #ASCE (2005) Eq. 14
            ea = rhum/100.*0.6108*math.exp((17.27*tavg)/(tavg+237.3))
        else:
            #FAO-56 (2025) Eq. 2.6
            #ASCE (2005) Appendix E
            tdew = tmin - 2.0
            ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
        self.var.update({'ea':ea})

        #vpd (float) : Vapor pressure deficit (kPa)
        #FAO-56 (2025) Box 3.1
        vpd = es-ea
        self.var.update({'vpd':vpd})

        #ra (float) : Extraterrestrial radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.18-3.22
        #ASCE (2005) Eqs. 21-27
        latrad = lat*math.pi/180.0 #Eq. 3.19
        dr = 1.0+0.033*math.cos(2.0*math.pi/365.0*doy) #Eq. 3.20
        ldelta = 0.409*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 3.21
        ws = math.acos(-1.0*math.tan(latrad)*math.tan(ldelta)) #Eq. 3.22
        ra1 = ws*math.sin(latrad)*math.sin(ldelta) #Eq. 3.18
        ra2 = math.cos(latrad)*math.cos(ldelta)*math.sin(ws) #Eq. 3.18
        ra = 24.0*60.0/math.pi*0.0820*dr*(ra1+ra2) #Eq. 3.18
        self.var.update({'latrad':latrad})
        self.var.update({'dr':dr})
        self.var.update({'ldelta':ldelta})
        self.var.update({'ws':ws})
        self.var.update({'ra':ra})

        #rs (float) : Shortwave radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.31-3.32
        #ASCE (2005) Appendix E
        N = float('NaN')
        if not math.isnan(srad):
            rs = srad
        elif not math.isnan(sunhr):
            N = 24.0/math.pi*ws #Eq. 3.31
            rs = (0.25+0.50*(sunhr/N))*ra #Eq. 3.32
        else:
            rs = float('NaN')
        self.var.update({'N':N})
        self.var.update({'rs':rs})

        #rso (float) : Clear sky solar radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.34-3.39
        #ASCE (2005) Eq. 19
        b1 = 0.3*latrad*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 3.39
        b2 = math.sin(0.85+b1-0.42*latrad*latrad) #Eq. 3.39
        beta24 = max([0.0001,math.asin(b2)]) #Eq. 3.39
        pwat = float('NaN')
        kb = float('NaN')
        kd = float('NaN')
        if csreq == 'S': #Simple Rso method
            rso = (0.75+2e-5*z)*ra #Eq. 3.34
        else: #Complex Rso method
            pwat = 0.14*ea*patm+2.1 #Eq. 3.37
            kt = sorted([0.0,kt,1.0])[1]
            kb1 = -0.00146*patm/(kt*math.sin(beta24))
            kb2 = 0.075*(pwat/math.sin(beta24))**0.4
            kb = 0.98*math.exp(kb1-kb2) #Eq. 3.36
            if kb >= 0.15:
                kd = 0.35-0.36*kb #Eq. 3.38a
            else:
                kd = 0.18+0.82*kb #Eq. 3.38b
            rso = (kb + kd)*ra #Eq. 3.35
        self.var.update({'beta24':beta24})
        self.var.update({'pwat':pwat})
        self.var.update({'kt':kt})
        self.var.update({'kb':kb})
        self.var.update({'kd':kd})
        self.var.update({'rso':rso})

        #rns (float) : Net shortwave radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.41
        #ASCE (2005) Eq. 16
        albedo = 0.23
        rns = (1.0-albedo)*rs
        self.var.update({'albedo':albedo})
        self.var.update({'rns':rns})

        #rnl (float) : Net longwave radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.42 limited to rs/rso<=1.0
        #FAO-56 (2025) page 77 also mentions 0.33<rs/rso<=1.0
        #ASCE (2005) Eqs. 17 and 18 limited to 0.3<rs/rso<=1.0, retained
        #The sources differ on conversion from C to K, 273.15 retained
        #The sources differ on Stefan-Boltzmann const, 4.903e-9 retained
        ratio = sorted([0.3,rs/rso,1.0])[1]
        fcd = sorted([0.05,1.35*ratio-0.35,1.0])[1] #ASCE (2005) Eq. 18
        tk4 = ((tmax+273.15)**4.0+(tmin+273.15)**4.0)/2.0
        rnl = 4.903e-9*tk4*(0.34-0.14*math.sqrt(ea))*fcd
        self.var.update({'ratio':ratio})
        self.var.update({'fcd':fcd})
        self.var.update({'rnl':rnl})

        #rn (float) : Net radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.43
        #ASCE (2005) Eq. 15
        rn = float('NaN')
        if (not math.isnan(rnet) and math.isnan(srad)
                                 and math.isnan(sunhr)):
            rn = rnet
        else:
            rn = rns-rnl #Eq. 3.43
        self.var.update({'rn':rn})

        #g (float) : Soil heat flux (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.45
        #ASCE (2005) Eq. 30
        g = 0.0
        self.var.update({'g':g})

        #u2 (float) : Wind profile relationship (m s^-1)
        #FAO-56 (2025) Eq. 3.50
        #ASCE (2005) Eq. 33 and Appendix E
        if math.isnan(wndsp): wndsp = 2.0
        u2 = wndsp * (4.87/math.log(67.8*wndht-5.42))
        self.var.update({'u2':u2})

        #Aerodynamic roughness and surface resistance constants
        #FAO-56 (2025) Eq. 2.4
        #ASCE (2005) Table 1
        if rfcrp == 'S': #Short reference crop (0.12-m grass)
            Cn = 900.0  #K mm s^3 Mg^-1 d^-1
            Cd = 0.34   #s m^-1
        elif rfcrp == 'T': #Tall reference crop (0.50-m alfalfa)
            Cn = 1600.0 #K mm s^3 Mg^-1 d^-1
            Cd = 0.38   #s m^-1

        #etsz (float) : Standardized daily reference ET (mm d^-1)
        #FAO-56 (2025) Eq. 2.4
        #ASCE (2005) Eq. 1
        etsz = 0.408*Udelta*(rn-g)+psycon*(Cn/(tavg+273.0))*u2*(es-ea)
        etsz = etsz/(Udelta+psycon*(1.0+Cd*u2))
        self.var.update({'etsz':etsz})

        return etsz

    def hourly(self, z, lat, lon, lzn, doy, sct, tmean, rfcrp='S',
               srad=float('NaN'), rnet=float('NaN'), vapr=float('NaN'),
               tdew=float('NaN'), rhum=float('NaN'), tmin=float('NaN'),
               wndsp=float('NaN'), wndht=2.0,
               tl=1.0, csreq='C', kt=1.0, fcdpt=0.65):
        """Compute hourly standardized reference evapotranspiration

        Parameters
        ----------
        z : float
            Weather site elevation above mean sea level (m)
        lat : float
            Latitude of the weather site (decimal degrees)
        lon : float
            Longitude of the weather site (decimal degrees)
        lzn : float
            Longitude of the center of the local time zone (decimal deg)
        doy : float
            Day number of the year between 1 and 366
        sct : float
            Standard clock time at the midpoint of the period (h)
            For the period between 1400-1500 hours, sct = 14.5 h
        tmean : float
            Mean air temperature (deg C)
        rfcrp : str
            'S' for the short reference crop (0.12-m grass)(default='S')
            'T' for the tall reference crop (0.50-m alfalfa)
        srad : float, optional
            Solar (shortwave) radiation (MJ m^-2 h^-1) (default = NaN)
        rnet : float, optional
            Net radiation (MJ m^-2 h^-1) (default = NaN)
        vapr : float, optional (but recommended)
            Mean vapor pressure (kPa) (default = NaN)
        tdew : float, optional (but recommended)
            Mean dew point temperature (deg C) (default = NaN)
        rhum : float, optional
            Mean relative humidity (%) (default = NaN)
        tmin : float, optional
            Daily minimum air temperature (deg C) (default = NaN)
        wndsp : float, optional  (but recommended)
            Mean wind speed (m s^-1) (default = NaN)
        wndht : float, optional (but recommended)
            Height of wind measurement above the ground (m)(default=2.0)
        tl : float, optional
            Length of the calculation period (h) (default = 1.0)
        csreq : str, optional
            'S' for simple clear sky solar radiation method (Eq. 3.34)
            'C' for complex clear sky solar radiation (Eq. 3.35-3.39)
        kt : float, optional
            Clearness coefficient for turbidity and haze (default = 1.0)
        fcdpt : float, optional
            Cloudiness value (fcd) from previous timestep (default=0.65)

        Returns
        -------
        etsz : float
            Hourly standardized reference evapotranspiration for the
            short or tall reference crop (mm h^-1)
        fcd : float
            Cloudiness value for possible use in next timestep
        """

        #Reset dictionary for storing variables.
        self.var.clear()
        self.var.update({'z':z})
        self.var.update({'lat':lat})
        self.var.update({'lon':lon})
        self.var.update({'lzn':lzn})
        self.var.update({'doy':doy})
        self.var.update({'sct':sct})
        self.var.update({'tmean':tmean})
        self.var.update({'rfcrp':rfcrp})
        self.var.update({'srad':srad})
        self.var.update({'rnet':rnet})
        self.var.update({'vapr':vapr})
        self.var.update({'tdew':tdew})
        self.var.update({'rhum':rhum})
        self.var.update({'tmin':tmin})
        self.var.update({'wndsp':wndsp})
        self.var.update({'wndht':wndht})
        self.var.update({'tl':tl})
        self.var.update({'csreq':csreq})
        self.var.update({'kt':kt})
        self.var.update({'fcdpt':fcdpt})

        #patm (float) : Mean atmospheric pressure at weather site (kPa)
        #FAO-56 (2025) Eq. 3.1
        #ASCE (2005) Eq. 34
        patm = 101.3*((293.0-0.0065*z)/293.0)**5.26
        self.var.update({'patm':patm})

        #psycon (float) : Psychrometric constant (kPa (deg C)^-1)
        #FAO-56 (2025) Eq. 3.3
        #ASCE (2005) Eq. 35
        psycon = 0.000665*patm
        self.var.update({'psycon':psycon})

        #Udelta (float) : Slope of the saturation vapor pressure
        #temperature curve (kPa (deg C)^-1)
        #FAO-56 (2025) Eq. 3.8
        #ASCE (2005) Eq. 36
        Udelta = 4098.0*(0.6108*math.exp(17.27*tmean/(tmean+237.3)))
        Udelta = Udelta/((tmean+237.3)**2.0)
        self.var.update({'Udelta':Udelta})

        #es (float) : Saturation vapor pressure (kPa)
        #FAO-56 (2025) Eq. 3.6
        #ASCE (2005) Eq. 37
        es = 0.6108*math.exp((17.27*tmean)/(tmean+237.3))
        self.var.update({'es':es})

        #ea (float): Actual vapor pressure (kPa)
        #FAO-56 (2025) Box 3.1 provides example calculations
        #FAO-56 (2025) discusses preferred equations (page 74)
        #ASCE (2005) Table 4 provides preferred order for data sources
        if not math.isnan(vapr):
            #ASCE (2005) Table 4
            ea = vapr
        elif not math.isnan(tdew):
            #FAO-56 (2025) Eq. 3.9
            #ASCE (2005) Eq. 38
            ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
        elif not math.isnan(rhum):
            #FAO-56 (2025) Eq. 3.15
            #ASCE (2005) Eq. 41
            ea = es*rhum/100.
        else:
            #FAO-56 (2025) Eq. 2.6
            #ASCE (2005) Appendix E
            tdew = tmin - 2.0
            ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
        self.var.update({'ea':ea})

        #vpd (float) : Vapor pressure deficit (kPa)
        #FAO-56 (2025) Box 3.1
        vpd = es-ea
        self.var.update({'vpd':vpd})

        #ra (float) : Extraterrestrial radiation (MJ m^-2 h^-1)
        #FAO-56 (2025) Eqs. 3.19-3.21 and 3.25-3.30
        #ASCE (2005) Eqs. 48-58
        latrad = lat*math.pi/180.0 #Eq. 3.19
        dr = 1.0+0.033*math.cos(2.0*math.pi/365.0*doy) #Eq. 3.20
        ldelta = 0.409*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 3.21
        b = 2.0*math.pi*(doy-81.0)/364.0 #Eq. 3.30
        sc = 0.1645*math.sin(2.0*b)
        sc = sc - 0.1255*math.cos(b) - 0.025*math.sin(b) #Eq. 3.29
        wmid = math.pi/12.0*((sct+0.06667*(lzn-lon)+sc)-12.0) #Eq. 3.28
        w1 = wmid-math.pi*tl/24.0 #Eq. 3.26
        w2 = wmid+math.pi*tl/24.0 #Eq. 3.27
        ws = math.acos(-1.0*math.tan(latrad)*math.tan(ldelta)) #Eq. 3.22
        if w1 < -1.0*ws: w1 = -1.0*ws #ASCE (2005) Eq. 56
        if w2 < -1.0*ws: w2 = -1.0*ws #ASCE (2005) Eq. 56
        if w1 > ws: w1 = ws #ASCE (2005) Eq. 56
        if w2 > ws: w2 = ws #ASCE (2005) Eq. 56
        if w1 > w2: w1 = w2 #ASCE (2005) Eq. 56
        ra1 = (w2-w1)*math.sin(latrad)*math.sin(ldelta) #Eq. 3.25
        ra2 = math.cos(latrad)*math.cos(ldelta) #Eq. 3.25
        ra3 = math.sin(w2)-math.sin(w1) #Eq. 3.25
        if wmid < -1.0*ws or wmid > ws:  #nightime, FAO-56 (2025) p. 84
            ra = 0.0
        else:
            ra = 12.0*60.0/math.pi*0.0820*dr*(ra1+ra2*ra3) #Eq. 3.25
        self.var.update({'latrad':latrad})
        self.var.update({'dr':dr})
        self.var.update({'ldelta':ldelta})
        self.var.update({'b':b})
        self.var.update({'sc':sc})
        self.var.update({'wmid':wmid})
        self.var.update({'w1':w1})
        self.var.update({'w2':w2})
        self.var.update({'ws':ws})
        self.var.update({'ra':ra})

        #rs (float) : Shortwave radiation (MJ m^-2 h^-1)
        if not math.isnan(srad):
            rs = srad
        else:
            rs = float('NaN')
        self.var.update({'rs':rs})

        #rso (float) : Clear sky solar radiation (MJ m^-2 h^-1)
        #FAO-56 (2025) Eq. 3.34-3.40
        #ASCE (2005) Eq. 46, 47 and Appendix D
        beta1 = math.sin(latrad)*math.sin(ldelta) #Eq. 3.40
        beta2 = math.cos(latrad)*math.cos(ldelta)*math.cos(wmid) #Eq. 3.40
        beta = math.asin(beta1+beta2) #Eq. 3.40
        pwat = float('NaN')
        kb = float('NaN')
        kd = float('NaN')
        if wmid < -1.0*ws or wmid > ws: #nightime, ASCE (2005) p. 41
            rso = 0.0
        elif csreq == 'S': #Simple Rso method
            rso = (0.75+2e-5*z)*ra #Eq. 3.34
        else: #Complex Rso method
            pwat = 0.14*ea*patm+2.1 #Eq. 3.37
            kt = sorted([0.0,kt,1.0])[1]
            kb1 = -0.00146*patm/(kt*math.sin(beta))
            kb2 = 0.075*(pwat/math.sin(beta))**0.4
            kb = 0.98*math.exp(kb1-kb2) #Eq. 3.36
            if kb >= 0.15:
                kd = 0.35-0.36*kb #Eq. 3.38a
            else:
                kd = 0.18+0.82*kb #Eq. 3.38b
            rso = (kb + kd)*ra #Eq. 3.35
        self.var.update({'beta':beta})
        self.var.update({'pwat':pwat})
        self.var.update({'kb':kb})
        self.var.update({'kd':kd})
        self.var.update({'rso':rso})

        #rns (float) : Net shortwave radiation (MJ m^-2 h^-1)
        #FAO-56 (2025) Eq. 3.41
        #ASCE (2005) Eq. 43
        albedo = 0.23
        rns = (1.0-albedo)*rs
        self.var.update({'albedo':albedo})
        self.var.update({'rns':rns})

        #rnl (float) : Net longwave radiation (MJ m^-2 h^-1)
        #FAO-56 (2025) Eq. 3.42
        #ASCE (2005) Eqs. 44-46 and 62
        #FAO-56 (2025) Eq. 3.42 limited to rs/rso<=1.0
        #FAO-56 (2025) page 77 also mentions 0.33<rs/rso<=1.0
        #ASCE (2005) Eqs. 44 and 45 limited to 0.3<rs/rso<=1.0, retained
        #The sources differ on conversion from C to K, 273.15 retained
        #The sources differ on Stefan-Boltzmann const, 2.043e-10 retained
        #Stephan-Boltzmann constant taken from FAO-56 (2025) p.122
        ratio = float('NaN')
        fcd = float('NaN')
        if beta < 0.3 or rso <= 0.0: #nighttime, ASCE (2005) Eq. 46
            fcd = fcdpt
        else: #daytime
            ratio = sorted([0.3,rs/rso,1.0])[1] #ASCE (2005) Eq. 45
            fcd = sorted([0.05,1.35*ratio-0.35,1.0])[1]
        tk4 = (tmean+273.15)**4.0 #Eq. 3.42
        rnl = 2.043e-10*tk4*(0.34-0.14*math.sqrt(ea))*fcd #Eq. 3.42
        self.var.update({'ratio':ratio})
        self.var.update({'fcd':fcd})
        self.var.update({'rnl':rnl})

        #rn (float) : Net radiation (MJ m^-2 h^-1)
        #FAO-56 (2025) Eq. 3.43
        #ASCE (2005) Eq. 42
        rn = float('NaN')
        if not math.isnan(rnet) and math.isnan(srad):
            rn = rnet
        else:
            rn = rns-rnl #Eq. 3.43
        self.var.update({'rn':rn})

        #g (float) : Soil heat flux (MJ m^-2 h^-1)
        #FAO-56 (2025) Eq. 3.48 and 3.49
        #Aerodynamic roughness and surface resistance constants
        #ASCE (2005) Table 1
        if rfcrp == 'S': #Short reference crop (0.12-m grass)
            Cn = 37.0 #K mm s^3 Mg^-1 h^-1
            if rn < 0.0: #nighttime
                g = 0.5*rn
                Cd = 0.96 #!s m^-1
            else: #daytime
                g = 0.1*rn
                Cd = 0.24 #!s m^-1
        elif rfcrp == 'T': #Tall reference crop (0.50-m alfalfa)
            Cn = 66.0 #K mm s^3 Mg^-1 h^-1
            if rn < 0.0: #nighttime
                g = 0.2*rn #ASCE (2005) Eq. 66b
                Cd = 1.7 #!s m^-1
            else: #daytime
                g = 0.04*rn #ASCE (2005) Eq. 66a
                Cd = 0.25 #!s m^-1
        self.var.update({'g':g})

        #u2 (float) : Wind profile relationship (m s^-1)
        #FAO-56 (2025) Eq. 3.50
        #ASCE (2005) Eq. 67 and Appendix E
        if math.isnan(wndsp): wndsp = 2.0
        u2 = wndsp * (4.87/math.log(67.8*wndht-5.42))
        self.var.update({'u2':u2})

        #etsz (float) : Standardized hourly reference ET (mm h^-1)
        #FAO-56 (2025) Eq. 2.5a and 2.56b
        #ASCE (2005) Eq. 1
        etsz = 0.408*Udelta*(rn-g)+psycon*(Cn/(tmean+273.0))*u2*(es-ea)
        etsz = etsz/(Udelta+psycon*(1.0+Cd*u2))
        self.var.update({'etsz':etsz})

        return (etsz, fcd)

    def monthly(self, z, lat, doy, tmax, tmin, tpre, tnxt=float('NaN'),
                rfcrp='S', srad=float('NaN'), sunhr=float('NaN'),
                rnet=float('NaN'), vapr=float('NaN'), tdew=float('NaN'),
                rhmax=float('NaN'), rhmin=float('NaN'),
                rhum=float('NaN'), wndsp=float('NaN'), wndht=2.0,
                csreq='S', kt=1.0):
        """Compute mean daily standardized reference evapotranspiration
           using data for monthly periods

        Parameters
        ----------
        z : float
            Weather site elevation above mean sea level (m)
        lat : float
            Latitude of the weather site (decimal degrees)
        doy : float
            Day number of the year for the 15th day of the month
        tmax : float
            Mean daily maximum air temperature for the month (deg C)
        tmin : float
            Mean daily minimum air temperature for the month (deg C)
        tpre : float
            Mean daily average temperature for previous month (deg C)
        tnxt : float, optional
            Mean daily average temperature for next month (deg C)
            (default = NaN)
        rfcrp : str, optional
            'S' for the short reference crop (0.12-m grass)(default='S')
            'T' for the tall reference crop (0.50-m alfalfa)
        srad : float, optional (but recommended)
            Mean daily solar (shortwave) radiation for the month
            (MJ m^-2 d^-1) (default = NaN)
        sunhr : float, optional
            Mean daily duration of sunshine for the month (h)
            (default = NaN)
        rnet : float, optional
            Mean daily net radiation for the month (MJ m^-2 d^-1)
            (default = NaN)
        vapr : float, optional (but recommended)
            Mean daily vapor pressure for the month (kPa)
            (default = NaN)
        tdew : float, optional (but recommended)
            Mean daily average dew point temperature for the month
            (deg C) (default = NaN)
        rhmax : float, optional
            Mean daily maximum relative humidity for the month (%)
            (default = NaN)
        rhmin : float, optional
            Mean daily minimum relative humidity for the month (%)
            (default = NaN)
        rhum : float, optional
            Mean daily relative humidity for the month (%)
            (default = NaN)
        wndsp : float, optional  (but recommended)
            Mean daily average wind speed for the month (m s^-1)
            (default = NaN)
        wndht : float, optional (but recommended)
            Height of wind measurement above the ground surface (m)
            (default = 2.0)
        csreq : str, optional
            'S' for simple clear sky solar radiation method (Eq. 3.34)
            'C' for complex clear sky solar radation (Eqs. 3.35-3.39)
            (default = 'S')
        kt : float, optional
            Clearness coefficient for turbidity and haze (default = 1.0)

        Returns
        -------
        etsz  : float
            Mean daily standardized reference evapotranspiration for the
            short or tall reference crop over the month (mm d^-1)
        """

        #Reset dictionary for storing variables.
        self.var.clear()
        self.var.update({'z':z})
        self.var.update({'lat':lat})
        self.var.update({'doy':doy})
        self.var.update({'tmax':tmax})
        self.var.update({'tmin':tmin})
        self.var.update({'tpre':tpre})
        self.var.update({'tnxt':tnxt})
        self.var.update({'rfcrp':rfcrp})
        self.var.update({'srad':srad})
        self.var.update({'sunhr':sunhr})
        self.var.update({'rnet':rnet})
        self.var.update({'vapr':vapr})
        self.var.update({'tdew':tdew})
        self.var.update({'rhmax':rhmax})
        self.var.update({'rhmin':rhmin})
        self.var.update({'rhum':rhum})
        self.var.update({'wndsp':wndsp})
        self.var.update({'wndht':wndht})
        self.var.update({'csreq':csreq})
        self.var.update({'kt':kt})

        #patm (float) : Mean atmospheric pressure at weather site (kPa)
        #FAO-56 (2025) Eq. 3.1
        #ASCE (2005) Eq. 3
        patm = 101.3*((293.0-0.0065*z)/293.0)**5.26
        self.var.update({'patm':patm})

        #psycon (float) : Psychrometric constant (kPa (deg C)^-1)
        #FAO-56 (2025) Eq. 3.3
        #ASCE (2005) Eq. 4
        psycon = 0.000665*patm
        self.var.update({'psycon':psycon})

        #tavg (float) : Mean daily air temperature (deg C)
        #FAO-56 (2025) Eq. 3.4
        #ASCE (2005) Eq. 2
        tavg = (tmax+tmin)/2.0
        self.var.update({'tavg':tavg})

        #Udelta (float) : Slope of the saturation vapor pressure
        #temperature curve (kPa (deg C)^-1)
        #FAO-56 (2025) Eq. 3.8
        #ASCE (2005) Eq. 5
        Udelta = 4098.0*(0.6108*math.exp(17.27*tavg/(tavg+237.3)))
        Udelta = Udelta/((tavg+237.3)**2.0)
        self.var.update({'Udelta':Udelta})

        #es (float) : Average saturation vapor pressure (kPa)
        #FAO-56 (2025) Eqs. 3.6 and 3.7
        #ASCE (2005) Eqs. 6 and 7
        emax = 0.6108*math.exp((17.27*tmax)/(tmax+237.3))
        emin = 0.6108*math.exp((17.27*tmin)/(tmin+237.3))
        es = (emax+emin)/2.0
        self.var.update({'emax':emax})
        self.var.update({'emin':emin})
        self.var.update({'es':es})

        #ea (float): Actual vapor pressure (kPa)
        #FAO-56 (2025) Box 3.1 provides example calculations
        #FAO-56 (2025) discusses preferred equations (page 74)
        #ASCE (2005) Table 3 provides preferred order for data sources
        if not math.isnan(vapr):
            #ASCE (2005) Table 3
            ea = vapr
        elif not math.isnan(tdew):
            #FAO-56 (2025) Eq. 3.9
            #ASCE (2005) Eq. 8
            ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
        elif not math.isnan(rhmax) and not math.isnan(rhmin):
            #FAO-56 (2025) Eq. 3.13
            #ASCE (2005) Eq. 11
            ea = (emin*rhmax/100. + emax*rhmin/100.)/2.0
        elif not math.isnan(rhmax):
            #FAO-56 (2025) Eq. 3.14
            #ASCE (2005) Eq. 12
            ea = emin*rhmax/100.
        elif not math.isnan(rhmin):
            #FAO-56 (2025) discourages this approach (page 74)
            #ASCE (2005) Eq. 13 with cautions related to RHmin integrity
            ea = emax*rhmin/100.
        elif not math.isnan(rhum):
            #FAO-56 (2025) Eq. 3.15
            #ASCE (2005) Eq. 14
            ea = rhum/100.*0.6108*math.exp((17.27*tavg)/(tavg+237.3))
        else:
            #FAO-56 (2025) Eq. 2.6
            #ASCE (2005) Appendix E
            tdew = tmin - 2.0
            ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
        self.var.update({'ea':ea})

        #vpd (float) : Vapor pressure deficit (kPa)
        #FAO-56 (2025) Box 3.1
        vpd = es-ea
        self.var.update({'vpd':vpd})

        #ra (float) : Extraterrestrial radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.18-3.22
        #ASCE (2005) Eqs. 21-27
        latrad = lat*math.pi/180.0 #Eq. 3.19
        dr = 1.0+0.033*math.cos(2.0*math.pi/365.0*doy) #Eq. 3.20
        ldelta = 0.409*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 3.21
        ws = math.acos(-1.0*math.tan(latrad)*math.tan(ldelta)) #Eq. 3.22
        ra1 = ws*math.sin(latrad)*math.sin(ldelta) #Eq. 3.18
        ra2 = math.cos(latrad)*math.cos(ldelta)*math.sin(ws) #Eq. 3.18
        ra = 24.0*60.0/math.pi*0.0820*dr*(ra1+ra2) #Eq. 3.18
        self.var.update({'latrad':latrad})
        self.var.update({'dr':dr})
        self.var.update({'ldelta':ldelta})
        self.var.update({'ra':ra})

        #rs (float) : Shortwave radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.31-3.32
        #ASCE (2005) Appendix E
        N = float('NaN')
        if not math.isnan(srad):
            rs = srad
        elif not math.isnan(sunhr):
            N = 24.0/math.pi*ws #Eq. 3.31
            rs = (0.25+0.50*(sunhr/N))*ra #Eq. 3.32
        else:
            rs = float('NaN')
        self.var.update({'N':N})
        self.var.update({'rs':rs})

        #rso (float) : Clear sky solar radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.34-3.39
        #ASCE (2005) Eq. 19
        b1 = 0.3*latrad*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 3.39
        b2 = math.sin(0.85+b1-0.42*latrad*latrad) #Eq. 3.39
        beta24 = max([0.0001,math.asin(b2)]) #Eq. 3.39
        pwat = float('NaN')
        kb = float('NaN')
        kd = float('NaN')
        if csreq == 'S': #Simple Rso method
            rso = (0.75+2e-5*z)*ra #Eq. 3.34
        else: #Complex Rso method
            pwat = 0.14*ea*patm+2.1 #Eq. 3.37
            kt = sorted([0.0,kt,1.0])[1]
            kb1 = -0.00146*patm/(kt*math.sin(beta24))
            kb2 = 0.075*(pwat/math.sin(beta24))**0.4
            kb = 0.98*math.exp(kb1-kb2) #Eq. 3.36
            if kb >= 0.15:
                kd = 0.35-0.36*kb #Eq. 3.38a
            else:
                kd = 0.18+0.82*kb #Eq. 3.38b
            rso = (kb + kd)*ra #Eq. 3.35
        self.var.update({'beta24':beta24})
        self.var.update({'pwat':pwat})
        self.var.update({'kt':kt})
        self.var.update({'kb':kb})
        self.var.update({'kd':kd})
        self.var.update({'rso':rso})

        #rns (float) : Net shortwave radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.41
        #ASCE (2005) Eq. 16
        albedo = 0.23
        rns = (1.0-albedo)*rs
        self.var.update({'albedo':albedo})
        self.var.update({'rns':rns})

        #rnl (float) : Net longwave radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.42 limited to rs/rso<=1.0
        #FAO-56 (2025) page 77 also mentions 0.33<rs/rso<=1.0
        #ASCE (2005) Eqs. 17 and 18 limited to 0.3<rs/rso<=1.0, retained
        #The sources differ on conversion from C to K, 273.15 retained
        #The sources differ on Stefan-Boltzmann const, 4.903e-9 retained
        ratio = sorted([0.3,rs/rso,1.0])[1]
        fcd = sorted([0.05,1.35*ratio-0.35,1.0])[1] #ASCE (2005) Eq. 18
        tk4 = ((tmax+273.15)**4.0+(tmin+273.15)**4.0)/2.0
        rnl = 4.903e-9*tk4*(0.34-0.14*math.sqrt(ea))*fcd
        self.var.update({'ratio':ratio})
        self.var.update({'fcd':fcd})
        self.var.update({'rnl':rnl})

        #rn (float) : Net radiation (MJ m^-2 d^-1)
        #FAO-56 (2025) Eq. 3.43
        #ASCE (2005) Eq. 15
        rn = float('NaN')
        if (not math.isnan(rnet) and math.isnan(srad)
                                 and math.isnan(sunhr)):
            rn = rnet
        else:
            rn = rns-rnl #Eq. 3.43
        self.var.update({'rn':rn})

        #g (float) : Soil heat flux (MJ m^-2 d^-1)
        #FAO-56 (2025) Eqs. 3.46 and 3.47
        #ASCE (2005) Eqs. 31 and 32
        if not math.isnan(tnxt):
            g = 0.7*(tnxt-tpre)
        else:
            g = 0.14*(tavg-tpre)
        self.var.update({'g':g})

        #u2 (float) : Wind profile relationship (m s^-1)
        #FAO-56 (2025) Eq. 3.50
        #ASCE (2005) Eq. 33 and Appendix E
        if math.isnan(wndsp): wndsp = 2.0
        u2 = wndsp * (4.87/math.log(67.8*wndht-5.42))
        self.var.update({'u2':u2})

        #Aerodynamic roughness and surface resistance constants
        #FAO-56 (2025) Eq. 2.4
        #ASCE (2005) Table 1
        if rfcrp == 'S': #Short reference crop (0.12-m grass)
            Cn = 900.0  #K mm s^3 Mg^-1 d^-1
            Cd = 0.34   #s m^-1
        elif rfcrp == 'T': #Tall reference crop (0.50-m alfalfa)
            Cn = 1600.0 #K mm s^3 Mg^-1 d^-1
            Cd = 0.38   #s m^-1

        #etsz (float) : Mean daily standardized reference ET (mm d^-1)
        #FAO-56 (2025) Eq. 2.4
        #ASCE (2005) Eq. 1
        etsz = 0.408*Udelta*(rn-g)+psycon*(Cn/(tavg+273.0))*u2*(es-ea)
        etsz = etsz/(Udelta+psycon*(1.0+Cd*u2))
        self.var.update({'etsz':etsz})

        return etsz
