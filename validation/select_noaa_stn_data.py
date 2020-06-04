""""Select data from NOAA/ESRL/GMD/GRAD Radiation Archive files previously converted to CSV using
convert_noaa_stn_data.py
Script also converts year, month, day, hour, minute to decimal day for ease of comparison with GC-Net data,
and calculates albedo as U_GLOBAL/D_GLOBAL (upward solar radiance / downwelling total solar radiance)
Author: Arthur Elmes

NOTE: This code now redundant, as it has been incorporated into plot_stn_vs_sat.ipynb

Date: 2020-05-27"""

import pandas as pd
import os

workspace = '/home/arthur/Dropbox/projects/greenland/station_data/noaa_summit_data'
os.chdir(workspace)

df_csv = pd.read_csv('noaa_summit_all.csv')

# Add column to contain entire date string
df_csv['date_time'] = pd.to_datetime(df_csv['Year'].map(str) + "-" + df_csv['Mn'].map(str) + "-" +
                                     df_csv['Dy'].map(str) + " " + df_csv['Hr'].map(str) + ":" + df_csv['Mi'].map(str))

# Note the .copy() prevents the new variable from simply pointing to the original df
df_selection = df_csv.loc[(df_csv['Hr'] == 12) & (df_csv['Mi'] == 0)].copy()

# Now that we have our combined date/time col, get rid of these
del df_selection['Year']
del df_selection['Mn']
del df_selection['Dy']
del df_selection['Hr']
del df_selection['Mi']

# These are longwave radiation
del df_selection['D_IR']
del df_selection['U_IR']

# Calculate "albedo" simply as the ratio of upward to downwelling radiance
df_selection['alb'] = df_selection['U_GLOBAL'] / df_selection['D_GLOBAL']

# Filter out spurious albedo values (sensor errors?)
df_selection = df_selection.loc[(df_selection['alb'] < 1.0) & (df_selection['alb'] > 0.0)]

print(df_selection.head())
