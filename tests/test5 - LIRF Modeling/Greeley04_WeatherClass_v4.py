from pyfao56 import Weather
import pandas as pd
import numpy as np
import datetime

#previous versions are saved as Jupyter notebooks in Bo_LIRF_Water_Balance-main
# TODO: Rework customload and import so that it takes just file path
class Greeley04(Weather):
    """A class for obtaining weather data from Greeley, Colorado

    Obtains and prepares weather data from the Greeley-04 weather
    station that is part of the CoAgMET network.
    Computes ASCE Standardized Reference Evapotranspiration for the
    resulting data set. Checks for missing weather data. The class
    inherits from the pyfao56 Weather class.

    Attributes
    ----------
    rfcrp : str
        Type of reference crop  - Short ('S') or Tall ('T')
    z : float
        Weather station elevation (z) (m)
    lat : float
        Weather station latitude (decimal degrees)
    wndht : float
        Weather station wind speed measurement height (m)
    cnames : list
        Column names for wdata
    wdata : DataFrame
        Weather data as float
        index - Year and day of year as string ('yyyy-ddd')
        columns - ['Srad','Tmax','Tmin','Tdew','RHmax','RHmin',
                   'Wndsp','Rain','ETref','MorP']
            Srad  - Incoming solar radiation (MJ/m2)
            Tmax  - Daily maximum air temperature (deg C)
            Tmin  - Daily minimum air temperature (deg C)
            Tdew  - Daily average dew point temperature (deg C)
            RHmax - Daily maximum relative humidity (%)
            RHmin - Daily minimum relative humidity (%)
            Wndsp - Daily average wind speed (m/s)
            Rain  - Daily precipitation (mm)
            ETref - Daily reference ET (mm)
            MorP  - Measured ('M') or Predicted ('P') data
    Methods
    -------
    import_GLY04_daily_dat_file(self, file_path, file_name)
        Import daily weather data from the LIRF weather station.
        Look for files at "U:\LIRF\DATA\DataLogger"
        Returns a dataframe that can be used in the customload.
    import_coag_weather_file(self, file_path, file_name)
        Import CoAgMET Daily Weather File. Returns a dataframe
        that can be used in the customload function.
    customload(self, df, rfcrp='T')
        Overridden method from the pyfao56 Weather class to provide
        customization for loading weather data from the Greeley-04
        CoAgMET weather station.
    get_etref_dataframe(self)
        Extract ETref and Date from pyfao56.wdata attribute. Returns a pandas
        dataframe of ET calculations from pyfao56 and the date.
    """

    def import_GLY04_daily_dat_file(self, file_path, file_name):
        '''Import daily weather data from the LIRF weather station.
        Look for files at "U:\LIRF\DATA\DataLogger"
        Returns a dataframe that can be used in the customload
        function.

        Parameters
        ----------
        file_path : str
            Path to the folder where the GLY04_D144 is kept
            (e.g. '../Data/')
        file_name : str
            Name of the file of daily weather data
            (e.g. 'GLY04_D144.DAT')
        '''
        # Part 1:
        # Loading in the file to be used for weather data.
        # This function is currently designed to accept csv files
        # formatted in the same way as 'GLY04_D144_LIRF_2019.dat'.

        # Reading in the file:
        df = pd.read_csv(file_path + file_name, skiprows=1, index_col=0)
        # leftover test commands
        # print(df.columns)
        # print(df.iloc[0, 23:26])
        # print(df.iloc[1, 23:26])

        # Dropping rows that do not contain observed data:
        df.drop(['TS'], inplace=True)
        df = df[df.index.notnull()]

        # Adding a column for the date and the doy, and then resetting the index.
        df.index = pd.to_datetime(df.index)
        df['Date'] = df.index
        # df['DOY'] = df.index.strftime("%j")
        df['DOY'] = [(((x - datetime.datetime(df.index[0].year, 1, 1)).days) + 1) for x in df.index]
        df = df.reset_index()

        # Cleaning up the dataframe by getting rid of unnecessary columns of data
        columns_to_drop = ['TIMESTAMP', 'AirTemp_TMx', 'AirTemp_TMn', 'SoilTemp_5cm_Max',
                           'SoilTemp_5cm_TMx', 'SoilTemp_5cm_Min', 'SoilTemp_5cm_TMn',
                           'SoilTemp_15cm_Max', 'SoilTemp_15cm_TMx', 'SoilTemp_15cm_Min',
                           'SoilTemp_15cm_TMn', 'BattVolt', 'RH_TMx', 'RH_TMn']
        df.drop(columns_to_drop, axis=1, inplace=True)

        # Changing the datatypes in the dataframe
        dtypes_dict = {}
        column_names = list(df.columns)
        d_types_list = ['float64', 'datetime64[ns]', 'int64']
        for i in column_names:
            if i == 'Date':
                dtypes_dict[i] = d_types_list[1]
            elif (i == 'DOY') | (i == 'RECORD'):
                dtypes_dict[i] = d_types_list[2]
            else:
                dtypes_dict[i] = d_types_list[0]

        for column in df:
            cdtype = df.dtypes[column]
            for key in dtypes_dict:
                if (key == column) & (cdtype != dtypes_dict[key]):
                    df[column] = df[column].astype(dtypes_dict[key])
                else:
                    pass

        # Checking and dropping NaN/null values.
        nanrows = df.isna().any(1).to_numpy().nonzero()[0]
        dropped_indices = []
        for item in nanrows:
            mykey = df.loc[item, 'Date']
            dropped_indices += [item]
            print(f'This day was dropped due to missing/bad data: {mykey}.')
        df.drop(dropped_indices, axis=0, inplace=True)
        return df

    def import_coag_weather_file(self, file_path, file_name):
        '''Import CoAgMET Daily Weather File. Returns a dataframe
        that can be used in the customload function.
        Parameters
        ----------
        file_path : str
            Path to the folder where the GLY04_D144 is kept
            (e.g. '../Data/')
        file_name : str
            Name of the file of daily weather data
            (e.g. 'GLY04_D144_LIRF_2019.dat')
        '''

        # Part 1:
        # Loading in the file to be used for weather data.
        # This function is currently designed to accept csv files
        # formatted in the same way as 'GLY04_D144_LIRF_201721.dat'.

        # Reading in the file:
        df = pd.read_csv(file_path + file_name, skiprows=0, index_col=1)

        # Dropping rows that do not contain observed data:
        df.drop(['date'], inplace=True)
        df = df[df.index.notnull()]

        # Adding a column for the date and the doy
        df.index = pd.to_datetime(df.index)
        df['DOY'] = df.index.strftime("%j")

        # Resetting the index.
        df = df.reset_index()

        # Cleaning up the dataframe by getting rid of unnecessary columns of data
        columns_to_drop = ['Station', 'Max Temp Time',
                           'Min Temp Time', 'RH Max Time', 'Avg Temp',
                           'RH Min Time', 'Gust Speed', 'Gust Time', 'Gust Dir',
                           '5cm Soil Max Temp', '5cm Soil Max Temp Time',
                           '5cm Soil Min Temp', '5cm Soil Min Temp Time',
                           '15cm Soil Max Temp', '15cm Soil Max Temp Time',
                           '15cm Soil Min Temp', '15cm Soil Min Temp Time']
        df.drop(columns_to_drop, axis=1, inplace=True)

        # Changing the datatypes in the dataframe
        dtypes_dict = {}
        column_names = list(df.columns)
        d_types_list = ['float64', 'datetime64[ns]', 'int64']
        for i in column_names:
            if i == 'Date':
                dtypes_dict[i] = d_types_list[1]
            elif (i == 'DOY'):
                dtypes_dict[i] = d_types_list[2]
                # Consider returning a string here. Might make later stuff easier.
            else:
                dtypes_dict[i] = d_types_list[0]

        for column in df:
            cdtype = df.dtypes[column]
            for key in dtypes_dict:
                if (key == column) & (cdtype != dtypes_dict[key]):
                    df[column] = df[column].astype(dtypes_dict[key])
                else:
                    pass

        # Renaming columns to match Greeley04 customload
        column_names = {'Max Temp': 'AirTemp_Max',
                        'Min Temp': 'AirTemp_Min',
                        'RH Max': 'RH_Max',
                        'RH Min': 'RH_Min',
                        'Vapor Pressure': 'Vap_Press_Avg',
                        'Precip': 'DlyRain',
                        'Wind Run': 'WindRun_Tot',
                        'Solar Rad': 'DlySolRad_Avg'}
        df.rename(columns=column_names, inplace=True)

        # Converting units of Solar radiation from w/m2 to MJ/m2 to match custload
        df['DlySolRad_Avg'] = df['DlySolRad_Avg'].multiply(0.086400)

        # Checking and dropping NaN/null values.
        nanrows = df.isna().any(1).to_numpy().nonzero()[0]
        dropped_indices = []
        for item in nanrows:
            mykey = df.loc[item, 'Date']
            dropped_indices += [item]
            print(f'This day was dropped due to missing/bad data: {mykey}.')
        df.drop(dropped_indices, axis=0, inplace=True)

        dropped_index = []
        column_names = df.columns.tolist()

        # Removing -999 entries
        for idx in df.index:
            for e in column_names:
                if df[e][idx] == -999:
                    print(f'The following row was dropped due to outlier data in {e}: {idx}')
                    if idx not in dropped_index:
                        dropped_index += [idx]
                        # print(dropped_index)
                    else:
                        pass
                else:
                    pass

        # Removing entries with obvious outlier data.
        for idx in df.index:
            if df['AirTemp_Max'][idx] <= -39:
                if idx not in dropped_index:
                    print(f'The following row was dropped due to outlier data in Max Temperature Column: {idx}')
                    dropped_index += [idx]
                else:
                    pass
            else:
                pass
            if df['AirTemp_Max'][idx] <= df['AirTemp_Min'][idx]:
                if idx not in dropped_index:
                    print(f'The following row was dropped because MaxTemp <= MinTemp: {idx}')
                    dropped_index += [idx]
                else:
                    pass
            else:
                pass
            if df['AirTemp_Min'][idx] <= -50:
                if idx not in dropped_index:
                    print(f'The following row was dropped because MinTemp is below -50C: {idx}')
                    dropped_index += [idx]
                else:
                    pass
            else:
                pass

        df.drop(dropped_index, axis=0, inplace=True)

        return df

    def customload(self, df, rfcrp='T'):
        """Prepare the wdata DataFrame with required weather data.
        Parameters
        ----------
        df : pandas DataFrame
            A dataframe that can be converted into the wdata DataFrame
        rfcrp : str, optional
            Define the reference crop (default='T')
        """

        # Part 2:
        # Assigning Weather class attributes to Greeley-specific info
        self.rfcrp = rfcrp
        self.z = 0.3048 * 4683  # converting feet to meters
        self.lat = 40.4487
        self.wndht = 2.0000

        # Set up wdata dataframe with column names but pulling data from df
        # I will make an empty dataframe to be filled with weather values, and then
        # once I have all of the values listed in the columns above, I will then
        # set the wdata attribute equal to that dataframe.
        # It will be straightforward to populate the dataframe with the data that
        # does not need a conversion. However, some columns (and the index) will
        # need to be converted in order to work. So I will need to make code blocks
        # for each of those conversions. I will focus on doing that after I get all
        # the columns that do not need conversions populated. I am wondering, though
        # if the columns need to be in the exact order as above. That makes me think
        # I might need some sort of column rearranger, or make the code operate in a
        # specific order. The former would be more flexible, but riskier since it could
        # easily lead to some issues. This is just something to consider moving forward.
        # Also, I think it is more computationally demanding to make a dataframe and then
        # grow it over time. So instead, I will make the columns into lists, make a
        # dictionary with column names as keys and the column lists as values, and then
        # make a dataframe out of the dictionary. I am a little concerned about the data
        # getting scrambled / offset / mixed up in some way on this approach, so I will
        # need to do some tests to make sure that does not occur. However, this approach
        # avoids my concerns about the column names needing to be in the right order.

        # Making column values lists for data that does not require a conversion
        # Solar Radiation
        Srad_list = df['DlySolRad_Avg'].tolist()
        # Max daily temperature
        Tmax_list = df['AirTemp_Max'].tolist()
        # Min daily temperature
        Tmin_list = df['AirTemp_Min'].tolist()
        # Daily precipitation
        Rain_list = df['DlyRain'].tolist()
        # Measured or Predicted
        MorP_list = ['M'] * (len(df.index))

        # For this version, I don't need to convert RH - just kidding
        # RH_max_list = (df['RH_Max']).tolist()
        # RH_min_list = (df['RH_Min']).tolist()

        # Lists for columns that need conversions
        # Daily average windspeed
        Wndsp_list = (df['WindRun_Tot'] / 86.4).tolist()
        # RH Max - convert from fraction to percentage
        RH_max_list = (df['RH_Max'] * 100).tolist()
        # RH Min - convert from fraction to percentage
        RH_min_list = (df['RH_Min'] * 100).tolist()
        # Tdew - generate data based on the data I have??
        # An Introduction of Environmental Biophysics (Campbell and Norman, 2nd ed.)
        # has equations for calculating dew point temperature from constants and
        # vapor pressure. The equation is described in pages 42-44.
        # Constants from p. 41 of Campbell and Norman, 2nd ed.
        A = 0.611
        B = 17.502
        C = 240.97
        # Equation 3.14 (44, Campbell and Norman, 2nd ed.)
        Tdew_list = ((C * np.log(df['Vap_Press_Avg'] / A)) / (B - np.log(df['Vap_Press_Avg'] / A))).tolist()
        # Tdew_list = [float('NaN')] * (len(df.index))

        # Calculate reference ET and create a list out of it
        # I don't really want to do this until I have the customload function
        # in the child class completed. So I have a stand in for now.
        ETref_list = [float('NaN')] * (len(df.index))
        # Interestingly, Kelly also sets ETref to non/NaN until the dataframe is set.
        # So, maybe this is the intended way to do this? I am not sure.
        # Create a list of lists for values, then a dictionary, then a dataframe
        # Create a list of column data lists, with the columns in order
        list_of_lists = [Srad_list, Tmax_list, Tmin_list, Tdew_list, RH_max_list,
                         RH_min_list, Wndsp_list, Rain_list, ETref_list, MorP_list]
        # Create a dictionary with column names as keys, list of lists as values
        col_names = self.cnames
        wth_dictionary = dict(zip(col_names, list_of_lists))
        # Create a dataframe from the dictionary
        wthdata = pd.DataFrame.from_dict(wth_dictionary)

        # Need to make a list to use as the index in my dataframe of weather values
        # First, I will make a list of strings of the year for each entry
        year_list = []
        ## Debugging: for some reason, the doy is off by one. My fix isn't the best one,
        ## but it should work.
        #         for idx in df.index:
        #             year_list += [df['Date'][idx].strftime("%Y-%j")]
        for idx in df.index:
            year_list += [(df['Date'][idx] - datetime.timedelta(1)).strftime("%Y-%j")]

        # Then, I will loop through the DOY column of df, and append the year strings
        # Setup for loop. for idx in df.['DOY']:
        # for idx in df.index:
        # doy = df['DOY'][idx]
        # if DOY < 10, append yearlist[idx] '-00' + str(DOY)
        # if doy < 10:
        # year_list[idx] = year_list[idx] + '-00' + str(doy)
        # elif DOY < 100, append yearlist[idx] '-0' + str(DOY)
        # elif doy < 100:
        # year_list[idx] = year_list[idx] + '-0' + str(doy)
        # else append yearlist[idx] '-' + str(DOY)
        # else:
        # year_list[idx] = year_list[idx] + '-' + str(doy)

        # Now that I have my list of strings in the right format, I need to set them
        # to the index for the wthdata data frame.
        wthdata['Year-DOY'] = year_list
        # This makes the list of strings a column
        # wthdata.set_index('Year-DOY') - turns out this messes up the output.
        # need to set the index after assigning the attribute

        # Debugging attempt: Force data types
        dtypes_dict = {'Srad': 'float64',
                       'Tmax': 'float64',
                       'Tmin': 'float64',
                       'Tdew': 'float64',
                       'RHmax': 'float64',
                       'RHmin': 'float64',
                       'Wndsp': 'float64',
                       'Rain': 'float64',
                       'ETref': 'float64',
                       'MorP': 'string',
                       'Year-DOY': 'string',
                       }
        for column in wthdata:
            cdtype = wthdata.dtypes[column]
            for key in dtypes_dict:
                if (key == column) & (cdtype != dtypes_dict[key]):
                    wthdata[column] = wthdata[column].astype(dtypes_dict[key])
                else:
                    pass

        # Assign self.wdata to the dataframe.
        self.wdata = wthdata
        self.wdata.set_index('Year-DOY', inplace=True)
        self.wdata.index.name = None
        # self.wdata.drop_duplicates(subset='Date',keep='first',
        # inplace=True)
        # print(self.wdata.index.dtype)
        # print(wthdata.dtypes)
        # print(self.wdata.dtypes)

        # Calculate ASCE Standardized Reference ET using the ETref utility
        for index, row in self.wdata.iterrows():
            etref = self.compute_etref(index)
            self.wdata.loc[index, 'ETref'] = etref

    def get_etref_dataframe(self):
        '''
        Extract ETref and Date from pyfao56.wdata attribute. Returns a pandas
        dataframe of ET calculations from pyfao56 and the date.
        '''
        # Getting a copy of the weather dataset
        df = self.wdata.copy()

        # Getting a date column and resetting the index. My comparison just uses ET and Date
        df['Date'] = df.index
        df.reset_index(inplace=True, drop=True)

        # Setting the date column to string dtype to avoid parsing errors
        df = df.astype({'Date': 'string'}).dtypes

        # Getting a column of dates formatted like my other dataframes's dates
        for idx in df.index:
            df['Date'][idx] = datetime.datetime.strptime(df['Date'][idx], '%Y-%j').date()

        # Making sure date is in the datetime dataformat
        df = df.astype({'Date': 'datetime64[ns]'}).dtypes

        # Dropping columns not needed for comparison
        columns_to_drop = ['Srad', 'Tmax', 'Tmin', 'Tdew', 'RHmax',
                           'RHmin', 'Wndsp', 'Rain', 'MorP']
        df.drop(columns_to_drop, axis=1, inplace=True)

        # Renaming ET column to something more informative
        df.rename({'ETref': 'pyfao56_ETr'}, axis=1, inplace=True)

        return df