"""
########################################################################
The custom subpackage within the pyfao56 Python package demonstrates
user customizations, particularly for loading weather and soil data.

The custom subpackage contains the following modules:
    azmet_maricopa.py - Prepares weather data from the AZMET weather
        station in Maricopa, Arizona.
    example_soil.py - provides I/O functionality for creating a
        SoilProfile sdata class object from four ordered lists

11/04/2021 Module created by Kelly Thorp
11/30/2022 example_soil.py created by Josh Brekel
########################################################################
"""

from .azmet_maricopa import AzmetMaricopa
from .example_soil import ExampleSoil
