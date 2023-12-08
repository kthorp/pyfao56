"""
########################################################################
The refet.py module contains functions for computing short-crop or
tall-crop reference evapotranspiration following the ASCE Standardized
Reference Evapotranspiration Equation.

The ASCE Standarized Reference Evapotranspiration Equation is
documented in the following publications:
https://ascelibrary.org/doi/book/10.1061/9780784408056

ASCE Task Committee on Standardization of Reference Evapotranspiration 
(Walter, I. A., Allen, R. G., Elliott, R., Itenfisu, D., Brown, P., 
Jensen, M. E.,Mecham, B., Howell, T. A., Snyder, R., Eching, S., 
Spofford, T., Hattendorf, M., Martin, D., Cuenca, R. H., Wright, J. L.)
, 2005. The ASCE Standardized Reference Evapotranspiration Equation.
American Society of Civil Engineers, Reston, VA.

The refet.py module contains the following:
    ascedaily - function to compute daily ASCE Standardized Reference ET
    ascehourly - function to compute hourly ASCE Std. Reference ET

01/07/2016 Initial Python script by Kelly Thorp
11/04/2021 Finalized updates for inclusion in pyfao56 Python package
08/01/2022 Added the ASCE hourly reference ET algorithm
08/03/2022 Added functionality to input vapor pressure
########################################################################
"""

import math

