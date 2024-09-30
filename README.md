# pyfao56
A Python implementation of the FAO-56 dual crop coefficient approach for crop water use estimation and irrigation scheduling

The pyfao56 Python package facilitates FAO-56 computations of daily soil water balance using the dual crop coefficient method to estimate crop evapotranspiration (ET).

The FAO-56 method is described in the following documentation:
[Allen, R. G., Pereira, L. S., Raes, D., Smith, M., 1998.  FAO Irrigation and Drainage Paper No. 56. Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements. Food and Agriculture Organization of the United Nations, Rome Italy.](http://www.fao.org/3/x0490e/x0490e00.htm)

Reference ET is computed using the ASCE Standardized Reference ET Equation, which is described in the following documentation:
[ASCE Task Committee on Standardization of Reference Evapotranspiration (Walter, I. A., Allen, R. G., Elliott, R., Itenfisu, D., Brown, P., Jensen, M. E.,Mecham, B., Howell, T. A., Snyder, R., Eching, S., Spofford, T., Hattendorf, M., Martin, D., Cuenca, R. H., Wright, J. L.), 2005. The ASCE Standardized Reference Evapotranspiration Equation. American Society of Civil Engineers, Reston, VA.](https://ascelibrary.org/doi/book/10.1061/9780784408056)

## Source Code
The main pyfao56 package contains the following modules:
* autoirrigate.py - I/O tools to specify parameters for autoirrigation
* irrigation.py - I/O tools to specify irrigation schedules explicitly
* model.py - Equations for daily soil water balance computations
* parameters.py - I/O tools for required input parameters
* refet.py - Equations for computing ASCE Standardized Reference ET
* soil_profile.py - I/O tools to define stratified soil layer properties
* update.py - I/O tools and methods for state variable updating
* weather.py - I/O tools for required weather information

The source code is available [here](http://github.com/kthorp/pyfao56/). It uses a basic object-oriented design with separate classes to make FAO-56 calculations and to manage parameter, weather, irrigation management, and soil profile data. [Pandas](https://pandas.pydata.org/) data frames are used for data storage and management. Further documentation of the class structure is contained in the source files.

The pyfao56 package contains a subpackage called [tools](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/tools), which has several modules to facilitate model use as follows:
* forecast.py - Obtain a seven-day weather forecast from the National Digital Forecast Database ([NDFD](https://graphical.weather.gov/xml/rest.php))
* soil_water.py - I/O tools for managing measured volumetric soil water content data and computing root zone soil water metrics from those measurements
* visualization.py - Develop plots to visualize measured and simulated data for root zone soil water depletion and evapotranspiration
* statistics.py - Compute 15 goodness-of-fit statistics between measured and simulated data

The pyfao56 package also contains a subpackage called [custom](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/custom). Here, users can add customized scripts to improve their personal pyfao56 workflows. For example, the [custom](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/custom) subpackage contains modules for development of customized weather files using data from the Arizona Meteorological Network ([AZMET](https://ag.arizona.edu/azmet/)) station at Maricopa, Arizona and from the National Digital Forecast Database ([NDFD](https://graphical.weather.gov/xml/rest.php)). These modules were developed to facilitate irrigation management for field studies conducted at the Maricopa Agricultural Center. Users can follow this example to create customized weather tools for other weather data sources. Additionally, the [custom](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/custom) subpackage contains a module for customizing the creation of soil files using ordered lists of soil water holding limits and initial soil water content data.

## Install
`pip install pyfao56`

## Quickstart

### Import the package
`import pyfao56 as fao`

### Specify the model parameters
* Instantiate a Parameters class: `par = fao.Parameters()`
* To print parameter values: `print(par)`
* To adjust parameter values: `par.Kcbmid = 1.225`
* To load values from a file: `par.loadfile('myfilename.par')`
* To write values to a file: `par.savefile('myfilename.par')`

An example of the parameter file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.par).

### Specify the weather information
* Instantiate a Weather data class: `wth = fao.Weather()`
* To print weather data: `print(wth)`
* To load data from a file: `wth.loadfile('myfilename.wth')`
* To write data to a file: `wth.savefile('myfilename.wth')`
* To compute daily reference ET for yyyy-ddd (4-digit year and day of year): `refet = wth.compute_etref('2021-150')`

An example of the weather file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.wth).

Users can customize loading of weather data with wth.customload(). The azmet_maricopa.py module in the [custom](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/custom) subpackage provides an example for developing a custom weather data class that inherits from Weather and overrides its customload() function.

### Specify the irrigation management information
* Instantiate an Irrigation data class: `irr = fao.Irrigation()`
* To print irrigation data: `print(irr)`
* To load data from a file: `irr.loadfile('myfilename.irr')`
* To write data to a file: `irr.savefile('myfilename.irr')`
* To add an irrigation event (provide yyyy, ddd, depth in mm, and fw): `irr.addevent(2019, 249, 28.3, 1.00)`
* Optionally, add an irrigation efficiency (default = 100.0%): `irr.addevent(2019, 249, 28.3, 1.00, 95.0)`

An example of the irrigation file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cottondry2013.irr).

### Run the daily soil water balance model
* Instantiate a Model class (provide starting yyyy-ddd, ending yyyy-ddd, and classes for Parameters, Weather, and optionally Irrigation): `mdl = fao.Model('2013-113','2013-312', par, wth, irr=irr)`
* To run the model: `mdl.run()`
* To print the output: `print(mdl)`
* To save the output to file: `mdl.savefile('myoutputfile.out')`

An example of the model output file is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cottondry2013.out).

### Specify a layered soil profile (optional)
* Instantiate a SoilProfile class: `sol = fao.SoilProfile()`
* To load data from a file: `sol.loadfile('myfilename.sol')`
* To write data to a file: `sol.savefile('myfilename.sol')`
* Instantiate a Model class with stratified soil layer data (provide starting yyyy-ddd, ending yyyy-ddd, and classes for Parameters, Weather, Irrigation, and SoilProfile): `mdl = fao.Model('2019-108','2019-274', par, wth, irr=irr, sol=sol)`
* To run the model: `mdl.run()`

An example of the soil file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test5/E12FF2022.sol).

Users can customize loading of soil profile data with sol.customload(). The example_soil.py module in the custom subpackage provides an example for developing a custom soil data class that inherits from SoilProfile and overrides its customload() function.

### Run the daily soil water balance model with autoirrigation (optional)
* Instantiate an AutoIrrigate class: `airr = fao.AutoIrrigate()`
* Add one (or more) autoirrigation parameter set(s): `airr.addset('2018-108','2018-250',mad=0.4)`
* Instantiate a Model class with autoirrigation enabled: `mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)`
* To run the model: `mdl.run()`

There are currently 25 parameters that can be used to customize the autoirrigation computation. The autoirrigation parameters are described in the comments of the [autoirrigate.py module](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/autoirrigate.py). Furthermore, the [cotton2018.py module](https://github.com/kthorp/pyfao56/tree/main/tests/test9/cotton2018.py) in [test9](https://github.com/kthorp/pyfao56/tree/main/tests/test9/) provides many examples of various ways to implement the autoirrigation method.

### Update basal crop coefficients (Kcb), crop height (h), or crop cover (fc) (optional)
* Instantiate an Update class: `upd = fao.Update()`
* To load data from a file: `upd.loadfile('myfilename.upd')`
* To write data to a file: `upd.savefile('myfilename.upd')`
* Instantiate a model class with updating (provide starting yyyy-ddd, ending yyyy-ddd, and classes for Parameters, Weather, Irrigation, and Updates): `mdl = fao.Model('2019-108','2019-274', par, wth, irr=irr, upd=upd)`
* To run the model: `mdl.run()`

An example of the update file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test3/cotton2019.upd).

## Further examples
Further example scripts for setting up and running the model are [here](https://github.com/kthorp/pyfao56/tree/main/tests).

[test1](https://github.com/kthorp/pyfao56/tree/main/tests/test1) - The cottondry2013.py  and cottonwet2013.py modules contain code to setup and run pyfao56 for the water-limited and well-watered treatments for a 2013 cotton field study at Maricopa, Arizona.

[test2](https://github.com/kthorp/pyfao56/tree/main/tests/test2) - The refet_testA.py module contains a function to compare the short crop reference evapotranspiration (ETo) calculation from the pyfao56 refet.py module with ETo reported by the [AZMET](https://ag.arizona.edu/azmet/) station at Maricopa, Arizona for 2003 through 2020. The refet_testB.py module contains a function to compare the daily short crop reference evapotranspiration (ETo) and daily tall crop reference evapotranspiration (ETr) calculations from the pyfao56 refet.py module with ETo and ETr computed by [Ref-ET software](https://www.uidaho.edu/cals/kimberly-research-and-extension-center/research/water-resources/ref-et-software) based on weather data from the [AZMET](https://ag.arizona.edu/azmet/) station at Maricopa, Arizona for 2003 through 2020. The refet_testC.py module contains a function to compare the hourly ETo and hourly ETr from the pyfao56 refet.py module with ETo and ETr computed by [Ref-ET software](https://www.uidaho.edu/cals/kimberly-research-and-extension-center/research/water-resources/ref-et-software) based on weather data from the [AZMET](https://ag.arizona.edu/azmet/) station at Maricopa, Arizona for 2003 through 2020.

[test3](https://github.com/kthorp/pyfao56/tree/main/tests/test3) - The updateKcb.py module contains a function to setup and run pyfao56 with basal crop coefficient (Kcb) updates for Zone 12-11 in a 2019 cotton field study at Maricopa, Arizona. The Kcb was estimated from fractional cover measurements based on weekly imagery from a small unoccupied aircraft system (sUAS).

[test4](https://github.com/kthorp/pyfao56/tree/main/tests/test4) - The cotton2018.py module contains code to setup and run pyfao56 for water-limited and well-watered treatments for a 2018 cotton field study at Maricopa, Arizona.

[test5](https://github.com/kthorp/pyfao56/tree/main/tests/test5) - The cornE12FF2022.py module contains code to setup and run several pyfao56 scenarios (including instances that use the SoilProfile class, the Update class, and both together) for a full-irrigation treatment in a 2022 maize study at Greeley, Colorado.

[test6](https://github.com/kthorp/pyfao56/tree/main/tests/test6) - The cotton2022.py module contains code to setup and run pyfao56 for a full-irrigation treatment in a 2022 cotton study at Maricopa, Arizona and to demonstrate the SoilWaterSeries class for computing root zone soil water depletion from  measured soil water content data. The Visualization and Statistics classes are also demonstrated.

[test7](https://github.com/kthorp/pyfao56/tree/main/tests/test7) - The cornE42FF2023.py module contains code to setup and run pyfao56 for a full-irrigation treatment in a 2023 maize study at Greeley, Colorado and to demonstrate the Visualization class for visualizing root zone soil water depletion and evapotranspiration time series. The SoilWaterSeries and Statistics classes are also demonstrated.

[test8](https://github.com/kthorp/pyfao56/tree/main/tests/test8) - The runoff.py module contains code to setup and run pyfao56 while considering surface runoff for field conditions in McLean County, Illinois. A customized figure is created to demonstrate the water balance with surface runoff enabled.

[test9](https://github.com/kthorp/pyfao56/tree/main/tests/test9) - The cotton2018.py module contains code to setup and run pyfao56 for a well-watered treatment in a 2018 cotton field study at Maricopa, Arizona. The module provides many examples of ways to parameterize the autoirrigation methododogy in pyfao56.

## Detailed Startup Information
### Core Functionality
The core pyfao56 model was originally designed to follow the [FAO-56](http://www.fao.org/3/x0490e/x0490e00.htm) methodology in the strictest and purest sense. To implement the model, users must first populate two pyfao56 classes with appropriate data: Parameters and Weather. Together, these two classes represent the minimum data inputs that users must provide to conduct a simulation. Irrigation data is also often provided via the Irrigation class, although with version 1.2, irrigation data is not strictly required, and the model will run without it.

After the input classes are created and populated, users must then instantiate a Model class by providing the simulation starting date ('yyyy-ddd'), simulation ending date ('yyyy-ddd'), and the instances of the Parameters, Weather, and other optional classes. Users can then run the daily soil water balance model by calling the "run()" method of the Model class.

Each pyfao56 simulation is intended to model a single realization of the crop system (i.e., a single treatment, plot, sub-plot, or other homogenous area). Users can iterate simulations among different model realizations by instantiating multiple pyfao56 classes of a particular type (i.e., Parameters, Irrigation, SoilProfile, Model, etc.) and conducting iterative simulations with different input class combinations. The [test scripts](https://github.com/kthorp/pyfao56/tree/main/tests) provide simple examples of this, while more complex applications are possible.

### Optional Functionality
The pyfao56 package also provides optional functionality that is intended to enhance the implementation of FAO-56 methodology. While the following enhancements may be beneficial for some users, their methodologies are not specifically described in FAO-56.

* #### AutoIrrigate Class
While users can specify irrigation management schedules explicitly using the Irrigation class, the AutoIrrigate class was developed for pyfao56 to compute irrigation schedules automatically, based on model states and other user-defined contraints for irrigation decisions. The AutoIrrigate class provides 25 parameters that can be used to customize automatic irrigation scheduling in pyfao56. Parameters for controlling autoirrigation timing include the start and end dates for the autoirrigation time period, day(s) of the week that irrigation is permitted, consideration of forecasted precipitation events, managment allowed depletion, the transpiration reduction coefficient (Ks) below a critical value, and days since last irrigation or watering event. When autoirrigation is triggered, the default irrigation amount is the root-zone soil water depletion (Dr, mm). Parameters to adjust this amount include a constant application depth, a targeted depletion (i.e., deficit irrigation), a variety of ET replacement options, an adjustment of the default rate by a fixed percentage, an adjustment for irrigation efficiency, and limits for minimum and maximum irrigation application amount. The Model class can be instantiated with an Irrigation class, an AutoIrrigate class, or both or neither.

* #### SoilProfile Class
The SoilProfile class enables input of stratified soil layer information to the model. If available, layered soil profile data should improve the estimates of total available water (TAW) and soil water depletion (Dr) in pyfao56. When including a SoilProfile class in the simulation, the model ignores the thetaFC, thetaWP, and theta0 inputs provided in the Parameters class. Because standard FAO-56 methodology considers only a single, homogenous soil layer, the SoilProfile class can enhance the representation of the soil profile and improve estimates of TAW and Dr when layered soil profile information is available. However, the soil water balance is still computed for the entire root zone and not for individual soil layers.

* #### Update Class
The Update class enables users to update key state variables during the model simulation. At this time, the following variables can be updated: basal crop coefficients (Kcb), crop height (h), and crop cover (fc). When the pyfao56 Update class is populated and provided as an input to the Model class, pyfao56 overwrites model state variables with the data provided in the Update class.

* #### Surface Runoff
By default, pyfao56 does not consider surface runoff. However, the [ASCE Manual of Practice #70](https://ascelibrary.org/doi/book/10.1061/9780784414057) describes a straightforward surface runoff algorithm that integrates well with the FAO-56 dual crop coefficient method. Based on the USDA-NRCS curve number (CN) approach, the method uses readily evaporable water (REW), total evaporable water (TEW), and cumulative depth of evaporation (De) variables from the FAO-56 water balance to compute CN for surface runoff estimation. The method requires an additional input parameter, the curve number for antecedent water condition 2 (CN2), which can be specified in the Parameters class. Users can run the model with surface runoff by issuing `roff=True` at Model instantiation: `mdl = fao.Model('2019-108', '2019-274', par, wth, irr=irr, roff=True)`. By default, the model is instantiated with `roff=False` and surface runoff is not considered.

* #### Constant Depletion Fraction
The pyfao56 Model class provides an argument to optionally set the TAW depletion fraction (p) to a constant value. FAO-56 specifies a methodology for varying the depletion fraction based on daily crop evapotranspiration (ETc) (see [FAO-56 page 162 and Table 22](https://www.fao.org/3/x0490e/x0490e0e.htm#readily%20available%20water%20(raw))). However, FAO-56 also discusses using constant values for depletion fraction (see [FAO-56 page 162](https://www.fao.org/3/x0490e/x0490e0e.htm#readily%20available%20water%20(raw)) and [Annex 8](https://www.fao.org/3/x0490e/x0490e0p.htm#annex%208.%20calculation%20example%20for%20applying%20the%20dual%20kc%20procedure%20in%20irrigation%20sc)). Annex 8 of FAO-56 suggests setting a constant depletion fraction equal to the management allowed depletion (MAD). Using a constant depletion fraction makes readily available water (RAW) vary only with rooting depth (Zr). Users can run the model with a constant depletion fraction by issuing `cons_p=True` at Model instantiation: `mdl = fao.Model('2019-108', '2019-274', par, wth, irr=irr, cons_p=True)`. By default, the model is instantiated with `cons_p=False`, which leads to depletion fraction adjustments with ETc.

* #### Curvilinear Ks
By default, pyfao56 uses the linear computation of Ks as a function of root zone soil water depletion (Dr) when Dr is greater than readily available water (RAW), as described in FAO-56. [Maize field studies in Colorado](https://doi.org/10.1061/(ASCE)IR.1943-4774.0001600) suggested that a curvilinear relationship between Ks and Dr, as used in the AquaCrop model, was better than the linear computation from FAO-56. Users can run the model with the curvilinear Ks computation by issuing `aq_ks=True` at Model instatiation: `mdl = fao.Model('2019-108', '2019-274', par, wth, irr=irr, aq_ks=True)`. By default, the model is instantiated with `aq_ks=False`, which defaults to the linear Ks computation from FAO-56.

### Supporting Tools
* #### Forecast Class
The Forecast class is used to retrieve seven-day weather forecasts from the National Digital Forecast Database (NDFD). It uses the REST approach, which was more robust than the SOAP method, in terms of server responsiveness. Data is retrieved for computation of ASCE Standardized Reference Evapotranspiration, including wind speed (m/s) and minimum, maximum, and dew point air temperatures (degrees C). Solar radiation forecasts are not directly provided by NDFD, but NDFD does provide cloud cover forecasts. By providing the optional "elevation" parameter, users can obtain solar radiation forecasts computed by multiplication of cloud cover and clear-sky solar radiation. (However, these soil radiation forecasts were found unreliable at Maricopa, Arizona.) Liquid precipitation forecasts (mm) are also obtained. The NDFD provides wind speed forecasts at 10 m height. The Forecast class contains methods to convert the 10 m wind speeds to the anemometer height of the local weather station. Wind speeds from different sources should be represented at matching heights.

* #### SoilWaterSeries Class
The SoilWaterSeries class provides I/O tools for processing measured volumetric soil water content (SWC, cm3/cm3) data in the pyfao56 environment. The SoilWaterSeries class manages SWC data collected at one location over time (e.g., at one access tube over a growing season). A subclass called SoilWaterProfile handles data storage and computations for one soil water profile measurement event (i.e., measurements of the soil water profile on a single date). The SoilWaterProfile class computes root zone soil water metrics, especially the root zone soil water depletion (SWD, mm), given estimates of root depth.

* #### Visualization Class
The Visualization class provides tools for visualizing pyfao56 Model output with measured soil water data represented in the SoilWaterSeries class. The methods use Python's matplotlib library to format time series plots of soil water depletion, evapotranspiration, and crop coefficient data.

* #### Statistics Class
The Statistics class provides computations of 15 goodness-of-fit statistics when provided arrays of simulated and measured data. Computed statistics include bias, relative bias, percent bias, maximum error, mean error, mean absolute error, sum of squared error, Pearson's correlation coefficient, coefficient of determination, root mean squared error, relative root mean squared error, percent root mean squared error, coefficient of residual mass, the Nash & Sutcliffe (1970) model efficiency, and the Willmott (1981) index of agreement.

## Further information
The pyfao56 package is further described in the following articles:

Thorp, K. R., 2022. pyfao56: FAO-56 evapotranspiration in Python. SoftwareX 19, 101208. [doi:10.1016/softx.2022.101208](https://doi.org/10.1016/j.softx.2022.101208).

Brekel, J., Thorp, K. R., DeJonge, K. C., Trout, T. J., 2023. Version 1.1.0 - pyfao56: FAO-56 evapotranspiration in Python. SoftwareX 22, 101336. [doi:10.1016/j.softx.2023.101336](https://doi.org/10.1016/j.softx.2023.101336).

Thorp, K. R., Brekel, J., DeJonge, K. C., 2023. Version 1.2.0 - pyfao56: FAO-56 evapotranspiration in Python. SoftwareX 24, 101518. [doi.10.1016/j.softx.2023.101518](https://doi.org/10.1016/j.softx.2023.101518).

Thorp, K. R., DeJonge, K. C., Pokoski, T., Gulati, D., Kukal, M., Farag, F., Hashem, A., Erismann, G., Baumgartner, T., Holzkaemper, A., 2024. Version 1.3.0 - pyfao56: FAO-56 evapotranspiration in Python. SoftwareX 26, 101724. [doi:10.1016/j.softx.2024.101724](https://doi.org/10.1016/j.softx.2024.101724).

DeJonge, K. C., Thorp, K. R., Brekel, J., Pokoski, T., Trout, T. J., 2024. Customizing pyfao56 for evapotranspiration estimation and irrigation scheduling at the Limited Irrigation Research Farm (LIRF), Greeley, Colorado. Agricultural Water Management 299, 108891. [doi:10.1016/j.agwat.2024.108891](https://doi.org/10.1016/j.agwat.2024.108891).


Also, the pyfao56 package was used to conduct the following research:

Thorp, K. R., Thompson, A. L., Harders, S. J., French, A. N., Ward, R. W., 2018. High-throughput phenotyping of crop water use efficiency via multispectral drone imagery and a daily soil water balance model. Remote Sensing 10, 1682. [doi:10.3390/rs10111682](https://doi.org/10.3390/rs10111682)

Thorp, K. R., Calleja, S., Pauli, D., Thompson, A. L., Elshikha, D. E., 2022. Agronomic outcomes of precision irrigation technologies with varying complexity. Journal of the ASABE. 65(1):135-150. [doi:10.13031/ja.14950](https://doi.org/10.13031/ja.14950)

Thorp, K. R., 2023. Combining soil water content data with computer simulation models for improved irrigation scheduling. Journal of the ASABE. 66(5):1265-1279. [doi:10.13031/ja.15591](https://doi.org/10.13031/ja.15591)
