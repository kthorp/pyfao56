"""
########################################################################
The custom subpackage within the pyfao56 Python package facilitates
user customizations, particularly for loading weather data.

The custom subpackage contains the following modules:
    azmet_maricopa.py - Prepares weather data from the AZMET weather
        station in Maricopa, Arizona.
    forecast.py - Obtains weather forecast data from the National
        Digital Forecast Database (NDFD)

11/04/2021 Module created by Kelly Thorp
########################################################################
"""
from .azmet_maricopa import AzmetMaricopa
from .forecast import Forecast