def ascedaily(rfcrp,z,lat,doy,israd,tmax,tmin,
              vapr=float('NaN'),tdew=float('NaN'),
              rhmax=float('NaN'),rhmin=float('NaN'),
              wndsp=float('NaN'),wndht=2.0):
    """Compute daily ASCE Standardized Reference Evapotranspiration

    Parameters
    ----------
    rfcrp : str
        'S' for the short reference crop (0.12-m grass)
        'T' for the tall reference crop (0.50-m alfalfa)
    z : float
        Weather site elevation above mean sea level (m)
    lat : float
        Latitude of the weather site (decimal degrees)
    doy : float
        Day number of the year between 1 and 366
    israd : float
        Incoming solar radiation (MJ m^-2 d^-1)
    tmax : float
        Daily maximum air temperature (deg C)
    tmin : float
        Daily minimum air temperature (deg C)
    vapr : float, optional (but recommended)
        Daily average vapor pressure (kPa) (default = NaN)
    tdew : float, optional (but recommended)
        Daily average dew point temperature (deg C) (default = NaN)
    rhmax : float, optional
        Daily maximum relative humidity (%) (default = NaN)
    rhmin : float, optional
        Daily minimum relative humidity (%) (default = NaN)
    wndsp : float, optional  (but recommended)
        Daily average wind speed (m s^-1) (default = NaN)
    wndht : float, optional (but recommended)
        Height of wind measurement above the ground (m) (default = 2.0)

    Returns
    -------
    etsz  : float
        Daily standardized reference evapotranspiration for the
        short or tall reference crop (mm)
    """

    #tavg (float) : Mean daily air temperature (deg C)
    #ASCE (2005) Eq. 2
    tavg = (tmax+tmin)/2.0

    #patm (float) : Mean atmospheric pressure at weather station (kPa)
    #ASCE (2005) Eq. 3
    patm = 101.3*((293.0-0.0065*z)/293.0)**5.26

    #psycon (float) : Psychrometric constant (kPa (deg C)^-1)
    #ASCE (2005) Eq. 4
    psycon = 0.000665*patm

    #Udelta (float) : Slope of the saturation vapor pressure
    #temperature curve (kPa (deg C)^-1)
    #ASCE (2005) Eq. 5
    Udelta = 2503.0*math.exp(17.27*tavg/(tavg+237.3))
    Udelta = Udelta/((tavg+237.3)**2.0)

    #es (float) : Saturation vapor pressure (kPa)
    #ASCE (2005) Eqs. 6 and 7
    emax = 0.6108*math.exp((17.27*tmax)/(tmax+237.3))
    emin = 0.6108*math.exp((17.27*tmin)/(tmin+237.3))
    es = (emax+emin)/2.0

    #ea (float): Actual vapor pressure (kPa) ASCE (2005) Table 3
    if not math.isnan(vapr):
        #ASCE (2005) Table 3
        ea = vapr
    elif not math.isnan(tdew):
        #ASCE (2005) Eq. 8
        ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
    elif not math.isnan(rhmax) and not math.isnan(rhmin):
        #ASCE (2005) Eq. 11
        ea = (emin*rhmax/100. + emax*rhmin/100.)/2.0
    elif not math.isnan(rhmax):
        #ASCE (2005) Eq. 12
        ea = emin*rhmax/100.
    elif not math.isnan(rhmin):
        #ASCE (2005) Eq. 13
        ea = emax*rhmin/100.
    else:
        #ASCE (2005) Appendix E
        tdew = tmin - 2.0
        ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))

    #rns (float) : Net shortwave radiation (MJ m^-2 d^-1)
    #ASCE (2005) Eq. 16
    albedo = 0.23
    rns = (1.0-albedo)*israd

    #ra (float) : Extraterrestrial radiation (MJ m^-2 d^-1)
    #ASCE (2005) Eqs. 21-27
    latrad = lat*math.pi/180.0 #Eq. 22
    dr = 1.0+0.033*math.cos(2.0*math.pi/365.0*doy) #Eq. 23
    ldelta = 0.409*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 24
    ws = math.acos(-1.0*math.tan(latrad)*math.tan(ldelta)) #Eq. 27
    ra1 = ws*math.sin(latrad)*math.sin(ldelta) #Eq. 21
    ra2 = math.cos(latrad)*math.cos(ldelta)*math.sin(ws) #Eq. 21
    ra = 24.0/math.pi*4.92*dr*(ra1+ra2) #Eq. 21

    #rso (float) : Clear sky solar radiation (MJ m^-2 d^-1)
    #ASCE (2005) Eq. 19
    rso = (0.75+2e-5*z)*ra

    #rnl (float) : Net longwave radiation (MJ m^-2 d^-1)
    #ASCE (2005) Eqs. 17 and 18
    ratio = sorted([0.3,israd/rso,1.0])[1]
    fcd = sorted([0.05,1.35*ratio-0.35,1.0])[1] #Eq. 18
    tk4 = ((tmax+273.16)**4.0+(tmin+273.16)**4.0)/2.0 #Eq. 17
    rnl = 4.901e-9*fcd*(0.34-0.14*math.sqrt(ea))*tk4 #Eq. 17

    #rn (float) : Net radiation (MJ m^-2 d^-1)
    #ASCE (2005) Eq. 15
    rn = rns-rnl

    #g (float) : Soil heat flux (MJ m^-2 d^-1)
    #ASCE (2005) Eq. 30
    g = 0.0

    #u2 (float) : Wind profile relationship (m s^-1)
    #ASCE (2005) Eq. 33 and Appendix E
    if math.isnan(wndsp): wndsp = 2.0
    u2 = wndsp * (4.87/math.log(67.8*wndht-5.42))

    #Aerodynamic roughness and surface resistance constants
    #ASCE (2005) Table 1
    if rfcrp == 'S': #Short reference crop (0.12-m grass)
        Cn = 900.0  #K mm s^3 Mg^-1 d^-1
        Cd = 0.34   #s m^-1
    elif rfcrp == 'T': #Tall reference crop (0.50-m alfalfa)
        Cn = 1600.0 #K mm s^3 Mg^-1 d^-1
        Cd = 0.38   #s m^-1

    #etsz (float) : Standardized daily reference crop ET (mm d^-1)
    #ASCE (2005) Eq. 1
    etsz = 0.408*Udelta*(rn-g)+psycon*(Cn/(tavg+273.0))*u2*(es-ea)
    etsz = etsz/(Udelta+psycon*(1.0+Cd*u2))

    return etsz

