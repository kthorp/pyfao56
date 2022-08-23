"""
########################################################################
The soil_water.py module contains the SoilWater class, which provides
I/O tools for defining input soil water characteristics and for creating
a projected root zone for the growing season.

The soil_water.py module contains the following:
    SoilWater - A class for managing input soil water characteristics
        and projected root zone depth.

08/10/2022 Initial Python functions developed by Josh Brekel
########################################################################
"""

# Importing necessary dependencies
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.interpolate import pchip

class SoilWater:
    """A class for managing soil characteristics and soil water data used
    for FAO-56 calculations applied to stratified soil layers and a
    dynamic root zone.

    Attributes
    ----------
    rz_curve_df : DataFrame
        Contains depths (meters) of the root zone curve that is generated
        by the projected_root_zone_curve class method. Root zone depths
        are organized by date and days after planting (DAP) in this
        pandas data frame.
    depths : tuple
        Depths (meters) that are assumed to be representative
        of each layer of soil. List depths in order from the most shallow
        to the deepest. For all layers except the first, the depth given
        here is usually the middle of the soil layer.
        For example, a soil layer between 0.45 and 0.75 meters might use
        a depth of 0.6 meters in this tuple.
    theta_fc : tuple
        Field capacities (m^3/m^3) for each soil layer. List field
        capacities in the same order as the depths tuple.
    theta_ini : tuple
        Initial volumetric soil water content readings (m^3/m^3) for each
         soil layer. List in the same order as the depths tuple.
    theta_wp : tuple
        Assumed wilting points (m^3/m^3) for each soil layer. List in the
        same order as the depths tuple.
    soil_water_profile : dictionary
        A dictionary with the depth of the assumed soil layers as keys
        and information about the soil layer as values. This dictionary
        should be constructed via the create_soil_water_profile class
        method. The values of the dictionary are the theta_FC for the
        layer, the theta_ini for the layer, the theta_WP for the layer,
        a tuple of the boundaries of the soil layer in meters, the layer
        thickness in meters, the field capacity of the layer in
        millimeters, and the wilting point of the layer in millimeters.

    Methods
    -------
    projected_root_zone_curve(planting_date, end_date,
                              initial_depth=0.05, emergence_depth=0.06,
                              full_rz_depth=1.05, emergence_dap=10,
                              full_rz_dap=90)
        Use crucial values in the growing season to fit a projected root
        zone growth curve for an entire season.
    create_soil_water_profile(self, depths, theta_fc, theta_ini,
                              theta_wp, profile)
        Takes in information about soil layers and uses that information
        to create a dictionary with information about each soil layer.
        The dictionary can then be used in the model class to see a
        "dynamic" SWD (SWD for a root zone that changes across the
        growing season).
    """
    def __init__(self):
        """Initialize the SoilWater class attributes."""
        self.rz_curve_df = None
        self.depths = None
        self.theta_fc = None
        self.theta_ini = None
        self.theta_wp = None
        self.soil_water_profile = None

    def __str__(self):
        """Represents SoilWater Class as a string"""

        ast = '*' * 72
        if self.rz_curve_df is None:
            s = (f'{ast}\n'
                 f'pyfao56: FAO-56 in Python\n'
                 f'Soil Water Information\n'
                 f'{ast}\n'
                 f'Soil Layer Depths (m):\n'
                 f'     {self.depths}\n'
                 f'Soil Layer Field Capacities (m^3/m^3):\n'
                 f'     {self.theta_fc}\n'
                 f'Soil Layer Initial Volumetric Water Content (m^3/m^3)'
                 f':\n'
                 f'     {self.theta_ini}\n'
                 f'Soil Layer Assumed Wilting Points (m^3/m^3):\n'
                 f'     {self.theta_wp}\n'
                 f'Overall Soil Water Profile:\n'
                 f'     {self.soil_water_profile}')
        else:
            # Creating a temporary dataframe to avoid damaging the class
            # attribute (could be changed for speed?)
            temp_df = self.rz_curve_df.copy()
            # Putting dates into a string format
            dates = []
            for idx in temp_df.index:
                date = temp_df['Date'][idx]
                str_date = datetime.strftime(date, '%Y-%m-%d')
                dates += [str_date]
            # Over writing temporary dataframe with string dates
            temp_df['Date'] = dates
            # Setting the formats for the output text file
            fmts = {'Date': '{:.10s}'.format, 'DAP': '{:3d}'.format,
                    'Root Zone Depth': '{:8.3f}'.format}
            # Setting the headings for the output text file
            headings = ['YYYY-MM-DD', '                 DAP',
                        '                   RZ Depth (m)']
            # Creating the text content to save to the file
            s = (f'{ast}\n'
                 f'pyfao56: FAO-56 in Python\n'
                 f'Soil Water Information\n'
                 f'{ast}\n'
                 f'Soil Layer Depths (m):\n'
                 f'     {self.depths}\n'
                 f'Soil Layer Field Capacities (m^3/m^3):\n'
                 f'     {self.theta_fc}\n'
                 f'Soil Layer Initial Volumetric Water Content '
                 f'(m^3/m^3):\n'
                 f'     {self.theta_ini}\n'
                 f'Soil Layer Assumed Wilting Points (m^3/m^3):\n'
                 f'     {self.theta_wp}\n'
                 f'Overall Soil Water Profile:\n'
                 f'     {self.soil_water_profile}\n'
                 f'{ast}\n'
                 f'Date        Days After Planting   Projected Root '
                 f'Zone '
                 f'Depth (m)\n')
            s += temp_df.to_string(header=headings, index=False,
                                   formatters=fmts)
        return s

    def projected_root_zone_curve(self, planting_date, end_date,
                                  initial_depth=0.05,
                                  emergence_depth=0.06,
                                  full_rz_depth=1.05, emergence_dap=10,
                                  full_rz_dap=90):
        """Use planting date, end-of-season date, initial depth (m),
        emergence depth (m), full-root-zone depth (m), emergence days
        after planting, and full-root-zone days after planting to fit a
        curve for the projected root zone throughout the growing season.
        Populates the rz_curve_df class attribute with the date, days
        after planting, and the depth of the root zone according to the
        interpolated root zone depth curve.

        Parameters
        ----------
        planting_date : str
            The day of year that the crop was planted. String must be
            given in "YYYY-DOY" format.
        end_date : str
            The day of year to finish the analysis (end of season date).
            String must be given in "YYYY-DOY" format.
        initial_depth : float, optional
            The assumed initial depth (meters) of the crop roots at time
            of planting (default=0.05).
        emergence_depth : float, optional
            The depth (meters) of the roots at time of emergence
            (default=0.06).
        full_rz_depth : float, optional
            The maximum depth (meters) of the crop's roots in the growing
            season (default=1.05).
        emergence_dap : int, optional
            The number of days (after the planting date) it takes for the
            crop to emerge (default=10). This parameter can be used to
            adjust the initial points of the interpolated curve.
        full_rz_dap : int, optional
            The number of days (after the planting date) it takes for the
            crop to reach full root zone depth (default=90). This
            parameter can be used to adjust the end points of
            interpolated curve.
        """
        # Initialization of Variables
        # Converting date strings to datetime data types
        planting_doy = datetime.strptime(planting_date, "%Y-%j")
        end_doy = datetime.strptime(end_date, "%Y-%j")

        # Making list of dates to be used in the root zone data frame
        delta = end_doy - planting_doy
        dates = []
        for i in range(delta.days + 1):
            day = planting_doy + timedelta(days=i)
            dates += [day]

        # Creating initial data frame populated with growing-season dates
        self.rz_curve_df = pd.DataFrame(dates, columns=['Date'])
        # Creating days after planting (DAP) column in the data frame
        self.rz_curve_df['DAP'] = self.rz_curve_df.index

        # Constructing projected root zone depth curve and then adding it
        # to the data frame
        # Creating the arrays that are needed for interpolation
        depths_array = np.array([initial_depth,
                                 emergence_depth,
                                 full_rz_depth,
                                 full_rz_depth])
        dap_array = np.array([self.rz_curve_df['DAP'][0],
                              emergence_dap,
                              full_rz_dap,
                              self.rz_curve_df['DAP'].iloc[-1]])
        smooth_dap_array = np.linspace(dap_array[0],
                                       dap_array[-1],
                                       dap_array[-1])
        # Defining the function used to interpolate the root zone curve
        inter_func = pchip(dap_array, depths_array)
        # Creating list of root zone depths according to interpolation
        predicted_rz = list(inter_func(smooth_dap_array))
        # Adding another entry of the full root zone depth to the list
        # (because the predicted list's length is one shorter than the
        # data frame that we will add it to)
        predicted_rz += [full_rz_depth]
        # Adding the list of predicted root zone depths to the data frame
        # as it's own column titled 'Projected Root Zone'
        self.rz_curve_df['Projected Root Zone'] = predicted_rz

        # # Some code that might help integrate to pyfao56:
        # # Making the index of the data frame follow the pyfao56 index
        # # formats (see wdata dataframe for an example).
        # index_dates = []
        # for idx in self.rz_curve_df.index:
        #     dt_date = self.rz_curve_df['Date'][idx]
        #     index_dates += [dt_date.strftime('%Y-%j')]
        # self.rz_curve_df['Date'] = index_dates
        # self.rz_curve_df.set_index('Date', inplace=True)
        # self.rz_curve_df.index.name = None

    def create_soil_water_profile(self, depths, theta_fc, theta_ini,
                                  theta_wp, layer_boundaries):
        """Use tuples to create a dictionary of values relevant to the
        assumed soil layers. Populates the soil_water_profile class
        attribute, which can then be used to calculate SWD for stratified
        soil layers. Also populates the depths, theta_fc, theta_ini_, and
        theta_wp class attributes.

        depths : tuple
            The depths (meters) that identify each layer of soil. List
            depths from shallowest to deepest.
            e.g. (0.15, 0.3, 0.6, 0.9, 1.2, 1.5, 2.0)
        theta_fc : tuple
            Assumed field capacity (m^3/m^3) values for each soil layer.
            List in the same order as the depths tuple.
            e.g. (0.29, 0.24, 0.182, 0.158, 0.12, 0.108, 0.144)
            ---where 0.29 corresponds to layer 0.15, 0.24 corresponds to
               layer 0.3, and so on.
        theta_ini : tuple
            Initial volumetric water (m^3/m^3) values for each soil
            layer. List in the same order as the depths tuple.
            e.g. (0.083, 0.058, 0.039, 0.033, 0.012, 0.005, 0.014)
            ---where 0.083 corresponds to layer 0.15, 0.058 corresponds
               to layer 0.3, and so on.
        theta_wp : tuple
            Assumed wilting point (m^3/m^3) values for each soil layer.
            List in the same order as the depths tuple.
            e.g. (0.145, 0.12, 0.091, 0.079, 0.06, 0.054, 0.072)
            ---where 0.145 corresponds to layer 0.15, 0.12 corresponds to
               layer 0.3, and so on.
        layer_boundaries : tuple of tuples
            Tuples of the boundaries of each soil layer. List in the same
            order as the depths tuple.
            e.g. (
                   (0, 0.15), (0.15, 0.45), (0.45, 0.75), (0.75, 1.05),
                   (1.05, 1.35), (1.35, 1.65), (1.65, 2.15)
                  )
            ---where (0, 0.15) corresponds to layer 0.15, (0.15, 0.45)
               corresponds to layer 0.3, and so on.
        """

        # Creating the soil water profile dictionary from the
        # user-provided tuples
        # Creating empty dictionary to populate
        sw_profile_dict = {}
        # Iterating through the depths tuple to construct dictionary
        for index, depth in enumerate(depths):
            layer_start = layer_boundaries[index][0]
            layer_end = layer_boundaries[index][1]
            layer_thickness = round((layer_end - layer_start), 3)
            layer_thetaFC = theta_fc[index]
            layer_thetaWP = theta_wp[index]
            layer_theta_ini = theta_ini[index]
            layer_FC_mm = (layer_thetaFC * 1000) * layer_thickness
            layer_WP_mm = (layer_thetaWP * 1000) * layer_thickness
            tup_theta = (layer_thetaFC, layer_theta_ini,
                         layer_thetaWP, layer_boundaries[index],
                         layer_thickness, layer_FC_mm, layer_WP_mm)
            sw_profile_dict[depth] = tup_theta

        # Setting class attributes equal to user-provided arguments
        self.depths = depths
        self.theta_fc = theta_fc
        self.theta_ini = theta_ini
        self.theta_wp = theta_wp
        self.soil_water_profile = sw_profile_dict
