# This makes a plot where all years are stacked up on top of each other, with a color ramp to generally
# tell them apart
import pandas as pd
import numpy as np
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
import datetime


def clean_df(input_df):
    # Pull off the dates and Category numbers (used to be 'ID', but 'Category' is safer from appears
    # (corresponding to distance from coast for transects), and make a new DF with unique values only
    dates = input_df.index.get_level_values('Date').tolist()
    ids = input_df.index.get_level_values('Category').tolist()
    cleaned_df = pd.DataFrame({'Category': ids})
    cleaned_df.drop_duplicates('Category', keep='first', inplace=True)
    cleaned_df['Category'] = cleaned_df['Category'].astype(int)
    cleaned_df.set_index('Category', inplace=True)
    cleaned_df.sort_index(inplace=True)

    # This is just an empty dataframe with the index set to the series of IDs, plus the dates in the range
    return cleaned_df, dates


def monthly_graphs(ts_df, years, aoi_name, csv_path):
    # This is for the the monthly averages
    for year in years:
        ts_df_yr = ts_df[str(year)]

        # Here's where the subsetting by year then month happens
        monthly_mean_df = pd.DataFrame(ts_df_yr.groupby(['Category', pd.Grouper(freq='M')])['Value'].mean())
        ids_df = clean_df(monthly_mean_df)[0]
        #todo Couldn't this be done outside the years loop to save time?

        # Use a temporary DF to organize the SW WSA values each time period into columns, then add them
        # to the previously created ids_df, so we have a df where the index is the IDs, then cols are each
        # month's average SW WSA
        for dt in clean_df(monthly_mean_df)[1]:
            build_df = monthly_mean_df.iloc[monthly_mean_df.index.get_level_values('Date') == dt].copy()
            build_df['Category_int'] = build_df.index.get_level_values('Category').astype(int)
            build_df = build_df.sort_values('Category_int')
            build_df.set_index('Category_int', inplace=True)
            build_df.sort_index(inplace=True)
            ids_df[str(dt)] = build_df['Value']

            # To check that the indices are aligned right, uncomment the below and check output
            # ids_df['test_index'] = build_df.index

            # ids_df = ids_df.join(build_df, lsuffix='_left', rsuffix='_right')

        # Make an overall average of SW WSA to use as a basline for a simpler set of plots
        # overall_ids_df[str(year) + '_mean'] = ids_df.mean(axis=1)
        # overall_ids_df = overall_ids_df.merge(ids_df, left_on='Category', right_on='Category')

        # Set up the color cycler for the plot
        n = 12 #len(ids_df.columns)
        color = plt.cm.hsv(np.linspace(0, 1, n))
        mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

        # Create a plot where all the years are combined in a single graph
        fig_monthly = plt.figure(figsize=(7, 5))
        ax_comb = fig_monthly.add_subplot(111)

        # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
        # check for year part first and only use cols with a valid part of the date in them, i.e. '20*'
        for ycol in ids_df.columns:
            if '20' in str(ycol):
                ax_comb.plot(ids_df.index * 3, ids_df[ycol], label=str(ycol[5:7]), linewidth=0.5)
                # *3 is bc each sample is 3km further inland

        ax_comb.set_ylabel('Shortwave White Sky Albedo')
        ax_comb.set_ylim(0.0, 1.0)
        ax_comb.set_xlabel('Km from Coastline')
        fig_monthly.suptitle(aoi_name + ', year ' + str(year) + ' Monthly Averages')
        plt.legend(ncol=3, loc='lower right', fontsize=7, title='Months')
        file_path, file_name = os.path.split(csv_path)
        save_name = os.path.join(file_path, 'figs', file_name[:-4] + aoi_name.replace(' ', '_') + '_year_' + str(year) +
                                 '_Monthly_Averages2.png')
        if not os.path.isdir(os.path.join(file_path, 'figs')):
            os.mkdir(os.path.join(file_path, 'figs'))
        fig_monthly.savefig(save_name, dpi=600)
        plt.show()


