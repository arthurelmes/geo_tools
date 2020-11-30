
# Script to explore time series data from in situ stations and satellite observations,
# both already in csv format.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys
import math
from sklearn.metrics import mean_squared_error
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# These two datasets are for the GCNet data
# os.chdir('/home/arthur/Dropbox/projects/greenland/station_data/appears_extraction')
# all_data_mcd = pd.read_csv('greenland-stations-MCD43A3-006-results.csv', index_col=0)
#
# os.chdir('/home/arthur/Dropbox/projects/greenland/station_data/tower_data/orig_data_std_format/')
# stn_df = pd.read_csv('Summit_06c.csv')

# This is the NOAA Summit stn data
os.chdir('/home/arthur/Dropbox/projects/greenland/station_data/noaa_summit_data')
stn_df = pd.read_csv('noaa_summit_all.csv')

# Raw Appears outputs
# os.chdir('/home/arthur/Dropbox/projects/greenland/station_data/appears_extraction/noaa_summit')
# all_data_mcd = pd.read_csv('noaa-summit-manual-location-MCD43A3-006-results.csv', index_col=0)

# Blue sky albedo outputs or whatever other albedo we're plotting
os.chdir('/home/arthur/Dropbox/projects/greenland/station_data/appears_extraction/noaa_summit/combined_manual_location/')
all_data_mcd = pd.read_csv('MODIS_VIIRS_summit_2013-2019.csv', index_col=0)

# Column variables for readability
date = 'Date'
#mcd_variable = 'MCD43A3_006_Albedo_WSA_shortwave'
#mcd_qa = 'MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave'

vnp_variable = 'VNP43_wsa_screened'
mcd_variable = 'MCD43_wsa_screened'
mcd_qa = 'MCD43_QA'
vnp_qa = 'VNP43_QA'
# Specify whether to keep QA == 1, i.e. magnitude inversions

high_qa_only = False

# Subset and mask station data

# Valid dataset options: GCNET, NOAA
dataset = "NOAA"

if dataset == "GCNET":
    # Filter out non-noon observations from dataset
    #TODO Can't figure out why these two filters cannot be combined into single line
    filter = stn_df['dec_day'] % 0.5 == 0
    stn_df.where(filter, inplace = True)

    filter = stn_df['dec_day'] % 1.0 != 0
    stn_df.where(filter, inplace = True)

    # Remove observations filtered out above
    stn_df = stn_df.dropna()

    # Clean up dec_days and combine wit.h year to make new date field in yyyy-mm-dd, use as index
    stn_df['dec_day'] = stn_df['dec_day'].apply(np.floor)
    stn_df['dec_day'] = stn_df['dec_day'].astype(int).astype(str)
    stn_df['dec_day'] = stn_df['dec_day'].str.zfill(3)
    stn_df['date'] = stn_df['year'].astype(int).astype(str) + stn_df['dec_day']
    stn_df['date'] = pd.to_datetime(stn_df['date'], format='%Y%j')
    stn_df = stn_df.set_index(stn_df['date'])

    # Delete now unnecessary dateparts
    del stn_df['year']
    del stn_df['dec_day']

    # Set albedo fill values to NaN
    stn_df['alb'].mask(stn_df['alb'] == 999, np.NaN, inplace=True)
