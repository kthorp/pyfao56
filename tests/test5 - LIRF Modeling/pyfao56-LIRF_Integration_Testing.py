# 8_10_22 Note:
# I am making this file to test the integration of pyfao56 and my new
# soil water class. It will be really similar to the E12FF_2022.py file,
# but it will utilize the new soil water class.

import pyfao56 as fao
from Greeley04_WeatherClass_v4 import Greeley04
from pyfao56_LIRF_features.src.pyfao56.model import Model
from pyfao56_LIRF_features.src.pyfao56.soil_water import SoilWater
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt


def run_e12_22():
    """Run pyfao56 with swc testing for E12FF in 2022 LIRF study"""

    # Creating a formatted date to add onto saved files
    date = datetime.today().strftime('%m_%d_%Y')

    # # PARAMETERS
    # Instantiate the parameters class of pyfao56
    par = fao.Parameters()
    # Kcb initial, mid, and end
    par.Kcbini = 0.15  # taken from WaterBalance, "Raw Data", cellB262
    par.Kcbmid = 0.96  # taken from WaterBalance, "Raw Data", cellB264
    par.Kcbend = 0.50  # pyfao56 default value
    # Length Stage Initial (days) from table 11 p. 106 is:
    par.Lini = 30
    # Length Stage Development (days) is:
    par.Ldev = 40
    # Length Stage Mid (days) is:
    par.Lmid = 50
    # Length Stage End (days) is:
    par.Lend = 50
    # Plant height is given in meters.
    # I am not sure what to put here, so I set it to the default value.
    par.hini = 0.05
    # FAO56 table 12, p. 111
    par.hmax = 2
    # thetaFC is volumetric soil water content at field capacity (cm3/cm3)
    # to run pyfao56 normally, this should be a weighted average of the
    # thetaFC values through the entire root zone.
    # I will define it as a weighted average, but my soil water class
    # should give me the ability to use thetaFC for each specific soil layer.
    # weighted average thetaFC = 217.4/1050
    par.thetaFC = 217.4 / 1050
    # The soil water class should make it so that the theta0 parameter is
    # not used. To ensure that is the case, I am going to set it to -999.
    par.theta0 = -999
    # thetaWP is volumetric soil water content at wilting point (cm3/cm3)
    # Since the WaterBalance sets TEW to 12, it implicitly assumes that
    # PWP is approximately half of field capacity.
    par.thetaWP = (par.thetaFC / 2)
    # Zrini is the initial rooting depth (m)
    # I pulled this from the WaterBalance Spreadsheet where it was given
    # in mm
    par.Zrini = 0.05
    # Zrmax is the maximum rooting depth (m) taken from FAO-56 Table 22
    # WaterBalance spreadsheet, and Clutter and DeJonge 2022 paper on
    # soil moisture measurements
    par.Zrmax = 1.05
    # pbase is the Depletion fraction (p), taken from FAO-56 Table 22.
    par.pbase = 0.55
    # Ze is the depth of surface evaporation layer (m) taken from FAO-56
    # The current WaterBalance model assumes TEW = 12 mm.
    # That assumption is used below to calculate Ze using FAO-56 eq. 73.
    # FAO-56 eq. 73 in terms of Ze
    ze = 12 / (1000 * (par.thetaFC - 0.5 * par.thetaWP))
    par.Ze = ze
    # REW is the total depth Stage 1 evaporation (mm) taken from FAO-56
    # table 19, page 144.
    par.REW = 8
    # I split the difference between 6 and 10...not sure what else to put

    # # WEATHER
    # Instantiate the Greeley 04 Weather Class with the overriding customload function
    wthr = Greeley04()
    # Set the names of the folder path and file paths of the daily
    # weather file so python can find it
    out_folder_name = "C:/Users/joshua.brekel/python_projects/" \
                      "pyfao56_LIRF_features/pyfao56_LIRF_features/tests" \
                      "/test5 - LIRF Modeling/Output folder/"
    wdata_folder_name = 'U:/LIRF/DATA/DataLogger/'
    # file_name = 'GLY04_D144.dat'
    file_name = 'GLY04_D144.dat.backup'
    # Use the weather class's import functions to generate daily weather dataframe
    weather_df = wthr.import_GLY04_daily_dat_file(file_path=wdata_folder_name,
                                                  file_name=file_name)
    # Use customload function to feed daily weather raw data into the model wdata dataframe
    wthr.customload(weather_df, rfcrp='T')
    # Use the savefile function to save the weather dataframe as a text file
    wthr.savefile(filepath=f'{out_folder_name}GLY04_Weather_File_{date}.wth')

    # # IRRIGATION
    # Specify the irrigation schedule for the treatment
    # Instantiate an irrigation data class
    irr = fao.Irrigation()
    # I will use the 2022 WaterBalance Spreadsheet to add events
    # and then save them to a file
    irr.addevent(2022, 165, 25.4, 1.0)
    irr.addevent(2022, 172, 25.4, 1.0)
    irr.addevent(2022, 179, 27.7, 1.0)
    irr.addevent(2022, 182, 15.0, 1.0)
    irr.addevent(2022, 187, 16.4, 1.0)
    irr.addevent(2022, 190, 17.0, 1.0)
    irr.addevent(2022, 193, 33.0, 1.0)
    irr.addevent(2022, 196, 19.0, 1.0)
    irr.addevent(2022, 200, 28.0, 1.0)
    irr.addevent(2022, 203, 23.0, 1.0)
    irr.addevent(2022, 207, 26.0, 1.0)
    irr.addevent(2022, 214, 26.3, 1.0)
    irr.addevent(2022, 217, 18.0, 1.0)
    irr.addevent(2022, 221, 26.0, 1.0)
    # Saving Irrigation Information to a file that can be used/updated later
    irr.savefile(filepath=f'{out_folder_name}GLY04Irrigation_File_{date}.irr')

    # # SOIL WATER CLASS
    # Instantiate the class
    dep = (0.15, 0.30, 0.60, 0.90, 1.20, 1.50, 2.00)
    pro = ((0, 0.15), (0.15, 0.45), (0.45, 0.75), (0.75, 1.05), (1.05, 1.35), (1.35, 1.65), (1.65, 2.15))
    fc = (0.29, 0.24, 0.182, 0.158, 0.120, 0.108, 0.144)
    ini = (0.083, 0.058, 0.039, 0.033, 0.012, 0.005, 0.014)
    wp = (fc[0] / 2, fc[1] / 2, fc[2] / 2, fc[3] / 2, fc[4] / 2, fc[5] / 2, fc[6] / 2)
    swc = SoilWater(depths=dep, theta_fc=fc, theta_ini=ini,
                    layer_boundaries=pro, theta_wp=wp)
    # Creating Root Zone Curve for E12FF
    # swc.projected_root_zone_curve(planting_date="2022-129",
    #                               end_date="2022-304",
    #                               full_rz_dap=98)
    # # Setting the Soil Water Profile Variables
    # dep = (0.15, 0.30, 0.60, 0.90, 1.20, 1.50, 2.00)
    # pro = ((0, 0.15), (0.15, 0.45), (0.45, 0.75), (0.75, 1.05), (1.05, 1.35), (1.35, 1.65), (1.65, 2.15))
    # # The three thetas that follow are the ones that I think should work.
    # fc = (0.29, 0.24, 0.182, 0.158, 0.120, 0.108, 0.144)
    # ini = (0.083, 0.058, 0.039, 0.033, 0.012, 0.005, 0.014)
    # wp = (fc[0] / 2, fc[1] / 2, fc[2] / 2, fc[3] / 2, fc[4] / 2, fc[5] / 2, fc[6] / 2)

    # swc.create_soil_water_profile(depths=dep, theta_fc=fc, theta_ini=ini,
    #                               layer_boundaries=pro, theta_wp=wp)
    print(swc.__str__())
    # print(swc.__str__()[0], '\n', swc.__str__()[1])
    # print(swc.soil_water_profile)

    # # # MODEL
    # mdl = Model('2022-129', '2022-223', par=par, wth=wthr, irr=irr,
    #             swc=swc)
    # # Run the model
    # mdl.run()
    # print(mdl)
    # # Save the model to file
    # mdl.savefile(f'{out_folder_name}Model_SWC_Integration_Testing_{date}')
    #
    #
    #
    # # # Prototyping Evaluation / Visualization Tool
    # # # SWD graph
    # new_odata = mdl.odata.loc[:, ~mdl.odata.columns.duplicated()].copy()
    # sns.lineplot(data=new_odata, x='DOY', y='Dr')
    # plt.xticks([6, 16, 26, 36, 46, 56, 66, 76, 86, 96, 106, 116, 126, 136, 146, 156, 166, 176])
    # plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    # plt.show()
    # # ETr vs Tc vs DOY Graph:
    # # sns.lineplot(data=new_odata, x='DOY', y='ETref', color='blue')
    # # sns.lineplot(data=new_odata, x='DOY', y='T', color='red')
    # # plt.xticks([6, 16, 26, 36, 46, 56, 66, 76, 86, 96, 106, 116, 126, 136, 146, 156, 166, 176])
    # # plt.yticks([0, 2, 4, 6, 8, 10, 12, 14])
    # # plt.show()
    # # RAW over time graph
    # # sns.lineplot(data=new_odata, x='DOY', y='RAW')
    # # plt.show()
    # # Ks over time graph
    # # sns.lineplot(data=new_odata, x='DOY', y='Ks')
    # # plt.show()


run_e12_22()
