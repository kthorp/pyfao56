"""
########################################################################
The example_soil.py module contains the ExampleSoil class, which
inherits from the pyfao56 SoilProfile class in soil_profile.py.
ExampleSoil provides I/O functionality for creating a SoilProfile sdata
class object from four ordered lists.

09/21/2022 Initial Python functions developed by Josh Brekel
11/30/2022 Finalized updates for inclusion in the pyfao56 Python package
########################################################################
"""

from pyfao56 import SoilProfile
import pandas as pd

class ExampleSoil(SoilProfile):
    """A class for loading soil profile data from four ordered lists.

    Inherits attributes and methods from pyfao56 SoilProfile. Overrides
    the SoilProfile customload function to allow soil profile data to be
    loaded from four ordered lists.

    Attributes
    ----------
    cnames : list
        Column names for sdata
    sdata : DataFrame
        Soil profile data as float
        index = Bottom depth of the layer as integer (cm)
        columns = ['thetaFC', 'thetaWP', 'theta0']
            thetaFC - Volumetric Soil Water Content, Field Capacity
                      (cm3/cm3)
            thetaWP - Volumetric Soil Water Content, Wilting Point
                      (cm3/cm3)
            theta0  - Volumetric Soil Water Content, Initial
                      (cm3/cm3)

    Methods
    -------
    customload()
        Overridden method from the pyfao56 SoilProfile class to provide
        customization for loading SoilProfile data from four lists.
    """

    def customload(self, bottom_depths, fc, wp, ini):
        """Loads soil profile information from four ordered lists.

        Parameters
        ----------
        bottom_depths : list
            A list of the bottom depths (cm, int) of assumed soil
            layers. Order the list from the shallowest layer to the
            deepest layer.
        fc : list
            A list of field capacities (cm3/cm3) of assumed soil
            layers. Order the list from the shallowest layer to the
            deepest layer.
        wp : list
            A list of wilting points (cm3/cm3) of assumed soil layers.
            Order the list from the shallowest layer to the deepest
            layer.
        ini : list
            A list of initial volumetric soil water content (cm3/cm3)
            measurements of assumed soil layers. Order the list from the
            shallowest layer to the deepest layer.

        ***Note on parameters: all lists should be created such that
        data is ordered from the top (shallow part) of the soil profile
        to the bottom (deep part) of the soil profile. For example, the
        FieldCapacity of the third layer down should be the third entry
        in the fc list.
        """

        soil_data_dict = {self.cnames[0]: fc,
                          self.cnames[1]: wp,
                          self.cnames[2]: ini}
        self.sdata = pd.DataFrame.from_dict(soil_data_dict,
                                            dtype='float64')
        self.sdata.index = bottom_depths
        self.sdata.index.astype('int32', copy=False)
