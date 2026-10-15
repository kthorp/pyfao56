"""
########################################################################
The refet_testD.py module contains a function to compare short crop
reference evapotranspiration (ETo) calculations and intermediate
variables with results presented in FAO-56 (2025) Examples 4.1, 4.2 and
4.3 for monthly, daily, and hourly periods, respectively.

The refet_testD.py module contains the following:
    run - function to compute ETo using data from FAO-56 (2025)
          Examples 4.1, 4.2, and 4.3.

09/28/2026 Added functionality to make tests for refet2.py
########################################################################
"""

from pyfao56 import refet2

def run():
    """Generate intermediate standardized reference ET output"""

    #FAO-56 (2025) Example 4.2 - ETo with daily data
    dailyETo = refet2.RefET2()
    lat = 50.0+48.0/60.0 #decimal degrees
    wind = 10.0 * 1000.0 / 60.0 / 60.0 #m/s
    dailyETo.daily(z=100., lat=lat, doy=187, tmax=21.5, tmin=12.3,
                   sunhr=9.25, rhmax=84.0, rhmin=63.0, wndsp=wind,
                   wndht=10.)
    print('FAO-56 (2025) Example 4.2 - ETo with daily data')
    for key in dailyETo.var.keys():
        print(key + ' : ' + str(dailyETo.var[key]))
    print('')

    #FAO-56 (2025) Example 4.1 - Mean daily ETo with monthly data
    monthlyETo = refet2.RefET2()
    lat = 13.0+44.0/60.0 #decimal degrees
    monthlyETo.monthly(z=2.0, lat=lat, doy=105, tmax=34.8, tmin=25.6,
                       tpre=29.2, sunhr=8.5, vapr=2.85, wndsp=2.0)
    print('FAO-56 (2025) Example 4.1 - ETo with monthly data')
    for key in monthlyETo.var.keys():
        print(key + ' : ' + str(monthlyETo.var[key]))
    print('')

    #FAO-56 (2025) Example 4.1 - ETo with hourly data
    hourlyETo = refet2.RefET2()
    lat = 16.0+13.0/60.0 #decimal degrees
    lon = 16.0+15.0/60.0 #decimal degrees*
    #Example says West longitude, which should result a negative value.
    #However, the example calculations use a postive longitude.
    fcd = 1.35*0.8-0.35
    hourlyETo.hourly(z=8.0, lat=lat, lon=lon, lzn=15., doy=274, sct=2.5,
                     tmean=28., srad=0., rhum=90., wndsp=1.9, csreq='S',
                     fcdpt=fcd)
    print('FAO-56 (2025) Example 4.3 - ETo with hourly data, nighttime')
    for key in hourlyETo.var.keys():
        print(key + ' : ' + str(hourlyETo.var[key]))
    print('')
    hourlyETo.hourly(z=8.0, lat=lat, lon=lon, lzn=15., doy=274,
                     sct=14.5, tmean=38., srad=2.45, rhum=52.,
                     wndsp=3.3, csreq='S')
    print('FAO-56 (2025) Example 4.3 - ETo with hourly data, daytime')
    for key in hourlyETo.var.keys():
        print(key + ' : ' + str(hourlyETo.var[key]))
    print('')

if __name__ == '__main__':
    run()
