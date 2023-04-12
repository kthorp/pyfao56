"""
########################################################################
The soil_water.py module contains the SoilWater class, which provides
I/O tools for using measured volumetric soil water content data in the
pyfao56 environment. The SoilWater class is capable of storing measured
volumetric soil water content (SWC, cm3/cm3) data and computing and
storing root zone soil water deficit (SWDr, mm) data.

The soil_water.py module contains the following:
    SoilWater - A class for managing measured soil water data

10/17/2022 SWC Python functions developed by Josh Brekel, USDA-ARS
03/07/2023 SoilWater functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

import pandas as pd
import datetime

class SoilWater:
    """A class for managing measured soil water content data in pyfao56.

    Attributes
    ----------
    swcdata : DataFrame
        Volumetric soil water content data as float (cm3/cm3)
        index   - Bottom depth of soil profile layer as integer (cm)
        columns - SWC measurement dates as string ('yyyy-ddd')
#The variable name does not indicate anything about soil water deficit.
    rzdata : DataFrame
        Soil water deficit data as float (mm)
        index   - Year and day of year as string ('yyyy-ddd')
        columns - ['Year', 'DOY', 'Zr', 'SWDr', 'SWDrmax', 'SWCr',
                   'SWCrmax']
            Year    - 4-digit year (yyyy)
            DOY     - Day of year  (ddd)
            Zr      - Simulated root depth (m), FAO-56 page 279
            SWDr    - Measured SWD for root depth (mm)
            SWDrmax - Measured SWD for max root depth (mm)
            SWCr    - Measured SWC for root depth (cm3/cm3)
            SWCrmax - Measured SWC for max root depth (cm3/cm3)

    Methods
    -------
    savefile(swc_path='pyfao56tools.vswc',rzsw_path='pyfao56tools.rzsw')
        Save SoilWater attribute(s) to file(s)
    loadfile(swc_path='pyfao56tools.vswc',rzsw_path='pyfao56tools.rzsw')
        Load SoilWater attribute(s) from file(s)
    customload()
        Override this function to customize loading measured volumetric
        soil water content data.
    compute_root_zone_sw(start, end)
        Compute measured soil water deficit (mm) and measured volumetric
        soil water content (mm) in the (simulated) active root zone and
        in the maximum root zone. Populates rzdata class attribute.
    """

    def __init__(self, par=None,sol=None, swc_path=None,rzsw_path=None):
        """
        Initialize the SoilWater class attributes.

        Parameters
        ----------
        par : pyfao56 Parameters object, optional
            Used for calculating soil water deficit and for simulating
            rooting depth (default = None)
        sol : pyfao56 SoilProfile object, optional
            Used for calculating soil water deficit (default = None)
        swc_path : str, optional
            Any valid filepath for loading a soil water content file
            (default = None)
        rzsw_path : str, optional
            Any valid filepath for loading a root zone soil water file
            (default = None)

        Notes
        -----
        If the user does not load from a file, then they can use the
        customload and compute_root_zone_sw methods to populate the
        SoilWater class attributes.
        """
        # Initialize rzdata column names
        self.rz_cnames = ['Year', 'DOY', 'Zr', 'SWDr', 'SWDrmax',
                          'SWCr', 'SWCrmax']
        # Set Parameters object
        self.par = par
        # Set SoilProfile object
        self.sol = sol
        # Load the SWC class attribute
        if swc_path is not None:
            self.loadfile(swc_path=swc_path)
        else:
            self.swcdata = pd.DataFrame()
        # Load the RZSW class attribute
        if rzsw_path is not None:
            self.loadfile(rzsw_path=rzsw_path)
        else:
            self.rzdata = pd.DataFrame(columns=self.rz_cnames)

    def __str__(self, method='all'):
        """Represent the SoilWater class as a string"""

        method = method.lower()
        accepted_methods = ['all', 'vswc', 'rzsw']
        title = 'pyfao56: FAO-56 Evapotranspiration in Python'
        ast = '*' * 72
        if method not in accepted_methods:
            raise ValueError(f'{method} is not an accepted argument. '
                             f'The acceptable formats are: '
                             f'{accepted_methods}')
        elif method == 'all':
#It seems kinda weird to call a function within itself, but apparently
#this works in Python. Could it be made easier to read by first
#creating a string variable for swc, then another for rzsw, then
#put the if statement at the end to print one, the other, or both?
            swc = self.__str__(method='vswc')
            rzsw = self.__str__(method='rzsw')
            s = swc + f'\n{ast}\n' + rzsw
            return s
        elif method == 'vswc':
#I don't understand what __index__ is.  I've not used it before.
            fmts = {'__index__': '{:5d}'.format}
            for date_col in list(self.swcdata.columns.values):
                fmts[date_col] = '{:8.3f}'.format
            s = ('{:s}\n'
                 '{:s}\n'
                 'Tools: Measured Soil Water Content (cm^3/cm^3) '
                 'by Layer\n'
                 '{:s}\n'
                 'Depth').format(ast, title, ast)
            for cname in list(self.swcdata.columns.values):
                s += '{:>9s}'.format(cname)
            s += '\n'
            s += self.swcdata.to_string(header=False,
#The NaN string is only 7 characters while the formats are 8.
#Have you checked that this NaN string works as intended?
                                        na_rep='    NaN',
                                        formatters=fmts)
            return s
        elif method == 'rzsw':
            fmts = {'Year': '{:4s}'.format, 'DOY': '{:3s}'.format,
                    'Zr': '{:5.3f}'.format, 'SWDr': '{:7.3f}'.format,
                    'SWDrmax': '{:7.3f}'.format,
                    'SWCr': '{:7.3f}'.format,
                    'SWCrmax': '{:7.3f}'.format}
            s = ('{:s}\n'
                 '{:s}\n'
                 'Tools: Simulated Root Zone Depth (m) & Measured Soil '

#I'm still confused by the difference between SWD and SWC.
#Is this printing both soil water deficit and soil water content in mm?
                 'Water (mm) Data\n'
                 '{:s}\n'
                 'Year DOY    Zr    SWDr SWDrmax    SWCr SWCrmax\n'
                 ).format(ast, title, ast)
            s += self.rzdata.to_string(header=False,
                                       index=False,
                                       formatters=fmts)
            return s

#Why not provide default filenames like the other modules do?
    def savefile(self, swc_path=None, rzsw_path=None):
        """Save measured soil water data to a file.

        Parameters
        ----------
        swc_path  : str, optional
            Any valid filepath string (default = None)
        rzsw_path : str, optional
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
                f.write(self.__str__(method='vswc'))
                f.close()
        if rzsw_path is not None:
            try:
                f = open(rzsw_path, 'w')
            except FileNotFoundError:
                print('The filepath for root zone soil water data is '
                      'not found.')
            else:
                f.write(self.__str__(method='rzsw'))
                f.close()
        if (swc_path is None) & (rzsw_path is None):
            print('Please specify a filepath for data to be saved.')