def tenday_graphs(ts_df, years, aoi_name, csv_path):
    # This is for the ten day averages.
    for year in years:
        ts_df_yr = ts_df[str(year)]
        # print(ts_df_yr.head())
        # Here's where the subsetting by year then month happens
        tenday_mean_df = pd.DataFrame(ts_df_yr.groupby(['Category', pd.Grouper(freq='10D')])['Value'].mean())
        ids_df = clean_df(tenday_mean_df)[0]

        for dt in clean_df(tenday_mean_df)[1]:
            build_df = tenday_mean_df.iloc[tenday_mean_df.index.get_level_values('Date') == dt].copy()
            build_df['Category_int'] = build_df.index.get_level_values('Category').astype(int)
            build_df = build_df.sort_values('Category_int')
            build_df.set_index('Category_int', inplace=True)
            build_df.sort_index(inplace=True)
            ids_df[str(dt)] = build_df['Value']

            # To check that the indices are aligned right, uncomment the below and check output
            #ids_df['test_index'] = build_df.index
            #ids_df.to_csv(workspace + 'test_index_alignment.csv')
            #ids_df = ids_df.join(build_df, lsuffix='_left', rsuffix='_right')

        n = len(ids_df.columns)
        color = plt.cm.hsv(np.linspace(0, 1, n))
        mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

        ### Possible todo: if the grid of all years is desirable, then make this spit out one big figure filled with
        ### subgrids, one per year

        # Create a plot where all the years are combined in a single graph
        fig_tenday = plt.figure(figsize=(8, 5))
        ax_comb = fig_tenday.add_subplot(111)

        # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
        # check for year part first
        for ycol in ids_df.columns:
            if '20' in str(ycol):
                ax_comb.plot(ids_df.index * 3, ids_df[ycol], label=str(ycol)[5:10], linewidth=0.5)

        ax_comb.set_ylabel('Shortwave White Sky Albedo')
        ax_comb.set_ylim(0.0, 1.0)
        ax_comb.set_xlabel('Km from Coastline')
        fig_tenday.suptitle(aoi_name + ', year ' + str(year) + ' Ten Day Averages')
        plt.legend(ncol=3, loc='lower right', fontsize=7, title='10 Day Averages')
        file_path, file_name = os.path.split(csv_path)
        save_name = os.path.join(file_path, 'figs', file_name[:-4] + aoi_name.replace(' ', '_') + '_year_' + str(year) +
                                 '_TenDay_Averages.png')
        if not os.path.isdir(os.path.join(file_path, 'figs')):
            os.mkdir(os.path.join(file_path, 'figs'))
        fig_tenday.savefig(save_name, dpi=600)
        plt.show()