elif dataset == "NOAA":
    # Add column to contain entire date string
    stn_df['date'] = pd.to_datetime(stn_df['Year'].map(str) + "-" + stn_df['Mn'].map(str) + "-" + stn_df['Dy'].map(str))
    # + " " + stn_df['Hr'].map(str) + ":" + stn_df['Mi'].map(str))

    # Here, instead of selecting noon, create a pivot of the selection using Hr == 11 AND Hr == 12 to average alb
    df_selection = stn_df.loc[(stn_df['Hr'] == 11) | (stn_df['Hr'] == 12) ].copy()
    df_selection = pd.pivot_table(df_selection,index=['date'], aggfunc=[np.average],
                                  values=['U_GLOBAL', 'D_GLOBAL']).copy()

    # The below steps are taken from https://bit.ly/301hrH2 to return the pivot_table back to workable df
    df_selection.columns = df_selection.columns.droplevel(0)
    df_selection.columns.name = None
    df_selection = df_selection.reset_index()
    # Note the .copy() prevents the new variable from simply pointing to the original df

    #df_selection = df_selection.loc[(stn_df['Hr'] == 12) & (stn_df['Mi'] == 0)].copy()

    # Now that we have our combined date/time col, get rid of these
    # del df_selection['Year']
    # del df_selection['Mn']
    # del df_selection['Dy']
    # del df_selection['Hr']
    # del df_selection['Mi']
    #
    # # These are longwave radiation
    # del df_selection['D_IR']
    # del df_selection['U_IR']

    # Calculate "albedo" simply as the ratio of upward to downwelling radiance
    df_selection['alb'] = df_selection['U_GLOBAL'] / df_selection['D_GLOBAL']
    df_selection = df_selection.loc[(df_selection['U_GLOBAL'] > 0.0)]
    df_selection = df_selection.loc[(df_selection['D_GLOBAL'] > 0.0)]

    # Filter out spurious albedo values (sensor errors?)
    df_selection = df_selection.loc[(df_selection['alb'] < 1.0) & (df_selection['alb'] > 0.0)]

    df_selection = df_selection.set_index(df_selection['date'])
    # Set the selection back to the original df variable to fit into exisiting code.
    stn_df = df_selection.copy()


# Subset and mask mcd43 data
mcd_df = all_data_mcd.loc['noaasummit', [date, mcd_variable, mcd_qa]]
vnp_df = all_data_mcd.loc['noaasummit', [date, vnp_variable, vnp_qa]]

# Mask out fill values
mcd_df[mcd_variable].mask(mcd_df[mcd_qa] == 255, np.NaN, inplace=True)
vnp_df[vnp_variable].mask(vnp_df[vnp_qa] == 255, np.NaN, inplace=True)

# If specified, remove QA == 1
if high_qa_only:
    mcd_df[mcd_variable].mask(mcd_df[mcd_qa] == 1, np.NaN, inplace=True)
    vnp_df[vnp_variable].mask(vnp_df[vnp_qa] == 1, np.NaN, inplace=True)

# Remove spuriously low albedo values in both satellite and stn records
mcd_df[mcd_variable].mask(mcd_df[mcd_variable] < 0.4, np.NaN, inplace=True)
vnp_df[vnp_variable].mask(vnp_df[vnp_variable] < 0.4, np.NaN, inplace=True)
stn_df['alb'].mask(stn_df['alb'] < 0.4, np.NaN, inplace=True)


# Plot data
mcd_df[date] = pd.to_datetime(mcd_df[date], yearfirst=True)
vnp_df[date] = pd.to_datetime(vnp_df[date], yearfirst=True)
mcd_df = mcd_df.set_index(mcd_df[date])
vnp_df = vnp_df.set_index(vnp_df[date])

stn_df.set_index(stn_df['date'])

# Join satellite observations to stn data based on date
joined_df_mcd = mcd_df.join(stn_df, lsuffix='_mcd', rsuffix='_stn')
joined_df_vnp = vnp_df.join(stn_df, lsuffix='_vnp', rsuffix='_stn')

if dataset == "GCNET":
    #del joined_df['date']
    del joined_df_mcd[mcd_qa]
    del joined_df_mcd['sw_down']
    del joined_df_mcd['sw_up']
    del joined_df_mcd['net_rad']
    del joined_df_mcd['Date']
    del joined_df_vnp[vnp_qa]
    del joined_df_vnp['sw_down']
    del joined_df_vnp['sw_up']
    del joined_df_vnp['net_rad']
    del joined_df_vnp['Date']
elif dataset == "NOAA":
    del joined_df_mcd[mcd_qa]
    del joined_df_mcd['Date']
    del joined_df_mcd['D_GLOBAL']
    del joined_df_mcd['U_GLOBAL']
    del joined_df_vnp[vnp_qa]
    del joined_df_vnp['Date']
    del joined_df_vnp['D_GLOBAL']
    del joined_df_vnp['U_GLOBAL']

