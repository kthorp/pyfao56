"""
########################################################################
The soil_water.py module contains the SoilWater class, which provides
I/O tools for using observed volumetric soil water content data in the
pyfao56 environment. The SoilWater class is capable of storing observed
volumetric soil water content (cm^3/cm^3) data, observed fractional soil
water deficit (cm^3/cm^3) data, computing observed soil water deficit
based on data, and computing root zone soil water deficit (mm) data.

The soil_water.py module contains the following:
    SoilWater - A class for managing observed soil water data

10/17/2022 SWC Python functions developed by Josh Brekel, USDA-ARS
11/07/2022 SWD Python functions developed by Josh Brekel, USDA-ARS
03/07/2023 SoilWater Class functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

import pandas as pd

class SoilWater:
    """A class for managing observed soil water data in pyfao56.

    Attributes
    ----------
    swcdata : DataFrame
        Volumetric soil water content (cm^3/cm^3) data as float
        index - Bottom depth of soil profile layer as integer (cm)
        columns - measurement date in string 'YYYY-DOY' format
    swddata : DataFrame
        Fractional soil water deficit data as float
        index - Bottom depth of soil profile layer as integer (cm)
        columns - string measurement date in 'YYYY-DOY' format
    rzdata : DataFrame
        Soil water deficit (mm) data as float
        index - string measurement date in 'YYYY-DOY' format
        columns - ['Year', 'DOY', 'Zr', 'SWDr', 'SWDrmax']
            Year    - 4-digit year (yyyy)
            DOY     - Day of year  (ddd)
            Zr      - Root depth (m), FAO-56 page 279
            SWDr    - Observed soil water deficit(mm) for root depth
            SWDrmax - Observed soil water deficit(mm) for max root depth
            SWCr    - Observed soil water deficit(mm) for root depth
            SWCrmax - Observed soil water deficit(mm) for max root depth
            ObsKs   - Observed Ks based on SWDr and pyfao56 Model class

    Methods
    -------
    savefile(swc_path='tools_pyfao56.swc',swd_path='tools_pyfao56.swd',
             swrz_path='tools_pyfao56.swrz')
        Save SoilWater attribute(s) to file(s)
    loadfile(swc_path='tools_pyfao56.swc',swd_path='tools_pyfao56.swd',
             swrz_path='tools_pyfao56.swrz')
        Load SoilWater attribute(s) from file(s)
    customload()
        Override this function to customize loading observed
        volumetric soil water content data.
    compute_swd_from_swc()
        Compute observed soil water deficit (for each soil layer)
        from swcdata class atrribute. Populates swddata class attribute.
    compute_root_zone_sw()
        Compute observed soil water deficit (mm) and observed volumetric
        soil water content (mm) in the active root zone and in the
        maximum root zone, based on pyfao56 Model root depth estimates.
        Also computes Ks based on observed SWD and pyfao56 Model class
        object. Populates rzdata class attribute.
    """

    def __init__(self, mdl=None, *args):
        """
        Initialize the SoilWater class object.

        Parameters
        ----------
        mdl   : pyfao56 Model class object, optional
            pyfao56 Model class that can be used for calculating soil
            water deficit and/or root zone soil water values.
            Default is None.
        *args : str
            A variable number of file paths that the user wants to load.
            The supported file extensions are 'swc', 'swd', and 'swrz'.

        Raises
        ------
        ValueError
            If the file does not have an accepted file extension.

        Notes
        -----
        If only 'swc' file is passed, then SWD and SWrz are computed.
        If only 'swc' and 'swd' files are passed, then the root zone
        soil water values are calculated.

        If the user does not load from a file, then they can use the
        customload method to populate the swcdata attribute.
        """
        # Initialize two main class attributes as None types:
        self.swcdata = None
        self.swddata = None
        # Initialize rzdata column names and empty rzdataframe
        self.rz_cnames = ['Year', 'DOY', 'Zr', 'SWDr',
                          'SWDrmax', 'SWCr', 'SWCrmax', 'ObsKs']
        self.rzdata = pd.DataFrame(columns=self.rz_cnames)

        # Create list of acceptable file extensions
        accepted_extensions = ['swc', 'swd', 'swrz']
        # Set class model object (if one is passed at instantiation)
        if mdl is not None:
            self.mdl = mdl
        # Load files to the class attributes
        if args:
            for filepath in args:
                deconstructed_filepath = filepath.rsplit('.', 1)
                extension = deconstructed_filepath[-1].lower()
                if extension not in accepted_extensions:
                    raise ValueError(f'{filepath} does not have an '
                                     f'accepted file extension.')
                elif extension == 'swc':
                    self.loadfile(swc_filepath=filepath)
                elif extension == 'swd':
                    self.loadfile(swd_filepath=filepath)
                elif extension == 'swrz':
                    self.loadfile(swrz_filepath=filepath)
            # If only a swc file is given, then compute SWD and SWrz
            if self.swddata is None and self.rzdata is None:
                self.compute_swd_from_swc()
                self.compute_root_zone_sw()
            # If only swc and swd files are given, then compute SWrz
            elif self.rzdata is None:
                self.compute_root_zone_sw()
        # If not loading from file, then use customload to populate swc
        else:
            self.swcdata = pd.DataFrame()

    def __str__(self, method='all'):
        """Represent the SoilWater class as a string"""

        method = method.lower()
        accepted_methods = ['all', 'swc', 'swd', 'swrz']
        title = 'pyfao56: FAO-56 Evapotranspiration in Python'
        ast = '*' * 72
        if method not in accepted_methods:
            raise ValueError(f'{method} is not an accepted argument. '
                             f'The acceptable formats are: '
                             f'{accepted_methods}')
        elif method == 'all':
            swc = self.__str__(method='swc')
            swd = self.__str__(method='swd')
            swrz = self.__str__(method='swrz')
            s = swc + f'\n{ast}\n' + swd + f'\n{ast}\n' + swrz
            return s
        elif method == 'swc':
            fmts = {'__index__': '{:5d}'.format}
            for date_col in list(self.swcdata):
                fmts[date_col] = '{:8.3f}'.format
            s = ('{:s}\n'
                 '{:s}\n'
                 'Tools: Fractional Soil Water Content Data by Layer\n'
                 '{:s}\n'
                 'Depth').format(ast, title, ast)
            for cname in list(self.swcdata):
                s += '{:>9s}'.format(cname)
            s += '\n'
            s += self.swcdata.to_string(header=False,
                                        na_rep='    NaN',
                                        formatters=fmts)
            return s
        elif method == 'swd':
            fmts = {'__index__': '{:5d}'.format}
            for date_col in list(self.swddata):
                fmts[date_col] = '{:8.3f}'.format
            s = ('{:s}\n'
                 '{:s}\n'
                 'Tools: Fractional Soil Water Deficit Data by Layer\n'
                 '{:s}\n'
                 'Depth').format(ast, title, ast)
            for cname in list(self.swddata):
                s += '{:>9s}'.format(cname)
            s += '\n'
            s += self.swddata.to_string(header=False,
                                        na_rep='    NaN',
                                        formatters=fmts)
            return s
        elif method == 'swrz':
            fmts = {'Year': '{:4s}'.format, 'DOY': '{:3s}'.format,
                    'Zr': '{:5.3f}'.format, 'SWDr': '{:7.3f}'.format,
                    'SWDrmax': '{:7.3f}'.format,
                    'SWCr': '{:7.3f}'.format,
                    'SWCrmax': '{:7.3f}'.format,
                    'ObsKs': '{:5.3f}'.format}
            s = ('{:s}\n'
                 '{:s}\n'
                 'Tools: Root Zone Soil Water Values (mm)\n'
                 '{:s}\n'
                 'Year DOY    Zr    SWDr SWDrmax SWDr SWDrmax ObsKs\n'
                 ).format(ast, title, ast)
            s += self.swrzdata.to_string(header=False,
                                       index=False,
                                       formatters=fmts)
            return s

    def savefile(self, swc_path=None, swd_path=None, swrz_path=None):
        """Save observed soil water data to a file.

        Parameters
        ----------
        swc_path  : str, optional
            Any valid filepath string (default = None)
        swd_path  : str, optional
            Any valid filepath string (default = None)
        swrz_path : str, optional
            Any valid filepath string (default = None)

        Raises
        ------
        FileNotFoundError
            If a filepath is not found.
        """
        if swc_path is not None:
            try:
                f = open(swc_path, 'w')
            except FileNotFoundError:
                print('The filepath for soil water content data is not '
                      'found.')
            else:
                f.write(self.__str__(method='swc'))
                f.close()
        if swd_path is not None:
            try:
                f = open(swd_path, 'w')
            except FileNotFoundError:
                print('The filepath for soil water deficit data is not '
                      'found.')
            else:
                f.write(self.__str__(method='swd'))
                f.close()
        if swrz_path is not None:
            try:
                f = open(swrz_path, 'w')
            except FileNotFoundError:
                print('The filepath for root zone soil water  data is '
                      'not found.')
            else:
                f.write(self.__str__(method='swrz'))
                f.close()
        if (swc_path is None)&(swd_path is None)&(swrz_path is None):
            print('Please specify a filepath for data to be saved.')

    def loadfile(self, swc_path=None, swd_path=None, swrz_path=None):
        """Load pyfao56 soil profile data from a file.

        Parameters
        ----------
        swc_path  : str, optional
            Any valid filepath string (default = None)
        swd_path  : str, optional
            Any valid filepath string (default = None)
        swrz_path : str, optional
            Any valid filepath string (default = None)

        Raises
        ------
        FileNotFoundError
            If a filepath is not found.
        """
        if swc_path is not None:
            try:
                f = open(swc_path, 'r')
            except FileNotFoundError:
                print('The filepath for soil water content data is not '
                      'found.')
            else:
                lines = f.readlines()
                f.close()
                cols = lines[4].strip().split()[1:]
                self.swcdata = pd.DataFrame(columns=cols)
                for line in lines[5:]:
                    line = line.strip().split()
                    depth = int(line[0])
                    data = list()
                    for i in list(range(1, len(cols) + 1)):
                        data.append(float(line[i]))
                    self.swcdata.loc[depth] = data
        if swd_path is not None:
            try:
                f = open(swd_path, 'r')
            except FileNotFoundError:
                print('The filepath for soil water deficit data is not '
                      'found.')
            else:
                lines = f.readlines()
                f.close()
                cols = lines[4].strip().split()[1:]
                self.swddata = pd.DataFrame(columns=cols)
                for line in lines[5:]:
                    line = line.strip().split()
                    depth = int(line[0])
                    data = list()
                    for i in list(range(1, len(cols) + 1)):
                        data.append(float(line[i]))
                    self.swddata.loc[depth] = data
        if swrz_path is not None:
            try:
                f = open(swrz_path, 'r')
            except FileNotFoundError:
                print('The filepath for root zone soil water data is '
                      'not found.')
            else:
                lines = f.readlines()
                f.close()
                cnames = ['Zr', 'SWDr', 'SWDrmax', 'SWCr',
                          'SWCrmax', 'ObsKs']
                self.rzdata = pd.DataFrame(columns=cnames)
                for line in lines[5:]:
                    line = line.strip().split()
                    year = line[0]
                    doy = line[1]
                    key = '{:04d}-{:03d}'.format(int(year), int(doy))
                    data = list()
                    for i in list(range(2, 8)):
                        data.append(float(line[i]))
                    self.rzdata.loc[key] = data
        if (swc_path is None)&(swd_path is None)&(swrz_path is None):
            print('Please specify a filepath for data to be loaded.')

    def customload(self):
        """Override this function to customize loading observed
        volumetric soil water content data for the swcdata attribute.
        """

        pass

    def compute_swd_from_swc(self):
        """Compute observed soil water deficit (for each soil layer)
        from swcdata class atrribute. Populates swddata class attribute.
        """
        # Making a base dataframe out of swcdata
        swddata = self.swcdata.copy()
        # Copying soil data from the model class
        sol = self.mdl.sol.sdata
        # Copying field capacity info over to swddata
        if sol is None:
            thetaFC = self.mdl.par.thetaFC
            swddata['thetaFC'] = [thetaFC] * swddata.shape[0]
        else:
            swddata['thetaFC'] = sol['thetaFC'].copy()
        # Creating a list of the column names in the swddata dataframe
        cnames = list(swddata.columns)
        # Looping through column names; calculating SWD on date columns
        for cname in cnames:
            if cname != 'thetaFC':
                # "Clip" sets negative SWD values to zero
                swddata[cname] = (swddata['thetaFC'] -
                                       swddata[cname]).clip(lower=0)
        # Dropping the Field Capacity info from the dataframe (K.I.S.)
        swddata.drop('thetaFC', axis=1, inplace=True)
        # Write swddata to class attribute
        self.swddata = swddata

    def compute_root_zone_sw(self):
        """Compute observed soil water deficit (mm) and observed
        volumetric soil water content (mm) in the active root zone and
        in the maximum root zone, based on pyfao56 Model root depth
        estimates. Also computes Ks based on observed SWD and pyfao56
        Model class object. Populates rzdata class attribute."""

        # ********************* Setting things up **********************
        # Make swddata into a dictionary to easily store/access values
        swd_dict = self.swddata.to_dict()
        # Make swcdata into a dictionary to easily store/access values
        swc_dict = self.swcdata.to_dict()
        # List of swddata column names (which are measurement dates)
        dates = list(swd_dict.keys())
        # Get lists of years and days of measurements from dates list
        years = []
        days = []
        for i in dates:
            deconstructed_date = i.split('-')
            years += [deconstructed_date[0]]
            days += [deconstructed_date[1]]

        # Make initial dataframe out of the measurement date info
        rzdata = pd.DataFrame({'Year-DOY': dates,
                               'Year': years,
                               'DOY': days})
        # Set row index to be the same as pyfao56 Model output dataframe
        rzdata = rzdata.set_index('Year-DOY')

        # Merging Zr column to the initial dataframe on measurement days
        rzdata = rzdata.merge(self.mdl.odata[['Zr']], left_index=True,
                              right_index=True)

        # Setting variable for max root zone in #10^-5 meters
        rmax = self.mdl.par.Zrmax * 100000 #10^-5 meters

        # ****************** Computing Root Zone SW ********************
        # Loop through swd_dict to compute SWD and SWC values
        SWDr    = {}
        SWDrmax = {}
        SWCr    = {}
        SWCrmax = {}
        for mykey, swdByLyr in swd_dict.items():
            # Hint:
            #          mykey is a column name of swddata ('YYYY-DOY')
            #          swdByLyr is a dictionary:
            #               -Keys: layer depths
            #               -Values: fractional SWD measured on mykey
            # Finding root depth(10^-5 m) on measurement days
            try:
                Zr = rzdata.loc[mykey, 'Zr'] * 100000  # 10^-5 meters
            except KeyError:
                # Ignoring mismatches in observed/modeled data
                pass
            # Access the soil water content values for the mykey day
            swcByLyr = swc_dict[mykey]
            # Setting temp variables for SWDr and SWDrmax on meas. days
            Dr = 0.
            Drmax = 0.
            # Setting temp variables for SWCr and SWCrmax on meas. days
            vH2O = 0.
            vH2Omax = 0.
            # Iterate down to max root depth in 10^-5 meters increments
            for inc in list(range(1, int(rmax + 1))):
                # Find soil layer that contains the increment
                lyr = [dpth for (idx, dpth)
                       in enumerate(list(swdByLyr.keys()))
                       if inc <= dpth * 1000][0]  # 10^-5 meters
                # Compute SWD(mm) & SWC(mm) in active root depth for day
                if inc <= Zr:
                    Dr   += swdByLyr[lyr] / 100  #mm
                    vH2O += swcByLyr[lyr] / 100  #mm
                # Compute measured SWD(mm) & SWC(mm) in max root depth
                Drmax   += swdByLyr[lyr] / 100  #mm
                vH2Omax += swcByLyr[lyr] / 100  #mm
            # Add SWD values to dictionaries with measurement day as key
            SWDr[mykey] = Dr
            SWDrmax[mykey] = Drmax
            # Add SWC values to dictionaries with measurement day as key
            SWCr[mykey] = vH2O
            SWCrmax[mykey] = vH2Omax

        # Add SWD and SWC dictionaries to rzdata as columns
        rzdata['SWDr']    = pd.Series(SWDr)
        rzdata['SWDrmax'] = pd.Series(SWDrmax)
        rzdata['SWCr']    = pd.Series(SWCr)
        rzdata['SWCrmax'] = pd.Series(SWCrmax)

        # ****************** Calculating Observed Ks *******************
        Ks = {}
        for mykey, value in rzdata.iterrows():
            taw = self.mdl.odata.loc[mykey, 'TAW']
            raw = self.mdl.odata.loc[mykey, 'RAW']
            dr = rzdata.loc[mykey, 'SWDr']
            Ks[mykey] = sorted([0.0, (taw - dr) / (taw - raw), 1.0])[1]

        rzdata['ObsKs'] = pd.Series(Ks)

        # Populate rzdata class attribute
        self.rzdata = rzdata