def overall_mean_graph(ts_df, aoi_name, csv_path, month_labels):
    # Here's where the subsetting by year then month happens
    monthly_mean_df = pd.DataFrame(ts_df.groupby(['Category', pd.Grouper(freq='M')])['Value'].mean())

    # Pull off the dates and Category numbers (corresponding to distance from coast for transects),
    # and make a new DF with unique values only
    dates = monthly_mean_df.index.get_level_values('Date').tolist()
    ids = monthly_mean_df.index.get_level_values('Category').tolist()
    ids_df = pd.DataFrame({'Category': ids})
    ids_df.drop_duplicates('Category', keep='first', inplace=True)
    ids_df['Category'] = ids_df['Category'].astype(int)
    ids_df.set_index('Category', inplace=True)
    ids_df.sort_index(inplace=True)

    ids_df_climo = ids_df.copy()
    # Remove all columns between column index 1 to 3
    ids_df_climo.drop(ids_df_climo.iloc[:, :], inplace=True, axis=1)
    ids_df_climo_temp = ids_df_climo.copy()

    # Use a temporary DF to organize the SW WSA values each time period into columns, then add them
    # to the previously created ids_df, so we have a df where the index is the Categories, then cols are each
    # month's average SW WSA
    for dt in dates:
        build_df = monthly_mean_df.iloc[monthly_mean_df.index.get_level_values('Date') == dt].copy()
        build_df['Category_int'] = build_df.index.get_level_values('Category').astype(int)
        build_df = build_df.sort_values('Category_int')
        build_df.set_index('Category_int', inplace=True)
        build_df.sort_index(inplace=True)
        ids_df[str(dt)] = build_df['Value']

        # To check that the indices are aligned right, uncomment the below and check output
        # ids_df['test_index'] = build_df.index
        # ids_df = ids_df.join(build_df, lsuffix='_left', rsuffix='_right')

    for mnth in month_labels:
        for col in ids_df.columns:
            if mnth in str(col):
                ids_df_climo_temp[str(col)] = ids_df[col]
        ids_df_climo[mnth[1:-1]] = ids_df_climo_temp.mean(axis=1, skipna=True)
        ids_df_climo_temp.drop(ids_df_climo_temp.iloc[:, :], inplace=True, axis=1)

    # Set up the color cycler for the plot
    n = 12  # len(ids_df_climo_temp.columns)
    color = plt.cm.hsv(np.linspace(0, 1, n))
    mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

    # Create a plot where all the years are combined in a single graph
    fig_overall_mean = plt.figure(figsize=(7, 5))
    ax_comb = fig_overall_mean.add_subplot(111)
    # ids_df_climo.to_csv(workspace + 'test_final_climo.csv')
    # Add each year to same plot
    for ycol in ids_df_climo.columns:
        ax_comb.plot(ids_df_climo.index * 3, ids_df_climo[ycol], label=str(ycol),
                     linewidth=0.5)  # * 3 is bc each sample is 3km further inland

    ax_comb.set_ylabel('Shortwave White Sky Albedo')
    ax_comb.set_ylim(0.0, 1.0)
    ax_comb.set_xlabel('Km from Coastline')
    fig_overall_mean.suptitle(aoi_name + ' 2000-2020 Mean')
    plt.legend(ncol=3, loc='lower right', fontsize=7, title='Monthly Mean')
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', file_name[:-4] + aoi_name.replace(' ', '_') + '_2000-2020_mean_' +
                             '_Monthly_Averages2.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    fig_overall_mean.savefig(save_name, dpi=600)
    plt.show()