# Subset dataset to correct time period (different for different stations?
joined_subset_mcd_df = joined_df_mcd.loc['2013-01-01':'2019-12-01']
joined_subset_vnp_df = joined_df_vnp.loc['2013-01-01':'2019-12-01']

# Calculate stats on dataset that has no missing values
joined_subset_mcd_no_nans_df = joined_subset_mcd_df.dropna()
mcd_sw_wsa_mse = mean_squared_error(joined_subset_mcd_no_nans_df[mcd_variable], joined_subset_mcd_no_nans_df['alb'])
mcd_sw_wsa_rmse = round(math.sqrt(mcd_sw_wsa_mse), 2)
joined_subset_vnp_no_nans_df = joined_subset_vnp_df.dropna()
vnp_sw_wsa_mse = mean_squared_error(joined_subset_vnp_no_nans_df[vnp_variable], joined_subset_vnp_no_nans_df['alb'])
vnp_sw_wsa_rmse = round(math.sqrt(vnp_sw_wsa_mse), 2)

# Add back in the missing days in a plottable way
joined_subset_mcd_no_nans_filled_df = joined_subset_mcd_no_nans_df.asfreq('D')
joined_subset_mcd_no_nans_filled_df.to_csv('final_data_mcd_test.csv')
joined_subset_vnp_no_nans_filled_df = joined_subset_vnp_no_nans_df.asfreq('D')
joined_subset_vnp_no_nans_filled_df.to_csv('final_data_mcd_test.csv')

props = dict(boxstyle='round', facecolor='white', alpha=0.5)

fig_scatter = plt.figure(figsize=(8, 3))
ax_scatter = fig_scatter.add_subplot(111)

# Scatterplots for station, MCD, and VNP
plt.scatter(joined_subset_mcd_no_nans_filled_df['date'],
            joined_subset_mcd_no_nans_filled_df['alb'],
            color='Grey',
            marker='1',
            alpha=0.5,
            label='NOAA Summit')

plt.scatter(joined_subset_vnp_no_nans_filled_df['date'],
            joined_subset_vnp_no_nans_filled_df[vnp_variable],
            color='Green',
            marker='+',
            alpha=0.5,
            label='VNP43')

plt.scatter(joined_subset_mcd_no_nans_filled_df['date'],
            joined_subset_mcd_no_nans_filled_df[mcd_variable],
            color='Tomato',
            marker='.',
            alpha=0.5,
            label='MCD43')

ax_scatter.text(pd.Timestamp("2013-07-27"), 0.95, "Stn vs MCD RMSE: " + str(mcd_sw_wsa_rmse))
ax_scatter.text(pd.Timestamp("2013-07-27"), 0.91, "Stn vs VNP RMSE: " + str(vnp_sw_wsa_rmse))
ax_scatter.set_ylim([0.5, 1.0])
ax_scatter.set_xlim([pd.Timestamp("2013-07-01"), pd.Timestamp("2018-01-05")])
ax_scatter.grid(b=True, which='major', color='LightGrey', linestyle='-')
ax_scatter.minorticks_on()
ax_scatter.legend(loc='lower left')
ax_scatter.set_xlabel('Date')
ax_scatter.set_ylabel('Albedo')
ax_scatter.set_title('NOAA ICECAPS Observatory at Summit Station')
plt.tick_params(axis='x', labelsize=6)
plt.tick_params(axis='y', labelsize=6)
plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig('summit_noaa_vs_mcd43_vs_vnp43_wsa.png', dpi=300)

plt.show()

# joined_subset_df.plot(kind='scatter', y='alb', x='date', use_index=True)
# joined_subset_df.plot(kind='scatter', y=mcd_variable, x='date', use_index=True)
#
# # Export csv if needed
joined_subset_mcd_no_nans_filled_df.to_csv('test_high_qa_only.csv')