#Same question as before regarding providing a default filename.
    def loadfile(self, swc_path=None, rzsw_path=None):
        """Load measured soil water data from a file.

        Parameters
        ----------
        swc_path  : str, optional
            Any valid filepath string (default = None)
        rzsw_path : str, optional
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
        if rzsw_path is not None:
            try:
                f = open(rzsw_path, 'r')
            except FileNotFoundError:
                print('The filepath for root zone soil water data is '
                      'not found.')
            else:
                lines = f.readlines()
                f.close()
                self.rzdata = pd.DataFrame(columns=self.rz_cnames)
                for line in lines[5:]:
                    line = line.strip().split()
                    year = line[0]
                    doy = line[1]
                    key = '{:04d}-{:03d}'.format(int(year), int(doy))
                    data = [year, doy]
                    for i in list(range(2, 7)):
                        data.append(float(line[i]))
                    self.rzdata.loc[key] = data
        if (swc_path is None) & (rzsw_path is None):
            print('Please specify a filepath for data to be loaded.')

    def customload(self):
        """Override this function to customize loading measured
        volumetric soil water content data for the swcdata attribute.
        """

        pass

##I think this function should be made simpler, and likely more flexible and useful.
##It could likely be broken into multiple methods.
##Giving the user flexibility to define their own root zone depth for calculations
##would make the tool more flexible.
##Consider adding a "rzdep" (root zone depth) dictionary as a class attribute.
##The keys for the dictionary are the same as the date strings in swcdata.
##There could be multiple options in how the root depth is defined.
##A separate function could quantify the root depth
##(using the model) for each date and assign the value to rzdep.
##Another function could allow users to directly specify the depth for evalution
##for a given date. I think the tool should be built around this flexibility for the
##user to provide the root depth for evaluation.
##In my experience, defining the root depth is the value of greatest uncertainty
##in evaluating depletion using FAO-56 methods.  The tool should not restrict
##the users to only the modeled estimate of root depth.
    def compute_root_zone_sw(self, start, end):
        """Compute measured soil water deficit (mm) and measured
        volumetric soil water content (mm) in the (simulated) active
        root zone and in the maximum root zone. Populates rzdata class
        attribute.

        Parameters
        ----------
        start  : str
            Root depth simulation start year and doy ('yyyy-ddd')
        end : str
            Root depth simulation end year and doy ('yyyy-ddd')

        Notes
        -----
        This method simulates rooting depth. To simulate rooting depth,
        the SoilWater class must contain a pyfao56 Parameters class.
        """

        # ********************** Error Checking ************************
        if self.par is None:
            print('Please supply a pyfao56 Parameters class, which is '
                  'needed to simulate rooting depth.')
            return

        # ****************** Computing SWD by Layer ********************
        # Make a DataFrame for measured soil water deficit from swcdata
        swddata = self.swcdata.copy()
        # Determine field capacity based on info given to the class
        if self.sol is None:
            # Copying field capacity info from par over to swddata
            swddata['thetaFC'] = [self.par.thetaFC] * swddata.shape[0]
        else:
            # Copying field capacity info over to swddata from sol
            swddata['thetaFC'] = self.sol.sdata['thetaFC'].copy()
        # Creating a list of the column names in the swddata dataframe
        cnames = list(swddata.columns.values)
        swd_dates = []
        # Loop through column names and calculate SWD on date columns
        for cname in cnames:
            if cname != 'thetaFC':
                # Create list of measurement dates
                swd_dates += [cname]
                # "Clip" sets negative SWD values to zero
                swddata[cname] = (swddata['thetaFC'] -
                                  swddata[cname]).clip(lower=0)

        # ****************** Root Depth Simulation *********************
        # Get lists of years and days of measurements from dates list
        years = []
        days = []
        for i in swd_dates:
            deconstructed_date = i.split('-')
            years += [deconstructed_date[0]]
            days += [deconstructed_date[1]]

        # Make initial dataframe out of the measurement date info
        rzdata = pd.DataFrame({'Year-DOY': swd_dates,
                               'Year': years,
                               'DOY': days})
        rzdata = rzdata.set_index('Year-DOY')
        
##This is kinda overkill.
##I envision a separate method that calculates the root depths for each 
##of the observation dates.
        # Running simulation to compute rooting depth for measurements
        startDate = datetime.datetime.strptime(start, '%Y-%j')
        endDate   = datetime.datetime.strptime(end, '%Y-%j')
        # Initialize rooting depth simulation state
        io           = self.RootState()
        io.i         = 0
        io.Zrini     = self.par.Zrini
        io.Zrmax     = self.par.Zrmax
        io.Zr        = io.Zrini
        io.Kcbini    = self.par.Kcbini
        io.Kcbmid    = self.par.Kcbmid
        io.Kcbend    = self.par.Kcbend
        io.Lini      = self.par.Lini
        io.Ldev      = self.par.Ldev
        io.Lmid      = self.par.Lmid
        io.Lend      = self.par.Lend
        tcurrent     = startDate
        tdelta       = datetime.timedelta(days=1)

        while tcurrent <= endDate:
            mykey = tcurrent.strftime('%Y-%j')
            # Advance root depth simulation
            self._advance(io)
            # Record Zr for measurement dates
            if mykey in swd_dates:
                rzdata.loc[mykey, 'Zr'] = io.Zr
            # Update state variables
            tcurrent += tdelta
            io.i     += 1

##This should probably be pulled out as a unique method.
##It should be easier for a user to read the code and understand how the values
##are computed.  Maybe the method should should work on a single measurement date.
##Then the looping and iterations are done elsewhere.

        # ****************** Computing Root Zone SW ********************
        # Setting variable for max root zone in #10^-5 meters
        rmax = self.par.Zrmax * 100000  # 10^-5 meters

        # Loop through measurement dates to compute SWD and SWC values
        SWDr    = {}
        SWDrmax = {}
        SWCr    = {}
        SWCrmax = {}
        for mykey in swd_dates:
            date = datetime.datetime.strptime(mykey, '%Y-%j')
            print(f"Computing soil water values for",
                  date.strftime("%m-%d-%Y"))
            lyr_dpths = list(swddata[mykey].index)
            # Finding root depth in 10^-5m on measurement days
            Zr = rzdata.loc[mykey, 'Zr'] * 100000  #10^-5 meters
            # Setting temp variables for SWDr and SWDrmax on meas. days
            Dr      = 0.
            Drmax   = 0.
            # Setting temp variables for SWCr and SWCrmax on meas. days
            H2Or    = 0.
            H2Ormax = 0.
            # Iterate down to max root depth in 10^-5 meters increments
            for inc in list(range(1, int(rmax + 1))):
                # Find soil layer that contains the increment
                lyr = [dpth for (idx, dpth) in enumerate(lyr_dpths)
                       if inc <= dpth * 1000][0]  #10^-5 meters
                # Compute SWD(mm) & SWC(mm) in active root depth for day
                if inc <= Zr:
                    Dr   += swddata.loc[lyr, mykey] / 100  #mm
                    H2Or += self.swcdata.loc[lyr, mykey] / 100  #mm
                # Compute measured SWD(mm) & SWC(mm) in max root depth
                Drmax   += swddata.loc[lyr, mykey] / 100  #mm
                H2Ormax += self.swcdata.loc[lyr, mykey] / 100  #mm
            # Add SWD values to dictionaries with measurement day as key
            SWDr[mykey] = Dr
            SWDrmax[mykey] = Drmax
            # Add SWC values to dictionaries with measurement day as key
            SWCr[mykey] = H2Or
            SWCrmax[mykey] = H2Ormax

        # Add SWD and SWC dictionaries to rzdata as columns
        rzdata['SWDr']    = pd.Series(SWDr)
        rzdata['SWDrmax'] = pd.Series(SWDrmax)
        rzdata['SWCr']    = pd.Series(SWCr)
        rzdata['SWCrmax'] = pd.Series(SWCrmax)

        # Populate rzdata class attribute
        self.rzdata = rzdata

##This RootState class is probably not necessary. 
##Just have a root depth calculation function that maybe creates a dictionary
##with dates as keys and root depth as the values.


    class RootState:
        """Contain parameters and states for a single timestep."""

        pass

##It may be better to just write a new function that computes root depth
##directly and bypasses the calculation of Kcb.
##I think the equations would be same as below, but just substitude Zrmax
##for Kcbmin and substitute Zrini for Kcbini.

    def _advance(self, io):
        """Advance the root simulation by one daily timestep.

        Parameters
        ----------
        io : RootState object
        """
        # Basal crop coefficient (Kcb)
        # From FAO-56 Tables 11 and 17
        s1 = io.Lini
        s2 = s1 + io.Ldev
        s3 = s2 + io.Lmid
        s4 = s3 + io.Lend
        if   0  <= io.i <= s1:
            io.Kcb = io.Kcbini
        elif s1 <  io.i <= s2:
            io.Kcb += (io.Kcbmid-io.Kcbini)/(s2-s1)
        elif s2 <  io.i <= s3:
            io.Kcb = io.Kcbmid
        elif s3 <  io.i <= s4:
            io.Kcb += (io.Kcbmid-io.Kcbend)/(s3-s4)
        elif s4 <  io.i:
            io.Kcb = io.Kcbend

        # Root depth (Zr, m) - FAO-56 page 279
        io.Zr = max([io.Zrini + (io.Zrmax-io.Zrini)*(io.Kcb-io.Kcbini) /
                     (io.Kcbmid - io.Kcbini),0.001,io.Zr])
