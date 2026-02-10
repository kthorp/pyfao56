"""
########################################################################
The blue_green.py module contains the BlueGreen class, which provides
a methodology for partitioning water balance components into into blue
(irrigation) and green (rainfall) water. The class implements the
blue-green water accounting framework based on Hoekstra (2019), applying
it to FAO-56 dual crop coefficient daily soil water balance model
outputs. It tracks the fraction of soil water storage attributable to
effective precipitation (EP, green water) versus applied water (AW, blue
water) and partitions evapotranspiration, evaporation, transpiration,
runoff, and deep percolation accordingly.

Hoekstra, A. Y., 2019. Green-blue water accounting in a soil water
balance. Advances in Water Resources 129, 112-117.

The blue_green.py module contains the following:
    BlueGreen - A class for attributing output to blue & green water

11/20/2025 Initial code developed by Gulati & Kukal, University of Idaho
02/09/2026 Reformatted code for incorporation into pyfao56
########################################################################
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt

class BlueGreen:
    """
    A class for attributing pyfao56 Model output to blue and green water

    Attributes
    ----------
    mdl : pyfao56 Model class
       Provides the pyfao56 simulated data
    cg : float
       Initial fraction of effective precipitation (green water) in
       available soil water storage
    cb : float
       Initial fraction of applied water (blue water) in available
       soil water storage
    bgdata : DataFrame or None
       Result of running the blue green partitioning model as float
       index - Year and day of year as string ('yyyy-ddd')
       columns - ['Year', 'DOY', 'DOW', 'Date', 'Rain', 'Irrig', 'S',
                  'Sep', 'Saw', 'ETa', 'ETa_ep', 'ETa_aw', 'E', 'E_ep',
                  'E_aw', 'T', 'T_ep', 'T_aw', 'Runoff', 'Runoff_ep',
                  'Runoff_aw', 'DP', 'DP_ep', 'DP_aw']
           Year      - 4-digit year (yyyy)
           DOY       - Day of year (ddd)
           DOW       - Day of week
           Date      - Month/Day/Year (mm/dd/yy)
           Rain      - Depth of precipitation (mm)
           Irrig     - Depth of applied irrigation (mm)
           S         - Total available water (mm)
           Sep       - S attributed to effective precipitation (mm)
           Saw       - S attributed to applied water (mm)
           ETa       - Actual evapotranspiration (mm)
           ETa_ep    - ETa attributed to effective precipitation (mm)
           ETa_aw    - ETa attributed to applied water (mm)
           E         - Soil water evaporation (mm)
           E_ep      - E attributed to effective precipitation (mm)
           E_aw      - E attributed to applied water (mm)
           T         - Actual plant transpiration (mm)
           T_ep      - T attributed to effective precipitation (mm)
           T_aw      - T attributed to applied water (mm)
           Runoff    - Surface runoff (mm)
           Runoff_ep - Runoff attributed to effective precipitation (mm)
           Runoff_aw - Runoff attributed to applied water (mm)
           DP        - Deep percolation (mm)
           DP_ep     - DP attributed to effective precipitation (mm)
           DP_aw     - DP attributed to applied water (mm)

    Methods
    -------
    run()
        Execute the blue-green water partitioning algorithm
    savefile(filepath='bluegreen_output.iwp')
        Save the formatted blue-green partitioned results to a text file
    plot(var='ETa', filename=None)
        Plot time series of a variable and its EP and AW components
    """

    def __init__(self, mdl, cg=0.5, cb=0.5, comment=''):
        """Initialize the BlueGreen class attributes.

        Parameters
        ----------
        mdl : pyfao56 Model object
           Object with `odata` DataFrame attribute indexed as YYYY-DOY
           and containing: ['Year', 'DOY', 'Date', 'ETa', 'E', 'T', 
           'Runoff', 'DP', 'Rain', 'Irrig', 'TAW', 'Dr']
        cg : float, optional
           Initial fraction of effective precipitation (green water) in
           available soil water storage
           (default is 0.5)
        cb : float, optional
           Initial fraction of applied water (blue water) in available
           soil water storage
           (default is 0.5)
        comment : str, optional
           User-defined file descriptions or metadata (default = '')
        """
        self.df = mdl.odata.copy().iloc[:, :-4]
        self.cg = cg
        self.cb = cb
        self.comment = 'Comments: ' + comment.strip()
        self.bg_cnames = ['Year', 'DOY', 'DOW', 'Date', 'Rain', 'Irrig',
                          'S', 'Sep', 'Saw', 'ETa', 'ETa_ep', 'ETa_aw',
                          'E', 'E_ep', 'E_aw', 'T', 'T_ep', 'T_aw',
                          'Runoff', 'Runoff_ep', 'Runoff_aw', 'DP',
                          'DP_ep', 'DP_aw']
        self.startDate = mdl.startDate
        self.endDate = mdl.endDate
        self.tmstmp = datetime.datetime.now()
        self.bgdata = pd.DataFrame(columns=self.bg_cnames)

    def _water_fraction(self, S_tot_prev, S_py_prev, Win_py, Win_sy,
                        ETa, RO, DP):
        """Calculate water allocation for either the EP or AW component
           based on previous day storage

        Parameters
        ----------
        S_tot_prev : float
            Total available soil water on previous day (mm)
        S_py_prev : float
            Previous day's primary storage (EP or AW) (mm)
        Win_py : float
            Primary wetting influx (e.g., irrigation for EP)
        Win_sy : float
            Secondary wetting influx (e.g., rainfall for EP)
        ETa : float
            Actual evapotranspiration (ETa, mm)
        RO : float
            Runoff (mm)
        DP : float
            Deep percolation (mm)

        Returns
        -------
        S_py_new : float
            Updated water storage component (mm)
        """
        if S_tot_prev == 0:
            S_py_new = S_py_prev + Win_py \
                - (0. if RO==0 else (Win_py / (Win_py + Win_sy)) * RO)
        else:
            S_py_new = S_py_prev + Win_py \
                - (0. if RO==0 else (Win_py / (Win_py + Win_sy)) * RO) \
                - ((S_py_prev / S_tot_prev) * ETa) \
                - ((S_py_prev / S_tot_prev) * DP)
        S_py_new = max(0. , S_py_new)
        return S_py_new

    def run(self):
        """Run blue-green partitioning model on the loaded dataframe"""

        df = self.df

        sep, saw = 0.0, 0.0  # initialize EP and AW storage

        for idx, row in df.iterrows():
            ETa = row['ETa']
            RO = row['Runoff']
            DP = row['DP']
            Rain = row['Rain']
            Irrig = row['Irrig']
            #Available soil water from previous day
            S_prev = S if idx > self.startDate.strftime('%Y-%j') else 0.
            #Available soil water from current day
            S = row['TAW'] - row['Dr']
            E = row['E']
            T = row['T']

            if idx == self.startDate.strftime('%Y-%j'):
                sep = self.cg * S
                saw = self.cb * S
            else:
                # Update EP and AW storage using previous day's values
                sep = self._water_fraction(S_prev, sep, Rain, Irrig,
                                           ETa, RO, DP)
                saw = self._water_fraction(S_prev, saw, Irrig, Rain,
                                           ETa, RO, DP)

            if sep + saw == 0:
                fep = faw = 0
            else:
                fep = sep / (sep + saw)
                faw = saw / (sep + saw)

            row_data = [
                row['Year'], row['DOY'], row['DOW'], row['Date'],
                Rain, Irrig, S, sep, saw,
                ETa, fep * ETa, faw * ETa,
                E, fep * E, faw * E,
                T, fep * T, faw * T,
                RO, fep * RO, faw * RO,
                DP, fep * DP, faw * DP
            ]

            self.bgdata.loc[idx] = row_data

    def __str__(self):
        """Represent BlueGreen water allocation results as string"""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        sdate = self.startDate.strftime('%m/%d/%Y')
        edate = self.endDate.strftime('%m/%d/%Y')

        method_note = 'Based on conceptual framework of Hoekstra (2019)'
        ast = '*' * 72

        # Format specifiers
        fmts = {
            'Year': '{:>4}'.format, 'DOY': '{:>3}'.format,
            'Date': '{:10s}'.format, 'Rain': '{:7.2f}'.format,
            'Irrig': '{:7.2f}'.format, 'S': '{:7.2f}'.format,
            'Sep': '{:7.2f}'.format, 'Saw': '{:7.2f}'.format,
            'ETa': '{:7.2f}'.format, 'ETa_ep': '{:7.2f}'.format,
            'ETa_aw': '{:7.2f}'.format, 'E': '{:7.2f}'.format,
            'E_ep': '{:7.2f}'.format, 'E_aw': '{:7.2f}'.format,
            'T': '{:7.2f}'.format, 'T_ep': '{:7.2f}'.format,
            'T_aw': '{:7.2f}'.format, 'Runoff': '{:7.2f}'.format,
            'Runoff_ep': '{:7.2f}'.format,'Runoff_aw': '{:7.2f}'.format,
            'DP': '{:7.2f}'.format, 'DP_ep': '{:7.2f}'.format, 
            'DP_aw': '{:7.2f}'.format
        }

        header_note = (
            f"{ast}\n"
            f"pyfao56 wetting influx partitioning into "
            f"applied water (AP) (blue water) and "
            f"effective precipitation (EP) (green water) output\n"
            f"Timestamp: {timestamp}\n"
            f"Simulation Start Date: {sdate}\n"
            f"Simulation End Date: {edate}\n"
            f"Partitioning Method: {method_note}\n"
            f"{ast}\n"
            f"{self.comment}\n"
            f"{ast}\n"
            "Year-DOY Year DOY DOW     Date      Rain   Irrig       S" \
            "     Sep     Saw     ETa  ETa_ep  ETa_aw       E    E_ep" \
            "    E_aw       T    T_ep    T_aw      RO   RO_ep   RO_aw" \
            "      DP   DP_ep   DP_aw\n"
        )

        # Print output table if results exist
        body = ''
        if self.bgdata is not None and not self.bgdata.empty:
            display_df = self.bgdata.reset_index().copy()
            body = display_df.to_string(index=False, header=False,
                                        formatters=fmts)

        return header_note + body

    def savefile(self, filepath='bluegreen_output.iwp'):
        """Save BlueGreen output data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'bluegreen_output.iwp')

        Raises
        ------
        FileNotFoundError
            If the filepath is invalid or cannot be opened.
        """
        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for output data is not found.')
        else:
            f.write(self.__str__())
            f.close()

    def plot(self, var='ETa', filename=None):
        """Time series plot of a variable and its EP/AW components.
        saves the figure if filename is provided. Returns plt.show().

        Parameters
        ----------
        var : str
            Variable name in res_pyfao.bgdata 
            (e.g., 'ETa', 'T', 'E', 'Runoff', 'DP').
        filename : str, optional
            If provided, save the figure to this filename (PNG, 300 DPI)
        """

        if self.bgdata is None or self.bgdata.empty:
            raise ValueError("No BlueGreen data available. " \
                             "Please run the model first.")
        ep = f"{var}_ep"
        aw = f"{var}_aw"
        for col in [var, ep, aw]:
            if col not in self.bgdata.columns:
                raise ValueError(f"Column '{col}' not found in result. "
                                 "Try another variable.")

        # Create figure with higher quality
        fig, ax = plt.subplots(figsize=(14, 6), dpi=200)

        # Plot filled areas for components
        ax.fill_between(self.bgdata['Date'], 0, self.bgdata[ep],
                        color='#2ecc71', alpha=0.4,
                        label=f'{var} (eff. precip.)')
        ax.fill_between(self.bgdata['Date'], 0, self.bgdata[aw],
                        color='#3498db', alpha=0.4,
                        label=f'{var} (applied water)')
        ax.plot(self.bgdata['Date'], self.bgdata[var], linestyle='--',
                lw=2.5, color='black', label=f'{var} (Total)', zorder=5)

        # Secondary y-axis for precipitation and irrigation
        ax01 = ax.twinx()
        ax01.bar(self.bgdata['Date'], self.bgdata['Rain'], width=0.5,
                 color="#05EF6E", alpha=0.2, label='Rainfall',
                 edgecolor='none')
        ax01.bar(self.bgdata['Date'], self.bgdata["Irrig"], width=0.5,
                 color="#0B7BD7", alpha=0.2, label='Irrigation',
                 edgecolor='none')
        ax01.set_ylim(self.bgdata[['Rain', 'Irrig']].max().max()*1.2, 0)
        ax01.set_ylabel("Rainfall & Irrigation (mm)", fontsize=11,
                        fontweight='bold', rotation=270, labelpad=20)
        ax01.tick_params(axis='y', labelsize=10)
        ax01.spines['right'].set_linewidth(1.5)

        # Primary axis styling
        ax.set_xticks(self.bgdata['Date'][::15].to_list())
        ax.set_xlabel("Date", fontsize=12, fontweight='bold')
        ax.set_ylabel(f"{var} (mm/day)", fontsize=12, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.3, linewidth=0.8)
        ax.set_ylim(bottom=0)
        ax.set_xlim(self.bgdata['Date'].min(),self.bgdata['Date'].max())

        # Format x-axis dates
        ax.tick_params(axis='x', rotation=30, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Spines
        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_linewidth(1.5)

        # Combined legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax01.get_legend_handles_labels()
        ax.legend(lines1+lines2, labels1 + labels2, loc='upper center',                 bbox_to_anchor=(0.5, 1.15), ncol=5, frameon=True, 
                  fontsize=10, fancybox=True,)

        plt.tight_layout()

        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                        facecolor='white')

        return plt.show()