def anomalies_graph(ts_df, years, aoi_name, csv_path):
    # This whole function is god awfully written. but it works.
    ts_df_doy_location_mean = ts_df.copy()
    ts_df_doy_location_mean.reset_index(inplace=True)
    ts_df_doy_location_mean['doy'] = ts_df_doy_location_mean['Date'].dt.dayofyear
    ts_df_doy_location_mean = pd.DataFrame(ts_df_doy_location_mean.groupby(['Category', 'doy'])['Value'].mean())
    # modify this from monthly_mean func
    #for year in years:
        #ts_df_yr = ts_df[str(year)]

    ts_df_dates = ts_df.copy()
    ts_df_dates.reset_index(inplace=True)
    del ts_df_dates['Category']
    ts_df_dates.drop_duplicates('Date', keep='first', inplace=True)
    dates = ts_df_dates.Date.tolist()

    ids = ts_df.Category.unique().tolist()
    ids_df = pd.DataFrame({'Category': ids})
    ids_df.drop_duplicates('Category', keep='first', inplace=True)
    ids_df['Category'] = ids_df['Category'].astype(int)
    ids_df.set_index('Category', inplace=True)
    ids_df.sort_index(inplace=True)

    # Use a temporary DF to organize the SW WSA values each time period into columns, then add them
    # to the previously created ids_df, so we have a df where the index is the IDs, then cols are each
    # month's average SW WSA
    for dt in dates:
        build_df = ts_df.iloc[ts_df.index.get_level_values('Date') == dt].copy()
        build_df['Category_int'] = build_df.Category.unique().astype(int)
        build_df = build_df.sort_values('Category_int')
        build_df.set_index('Category_int', inplace=True)
        build_df.sort_index(inplace=True)
        ids_df[str(dt)] = build_df['Value']

    ts_df_doy_location_mean = ts_df_doy_location_mean.unstack(level=1)
    ts_df_doy_location_mean.columns = [col[1] for col in ts_df_doy_location_mean.columns]

    for year in years:
        # ts_df_doy_location_mean.reset_index(inplace=True)
        # ts_df_doy_location_mean.set_index('Category')
        #ts_df_doy_location_mean.columns = str(year) + ts_df_doy_location_mean.columns
        col_selection = []
        for col in ids_df.columns:
            if str(year) in col:
                col_selection.append(col)
        temp_year_df = ids_df[col_selection].copy()
        tmp_cols = list(range(60, 60 + len(temp_year_df.columns)))
        temp_year_df.columns = tmp_cols


        #temp_year_df.to_csv(csv_path[:-10] + 'year_{yr}_subset.csv'.format(yr=year))
        #ts_df_doy_location_mean.to_csv(csv_path[:-10] + 'means.csv')

        temp_year_df = temp_year_df.subtract(ts_df_doy_location_mean, axis='index')
        # wtf why do I need this again? but I do..
        tmp_cols = list(range(60, 60 + len(temp_year_df.columns)))

        new_cols = []
        loc = 0
        while loc < len(tmp_cols):
            new_cols.append(pd.to_datetime(str(year) + str(tmp_cols[loc]), format='%Y%j'))
            loc += 1
        temp_year_df.columns = new_cols

        temp_year_df_transpose = temp_year_df.T
        monthly_anomalies_df = pd.DataFrame(temp_year_df_transpose.groupby(
            [pd.Grouper(freq='M')]).mean())
        monthly_anomalies_df = monthly_anomalies_df.T

        # Set up the color cycler for the plot
        n = 12 #len(ids_df.columns)
        color = plt.cm.hsv(np.linspace(0, 1, n))
        mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

        # Create a plot where all the years are combined in a single graph
        fig_monthly_anom = plt.figure(figsize=(7, 5))
        ax_monthly_anom = fig_monthly_anom.add_subplot(111)

        # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
        # check for year part first and only use cols with a valid part of the date in them, i.e. '20*'
        for ycol in monthly_anomalies_df.columns:
            if '20' in str(ycol):
                ax_monthly_anom.plot(monthly_anomalies_df.index * 3, monthly_anomalies_df[ycol],
                                     label=str(ycol.month), linewidth=0.5)
                # *3 is bc each sample is 3km further inland

        ax_monthly_anom.set_ylabel('Shortwave White Sky Albedo Anomaly')
        ax_monthly_anom.set_ylim(-1.0, 1.0)
        ax_monthly_anom.set_xlabel('Km from Coastline')
        fig_monthly_anom.suptitle(aoi_name + ', year ' + str(year) + ' Monthly Anomalies')
        plt.legend(ncol=3, loc='upper right', fontsize=7, title='Months')
        file_path, file_name = os.path.split(csv_path)
        save_name = os.path.join(file_path, 'figs', file_name[:-4] + aoi_name.replace(' ', '_') + '_year_' + str(year) +
                                 '_Monthly_anomalies.png')
        if not os.path.isdir(os.path.join(file_path, 'figs')):
            os.mkdir(os.path.join(file_path, 'figs'))
        fig_monthly_anom.savefig(save_name, dpi=600)
        plt.show()


