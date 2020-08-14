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
    years = years.astype(float)
    overall_mean = years.stack().mean()
    data_to_plot = years.to_numpy()

    # Filter out the NaNs, otherwise the boxplot is unhappy
    # https://stackoverflow.com/questions/44305873/how-to-deal-with-nan-value-when-plot-boxplot-using-python
    mask = ~np.isnan(data_to_plot)
    filtered_data = [d[m] for d, m in zip(data_to_plot.T, mask.T)]

    # Create a figure instance
    fig_box = plt.figure(1, figsize=(9, 6))
    fig_box.suptitle(aoi_name)

    # Create an axis instance
    ax_box = fig_box.add_subplot(111)
    ax_box.set_xticklabels(list(years.columns))
    ax_box.tick_params(
        axis='x',
        labelsize=5,
        labelrotation=45
                       )
    ax_box.set_ylim(0.0, 1.0)
    ax_box.grid(b=True, which='major', color='LightGrey', linestyle='-')
    ax_box.set_yticks([overall_mean])
    ax_box.tick_params(
        axis='y',
        labelsize=5
                   )
    ax_box.set_ylabel('White sky Albedo (Overall Mean)')
    outlier_marker = dict(markerfacecolor='black', fillstyle=None, marker='.')

    # print(filtered_data[0].shape)
    # data_years = np.empty(filtered_data[0].shape)
    # for i in filtered_data:
    #     np.concatenate((data_years, i))
    # print(data_years.shape)
    data_climo = np.concatenate((filtered_data[0], filtered_data[1]))

    #print(len(filtered_data))

    data_2019 = filtered_data[19]
    i = 0

    # Store t-test of each year vs 2019 in txt file
    stats_txt_name = csv_path[:-4] + '_t_stats_vs_2019.txt'
    stats_txt = open(stats_txt_name, 'w')

    for dst in filtered_data:
        data_year = filtered_data[i]
        #print('T test results for year {x}'.format(x=str(i+2000)))
        stats_txt.write('T test results for year {x}'.format(x=str(i+2000)) + '\n')
        #print(stats.ttest_ind(data_year, data_2019))
        stats_txt.write(str(stats.ttest_ind(data_year, data_2019)) + '\n')
        #print('Mean of year {x} is {y}'.format(x=str(i+2000), y=data_year.mean()))
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


def box_plot_anom(years, aoi_name, csv_path):
    # Quck boxplot for each year

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
    ax_box_anom.set_ylim(-0.5, 0.5)
    ax_box_anom.grid(b=True, which='major', color='LightGrey', linestyle='-')
    #ax_box_anom.set_yticks()
    ax_box_anom.tick_params(
        axis='y',
        labelsize=5
                   )
    ax_box_anom.set_ylabel('White sky Albedo Anomaly')
    outlier_marker = dict(markerfacecolor='black', fillstyle=None, marker='.')

    data_climo = np.concatenate((filtered_data[0], filtered_data[1]))

    data_2019 = filtered_data[19]
    i = 0
    for dst in filtered_data:
        data_year = filtered_data[i]
        # print('T test results for year {x}'.format(x=str(i+2000)))
        # print(stats.ttest_ind(data_year, data_2019))
        # print('Mean of year {x} is {y}'.format(x=str(i+2000), y=data_year.mean()))
        i += 1

    # Create the boxplot
    bp = ax_box_anom.boxplot(filtered_data, flierprops=outlier_marker)

    # Make subdir if needed and save fig
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + '_boxplot_anomalies.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')


def vert_stack_plot(years, nyears, strt_year, end_year, aoi_name, csv_path):
    ### Create plot with all years stacked vertically in a series of parallel time series graphs
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
            ax_stack.set_ylabel('White sky Albedo')
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


def vert_stack_plot_anom(years, nyears, strt_year, end_year, aoi_name, csv_path):
    ### Create plot with all years stacked vertically in a series of parallel time series graphs
    ncols = 1
    nrows = nyears + 1

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
            ax_stack_anom.set_ylabel('White sky Albedo Anomalies')
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

    ax_comb.plot(years.index, years['2019'], label='2019 Emphasis', color='orange')
    ax_comb.set_xlabel('DOY')
    ax_comb.set_ylabel('White Sky Albedo')
    ax_comb.set_ylim(0.0, 1.0)
    fig_comb.suptitle(aoi_name)
    plt.legend(ncol=4, loc='lower left', fontsize=10)

    # Save fig in figs subdir, making the subdir if needed
    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + 'white_sky_time_series_overpost_stack.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')


def overpost_all_plot_anom(years, aoi_name, csv_path):
    ### Create a plot where all the years are combined in a single graph

    years = calc_anom_doy(years)

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

    ax_comb_anom.plot(years.index, years['2019'], label='2019 Emphasis', color='orange')
    ax_comb_anom.set_xlabel('DOY')
    ax_comb_anom.set_ylabel('White Sky Albedo Anomaly')
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


