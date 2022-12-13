"""
########################################################################
The pyfao56 Python package facilitates FAO-56 computations of daily soil
water balance using the dual crop coefficient method to estimate crop
evapotranspiration (ET).

The FAO-56 method is described in the following documentation:
Allen, R. G., Pereira, L. S., Raes, D., Smith, M., 1998.  FAO Irrigation
and Drainage Paper No. 56. Crop Evapotranspiration: Guidelines for
Computing Crop Water Requirements. Food and Agriculture Organization of
the United Nations, Rome Italy.

http://www.fao.org/3/x0490e/x0490e00.htm


Reference ET is computed using the ASCE Standardized Reference ET
Equation, which is described in the following documentation:
ASCE Task Committee on Standardization of Reference Evapotranspiration
(Walter, I. A., Allen, R. G., Elliott, R., Itenfisu, D., Brown, P.,
Jensen, M. E.,Mecham, B., Howell, T. A., Snyder, R., Eching, S.,
Spofford, T., Hattendorf, M., Martin, D., Cuenca, R. H., Wright, J. L.)
, 2005. The ASCE Standardized Reference Evapotranspiration Equation.
American Society of Civil Engineers, Reston, VA.

https://ascelibrary.org/doi/book/10.1061/9780784408056


The pyfao56 package contains the following modules:
    irrigation.py
        I/O tools to define irrigation management schedules
    model.py 
        Equations for daily soil water balance computations
    parameters.py
        I/O tools for required input parameters
    refet.py
        Equations for computing ASCE Standardized Reference ET
    update.py
        I/O tools and methods for state variable updating
    weather.py
        I/O tools for required weather information

01/07/2016 Initial Python functions developed by Kelly Thorp
11/04/2021 Scripts updated for inclusion in the pyfao56 Python package
########################################################################
"""

from .irrigation import Irrigation
from .model import Model
from .parameters import Parameters
from .soil_profile import SoilProfile
from .update import Update
from .weather import Weather
