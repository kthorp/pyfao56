"""
########################################################################
The forecast.py module contains the Forecast class, which is used to
retrieve seven-day weather forecasts from the National Digital Forecast
Database (NDFD). It uses the REST approach, which was more robust than
the SOAP method, in terms of server responsiveness. Data is retrieved
for computation of ASCE Standardized Reference Evapotranspiration,
including wind speed (m/s) and minimum, maximum, and dew point air
temperatures (degrees C). Solar radiation forecasts are not directly
provided by NDFD, but NDFD does provide cloud cover forecasts. By
providing the optional "elevation" parameter, users can obtain solar
radiation forecasts computed by multiplication of cloud cover and
clear-sky solar radiation. Liquid precipitation forecasts (mm) are also
obtained.

#https://graphical.weather.gov/xml/rest.php
#https://graphical.weather.gov/xml/docs/elementInputNames.php
#https://digital.weather.gov/staticpages/definitions.php

xx/xx/2019 Initial Python functions developed by Kelly Thorp
11/04/2021 Finalized updates for inclusion in the pyfao56 Python package
06/05/2023 Added Srad and Rain columns -- Josh Brekel, USDA-ARS
08/17/2023 Added Clds column to output
########################################################################
"""

import datetime
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import numpy as np
import math

class Forecast():
    """A class for obtaining weather forecasts from the NDFD

    Obtains weather forecast data from the National Digital Forecast
    Database (NDFD). Given latitude and longitude, the class methods
    will obtain and store a seven-day weather forecast from today
    forward, including liquid precipitation, wind speed, cloud cover,
    and minimum, maximum, and dew point air temperatures. If the
    optional elevation parameter is provided, then daily incoming solar
    radiation is forecasted from cloud cover forecasts and clear-sky
    solar radiation.

    Attributes
    ----------
    latitude : float
        Site latitude (decimal degrees)
    longitude : float
        Site longitude (decimal degrees)
    wndht : float, optional
        Correction height for NDFD wind speed (m)
        Should be the same as wndht in Weather class
        (default = 10.0, no correction)
    elevation : float, optional
        Site elevation (m) (default = NaN)
    forecast : DataFrame
        Weather forecast data from NDFD as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Clds','Srad','Tmax','Tmin','Tdew','Wndsp','Rain']
            Clds  - Daily cloud cover (%)
            Srad  - Daily incoming solar radiation (MJ/m2)
            Tmax  - Daily maximum air temperature (deg C)
            Tmin  - Daily minimum air temperature (deg C)
            Tdew  - Daily average dew point temperature (deg C)
            Wndsp - Daily average wind speed (m/s)
            Rain  - Daily amount of liquid precipitation (mm)

    Methods
    -------
    getforecast()
        Request and process weather forecast data from NDFD and update
        the self.forecast DataFrame.
    """

    def __init__(self, latitude, longitude, wndht=10.0,
                 elevation=float('NaN')):
        """Initialize the Forecast class attributes

        Parameters
        ----------
        latitude : float
            Site latitude (decimal degrees)
        longitude : float
            Site longitude (decimal degrees)
        wndht : float, optional
            Correction height for NDFD wind speed (m)
            Should be the same as wndht in Weather class
            (default = 10.0, no correction)
        elevation : float, optional
            Site elevation (m) (default = NaN)
        """

        self.latitude = latitude
        self.longitude = longitude
        self.wndht = wndht
        self.elevation = elevation
        self._initialize()
        self._compute_rso()

    def __str__(self):
        """Represent the Forecast class variables as a string."""
        pd.options.display.float_format = '{:6.2f}'.format
        s = ('Latitude: {:12.7f}\n'
             'Longitude: {:12.7f}\n'
             'Elevation: {:12.7f}\n\n'
             'NDFD weather forecast data for year-doy:\n'
             ).format(self.latitude, self.longitude, self.elevation)
        s += self.forecast.to_string()
        return s

    def _initialize(self):
        """Initialize the self.forecast DataFrame."""
        init = []
        keys = []
        cols = ['Clds','Srad','Tmax','Tmin','Tdew','Wndsp','Rain']
        today = datetime.datetime.today()
        NaN = float('NaN')
        for i in list(range(-1,10)):
            day = today + datetime.timedelta(days=i)
            keys.append(day.strftime('%Y-%j'))
            init.append([NaN,NaN,NaN,NaN,NaN,NaN,NaN])
        self.forecast = pd.DataFrame(init,index=keys,columns=cols)

    def _compute_rso(self):
        """Compute clear sky solar radiation on forecast days."""
        self.rso = {}
        today = datetime.datetime.today()
        NaN = float('NaN')
        for i in list(range(-1,10)):
            day = today + datetime.timedelta(days=i)
            key = day.strftime('%Y-%j')

            #ra (float) : Extraterrestrial radiation (MJ m^-2 d^-1)
            #ASCE (2005) Eqs. 21-27
            doy = int(day.strftime('%j'))
            latrad = self.latitude*math.pi/180.0 #Eq.22
            dr = 1.0+0.033*math.cos(2.0*math.pi/365.0*doy) #Eq.23
            ldelta = 0.409*math.sin(2.0*math.pi/365.0*doy-1.39) #Eq.24
            ws = math.acos(-1.0*math.tan(latrad)*math.tan(ldelta))#Eq.27
            ra1 = ws*math.sin(latrad)*math.sin(ldelta) #Eq.21
            ra2 = math.cos(latrad)*math.cos(ldelta)*math.sin(ws) #Eq.21
            ra = 24.0/math.pi*4.92*dr*(ra1+ra2) #Eq.21

            #rso (float) : Clear sky solar radiation (MJ m^-2 d^-1)
            #ASCE (2005) Eq. 19
            if not math.isnan(self.elevation):
                self.rso.update({key:(0.75+2e-5*self.elevation)*ra})
            else:
                self.rso.update({key:NaN})

    def getforecast(self):
        """Request and process weather forecast data from NDFD."""

        #Submit the request to NDFD.
        request = {}
        request.update({'lat':self.latitude})
        request.update({'lon':self.longitude})
        request.update({'product':'time-series'})
        request.update({'begin':''})
        request.update({'end':''})
        request.update({'Unit':'m'})
        request.update({'sky': 'sky'})
        request.update({'maxt':'maxt'})
        request.update({'mint':'mint'})
        request.update({'dew':'dew'})
        request.update({'wspd':'wspd'})
        request.update({'qpf':'qpf'})
        url = 'https://graphical.weather.gov/xml/sample_products/'
        url+= 'browser_interface/ndfdXMLclient.php'
        r = requests.get(url,params=request)
        #print(r.text)

        #Process the resulting XML string from NDFD.
        tree = ET.fromstring(r.text)
        data = tree.find('data')
        pars = data.find('parameters')

        items = {'Clds' :['cloud-amount','total'   ,'start-valid-time'],
                 'Tmax' :['temperature','maximum'  ,'start-valid-time'],
                 'Tmin' :['temperature','minimum'  ,'end-valid-time'  ],
                 'Tdew' :['temperature','dew point','start-valid-time'],
                 'Wndsp':['wind-speed' ,'sustained','start-valid-time'],
                 'Rain' :['precipitation', 'liquid','start-valid-time']}

        self._initialize()
        times = []
        values = []
        dayvals = []
        today = datetime.datetime.today()
        for item in items.keys():
            values[:] = []
            tag = items[item][0]
            att = items[item][1]
            node1 = pars.find("./"+tag+"[@type='"+att+"']")
            for child in node1:
                if child.tag == 'value':
                    values.append(float(child.text))
            tl = node1.attrib['time-layout']
            times[:] = []
            node2 = data.find(".//layout-key[.='"+tl+"']..")
            for child2 in node2:
                if child2.tag == items[item][2]:
                    times.append(child2.text)
            for i in list(range(-1,10)):
                day = today + datetime.timedelta(days=i)
                key1 = day.strftime('%Y-%j')
                dayvals[:] = []
                for j in list(range(len(times))):
                    Ymd='%Y-%m-%d'
                    date = datetime.datetime.strptime(times[j][:10],Ymd)
                    key2 = date.strftime('%Y-%j')
                    if key1 == key2:
                        dayvals.append(values[j])
                if len(dayvals) > 0:
                    mean = np.mean(np.array(dayvals))
                    if item == 'Wndsp' and self.wndht != 10.0:
                        # Adjust NDFD wind speed from 10.0 m to station
                        # height (wndht in Weather class)
                        zNDFD = 10.0
                        # u2 : wind speed at 2 m (m s^-1)
                        #ASCE (2005) Eq. 33 and Appendix E
                        u2 = mean * (4.87/math.log(67.8*zNDFD-5.42))
                        # uz : wind speed at wndht in Weather (m s^-1)
                        # ASCE (2005) Eq. 33 and Appendix E
                        uz = u2 / (4.87/math.log(67.8*self.wndht-5.42))
                        mean = uz
                    self.forecast.loc[key1,item] = mean
                    #Estimate Srad from cloud cover and rso
                    if item == 'Clds':
                        srad = (1.0 - mean/100.) * self.rso[key1]
                        self.forecast.loc[key1,'Srad'] = srad
