"""
########################################################################
The cotton2018.py module from test4 has been modified to provide tests
of the autoirrigation routines.

The cotton2018.py module contains the following:
    run - function to setup and run pyfao56 for the 100%-100% irrigation
    treatment in a 2018 cotton field study at Maricopa, Arizona

02/07/2022 Scripts developed for running pyfao56 for 2018 cotton data
02/22/2024 Script modified to test the autoirrigation routine.
########################################################################
"""

import pyfao56 as fao
import pyfao56.custom as custom
import os
import time
import sys

def run(case=0):
    """Setup and run pyfao56 for a 2018 cotton field study"""

    start = time.time()

    #Get the module directory
    module_dir = os.path.dirname(os.path.abspath(__file__))

    #Specify the model parameters
    par = fao.Parameters(comment = '2018 Cotton')
    par.Kcbmid = 1.225
    par.Lini = 35
    par.Ldev = 50
    par.Lmid = 46
    par.Lend = 39
    par.hini = 0.05
    par.hmax = 1.20
    par.thetaFC = 0.2050
    par.thetaWP = 0.0980
    par.theta0  = 0.1515
    par.Zrini = 0.20
    par.Zrmax = 1.40
    par.pbase = 0.65
    par.Ze = 0.06
    par.REW = 4.0
    par.savefile(os.path.join(module_dir,'cotton2018.par'))

    #Specify the weather data
    #wth = custom.AzmetMaricopa(comment = '2018 Cotton')
    #wth.customload('2018-108','2018-303')
    #wth.savefile(os.path.join(module_dir,'cotton2018.wth'))
    wth = fao.Weather(comment = '2018 Cotton 100-100')
    wth.loadfile(os.path.join(module_dir,'cotton2018.wth'))

    #Specify the full irrigation schedule for the 100%-100% treatment
    irrfull = fao.Irrigation(comment = '2018 Cotton, 100%-100% ' +
                            'irrigation treatment full schedule')
    irrfull.addevent(2018, 110, 20.4, 1.0)
    irrfull.addevent(2018, 114, 20.4, 1.0)
    irrfull.addevent(2018, 117, 20.4, 1.0)
    irrfull.addevent(2018, 120,  5.1, 1.0)
    irrfull.addevent(2018, 127, 20.4, 1.0)
    irrfull.addevent(2018, 136, 20.2, 1.0)
    irrfull.addevent(2018, 143, 20.4, 1.0)
    irrfull.addevent(2018, 150, 25.5, 1.0)
    irrfull.addevent(2018, 157, 21.2, 1.0)
    irrfull.addevent(2018, 158, 12.7, 1.0)
    irrfull.addevent(2018, 164, 28.7, 1.0)
    irrfull.addevent(2018, 165, 25.3, 1.0)
    irrfull.addevent(2018, 171, 41.4, 1.0)
    irrfull.addevent(2018, 172, 25.5, 1.0)
    irrfull.addevent(2018, 178, 34.0, 1.0)
    irrfull.addevent(2018, 179, 34.0, 1.0)
    irrfull.addevent(2018, 186, 41.4, 1.0)
    irrfull.addevent(2018, 187, 34.0, 1.0)
    irrfull.addevent(2018, 192, 25.5, 1.0)
    irrfull.addevent(2018, 193, 34.0, 1.0)
    irrfull.addevent(2018, 194,  8.5, 1.0)
    irrfull.addevent(2018, 200, 32.9, 1.0)
    irrfull.addevent(2018, 201, 25.5, 1.0)
    irrfull.addevent(2018, 206, 34.0, 1.0)
    irrfull.addevent(2018, 207, 25.5, 1.0)
    irrfull.addevent(2018, 213, 34.0, 1.0)
    irrfull.addevent(2018, 214, 34.0, 1.0)
    irrfull.addevent(2018, 220, 25.5, 1.0)
    irrfull.addevent(2018, 221, 25.5, 1.0)
    irrfull.addevent(2018, 229, 17.0, 1.0)
    irrfull.addevent(2018, 234, 25.5, 1.0)
    irrfull.addevent(2018, 235, 17.0, 1.0)
    irrfull.addevent(2018, 242, 25.5, 1.0)
    irrfull.addevent(2018, 243, 25.5, 1.0)
    irrfull.addevent(2018, 248, 25.5, 1.0)
    irrfull.addevent(2018, 250, 25.5, 1.0)
    irrfull.savefile(os.path.join(module_dir,'cotton2018_full.irr'))

    #Specify the first half of the irrigation schedule for the 100%-100%
    #treatment
    irrhalf = fao.Irrigation(comment = '2018 Cotton, 100%-100% ' +
                            'irrigation treatment, first half schedule')
    irrhalf.addevent(2018, 110, 20.4, 1.0)
    irrhalf.addevent(2018, 114, 20.4, 1.0)
    irrhalf.addevent(2018, 117, 20.4, 1.0)
    irrhalf.addevent(2018, 120,  5.1, 1.0)
    irrhalf.addevent(2018, 127, 20.4, 1.0)
    irrhalf.addevent(2018, 136, 20.2, 1.0)
    irrhalf.addevent(2018, 143, 20.4, 1.0)
    irrhalf.addevent(2018, 150, 25.5, 1.0)
    irrhalf.addevent(2018, 157, 21.2, 1.0)
    irrhalf.addevent(2018, 158, 12.7, 1.0)
    irrhalf.addevent(2018, 164, 28.7, 1.0)
    irrhalf.addevent(2018, 165, 25.3, 1.0)
    irrhalf.addevent(2018, 171, 41.4, 1.0)
    irrhalf.addevent(2018, 172, 25.5, 1.0)
    irrhalf.addevent(2018, 178, 34.0, 1.0)
    irrhalf.addevent(2018, 179, 34.0, 1.0)
    irrhalf.addevent(2018, 186, 41.4, 1.0)
    irrhalf.addevent(2018, 187, 34.0, 1.0)
    irrhalf.savefile(os.path.join(module_dir,'cotton2018_half.irr'))

    #Instantiate AutoIrrigate class
    airr = fao.AutoIrrigate()

    #Case 0: Actual irrigation record, No autoirrigation
    if case==0:
        mdl = fao.Model('2018-108','2018-303', par, wth, irr=irrfull)
    #Case 1: Minimal autoirrigation input case
    #        Autoirrigate yesterday's Dr every day from start to end
    elif case==1:
        airr.addset('2018-108','2018-250')
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 2: Mixing half-season record and autoirrigation
    #        alre is 'True' by default
    #        Actual irrigation record for first half season
    #        Then autoirrigate yesterday's Dr in last half season
    elif case==2:
        airr.addset('2018-108','2018-250')
        mdl = fao.Model('2018-108','2018-303', par, wth, irr=irrhalf,
                        autoirr=airr)
    #Case 3: Full season autoirrigate with mad = 0.4
    elif case==3:
        airr.addset('2018-108','2018-250',mad=0.4)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 4: Autoirrigate with mad = 0.4 only on Tuesday and Friday
    elif case==4:
        airr.addset('2018-108','2018-250',mad=0.4,idow='25')
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 5: Autoirrigate with mad = 0.3, but cancel autoirrigation
    #        if 25 mm rain coming in the next three days
    elif case==5:
        airr.addset('2018-108','2018-250',mad=0.3,fpdep=25.,fpday=3,
                    fpact='cancel')
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 6: Autoirrigate with mad = 0.3, but if 25 mm rain coming in
    #        the next three days, reduce irrigation by rain amount.
    elif case==6:
        airr.addset('2018-108','2018-250',mad=0.3,fpdep=25.,fpday=3,
                    fpact='reduce')
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 7: Autoirrigate based on Dr, not fractional Dr.
    #        Notice lack of irrigation until June when root zone
    #        increases enough to have 40 mm of storage.
    elif case==7:
        airr.addset('2018-108','2018-250',madDr=40.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 8: Fix problem with early season irrigation in Case 7.
    elif case==8:
        airr.addset('2018-108','2018-120',madDr=10.)
        airr.addset('2018-121','2018-150',madDr=20.)
        airr.addset('2018-150','2018-250',madDr=40.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 9: Autoirrigate when Ks > 0.6.
    #        There is timestep issue with this method.
    elif case==9:
        airr.addset('2018-108','2018-250',ksc=0.6)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 10: Autoirrigate every 6 days
    elif case==10:
        airr.addset('2018-108','2018-250',dsli=6)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 11: Autoirrigate every 4 days or sooner with mad=0.3
    #         Early season mad driven, Late season dsli driven
    elif case==11:
        airr.addset('2018-108','2018-250',dsli=4)
        airr.addset('2018-108','2018-250',mad=0.3)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 12: Autoirrigate every 5 days after watering event > 14 mm
    elif case==12:
        airr.addset('2018-108','2018-250',dsle=5,evnt=14.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 13: Autoirrigate 20 mm constant rate every 4 days
    elif case==13:
        airr.addset('2018-108','2018-250',dsli=4,icon=20.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 14: Autoirrigate with mad=0.5 targeting 15 mm Dr deficit
    #         #Mostly nonsensible scheduling in the early season
    elif case==14:
        airr.addset('2018-108','2018-250',mad=0.5,itdr=15.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 15: Autoirrigate with mad=0.5 targeting 0.1 fDr deficit
    #         Somewhat more sensible than Case 14.
    elif case==15:
        airr.addset('2018-108','2018-250',mad=0.5,itfdr=0.1)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 16: Autoirrigate every 5 days with 5-day ET replacement
    #         less precipitation. Default ET is ETcadj.
    elif case==16:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 17: Autoirrigate with mad=0.4 and replace ET less
    #         precipitation since last irrigation event. Default ET is
    #         ETcadj.
    elif case==17:
        airr.addset('2018-108','2018-250',mad=0.4,ietri=True)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 18: Autoirrigate with mad=0.4 and replace ET less
    #         precipitation since last watering event > 14 mm.
    #         Default ET is ETcadj.
    elif case==18:
        airr.addset('2018-108','2018-250',mad=0.4,evnt=14,ietre=True)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 19: Autoirrigate every 5 days with 5-day ET replacement
    #         less precipitation. Use ETc instead of ETcadj.
    elif case==19:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5,ettyp='ETc')
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 20: Autoirrigate with mad=0.45 and apply 90% of Dr
    elif case==20:
        airr.addset('2018-108','2018-250',mad=0.45,iper=90.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 21: Autoirrigate with mad=0.45 considering an application
    #         efficiency of 80%.
    elif case==21:
        airr.addset('2018-108','2018-250',mad=0.45,ieff=80.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 22: Autoirrigate with mad=0.3 considering a minimum
    #         application rate of 12 mm.
    elif case==22:
        airr.addset('2018-108','2018-250',mad=0.3,imin=12.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 23: Autoirrigate with mad=0.3 considering a minimum
    #         application rate of 12 mm and maximum rate of 24 mm.
    elif case==23:
        airr.addset('2018-108','2018-250',mad=0.3,imin=12.,imax=24.)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    #Case 24: Autoirrigate with mad=0.4 and specify fw for the
    #         irrigation method at 0.5
    elif case==24:
        airr.addset('2018-108','2018-250',mad=0.4,fw=0.5)
        mdl = fao.Model('2018-108','2018-303', par, wth, autoirr=airr)
    else:
        print("No case for input value.")
        return

    #Test save and load methods
    airr.savefile(os.path.join(module_dir,'cotton2018.ati'))
    airr.loadfile(os.path.join(module_dir,'cotton2018.ati'))

    #Run the model
    mdl.run()
    #print(mdl)
    mdl.savefile(os.path.join(module_dir,'cotton2018.out'))
    mdl.savesums(os.path.join(module_dir,'cotton2018.sum'))

    end=time.time()
    print('Elapsed time = {:f} s'.format(end-start))

if __name__ == '__main__':
    case = int(sys.argv[1])
    run(case)