def anomalies_overall_mean_graph(ts_df, years, aoi_name, csv_path):
    # This whole function is god awfully written. but it works.
    ts_df_doy_location_mean = ts_df.copy()
    ts_df_doy_location_mean.reset_index(inplace=True)
    ts_df_doy_location_mean['doy'] = ts_df_doy_location_mean['Date'].dt.dayofyear
    ts_df_doy_location_mean = pd.DataFrame(ts_df_doy_location_mean.groupby(['Category', 'doy'])['Value'].mean())
    # modify this from monthly_mean func
    #for year in years:
        #ts_df_yr = ts_df[str(year)]

    ts_df_dates = ts_df.copy()
    ts_df_dates.reset_index(inplace=True)
    del ts_df_dates['Category']
    ts_df_dates.drop_duplicates('Date', keep='first', inplace=True)
    dates = ts_df_dates.Date.tolist()

    ids = ts_df.Category.unique().tolist()
    ids_df = pd.DataFrame({'Category': ids})
    ids_df.drop_duplicates('Category', keep='first', inplace=True)
    ids_df['Category'] = ids_df['Category'].astype(int)
    ids_df.set_index('Category', inplace=True)
    ids_df.sort_index(inplace=True)

    # Use a temporary DF to organize the SW WSA values each time period into columns, then add them
    # to the previously created ids_df, so we have a df where the index is the IDs, then cols are each
    # month's average SW WSA
    for dt in dates:
        build_df = ts_df.iloc[ts_df.index.get_level_values('Date') == dt].copy()
        build_df['Category_int'] = build_df.Category.unique().astype(int)
        build_df = build_df.sort_values('Category_int')
        build_df.set_index('Category_int', inplace=True)
        build_df.sort_index(inplace=True)
        ids_df[str(dt)] = build_df['Value']

    ts_df_doy_location_mean = ts_df_doy_location_mean.unstack(level=1)
    ts_df_doy_location_mean.columns = [col[1] for col in ts_df_doy_location_mean.columns]

    ids_df_transpose = ids_df.T

    ids_df_transpose.reset_index(inplace=True)
    ids_df_transpose['doy'] = pd.DatetimeIndex(ids_df_transpose['index']).dayofyear

    monthly_mean_df = pd.DataFrame(ids_df_transpose.groupby(['doy']).mean())
    ids_df = monthly_mean_df.T


    # col_selection = []
    # for col in ids_df.columns:
    #     #if str(year) in col:
    #     col_selection.append(col)
    temp_year_df = ids_df.copy()
    tmp_cols = list(range(60, 60 + len(temp_year_df.columns)))
    temp_year_df.columns = tmp_cols

    #temp_year_df.to_csv(csv_path[:-10] + 'year_{yr}_subset.csv'.format(yr=year))
    #ts_df_doy_location_mean.to_csv(csv_path[:-10] + 'means.csv')

    temp_year_df = ids_df.subtract(ts_df_doy_location_mean, axis='index')
    # wtf why do I need this again? but I do..
    tmp_cols = list(range(60, 60 + len(temp_year_df.columns)))

    new_cols = []
    loc = 0
    while loc < len(tmp_cols):
        new_cols.append(pd.to_datetime('2000' + str(tmp_cols[loc]), format='%Y%j'))
        loc += 1
    temp_year_df.columns = new_cols

    temp_year_df_transpose = temp_year_df.T

    monthly_anomalies_df = pd.DataFrame(temp_year_df_transpose.groupby(
        [pd.Grouper(freq='M')]).mean())

    monthly_anomalies_df = monthly_anomalies_df.T
    monthly_anomalies_df.reset_index(inplace=True)
    monthly_anomalies_df['xaxis'] = monthly_anomalies_df['Category'] * 3


    # Set up the color cycler for the plot
    n = 12 #len(ids_df.columns)
    color = plt.cm.hsv(np.linspace(0, 1, n))
    mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

    # Create a plot where all the years are combined in a single graph
    fig_monthly_anom = plt.figure(figsize=(7, 5))
    ax_monthly_anom = fig_monthly_anom.add_subplot(111)

    # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
    # check for year part first and only use cols with a valid part of the date in them, i.e. '20*'
    for ycol in monthly_anomalies_df.columns:
        if '20' in str(ycol):
            ax_monthly_anom.plot(monthly_anomalies_df['xaxis'], monthly_anomalies_df[ycol],
                                 label=str(ycol.month), linewidth=0.5)
            # *3 is bc each sample is 3km further inland

    ax_monthly_anom.set_ylabel('Shortwave White Sky Albedo Anomaly')
    ax_monthly_anom.set_ylim(-1.0, 1.0)
    ax_monthly_anom.set_xlabel('Km from Coastline')
    fig_monthly_anom.suptitle(aoi_name + ', year ' + ' Monthly Anomalies')
    plt.legend(ncol=3, loc='upper right', fontsize=7, title='Months')
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', file_name[:-4] + aoi_name.replace(' ', '_') + '_2000-2020_' +
                             '_Monthly_anomalies.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    fig_monthly_anom.savefig(save_name, dpi=600)
    plt.show()


