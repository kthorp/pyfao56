"""
########################################################################
The tools subpackage within the pyfao56 Python package provides tools
for implementing the pyfao56 model, including functionality for
incorporation of measured soil water content data for model evaluation.

The tools subpackage contains the following modules:
    soil_water.py  - provides I/O tools for measured volumetric soil
                     water content data

10/17/2022 Subpackage created by Josh Brekel
11/09/2022 Initial Visualization scripts created by Josh Brekel (coming soon!)
03/02/2023 SoilWater Class functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

from .soil_water import SoilWater
