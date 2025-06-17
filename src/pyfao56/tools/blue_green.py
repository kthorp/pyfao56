import pandas as pd
import datetime
import matplotlib.pyplot as plt

class BlueGreen:
    """
    BlueGreen is a water allocation model that partitions evapotranspiration,
    evaporation, transpiration, runoff, and deep percolation into:
    - EP (Effective Precipitation) component (typically rainfall-driven)
    - AW (Applied Water) component (typically irrigation-driven)

    The partitioning is based on a simplified daily soil water balance, tracking
    green and blue water storage fractions over time.

    Attributes:
    -----------
    df : pd.DataFrame
        Processed input DataFrame with required columns and reset index.
    cg : float
        Initial fraction of EP (green) water storage.
    cb : float
        Initial fraction of AW (blue) water storage.
    result : pd.DataFrame or None
        Resulting DataFrame after running the allocation model.
    """

    def __init__(self, mdl, cg=0.5, cb=0.5, comment=''):
        """
        Initialize the BlueGreen model with input data and initial conditions.

        Parameters:
        -----------
        mdl : object
            Object with `odata` attribute (DataFrame) indexed as YYYY-DOY and containing:
                ['Year', 'DOY', 'Date', 'ETa', 'E', 'T', 'Runoff', 'DP', 'Rain', 'Irrig', 'TAW', 'Dr']
        cg : float, optional
            Initial EP (green water) fraction of total available water (default is 0.5).
        cb : float, optional
            Initial AW (blue water) fraction of total available water (default is 0.5).
        comment : str, optional
            User-defined file descriptions or metadata (default = '')
        """
        self.df = mdl.odata.copy().iloc[:, :-4]
        self.cg = cg
        self.cb = cb
        self.comment = 'Comments: ' + comment.strip()
        self.bg_cnames = ['Year', 'DOY', 'DOW', 'Date',
                        'S', 'Sep', 'Saw',
                        'ETa', 'ETa_ep', 'ETa_aw',
                        'E', 'E_ep', 'E_aw',
                        'T', 'T_ep', 'T_aw',
                        'Runoff', 'Runoff_ep', 'Runoff_aw',
                        'DP', 'DP_ep', 'DP_aw'
                       ]
        self.startDate = mdl.startDate
        self.endDate = mdl.endDate
        self.tmstmp = datetime.datetime.now()
        self.result = pd.DataFrame(columns=self.bg_cnames)

    def _water_fraction(self, S_tot_prev, S_py_prev, Win_py, Win_sy, ETa, RO, DP):
        """
        Calculate water allocation for either EP or AW component based on previous day storage.

        Parameters:
        -----------
        S_tot_prev : float
            Total available soil water on previous day.
        S_py_prev : float
            Previous day's EP or AW storage.
        Win_py : float
            Primary water input (e.g., rainfall for EP).
        Win_sy : float
            Secondary water input (e.g., irrigation for EP).
        ETa : float
            Actual evapotranspiration (ETa).
        RO : float
            Runoff.
        DP : float
            Deep percolation.

        Returns:
        --------
        float
            Updated water storage component.
        """
        if S_tot_prev == 0:
            return max(0, S_py_prev + Win_py - (0 if RO == 0 else (Win_py / (Win_py + Win_sy)) * RO))
        else:
            return max(0,
                S_py_prev + Win_py
                - (0 if RO == 0 else (Win_py / (Win_py + Win_sy)) * RO)
                - ((S_py_prev / S_tot_prev) * ETa)
                - ((S_py_prev / S_tot_prev) * DP)
            )

    def run(self):
        """
        Execute the blue-green partitioning model on the loaded dataset.

        Returns:
        --------
        pd.DataFrame
            A DataFrame with EP and AW partitioned outputs for all water balance components.
        """
        df = self.df
        result_cols = self.bg_cnames

        df_part = pd.DataFrame(columns=result_cols)
        sep, saw = 0, 0  # initialize EP and AW storage

        for idx, row in df.iterrows():
            ETa = row['ETa']
            RO = row['Runoff']
            DP = row['DP']
            Rain = row['Rain']
            Irrig = row['Irrig']
            S = row['TAW'] - row['Dr']
            E = row['E']
            T = row['T']

            # if idx == 0:
            if idx == self.startDate.strftime('%Y-%j'):
                sep = self.cg * S
                saw = self.cb * S
            else:
                prev_idx = (datetime.datetime.strptime(idx, '%Y-%j') - datetime.timedelta(days=1)).strftime('%Y-%j')
                prev = df_part.loc[prev_idx]
                Sp = prev['S']
                sep = self._water_fraction(Sp, sep, Rain, Irrig, ETa, RO, DP)
                saw = self._water_fraction(Sp, saw, Irrig, Rain, ETa, RO, DP)

            if sep + saw == 0:
                fep = faw = 0
            else:
                fep = sep / (sep + saw)
                faw = saw / (sep + saw)

            row_data = [
                row['Year'], row['DOY'], row['DOW'], row['Date'],
                S, sep, saw,
                ETa, fep * ETa, faw * ETa,
                E, fep * E, faw * E,
                T, fep * T, faw * T,
                RO, fep * RO, faw * RO,
                DP, fep * DP, faw * DP
            ]

            df_part.loc[idx] = row_data

        self.result = df_part
        return df_part

    def __str__(self):
        """Formatted string output of BlueGreen water allocation model results."""

        self.tmstmp = datetime.datetime.now()
        timestamp = self.tmstmp.strftime('%m/%d/%Y %H:%M:%S')
        sdate = self.startDate.strftime('%m/%d/%Y')
        edate = self.endDate.strftime('%m/%d/%Y')

        method_note = 'Partitioned using EP (Rain) and AW (Irrigation) based on Hoekstra (2019)' #need to verify this
        ast = '*' * 72

        # Format specifiers
        fmts = {
            'Year': '{:>4}'.format, 'DOY': '{:>3}'.format, 'Date': '{:10s}'.format,
            'S': '{:7.2f}'.format, 'Sep': '{:7.2f}'.format, 'Saw': '{:7.2f}'.format,
            'ETa': '{:7.2f}'.format, 'ETa_ep': '{:7.2f}'.format, 'ETa_aw': '{:7.2f}'.format,
            'E': '{:7.2f}'.format, 'E_ep': '{:7.2f}'.format, 'E_aw': '{:7.2f}'.format,
            'T': '{:7.2f}'.format, 'T_ep': '{:7.2f}'.format, 'T_aw': '{:7.2f}'.format,
            'Runoff': '{:7.2f}'.format, 'Runoff_ep': '{:7.2f}'.format, 'Runoff_aw': '{:7.2f}'.format,
            'DP': '{:7.2f}'.format, 'DP_ep': '{:7.2f}'.format, 'DP_aw': '{:7.2f}'.format
        }

        header_note = (
            f"{ast}\n"
            f"pyfao56 BlueGreen Water Partitioning Output\n"
            f"Timestamp: {timestamp}\n"
            f"Simulation Start Date: {sdate}\n"
            f"Simulation End Date: {edate}\n"
            f"Partitioning Method: {method_note}\n"
            f"{ast}\n"
            f"{self.comment}\n"
            f"{ast}\n"
            "Year-DOY  Year  DOY  DOW      Date   S     Sep    Saw" \
                "ETa  ETa_ep  ETa_aw     E  E_ep  E_aw     T  T_ep  T_aw" 
                "Runoff  Runoff_ep  Runoff_aw     DP  DP_ep  DP_aw\n"
        )

        # Print output table if results exist
        body = ''
        if self.result is not None and not self.result.empty:
            display_df = self.result.reset_index().copy()
            body = display_df.to_string(index=False, header=True, formatters=fmts)

        return header_note + body

    def savefile(self, filepath='bluegreen_output.IWP'):
        """
        Save BlueGreen output data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'bluegreen_output.IWP')

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
        """
        Plot a selected variable and its EP/AW components over time.

        Parameters
        ----------
        var : str, optional
            The variable to plot (e.g., 'ETa', 'T', 'E', 'Runoff', 'DP'). Default is 'ETa'.
        filename : str, optional
            If provided, saves the figure to this filename in 300 DPI PNG format.
        """
        if self.result is None:
            raise ValueError("Run the model before plotting.")

        df_plot = self.result.reset_index()

        # Ensure columns exist
        base = var
        ep = f"{var}_ep"
        aw = f"{var}_aw"
        for col in [base, ep, aw]:
            if col not in df_plot.columns:
                raise ValueError(f"Column '{col}' not found in result. Try another variable.")

        fig, ax = plt.subplots(figsize=(12, 6), dpi=200)

        ax.plot(df_plot['Date'], df_plot[base], linestyle=':', lw=2, color='black', label=base)
        ax.plot(df_plot['Date'], df_plot[ep], linestyle='-', color='green', label=ep)
        ax.plot(df_plot['Date'], df_plot[aw], linestyle='-', color='blue', label=aw)

        ax.set_xlabel("Date")
        ax.set_ylabel(f"{var} (mm/day)")
        ax.set_title(f"Partitioned {var} over Crop Span")
        ax.grid(True, which='both', linestyle=':', color='grey', alpha=0.6)
        ax.legend()

        ticks = df_plot['Date'][::int(len(df_plot)/10)]
        ax.set_xticks(ticks, ticks, rotation=30)

        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        else:
            plt.show()

