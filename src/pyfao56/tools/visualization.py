"""
########################################################################
The visualization.py module contains the Visualization class, which
provides tools for visualizing pyfao56 Model output with measured soil
water data.

The visualization.py module contains the following:
    Visualization - A class for visualizing pyfao56 Model output

11/09/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
07/27/2023 Separated utility functions into their own classes, JB
08/28/2023 Major overhaul for pyfao56 release
10/31/2023 Added crop coefficient plot
########################################################################
"""

import matplotlib.pyplot as plt
from datetime import datetime as dt

class Visualization:
    """A class for visualizing pyfao56 Model output with measurements.

    Attributes
    ----------
    mdl : pyfao56 Model class
        Provides the simulated data
    sws : pyfao56 SoilWaterSeries class, optional
        Provides the measured soil water series data
        (default = None)
    todayidx : str
        Year and day of year of today ('yyyy-ddd')
    vdata : Dataframe
        Combined DataFrame of simulated (mdl.odata) and measured
        (sws.summarize()) root zone soil water data

    Methods
    -------
    plot_Dr(drmax=False, raw=False, events=False, obs=False, ks=False,
            dpro=False, title='', show=True, filepath=None)
        Create a plot of simulated soil water depletion
    plot_ET(refET=True, ETcm=True, ETc=True, ETa=True, events=False,
            title='', show=True, filepath=None)
        Create a plot of simulated evapotranspiration
    plot_Kc(Kcm=True, tKcb=True, Kcb=True, Ke=True, Kc=True, Ka=True,
            title='', show=True, filepath=None)
        Create a plot of simulated crop coefficient data
    """

    def __init__(self, mdl, sws=None, dayline=False):
        """Initialize the Visualization class attributes.

        Parameters
        ----------
        mdl : pyfao56 Model object
            Provides the simulated data
        sws : pyfao56 SoilWaterSeries object, optional
            Provides the measured soil water series data
            (default = None)
        dayline : boolean
            Adds a vertical line on the day the plot is created
            (default = False)
        """

        self.mdl = mdl
        self.sws = sws

        #Remove duplicated odata columns: Year, DOY, DOW, Date
        columns=['Year','DOY','DOW','Date']
        odatasub = mdl.odata.drop(columns=columns)

        #Add measured data if available
        if self.sws is not None:
            self.vdata = odatasub.merge(self.sws.summarize(),
                                        right_index=True,
                                        left_index=True,
                                        how='outer')
        else:
            self.vdata = odatasub

        #Set zero rain, irrigation, DP, and runoff to NaN
        NaN = float('NaN')
        self.vdata['Rain'] = self.vdata['Rain'].replace(0.0,NaN)
        self.vdata['Irrig'] = self.vdata['Irrig'].replace(0.0,NaN)
        self.vdata['DP'] = self.vdata['DP'].replace(0.0,NaN)
        self.vdata['Runoff'] = self.vdata['Runoff'].replace(0.0,NaN)

        #Determine today's index
        self.todayidx = ''
        if dayline:
            now = dt.today()
            self.todayidx = now.strftime('%Y-%j')

    def plot_Dr(self, drmax=False, raw=False, events=False, obs=False,
                ks=False,dpro=False,title='',show=True,filepath=None):
        """Plot soil water depletion (Dr) and related water data.

        Parameters
        ----------
        drmax : boolean, optional
            If True, include a line plot of simulated Drmax
            (default = False)
        raw : boolean, optional
            If True, include a line plot of simulated RAW
            (default = False)
        events : boolean, optional
            If True, include a scatter plot of irrigation and rain
            (default = False)
        obs : boolean, optional
            If True, include a scatter plot of measured Dr
            (default = False)
        ks : boolean, optional
            If True, include a plot of Ks and mKs at top
            (default = False)
        dpro : boolean, optional
            If True, include a scatter plot of simulated DP & runoff
            (default = False)
        title : str, optional
            Specify the title as the provided string
            (default = '')
        show : boolean, optional
            If True, the plot is displayed on the screen
            (default = True)
        filepath : str, optional
            Provide a filepath string to save the figure
            (default = None)
        """

        #Check plotting conditions to determine axes
        if self.vdata[['DP','Runoff']].isnull().all().all():
            dpro_max = 0
        else:
            dpro_max = round(self.vdata[['DP','Runoff']].max().max())
        if dpro and ks and dpro_max > 0.0:
            htrat = {'height_ratios':[4, 32, 6]}
            fig, (ax2,ax,ax3) = plt.subplots(3, sharex='all',
                                             gridspec_kw=htrat)
            ax3.yaxis.set_major_locator(plt.MaxNLocator(5))
        elif dpro and ks and dpro_max <= 0.0:
            htrat = {'height_ratios':[2, 16, 1]}
            fig, (ax2,ax,ax3) = plt.subplots(3, sharex='all',
                                             gridspec_kw=htrat)
            ax3.yaxis.set_major_locator(plt.MaxNLocator(2))
        elif dpro and not ks and dpro_max > 0.0:
            htrat = {'height_ratios':[16, 3]}
            fig, (ax,ax3) = plt.subplots(2, sharex='all',
                                         gridspec_kw=htrat)
            ax3.yaxis.set_major_locator(plt.MaxNLocator(5))
        elif dpro and not ks and dpro_max <= 0.0:
            htrat = {'height_ratios':[16, 1]}
            fig, (ax,ax3) = plt.subplots(2, sharex='all',
                                         gridspec_kw=htrat)
            ax3.yaxis.set_major_locator(plt.MaxNLocator(2))
        elif not dpro and ks:
            htrat = {'height_ratios': [1, 8]}
            fig, (ax2,ax) = plt.subplots(2, sharex='all',
                                         gridspec_kw=htrat)
        else: #not dpro and not ks
            fig, ax = plt.subplots()

        #Continue setting up the figure
        fig.set_size_inches(9.0,6.0)
        plt.subplots_adjust(left=0.06, right=0.99, bottom=0.07,
                            top=0.95, hspace=0.00, wspace=0.00)
        font = 8

        #Define x from 0 to n days to permit spanning years
        d = self.vdata
        x = range(len(d.index))
        xticks = []
        xlabels = []
        vline = float('NaN')
        for i, idx in enumerate(d.index):
            doy = int(idx[-3:])
            if not doy%5:  #if DOY is divisible by 5
                xticks.append(i)
                if not doy%2: #Label by tens
                    xlabels.append(idx[-3:])
                else:
                    xlabels.append('')
            if idx == self.todayidx:
                vline = i

        #Find maximum water state for scaling y axis
        maxwat = [d['Dr'].max()]
        if drmax:
            maxwat.append(d['Drmax'].max())
        if events:
            maxwat.append(d['Rain'].max())
            maxwat.append(d['Irrig'].max())
        if self.sws is not None:
            maxwat.append(d['mDr'].max())
            maxwat.append(d['mDrmax'].max())
        maxwat = round(max(maxwat))

        #Create the Ks plot
        if ks:
            ks_c = 'lightsalmon'
            ax2.plot(x, d['Ks'], color=ks_c, label='Simulated Ks')
            if obs:
                ax2.scatter(x, d['mKs'], color=ks_c, marker='s',
                            s=40,edgecolor='salmon',label='Measured Ks')
            ax2.set_xlim([xticks[0]-5, xticks[-1]+5])
            ax2.set_xticks(xticks)
            ax2.set_xticklabels(xlabels, fontsize=font)
            ax2.set_xlabel('Day of Year (DOY)', fontsize=font)
            ax2.set_ylim([-0.3, 1.2])
            ax2.set_yticks([0.0, 0.5, 1.0])
            ax2.set_yticklabels(['0.0','0.5','1.0'], fontsize=font)
            ax2.set_ylabel('Ks', fontsize=font)
            ax2.grid(ls=':')
            ax2.set_facecolor('whitesmoke')
            ax2.legend(fontsize=font,loc='upper right',frameon=False)
            if vline is not float('NaN'):
                ax2.axvline(x=vline, color='red', linestyle='--',
                            linewidth=0.5)

        #Create the DP plot
        if dpro:
            ax3.scatter(x, d['DP'], color='crimson', marker=10,
                       s=60, label='Deep Percolation (DP)')
            ax3.scatter(x, d['Runoff'], color='blue', marker="o",
                       s=60, label='Runoff (RO)')
            ax3.set_xlim([xticks[0]-5, xticks[-1]+5])
            ax3.set_xticks(xticks)
            ax3.set_xticklabels(xlabels,fontsize=font)
            ax3.set_xlabel('Day of Year (DOY)', fontsize=font)
            ax3.set_ylim([0.0, dpro_max + 5.])
            yticks = [round(i) for i in ax3.get_yticks()][1:]
            ax3.set_yticks(yticks)
            yticklabels = [str(i) for i in yticks]
            ax3.set_yticklabels(yticklabels, fontsize=font)
            ax3.set_ylabel('DP & RO (mm)', fontsize=font)
            ax3.invert_yaxis()
            ax3.grid(ls=':')
            ax3.set_facecolor('whitesmoke')
            ax3.legend(fontsize=font, loc='lower right', frameon=False)
            if vline is not float('NaN'):
                ax3.axvline(x=vline, color='red', linestyle='--',
                            linewidth=0.5)

        #Create the main plot
        ax.plot(x,d['Dr'],color='darkcyan',
                label='Simulated Root Zone Depletion')
        if drmax:
            ax.plot(x, d['Drmax'], color='darkturquoise',
                    label='Simulated Max Root Zone Depletion')
        if raw:
            ax.plot(x, d['RAW'], color='mediumorchid',
                    label='Readily Available Water (RAW)')
        if obs:
            ax.scatter(x, d['mDr'], color='darkcyan',
                       marker='s', s=40, edgecolor='darkslategray',
                       label='Measured Root Zone Depletion')
        if obs and drmax:
            ax.scatter(x, d['mDrmax'], color='darkturquoise',
                       marker='s', s=40, edgecolor='teal',
                       label='Measured Max Root Zone Depletion')
        if events:
            ax.scatter(x, d['Rain'], color='navy', marker='+',
                       s=35, linewidth=0.70, label='Rain')
            ax.scatter(x, d['Irrig'], color='navy', marker='x',
                       s=35, linewidth=0.70, label='Irrigation')
        ax.set_xlim([xticks[0]-5., xticks[-1]+5.])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels,fontsize=font)
        ax.set_xlabel('Day of Year (DOY)', fontsize=font)
        ax.set_ylim([0.0, maxwat+5.])
        ax.set_yticks(range(0, maxwat+5, 5))
        ax.set_yticklabels(range(0, maxwat+5, 5),fontsize=font)
        ax.set_ylabel('Depth (mm)', fontsize=font)
        ax.grid(ls=":")
        ax.set_facecolor('whitesmoke')
        ax.legend(fontsize=font, loc='upper left', frameon=False)
        if vline is not float('NaN'):
            ax.axvline(x=vline, color='red', linestyle='--',
                       linewidth=0.5)
        plt.suptitle(title, fontsize=10)

        #Save and show the plot if requested
        if filepath is not None:
            plt.savefig(filepath)
        if show:
            plt.show()
        else:
            plt.close(fig)

    def plot_ET(self, refET=True, ETcm=True, ETc=True, ETa=True,
                events=False, title='', show=True, filepath=None):
        """Plot evapotranspiration data versus time.

        Parameters
        ----------
        refET : boolean, optional
            If True, include a lineplot for reference ET
            (default = True)
        ETcm : boolean, optional
            If True, include a lineplot for ETcm (single method)
            (default = True)
        ETc : boolean, optional
            If True, include a lineplot for ETc (dual method)
            (default = True)
        ETa : boolean, optional
            If True, include a lineplot for actual ET
            (default = True)
        events : boolean, optional
            If True, include a scatter plot of irrigation and rain
            (default = False)
        title : str, optional
            Specify the title as the provided string
            (default = '')
        show : boolean, optional
            If True, the plot is displayed on the screen
            (default = True)
        filepath : str, optional
            Provide a filepath string to save the figure
            (default = None)
        """

        #Create the figure
        fig, ax = plt.subplots()
        fig.set_size_inches(9.0,6.0)
        plt.subplots_adjust(left=0.06, right=0.99, bottom=0.07,
                            top=0.95, hspace=0.00, wspace=0.00)
        font = 8

        #Define x from 0 to n days to permit spanning years
        d = self.vdata
        x = range(len(d.index))
        xticks = []
        xlabels = []
        vline = float('NaN')
        for i, idx in enumerate(d.index):
            doy = int(idx[-3:])
            if not doy%5: #if DOY is divisible by 5
                xticks.append(i)
                if not doy%2: #Label by tens
                    xlabels.append(idx[-3:])
                else:
                    xlabels.append('')
            if idx == self.todayidx:
                vline = i

        #Find maximum water state for scaling y axis
        maxwat = [d['ETref'].max(),d['ETcm'].max(),d['ETc'].max(),
                  d['ETa'].max()]
        if events:
            maxwat.append(d['Rain'].max())
            maxwat.append(d['Irrig'].max())
        maxwat = round(max(maxwat))

        #Create ET plot
        if refET:
            ax.plot(x, d['ETref'], color='darkred',
                    label='Reference ET (ETref)')
        if ETcm:
            ax.plot(x, d['ETcm'], color='blueviolet',
                    label='Non-stressed ET (ETcm, single)')
        if ETc:
            ax.plot(x, d['ETc'], color='blue',
                    label='Non-stressed ET (ETc, dual)')
        if ETa:
            ax.plot(x, d['ETa'], linestyle='-.', color='navy',
                    label='Actual ET (ETa)')
        if events:
            ax.scatter(x, d['Rain'], color='navy', marker='+',
                       s=35, linewidth=0.70, label='Rain')
            ax.scatter(x, d['Irrig'], color='navy', marker='x',
                       s=35, linewidth=0.70, label='Irrigation')

        ax.set_xlim([xticks[0]-5., xticks[-1]+5.])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels,fontsize=font)
        ax.set_xlabel('Day of Year (DOY)', fontsize=font)
        ax.set_ylim([0.0, maxwat+2.])
        yticks = [round(i) for i in ax.get_yticks()]
        ax.set_yticks(yticks)
        yticklabels = [str(i) for i in yticks]
        ax.set_yticklabels(yticklabels, fontsize=font)
        ax.set_ylabel('Depth (mm)', fontsize=font)
        ax.grid(ls=":")
        ax.set_facecolor('whitesmoke')
        ax.legend(fontsize=font, loc='upper left', frameon=False)
        if vline is not float('NaN'):
            ax.axvline(x=vline, color='red', linestyle='--',
                       linewidth=0.5)
        plt.suptitle(title, fontsize=10)

        #Save and show the plot if requested
        if filepath is not None:
            plt.savefig(filepath)
        if show:
            plt.show()
        else:
            plt.close(fig)

    def plot_Kc(self, Kcm=True, tKcb=True, Kcb=True, Ke=True, Kc=True,
                Ka=True, title='', show=True, filepath=None):
        """Plot crop coeffient data versus time.

        Parameters
        ----------
        Kcm : boolean, optional
            If True, include a plot of Kcm (single crop coefficient)
            (default = True)
        tKcb : boolean, optional
            If True, include a plot of tabular (trapezoidal) Kcb
            (default = True)
        Kcb : boolean, optional
            If True, include a plot of Kcb
            (default = True)
        Ke : boolean, optional
            If True, include a plot of Ke
            (default = True)
        Kc : boolean, optional
            If True, include a plot of Kc (dual crop coefficient)
            (default = True)
        Ka : boolean, optional
            If True, include a plot of Ka
            (default = True)
        title : str, optional
            Specify the title as the provided string
            (default = '')
        show : boolean, optional
            If True, the plot is displayed on the screen
            (default = True)
        filepath : str, optional
            Provide a filepath string to save the figure
            (default = None)
        """

        #Create the figure
        fig, ax = plt.subplots()
        fig.set_size_inches(9.0,6.0)
        plt.subplots_adjust(left=0.06, right=0.99, bottom=0.07,
                            top=0.95, hspace=0.00, wspace=0.00)
        font = 8

        # Define x from 0 to n days to permit spanning years
        d = self.vdata
        x = range(len(d.index))
        xticks = []
        xlabels = []
        vline = float('NaN')
        for i, idx in enumerate(d.index):
            doy = int(idx[-3:])
            if not doy%5:  #if DOY is divisible by 5
                xticks.append(i)
                if not doy%2: #Label by tens
                    xlabels.append(idx[-3:])
                else:
                    xlabels.append('')
            if idx == self.todayidx:
                vline = i

        #Create crop coefficient plot
        maxkc = 1.2
        if Kcm:
            kcm_c = 'blueviolet'
            ax.plot(x, d['Kcm'], color=kcm_c, label='Kcm')
            maxkc = round(max([maxkc,d['Kcm'].max()])+0.05,1)
        if tKcb:
            tkcb_c = 'mediumseagreen'
            ax.plot(x, d['tKcb'], linestyle='--', color=tkcb_c,
                    label='Tabular Kcb')
            maxkc = round(max([maxkc,d['tKcb'].max()])+0.05,1)
        if Kcb:
            kcb_c = 'seagreen'
            ax.plot(x, d['Kcb'], color=kcb_c, label='Kcb')
            maxkc = round(max([maxkc,d['Kcb'].max()])+0.05,1)
        if Ke:
            ke_c = 'lightskyblue'
            ax.plot(x, d['Ke'], color=ke_c, label='Ke')
            maxkc = round(max([maxkc,d['Ke'].max()])+0.05,1)
        if Kc:
            kc_c = 'blue'
            ax.plot(x, d['Kc'], color=kc_c, label='Kc')
            maxkc = round(max([maxkc,d['Kc'].max()])+0.05,1)
        if Ka:
            ka_c = 'dimgrey'
            ax.plot(x, d['Ka'], color=ka_c, label='Ka')
            maxkc = round(max([maxkc,d['Ka'].max()])+0.05,1)

        yticks=[]
        ylabels=[]
        for i in range(int(maxkc*10.)+1):
            yticks.append(float(i)/10.)
            ylabels.append(str(float(i)/10.))

        ax.set_xlim([xticks[0]-5., xticks[-1]+5.])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels, fontsize=font)
        ax.set_xlabel('Day of Year (DOY)', fontsize=font)
        ax.set_ylim([0.0, maxkc])
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels, fontsize=font)
        ax.set_ylabel('Crop Coefficients', fontsize=font)
        ax.grid(ls=':')
        ax.set_facecolor('whitesmoke')
        ax.legend(fontsize=font,loc='upper right',frameon=False)
        if vline is not float('NaN'):
            ax.axvline(x=vline, color='red', linestyle='--',
                       linewidth=0.5)
        plt.suptitle(title, fontsize=10)

        #Save and show the plot if requested
        if filepath is not None:
            plt.savefig(filepath)
        if show:
            plt.show()
        else:
            plt.close(fig)
