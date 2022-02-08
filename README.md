# pyfao56
A Python implementation of the FAO-56 dual crop coefficient approach for crop water use estimation and irrigation scheduling

The pyfao56 Python package facilitates FAO-56 computations of daily soil water balance using the dual crop coefficient method to estimate crop evapotranspiration (ET).

The FAO-56 method is described in the following documentation:
[Allen, R. G., Pereira, L. S., Raes, D., Smith, M., 1998.  FAO Irrigation and Drainage Paper No. 56. Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements. Food and Agriculture Organization of the United Nations, Rome Italy.](http://www.fao.org/3/x0490e/x0490e00.htm)

Reference ET is computed using the ASCE Standardized Reference ET Equation, which is described in the following documentation:
[ASCE Task Committee on Standardization of Reference Evapotranspiration (Walter, I. A., Allen, R. G., Elliott, R., Itenfisu, D., Brown, P., Jensen, M. E.,Mecham, B., Howell, T. A., Snyder, R., Eching, S., Spofford, T., Hattendorf, M., Martin, D., Cuenca, R. H., Wright, J. L.), 2005. The ASCE Standardized Reference Evapotranspiration Equation. American Society of Civil Engineers, Reston, VA.](https://ascelibrary.org/doi/book/10.1061/9780784408056)

## Source Code
The main pyfao56 package contains the following modules:
* irrigation.py - I/O tools to define irrigation management schedules
* model.py - Equations for daily soil water balance computations
* parameters.py - I/O tools for required input parameters
* refet.py - Equations for computing ASCE Standardized Reference ET
* update.py - I/O tools and methods for state variable updating
* weather.py - I/O tools for required weather information

The source code is available [here](http://github.com/kthorp/pyfao56/). It uses a basic object-oriented design with separate classes to make FAO-56 calculations and to manage parameter, weather, and irrigation management data. [Pandas](https://pandas.pydata.org/) data frames are used for data storage and management. Further documentation of the class structure is contained in the source files.

The pyfao56 package contains a subpackage called [custom](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/custom). It contains modules for development of customized weather files using data from the Arizona Meteorological Network ([AZMET](https://ag.arizona.edu/azmet/)) station at Maricopa, Arizona and from the National Digital Forecast Database ([NDFD](https://graphical.weather.gov/xml/rest.php)). These modules were developed to facilitate irrigation management for field studies conducted at the Maricopa Agricultural Center. Users can follow this example to create customized weather tools for other weather data sources.

## Install
`pip install pyfao56`

## Quickstart

### Import the package
`import pyfao56 as fao`

### Specify the model parameters
* Instantiate a parameters class: `par = fao.Parameters()`
* To print parameter values: `print(par)`
* To adjust parameter values: `par.Kcbmid = 1.225`
* To load values from a file: `par.loadfile('myfilename.par')`
* To write values to a file: `par.savefile('myfilename.par')`

An example of the parameter file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.par).

### Specify the weather information
* Instantiate a weather data class: `wth = fao.Weather()`
* To print weather data: `print(wth)`
* To load data from a file: `wth.loadfile('myfilename.wth')`
* To write data to a file: `wth.savefile('myfilename.wth')`
* To compute daily reference ET for yyyy-ddd (4-digit year and day of year): `refet = wth.compute_etref('2021-150')`

An examples of the weather file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.wth).

Users can customize loading of weather data with wth.customload(). The azmet_maricopa.py module in the custom subpackage provides an example for developing a custom weather data class that inherits from Weather and overrides its customload() function.

### Specify the irrigation management information
* Instantiate an irrigation data class: `irr = fao.Irrigation()`
* To print irrigation data: `print(irr)`
* To load data from a file: `irr.loadfile('myfilename.irr')`
* To write data to a file: `irr.savefile('myfilename.irr')`
* To add an irrigation event (provide yyyy, ddd, depth in mm, and fw): `irr.addevent(2019, 249, 28.3, 1.00)`

An example of the irrigation file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cottondry2013.irr).

### Run the daily soil water balance model
* Instantiate a model class (provide starting yyyy-ddd, ending yyyy-ddd and classes for Parameters, Weather, and Irrigation): `mdl = fao.Model('2013-113','2013-312', par, wth, irr)`
* To run the model: `mdl.run()`
* To print the output: `print(mdl)`
* To save the output to file: `mdl.savefile('myoutputfile.out')`

An example of the model output file is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cottondry2013.out).

### Update basal crop coefficients (Kcb), crop height (h), or crop cover (fc)
* Instantiate an update class: `upd = fao.Update()`
* To load data from a file: `upd.loadfile('myfilename.upd')`
* To write data to a file: `upd.savefile('myfilename.upd')`
* Instantiate a model class with updating (provide starting yyyy-ddd, ending yyyy-ddd and classes for Parameters, Weather, Irrigation, and Updates): `mdl = fao.Model('2019-108','2019-274', par, wth, irr, upd)`
* To run the model: `mdl.run()`

An example of the update file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test3/cotton2019.upd).

## Further examples
Further example scripts for setting up and running the model are [here](https://github.com/kthorp/pyfao56/tree/main/tests).

[test1](https://github.com/kthorp/pyfao56/tree/main/tests/test1) - The cottondry2013.py  and cottonwet2013.py modules contain code to setup and run pyfao56 for the water-limited and well-watered treatments for a 2013 cotton field study at Maricopa, Arizona.

[test2](https://github.com/kthorp/pyfao56/tree/main/tests/test2) - The refet_testA.py module contains a function to compare the short crop reference evapotranspiration (ETo) calculation from the pyfao56 refet.py module with ETo reported by the AZMET station at Maricopa, Arizona for 2003 through 2020. The refet_testB.py module contains a function to compare the short crop reference evapotranspiration (ETo) and tall crop reference evapotranspiration (ETr) calculations from the pyfao56 refet.py module with ETo and ETr computed by [Ref-ET software](https://www.uidaho.edu/cals/kimberly-research-and-extension-center/research/water-resources/ref-et-software) based on weather data from the AZMET station at Maricopa, Arizona for 2003 through 2020.

[test3](https://github.com/kthorp/pyfao56/tree/main/tests/test3) - The updateKcb.py module contains a function to setup and run pyfao56 with basal crop coefficient (Kcb) updates for Zone 12-11 in a 2019 cotton field study at Maricopa, Arizona. The Kcb was estimated from fractional cover measurements based on weekly imagery from a small unoccupied aircraft system (sUAS).

[test4](https://github.com/kthorp/pyfao56/tree/main/tests/test4) - The cotton2018.py module contains code to setup and run pyfao56 for water-limited and well-watered treatments for a 2018 cotton field study at Maricopa, Arizona.

## Further information
The pyfao56 package was used to conduct the following research:

Thorp, K. R., Calleja, S., Pauli, D., Thompson, A. L., Elshikha, D. E., 2022. Agronomic outcomes of precision irrigation technologies with varying complexity. Journal of the ASABE. 65(1):.  doi:10.13031/ja.14950

Thorp, K. R., Thompson, A. L., Harders, S. J., French, A. N., Ward, R. W., 2018. High-throughput phenotyping of crop water use efficiency via multispectral drone imagery and a daily soil water balance model. Remote Sensing 10, 1682. doi:10.3390/rs10111682