def ascehourly(rfcrp,z,lat,lon,lzn,doy,sct,israd,tavg,vapr=float('NaN'),
               tdew=float('NaN'),rhum=float('NaN'),tmin=float('NaN'),               wndsp=float('NaN'),wndht=2.0,tl=1.0,csreq='D',fcdpt=1.0):
    """Compute hourly ASCE Standardized Reference Evapotranspiration

    Parameters
    ----------
    rfcrp : str
        'S' for the short reference crop (0.12-m grass)
        'T' for the tall reference crop (0.50-m alfalfa)
    z : float
        Weather site elevation above mean sea level (m)
    lat : float
        Latitude of the weather site (decimal degrees)
    lon : float
        Longitude of the weather site (decimal degrees)
    lzn : float
        Longitude of the center of the local time zone (decimal degrees)
    doy : float
        Day number of the year between 1 and 366
    sct : float
        Standard clock time at the midpoint of the period (h)
        For the period between 1400-1500 hours, sct = 14.5 h
    israd : float
        Incoming solar radiation (MJ m^-2 d^-1)
    tavg : float
        Average air temperature (deg C)
    vapr : float, optional (but recommended)
        Average vapor pressure (kPa) (default = NaN)
    tdew : float, optional (but recommended)
        Average dew point temperature (deg C) (default = NaN)
    rhum : float, optional
        Average relative humidity (%) (default = NaN)
    tmin : float, optional
        Daily minimum air temperature (deg C) (default = NaN)
    wndsp : float, optional  (but recommended)
        Average wind speed (m s^-1) (default = NaN)
    wndht : float, optional (but recommended)
        Height of wind measurement above the ground (m) (default = 2.0)
    tl : float, optional
        Length of the calculation period (h) (default = 1.0)
    csreq : str, optional
        'S' for the simple Eq. 47 for clear sky solar radiation
        'D' for the complex method in Appendix D (default = 'D')
    fcdpt : float, optional
        Cloudiness value (fcd) from previous timestep (default = 1.0)

    Returns
    -------
    etsz : float
        Hourly standardized reference evapotranspiration for the
        short or tall reference crop (mm)
    fcd : Cloudiness value for possible use in next timestep
    """

    #patm (float) : Mean atmospheric pressure at weather station (kPa)
    #ASCE (2005) Eq. 34
    patm = 101.3*((293.0-0.0065*z)/293.0)**5.26

    #psycon (float) : Psychrometric constant (kPa (deg C)^-1)
    #ASCE (2005) Eq. 35
    psycon = 0.000665*patm

    #Udelta (float) : Slope of the saturation vapor pressure
    #temperature curve (kPa (deg C)^-1)
    #ASCE (2005) Eq. 36
    Udelta = 2503.0*math.exp(17.27*tavg/(tavg+237.3))
    Udelta = Udelta/((tavg+237.3)**2.0)

    #es (float) : Saturation vapor pressure (kPa)
    #ASCE (2005) Eq. 37
    es = 0.6108*math.exp((17.27*tavg)/(tavg+237.3))

    #ea (float): Actual vapor pressure (kPa) ASCE (2005) Table 4
    if not math.isnan(vapr):
        #ASCE (2005) Table 4
        ea = vapr
    elif not math.isnan(tdew):
        #ASCE (2005) Eq. 38
        ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))
    elif not math.isnan(rhum):
        #ASCE (2005) Eq. 41
        ea = es*rhum/100.
    else:
        #ASCE (2005) Appendix E
        tdew = tmin - 2.0
        ea = 0.6108*math.exp((17.27*tdew)/(tdew+237.3))

    #rns (float) : Net shortwave radiation (MJ m^-2 h^-1)
    #ASCE (2005) Eq. 43
    albedo = 0.23
    rns = (1.0-albedo)*israd

    #ra (float) : Extraterrestrial radiation (MJ m^-2 h^-1)
    #ASCE (2005) Eqs. 48-58
    dr = 1.0+0.033*math.cos(2.0*math.pi/365.0*doy) #Eq. 50
    ldelta = 0.409*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq. 51
    b = 2.0*math.pi*(doy-81.0)/364.0 #Eq. 58
    sc = 0.1645*math.sin(2.0*b)-0.1255*math.cos(b)-0.025*math.sin(b) #57
    wmid = math.pi/12.0*((sct+0.06667*(lzn-lon)+sc)-12.) #Eq. 55
    w1 = wmid-math.pi*tl/24.0 #Eq. 53
    w2 = wmid+math.pi*tl/24.0 #Eq. 54
    latrad = lat*math.pi/180.0 #Eq. 49
    ws = math.acos(-1.0*math.tan(latrad)*math.tan(ldelta)) #Eq. 59
    if w1 < -1.0*ws: w1 = -1.0*ws #Eq. 56
    if w2 < -1.0*ws: w2 = -1.0*ws #Eq. 56
    if w1 > ws: w1 = ws #Eq. 56
    if w2 > ws: w2 = ws #Eq. 56
    if w1 > w2: w1 = w2 #Eq. 56
    ra1 = (w2-w1)*math.sin(latrad)*math.sin(ldelta) #Eq. 48
    ra2 = math.cos(latrad)*math.cos(ldelta) #Eq. 48
    ra3 = math.sin(w2)-math.sin(w1) #Eq. 48
    if wmid < -1.0*ws or wmid > ws:
        ra = 0.0
    else:
        ra = 12.0/math.pi*4.92*dr*(ra1+ra2*ra3) #Eq. 48

    #rso (float) : Clear sky solar radiation (MJ m^-2 h^-1)
    #ASCE (2005) Eq. 47 and Appendix D
    beta1 = math.sin(latrad)*math.sin(ldelta)
    beta2 = math.cos(latrad)*math.cos(ldelta)*math.cos(wmid)
    beta = math.asin(beta1+beta2) #Eq. 62 or D.6
    if csreq == 'S':
        rso = (0.75+2e-5*z)*ra #Eq. 47
    else:
        if beta < 0.3:
            rso = 0.0
        else:
            pwat = 0.14*ea*patm+2.1 #Eq. D.3
            kt = 1.0
            kb1 = -0.00146*patm/(kt*math.sin(beta))
            kb2 = 0.075*(pwat/math.sin(beta))**0.4
            kb = 0.98*math.exp(kb1-kb2) #Eq. D.2
            if kb >= 0.15:
                kd = 0.35-0.36*kb #Eq. D.4
            else:
                kd = 0.18+0.82*kb #Eq. D.4
            rso = (kb + kd)*ra #Eq. D.1

    #rnl (float) : Net longwave radiation (MJ m^-2 h^-1)
    #ASCE (2005) Eqs. 44, 45, and 62
    if beta < 0.3 or rso <= 0.0: #nighttime
        fcd = fcdpt
    else: #daytime
        ratio = sorted([0.3,israd/rso,1.0])[1] #Eq. 45
        fcd = sorted([0.05,1.35*ratio-0.35,1.0])[1] #Eq. 45
    tk4 = (tavg+273.16)**4.0 #Eq. 44
    rnl = 2.042e-10*fcd*(0.34-0.14*math.sqrt(ea))*tk4 #Eq. 44

    #rn (float) : Net radiation (MJ m^-2 h^-1)
    #ASCE (2005) Eq. 42
    rn = rns-rnl

    #g (float) : Soil heat flux (MJ m^-2 h^-1)
    #ASCE (2005) Eqs. 65 and 66
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
            g = 0.2*rn
            Cd = 1.7 #!s m^-1
        else: #daytime
            g = 0.04*rn
            Cd = 0.25 #!s m^-1

    #u2 (float) : Wind profile relationship (m s^-1)
    #ASCE (2005) Eq. 67 and Appendix E
    if math.isnan(wndsp): wndsp = 2.0
    u2 = wndsp * (4.87/math.log(67.8*wndht-5.42))

    #etsz (float) : Standardized daily reference crop ET (mm h^-1)
    #ASCE (2005) Eq. 1
    etsz = 0.408*Udelta*(rn-g)+psycon*(Cn/(tavg+273.0))*u2*(es-ea)
    etsz = etsz/(Udelta+psycon*(1.0+Cd*u2))

    return (etsz, fcd)