def year_vs_avg_plot(years, aoi_name, csv_path):
    #### Now plot 2019 vs the 2000 - 2018 avg

    years = years.copy()
    years = years.astype(float)

    # Calculate stats
    cols = years.loc[:, "2000":"2020"]

    years['base_mean'] = cols.mean(axis=1)
    years['base_sd'] = cols.std(axis=1)
    years = years.iloc[80:250, ].copy()

    #TODO same issue here as in the anomaly version of this plot -- why the last value jump?

    fig_comb_mean = plt.figure(figsize=(10, 5))
    ax_comb_mean = fig_comb_mean.add_subplot(111)
    ax_comb_mean.plot(years.index, years['2010'], label='2010', color='chartreuse')
    ax_comb_mean.plot(years.index, years['2012'], label='2012', color='yellow')
    ax_comb_mean.plot(years.index, years['2014'], label='2014', color='green')
    ax_comb_mean.plot(years.index, years['2019'], label='2019', color='darkorange')
    ax_comb_mean.plot(years.index, years['2020'], label='2020', color='firebrick')
    ax_comb_mean.plot(years.index[:], years['base_mean'][:], label='2000-2020 Mean +/- 1 SD', color='slateblue',
                      alpha=0.5)
    plt.fill_between(years.index[:], years['base_mean'][:] - years['base_sd'][:], years['base_mean'][:] +
                     years['base_sd'][:], color='lightgrey')
    # ax_comb_mean.plot(years.index[:-85], years['base_mean'][:-85], label='2000-2020 Mean +/- 1 SD', color='slateblue',
    #                   alpha=0.5)
    # plt.fill_between(years.index[:-85], years['base_mean'][:-85] - years['base_sd'][:-85], years['base_mean'][:-85] +
    #                  years['base_sd'][:-85], color='lightgrey')
    ax_comb_mean.set_ylim(0.0, 1.0)
    ax_comb_mean.set_ylabel('White Sky Albedo')
    ax_comb_mean.set_xlabel('DOY')
    plt.legend(loc='lower left')

    fig_comb_mean.suptitle(aoi_name)

    file_path, file_name = os.path.split(csv_path)
    save_name = os.path.join(file_path, 'figs', aoi_name.replace(' ', '_') + '_2000-2020_mean_' +
                             '_white_sky_time_series_2019_vs_mean.png')
    if not os.path.isdir(os.path.join(file_path, 'figs')):
        os.mkdir(os.path.join(file_path, 'figs'))
    plt.savefig(save_name, dpi=300, bbox_inches='tight')


def year_vs_avg_plot_anom(years, aoi_name, csv_path):
    #### Now plot 2019 vs the 2000 - 2018 avg

    #TODO shouldn't the purple line in this plot be exactly flat? it probably isn't because of rounding -- check
    years = calc_anom_doy(years)

    # Calculate stats
    cols = years.loc[:, "2000":"2018"]
    years['base_mean'] = cols.mean(axis=1)
    years['base_sd'] = cols.std(axis=1)
    # base_mean = cols.mean(axis=1)
    # base_sd = cols.std(axis=1)

    #TODO wtf. why is the last value some giant leap up? SZN? or maybe the anom didn't get calculated right?

    fig_comb_mean_anom = plt.figure(figsize=(10, 5))
    ax_comb_mean_anom = fig_comb_mean_anom.add_subplot(111)
    ax_comb_mean_anom.plot(years.index, years['2019'], label='2019', color='orange')
    ax_comb_mean_anom.plot(years.index[:], years['base_mean'][:], label='2000-2018 Mean +/- 1 SD',
                           color='slateblue', alpha=0.5)
    plt.fill_between(years.index[:], years['base_mean'][:] - years['base_sd'][:],
                     years['base_mean'][:] + years['base_sd'][:], color='lightgrey')

    ax_comb_mean_anom.set_ylim(-0.3, 0.3)
    ax_comb_mean_anom.set_ylabel('White Sky Albedo Anomaly')
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


def calc_sza(lat, doy):

    doy = int(doy)
    lat = float(lat)
    # ported from MCD43C code
    # time uses 24 hours with local noon = 12
    time = 12
    h = (12.0 - time)/12.0 * math.pi
    lat = lat * math.pi / 180.0
    delta = -23.45 * (math.pi / 180) * math.cos(2 * math.pi / 365.0 * (doy + 10))
    sza = math.acos(math.sin(lat) * math.sin(delta) + math.cos(lat) * math.cos(delta) * math.cos(h))
    sza = sza * 180.0 / math.pi

    return sza


def main():
    # Update these as needed
    workspace = '/home/arthur/Dropbox/projects/greenland/blue_sky_variables/actual_albedo/'
    csv_name = 'west_coast_greenland_actual_albedo_2000_2020.csv'
    aoi_name = 'West Coast 100 km Buffer HDF'
    dt_indx = pd.date_range('2000-01-01', '2020-12-31')
    csv_path = workspace + csv_name

    # Define the fields of interest so we can ignore the rest
    fields = ['date', 'mean']

    # Import raw APPEARS output
    ts_df = pd.read_csv(csv_path, usecols=fields, parse_dates=[1])

    # Make the date index, then group by it to make monthly averages
    ts_df['date'] = pd.to_datetime(ts_df['date'])

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

    # print(years.head())
    # years = years.loc[60:250, ].copy()
    # print(years.head())
    # sys.exit()
    #make columns into strings for easier plot labeling
    years.columns = years.columns.astype(str)

    box_plot(years, aoi_name, csv_path)
    box_plot_anom(years, aoi_name, csv_path)
    vert_stack_plot(years, nyears, strt_year, end_year, aoi_name, csv_path)
    vert_stack_plot_anom(years, nyears, strt_year, end_year, aoi_name, csv_path)
    year_vs_avg_plot(years, aoi_name, csv_path)
    year_vs_avg_plot_anom(years, aoi_name, csv_path)
    overpost_all_plot(years, aoi_name, csv_path)
    overpost_all_plot_anom(years, aoi_name, csv_path)

if __name__ == '__main__':
    main()