def main():
    # Update these as needed
    workspace = '/media/arthur/Windows/LinuxShare/actual_albedo/wgs84/fig/'
    csv_name = '65_deg_north_ice_clip_wgs84_pts.csv_extracted_values_MCD43_actual_albedo_2020_stacked.csv'
    aoi_name = '65 Degree Transect 1'
    csv_path = workspace + csv_name

    #TODO the 'category' column name is only in the widened transect. check the shapefiles
    #to ensure that it is the correct field to be using

    # Define SZN-based time period for acceptable observations
    begin_month = 1
    end_month = 12
    month_labels = ['-' + str(x).zfill(2) + '-' for x in range(begin_month, end_month)]

    # Do some initial df cleanup here.. maybe move to the cleanup func

    # Define the fields of interest so we can ignore the rest
    # fields = ['Category', 'Date', 'MCD43A3_006_Albedo_WSA_shortwave',
    #           'MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave']
    fields = ['Category', 'Date', 'Value']

    ts_df = pd.read_csv(csv_path, usecols=fields, parse_dates=[1])
    ts_df['Date'] = ts_df['Date'].map(lambda x: datetime.datetime.strptime(x, '%Y%j').date())
    ts_df['Date'] = pd.to_datetime(ts_df['Date'])

    # Mask out fill values (and could optionally also mask out mag inversions by adding another condition == 1
    # ts_df['MCD43A3_006_Albedo_WSA_shortwave'].mask(
    #     ts_df['MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave'] == 255, np.NaN, inplace=True)
    # ts_df['MCD43A3_006_Albedo_WSA_shortwave'].mask(
    #     ts_df['MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave'] == 1, np.NaN, inplace=True)
    # ts_df['Value'] = ts_df['MCD43A3_006_Albedo_WSA_shortwave']
    # del ts_df['MCD43A3_006_BRDF_Albedo_Band_Mandatory_Quality_shortwave']
    # del ts_df['MCD43A3_006_Albedo_WSA_shortwave']

    #TODO Can I use this to input multiple concatenated appears requests??
    ts_df = pd.DataFrame(ts_df.groupby(['Category', 'Date'])['Value'].mean())

    years = [i for i in range(2000, 2021, 1)]

    # Here we mask out days where the local solar zenith angle is too steep (what is cutoff?)
    # Note this will be different for each AOI (actually every pixel, but this is a simpler approach for small AOIs)
    ts_df.reset_index(inplace=True)
    szn_mask = (ts_df['Date'].dt.month >= begin_month) & (ts_df['Date'].dt.month <= end_month)
    ts_df = ts_df.loc[szn_mask]

    #ts_df['Date'] = pd.to_datetime(ts_df['Date'])
    ts_df.set_index('Date', inplace=True)
    monthly_graphs(ts_df, years, aoi_name, csv_path)
    #tenday_graphs(ts_df, years, aoi_name, csv_path)
    #overall_mean_graph(ts_df, aoi_name, csv_path, month_labels)
    #anomalies_overall_mean_graph(ts_df, years, aoi_name, csv_path)
    #anomalies_graph(ts_df, years, aoi_name, csv_path)

if __name__ == '__main__':
    main()


# Junk room: maybe stuff in here could be useful?
# ts_df.reset_index(inplace=True)
# ts_df['year'] = ts_df['Date'].dt.year
# ts_df['month'] = ts_df['Date'].dt.month
#
# # Group data first by year, then by month
# g = ts_df.groupby(['year', 'month'])
#
# # For each group, calculate the average of only the snow_depth column
# monthly_averages = g.aggregate({"Value": np.mean})
# monthly_averages.to_csv(workspace + 'grouped_date.csv')
# sys.exit()