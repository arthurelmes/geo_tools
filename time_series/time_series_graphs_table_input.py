# This makes a plot where all years are stacked up on top of each other, with a color ramp to generally
# tell them apart
import pandas as pd
import datetime as dt
import numpy as np
import sys, os

from pandas import DataFrame
from pandas import Grouper
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from cycler import cycler
from scipy import stats
import math
np.random.seed(12412412)


def filter_data_numobs(ts_df, filter_pctl):
    filter = ts_df['valid_pixels_count'].quantile(filter_pctl)
    print('Filtering out data with fewer than {x} pctl valid obs, i.e. {y} obs.'.format(x=filter_pctl, y=filter))
    num_obs_mask = (ts_df['valid_pixels_count'] >= filter)
    ts_df = ts_df.loc[num_obs_mask]
    return ts_df


def calc_anom_doy(years):
    years = years.copy()
    years = years.astype(float)

    years['mean'] = years.mean(axis=1)

    for col in years.columns:
        if '20' in col:
            years[col] = years[col] - years['mean']
    del years['mean']
    return years


def box_plot(years, aoi_name, csv_path):
    # Quck boxplot for each year
    years = years.iloc[80:250, ].copy()
    years = years.astype(float)

    overall_mean = years.stack().mean()
    data_to_plot = years.to_numpy()

    # Filter out the NaNs, otherwise the boxplot is unhappy
    # https://stackoverflow.com/questions/44305873/how-to-deal-with-nan-value-when-plot-boxplot-using-python
    mask = ~np.isnan(data_to_plot)
    filtered_data = [d[m] for d, m in zip(data_to_plot.T, mask.T)]

    # Create a figure instance
    fig_box = plt.figure(1, figsize=(3, 2))
    fig_box.suptitle(aoi_name, size=5)

    # Create an axis instance
    ax_box = fig_box.add_subplot(111)
    ax_box.set_xticklabels(list(years.columns))
    ax_box.tick_params(
        axis='x',
        labelsize=5,
        labelrotation=45
                       )
    ax_box.set_ylim(0.4, 0.9)
    ax_box.grid(b=True, which='major', color='LightGrey', linestyle='-')
    ax_box.set_yticks([0.4, 0.6, 0.8])
    plt.axhline(y=[overall_mean], linewidth=0.5, label='Overall Mean: {x}'.format(x=round(overall_mean, 2)))
    ax_box.tick_params(
        axis='y',
        labelsize=5
                   )
    ax_box.set_ylabel('Blue Sky Albedo (Overall Mean)', size=5)
    outlier_marker = dict(markerfacecolor='black', fillstyle=None, marker='.', markersize=1)

    data_2019 = filtered_data[19]
    i = 0
    plt.legend(loc='lower right', prop={'size': 4})
    # Store t-test of each year vs 2019 in txt file
    stats_txt_name = csv_path[:-4] + '_t_stats_vs_2019.txt'
    stats_txt = open(stats_txt_name, 'w')

    for dst in filtered_data:
        data_year = filtered_data[i]
        stats_txt.write('T test results for year {x}'.format(x=str(i+2000)) + '\n')
        stats_txt.write(str(stats.ttest_ind(data_year, data_2019)) + '\n')
        stats_txt.write('Mean of year {x} is {y}'.format(x=str(i+2000), y=data_year.mean()) + '\n')
        i += 1

    stats_txt.close()

    # Create the boxplot
    bp = ax_box.boxplot(filtered_data, flierprops=outlier_marker)

    # Make subdir if needed and save fig
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + '_boxplot.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def box_plot_anom(years, aoi_name, csv_path):
    # Quck boxplot for each year
    years = years.iloc[80:250, ].copy()
    years = calc_anom_doy(years)

    overall_mean = years.stack().mean()
    data_to_plot = years.to_numpy()

    # Filter out the NaNs, otherwise the boxplot is unhappy
    # https://stackoverflow.com/questions/44305873/how-to-deal-with-nan-value-when-plot-boxplot-using-python
    mask = ~np.isnan(data_to_plot)
    filtered_data = [d[m] for d, m in zip(data_to_plot.T, mask.T)]

    # Create a figure instance
    fig_box_anom = plt.figure(1, figsize=(9, 6))
    fig_box_anom.suptitle(aoi_name)

    # Create an axis instance
    ax_box_anom = fig_box_anom.add_subplot(111)
    ax_box_anom.set_xticklabels(list(years.columns))
    ax_box_anom.tick_params(
        axis='x',
        labelsize=5,
        labelrotation=45
                       )
    ax_box_anom.set_ylim(-0.25, 0.25)
    ax_box_anom.grid(b=True, which='major', color='LightGrey', linestyle='-')
    plt.axhline(y=0)
    ax_box_anom.tick_params(
        axis='y',
        labelsize=5
                   )
    ax_box_anom.set_ylabel('Blue Sky Albedo Anomaly')
    outlier_marker = dict(markerfacecolor='black', fillstyle=None, marker='.')

    # Create the boxplot
    bp = ax_box_anom.boxplot(filtered_data, flierprops=outlier_marker)

    # Make subdir if needed and save fig
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + '_boxplot_anomalies.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def vert_stack_plot(years, nyears, strt_year, end_year, aoi_name, csv_path):
    ### Create plot with all years stacked vertically in a series of parallel time series graphs
    #years = years.iloc[80:250, ].copy()
    ncols = 1
    nrows = nyears + 1

    # create the plots
    fig_stack = plt.figure(figsize=(10, 15))
    axes = [fig_stack.add_subplot(nrows, ncols, r * ncols + c + 1) for r in range(0, nrows) for c in range(0, ncols)]

    yr = strt_year
    # add the data one year at a time
    for ax_stack in axes:
        col = str(yr)
        ax_stack.plot(years[col])
        ax_stack.set_xlim(80, 250)
        ax_stack.set_ylim(0.0, 1.0)
        ax_stack.grid(b=True, which='major', color='LightGrey', linestyle='-')
        ax_stack.set_yticks([0.5])
        ax_stack.tick_params(
            axis='y',
            labelsize=5
                       )
        ax_stack.text(260, 0.33, str(yr), fontsize=8)
        # Remove ticks for everything but final year so no overlapping/messiness
        if yr != end_year:
            ax_stack.set_xticklabels([])
        # Add label to middle year
        if yr == round((end_year + strt_year) / 2, 0):
            ax_stack.set_ylabel('Blue Sky Albedo')
        yr += 1

    # This only needs to apply to the last ax
    ax_stack.set_xlabel('DOY')
    ax_stack.set_ylim(0.0, 1.0)
    fig_stack.suptitle(aoi_name, y=0.9)

    # Make subdir if needed and save fig
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') +
                             '_white_sky_time_series_vert_stack.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def vert_stack_plot_anom(years, nyears, strt_year, end_year, aoi_name, csv_path):
    ### Create plot with all years stacked vertically in a series of parallel time series graphs
    ncols = 1
    nrows = nyears + 1

    years = years.iloc[80:250, ].copy()

    years = calc_anom_doy(years)

    # create the plots
    fig_stack_anom = plt.figure(figsize=(10, 15))
    axes = [fig_stack_anom.add_subplot(nrows, ncols, r * ncols + c + 1) for r in range(0, nrows) for c in range(0, ncols)]

    yr = strt_year
    # add the data one year at a time
    for ax_stack_anom in axes:
        col = str(yr)
        ax_stack_anom.plot(years[col])
        ax_stack_anom.set_xlim(80, 250)
        ax_stack_anom.set_ylim(-0.3, 0.3)
        ax_stack_anom.grid(b=True, which='major', color='LightGrey', linestyle='-')
        ax_stack_anom.set_yticks([0.0])
        ax_stack_anom.tick_params(
            axis='y',
            labelsize=5
                       )
        ax_stack_anom.text(260, -0.01, str(yr), fontsize=8)
        # Remove ticks for everything but final year so no overlapping/messiness
        if yr != end_year:
            ax_stack_anom.set_xticklabels([])
        # Add label to middle year
        if yr == round((end_year + strt_year) / 2, 0):
            ax_stack_anom.set_ylabel('Blue Sky Albedo Anomalies')
        yr += 1

    # This only needs to apply to the last ax
    ax_stack_anom.set_xlabel('DOY')
    ax_stack_anom.set_ylim(-0.3, 0.3)
    fig_stack_anom.suptitle(aoi_name, y=0.9)

    # Make subdir if needed and save fig
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') +
                             '_white_sky_time_series_vert_stack_anomalies.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def overpost_all_plot(years, aoi_name, csv_path):
    ### Create a plot where all the years are combined in a single graph


    fig_comb = plt.figure(figsize=(10,5))
    ax_comb = fig_comb.add_subplot(111)

    # Set colormap and cycler to automatically apply colors to years plotted below
    n = len(years.columns)
    color = plt.cm.hsv(np.linspace(0, 1, n))
    mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

    # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
    # check for year part first
    for ycol in years.columns:
        if '20' in ycol:
            ax_comb.plot(years.index, years[ycol], label=str(ycol), alpha=0.2)

    ax_comb.plot(years.index, years['2019'], label='2019 Emphasis', color='firebrick')
    ax_comb.set_xlabel('DOY')
    ax_comb.set_ylabel('Blue Sky Albedo')
    ax_comb.set_ylim(0.0, 1.0)
    fig_comb.suptitle(aoi_name)
    plt.legend(ncol=4, loc='lower left', fontsize=10)

    # Save fig in figs subdir, making the subdir if needed
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + 'white_sky_time_series_overpost_stack.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def overpost_all_plot_anom(years, aoi_name, csv_path):
    ### Create a plot where all the years are combined in a single graph

    years = calc_anom_doy(years)
    years = years.iloc[80:250, ].copy()

    fig_comb_anom = plt.figure(figsize=(10,5))
    ax_comb_anom = fig_comb_anom.add_subplot(111)

    # Set colormap and cycler to automatically apply colors to years plotted below
    n = len(years.columns)
    color = plt.cm.hsv(np.linspace(0, 1, n))
    mpl.rcParams['axes.prop_cycle'] = cycler('color', color)

    # Add each year to same plot -- for some reason a 'undefined' values comes back first, so
    # check for year part first
    for ycol in years.columns:
        if '20' in ycol:
            ax_comb_anom.plot(years.index, years[ycol], label=str(ycol), alpha=0.2)

    ax_comb_anom.plot(years.index, years['2019'], label='2019 Emphasis', color='firebrick')
    ax_comb_anom.set_xlabel('DOY')
    ax_comb_anom.set_ylabel('Blue Sky Albedo Anomaly')
    ax_comb_anom.set_ylim(-0.3, 0.3)
    fig_comb_anom.suptitle(aoi_name)
    plt.legend(ncol=4, loc='lower left', fontsize=10)

    # Save fig in figs subdir, making the subdir if needed
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') +
                             'white_sky_time_series_overpost_stack_anomalies.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def year_vs_avg_plot(years, aoi_name, csv_path):
    #### Now plot 2019 vs the 2000 - 2020 avg

    years = years.copy()
    years = years.astype(float)

    # Calculate stats
    cols = years.loc[:, "2000":"2020"]

    years['base_mean'] = cols.mean(axis=1)
    years['base_sd'] = cols.std(axis=1)
    years = years.iloc[80:250, ].copy()

    #TODO same issue here as in the anomaly version of this plot -- why the last value jump?

    fig_comb_mean = plt.figure(figsize=(3, 2))
    ax_comb_mean = fig_comb_mean.add_subplot(111)
    ax_comb_mean.plot(years.index, years['2003'], label='2003', color='#ffd92f', linewidth=0.75)
    ax_comb_mean.plot(years.index, years['2010'], label='2010', color='#66c2a5', linewidth=0.75)
    ax_comb_mean.plot(years.index, years['2012'], label='2012', color='#a6d854', linewidth=0.75)
    ax_comb_mean.plot(years.index, years['2019'], label='2019', color='firebrick', linewidth=0.75)
    ax_comb_mean.plot(years.index, years['2020'], label='2020', color='#fc8d62', linewidth=0.75)
    ax_comb_mean.plot(years.index[:], years['base_mean'][:], label='2000-2020 Mean +/- 1 SD', color='#8da0cb',
                      alpha=0.4, linewidth=0.7)
    plt.fill_between(years.index[:], years['base_mean'][:] - years['base_sd'][:], years['base_mean'][:] +
                     years['base_sd'][:], color='lightgrey')

    ax_comb_mean.set_ylim(0.4, 0.9)
    ax_comb_mean.set_ylabel('Blue Sky Albedo', size=5)
    ax_comb_mean.set_xlabel('DOY', size=5)
    ax_comb_mean.tick_params(
        axis='x',
        labelsize=5,
        labelrotation=45
                       )
    ax_comb_mean.tick_params(
        axis='y',
        labelsize=5,
                       )
    plt.legend(loc='lower left', prop={'size': 5})

    fig_comb_mean.suptitle(aoi_name, size=5)

    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + '_2000-2020_mean_' +
                             '_white_sky_time_series_2019_vs_mean.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def year_vs_avg_plot_anom(years, aoi_name, csv_path):
    #### Now plot 2019 vs the 2000 - 2018 avg

    #TODO shouldn't the purple line in this plot be exactly flat? it probably isn't because of rounding -- check
    years = calc_anom_doy(years)

    # Calculate stats
    cols = years.loc[:, "2000":"2018"]
    years['base_mean'] = cols.mean(axis=1)
    years['base_sd'] = cols.std(axis=1)
    years = years.iloc[80:250, ].copy()
    # base_mean = cols.mean(axis=1)
    # base_sd = cols.std(axis=1)

    fig_comb_mean_anom = plt.figure(figsize=(10, 5))
    ax_comb_mean_anom = fig_comb_mean_anom.add_subplot(111)
    ax_comb_mean_anom.plot(years.index, years['2019'], label='2019', color='firebrick')
    ax_comb_mean_anom.plot(years.index[:], years['base_mean'][:], label='2000-2018 Mean +/- 1 SD',
                           color='slateblue', alpha=0.5)
    plt.fill_between(years.index[:], years['base_mean'][:] - years['base_sd'][:],
                     years['base_mean'][:] + years['base_sd'][:], color='lightgrey')

    ax_comb_mean_anom.set_ylim(-0.3, 0.3)
    ax_comb_mean_anom.set_ylabel('Blue Sky Albedo Anomaly')
    ax_comb_mean_anom.set_xlabel('DOY')
    plt.legend(loc='lower left')

    fig_comb_mean_anom.suptitle(aoi_name)

    # Save the fig, make subdir if needed
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + '_2000-2020_mean_' +
                             '_white_sky_time_series_2019_vs_mean_anomalies.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    # Update these as needed
    filter_pctl = 0.25
    workspace = '/home/arthur/Dropbox/projects/greenland/aoi_albedo_time_series/catchments/'
    if workspace[:-1] != '/':
        workspace = workspace + '/'
    csv_name = 'actual_albedo_catchment_6.2_ekholm_stats.csv'
    aoi_name = 'Catchment 6.2 (ValiObs filter = {x} Pctl)'.format(x=filter_pctl)
    dt_indx = pd.date_range('2000-01-01', '2020-12-31')
    csv_path = workspace + csv_name

    # set this value to filter out observations with fewer than the given percentile of valid observations

    # Define the fields of interest so we can ignore the rest
    fields = ['date', 'mean', 'valid_pixels_count']

    # Import raw APPEARS output
    ts_df = pd.read_csv(csv_path, usecols=fields, parse_dates=[1])

    # Make the date index, then group by it to make monthly averages
    ts_df['date'] = pd.to_datetime(ts_df['date'])
    ts_df['mean'].replace({pd.NaT: np.nan}, inplace=True)
    ts_df = filter_data_numobs(ts_df, filter_pctl)
    del ts_df['valid_pixels_count']

    # Simple masking by month due to small available pixels, so noisy even when szn-masked
    begin_month = 3
    end_month = 9
    szn_mask = (ts_df['date'].dt.month >= begin_month) & (ts_df['date'].dt.month <= end_month)
    ts_df = ts_df.loc[szn_mask]

    ts_df.set_index('date', inplace=True)

    series = ts_df.squeeze()
    strt_year = dt_indx[0].to_pydatetime().year # do I need this stuff
    end_year = dt_indx[-1].to_pydatetime().year # and this?
    nyears = end_year - strt_year               # and this?
    series = series.reindex(dt_indx, fill_value=np.NaN)

    groups = series.groupby(Grouper(freq='A'))
    years = DataFrame()

    # This is how the dataframe is set up with each column being a year of data, each row a doy
    for name, group in groups:
        years[name.year] = group.values[:364]

    # make columns into strings for easier plot labeling
    years.columns = years.columns.astype(str)

    box_plot(years, aoi_name, csv_path)
    # box_plot_anom(years, aoi_name, csv_path)
    # vert_stack_plot(years, nyears, strt_year, end_year, aoi_name, csv_path)
    # vert_stack_plot_anom(years, nyears, strt_year, end_year, aoi_name, csv_path)
    year_vs_avg_plot(years, aoi_name, csv_path)
    # year_vs_avg_plot_anom(years, aoi_name, csv_path)
    # overpost_all_plot(years, aoi_name, csv_path)
    # overpost_all_plot_anom(years, aoi_name, csv_path)

if __name__ == '__main__':
    main()
