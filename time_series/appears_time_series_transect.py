# This makes a plot where all years are stacked up on top of each other, with a color ramp to generally
# tell them apart
import pandas as pd
import numpy as np
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler



# Update these as needed
workspace = '/home/arthur/Dropbox/projects/greenland/transect_points/appears/'
csv_name = 'russel-transect-3km-spacing-1-MCD43A3-006-results.csv'
aoi_name = 'Russel Glacier Transect 1'
dt_indx = pd.date_range('2000-01-01', '2020-12-31')

csv_path = workspace + csv_name

# Define the fields of interest so we can ignore the rest
fields = ['ID', 'Date', 'MCD43A3_006_Albedo_WSA_shortwave', 'MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave']

# Import raw APPEARS output
ts_df = pd.read_csv(csv_path, usecols=fields, parse_dates=[0])
ts_df['Date'] = pd.to_datetime(ts_df['Date'])
ts_df.set_index('Date', inplace=True)

# Mask out fill values (and could optionally also mask out mag inversions by adding another condition == 1
ts_df['MCD43A3_006_Albedo_WSA_shortwave'].mask(ts_df['MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave'] == 255,
                                               np.NaN, inplace=True)
ts_df['SW_WSA'] = ts_df['MCD43A3_006_Albedo_WSA_shortwave']
del ts_df['MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave']
del ts_df['MCD43A3_006_Albedo_WSA_shortwave']

years = [i for i in range(2000, 2021, 1)]

# This part is the monthly averages
#TODO make these into functions
for year in years:
    ts_df_yr = ts_df[str(year)]
    
    # Here's where the subsetting by year then month happens
    monthly_mean_sr = ts_df_yr.groupby(['ID', pd.Grouper(freq='M')])['SW_WSA'].mean()
    monthly_mean_df = pd.DataFrame(monthly_mean_sr)
    #monthly_mean_df.sort_index(inplace=True)
    #monthly_mean_df.to_csv(workspace + str(year) + "monthly_mean.csv")

    dates = monthly_mean_df.index.get_level_values('Date').tolist()
    ids = monthly_mean_df.index.get_level_values('ID').tolist()
    ids_df = pd.DataFrame({'ID': ids})
    ids_df.drop_duplicates('ID', keep='first', inplace=True)
    ids_df['ID'] = ids_df['ID'].astype(int)
    ids_df.set_index('ID', inplace=True)
    ids_df.sort_index(inplace=True)

    #ids_df.to_csv(workspace + 'ids_df_empty.csv')
    for dt in dates:
        build_df = monthly_mean_df.iloc[monthly_mean_df.index.get_level_values('Date') == dt].copy()
        build_df['ID_int'] = build_df.index.get_level_values('ID').astype(int)
        build_df = build_df.sort_values('ID_int')
        build_df.set_index('ID_int', inplace=True)
        build_df.sort_index(inplace=True)
        ids_df[str(dt)] = build_df['SW_WSA']

        # To check that the indices are aligned right, uncomment the below and check output
        #ids_df['test_index'] = build_df.index
        #ids_df.to_csv(workspace + 'test_index_alignment.csv')
        #ids_df = ids_df.join(build_df, lsuffix='_left', rsuffix='_right')


    n = len(ids_df.columns)
    color = plt.cm.twilight(np.linspace(0, 1, n))
    mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

    ### Create a plot where all the years are combined in a single graph
    fig_comb = plt.figure(figsize=(7, 5))
    ax_comb = fig_comb.add_subplot(111)

    # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
    # check for year part first
    for ycol in ids_df.columns:
        if '20' in str(ycol):
            ax_comb.plot(ids_df.index * 3, ids_df[ycol], label=str(ycol[5:7])) # *3 is bc each sample is 3km further inland

    ax_comb.set_ylabel('Shortwave White Sky Albedo')
    ax_comb.set_ylim(0.0, 1.0)
    ax_comb.set_xlabel('Km from Coastline')
    fig_comb.suptitle(aoi_name + ', year ' + str(year) + ' Ten Day Averages')
    plt.legend(ncol=3, loc='lower right', fontsize=7, title='Months')
    fig_comb.savefig(csv_path[:-4] + aoi_name + ', year ' + str(year) + ' Ten Day Averages2.png',
                     dpi=300)

    plt.show()


# These are the ten day averages.
#TODO make these into functions...

for year in years:
    ts_df_yr = ts_df[str(year)]
    # print(ts_df_yr.head())
    # Here's where the subsetting by year then month happens
    tenday_mean_sr = ts_df_yr.groupby(['ID', pd.Grouper(freq='10D')])['SW_WSA'].mean()
    tenday_mean_df = pd.DataFrame(tenday_mean_sr)
    #tenday_mean_df.sort_index(inplace=True)
    #tenday_mean_df.to_csv(workspace + str(year) + "tenday_mean.csv")

    dates = tenday_mean_df.index.get_level_values('Date').tolist()
    ids = tenday_mean_df.index.get_level_values('ID').tolist()
    ids_df = pd.DataFrame({'ID': ids})
    ids_df.drop_duplicates('ID', keep='first', inplace=True)
    ids_df['ID'] = ids_df['ID'].astype(int)
    ids_df.set_index('ID', inplace=True)
    ids_df.sort_index(inplace=True)

    #ids_df.to_csv(workspace + 'ids_df_empty.csv')
    for dt in dates:
        build_df = tenday_mean_df.iloc[tenday_mean_df.index.get_level_values('Date') == dt].copy()
        build_df['ID_int'] = build_df.index.get_level_values('ID').astype(int)
        build_df = build_df.sort_values('ID_int')
        build_df.set_index('ID_int', inplace=True)
        build_df.sort_index(inplace=True)
        ids_df[str(dt)] = build_df['SW_WSA']

        # To check that the indices are aligned right, uncomment the below and check output
        #ids_df['test_index'] = build_df.index
        #ids_df.to_csv(workspace + 'test_index_alignment.csv')
        #ids_df = ids_df.join(build_df, lsuffix='_left', rsuffix='_right')


    n = len(ids_df.columns)
    color = plt.cm.twilight(np.linspace(0, 1, n))
    mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

    ### Create a plot where all the years are combined in a single graph
    fig_comb = plt.figure(figsize=(8, 5))
    ax_comb = fig_comb.add_subplot(111)

    # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
    # check for year part first
    for ycol in ids_df.columns:
        if '20' in str(ycol):
            ax_comb.plot(ids_df.index * 3, ids_df[ycol], label=str(ycol)[5:10])

    ax_comb.set_ylabel('Shortwave White Sky Albedo')
    ax_comb.set_ylim(0.0, 1.0)
    ax_comb.set_xlabel('Km from Coastline')
    fig_comb.suptitle(aoi_name + ', year ' + str(year) + ' Ten Day Averages')
    plt.legend(ncol=3, loc='lower right', fontsize=7, title='10 Day Averages')
    fig_comb.savefig(csv_path[:-4] + aoi_name + ', year ' + str(year) + ' Ten Day Averages2.png',
                     dpi=300)

    plt.show()

