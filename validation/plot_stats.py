""" This script plots out the summary stats created during plot_two_tiles.py
The idea is to run that script on a long time series of data, then use this
one to sumamrize the results.
Author: Arthur Elmes
Date: 2020-12-11"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from glob import glob


def compose_date(years, months=1, days=1, weeks=None, hours=None, minutes=None,
                 seconds=None, milliseconds=None, microseconds=None, nanoseconds=None):
    years = np.asarray(years) - 1970
    months = np.asarray(months) - 1
    days = np.asarray(days) - 1
    types = ('<M8[Y]', '<m8[M]', '<m8[D]', '<m8[W]', '<m8[h]',
             '<m8[m]', '<m8[s]', '<m8[ms]', '<m8[us]', '<m8[ns]')
    vals = (years, months, days, weeks, hours, minutes, seconds,
            milliseconds, microseconds, nanoseconds)
    return sum(np.asarray(v, dtype=t) for t, v in zip(types, vals)
               if v is not None)


def plot_stats(df_list, out_name):
    for df in df_list:
        x = df['doy']
        y = df['RMSE']
        z = df['MB']

        fig, ax = plt.subplots(1, 2, figsize=(8, 4))
        fig.tight_layout(pad=3)
        fig.set_facecolor('black')
        ax[0].set_facecolor('black')
        ax[1].set_facecolor('black')

        ax[0].set_ylabel('RMSE of {}'.format(df.name.replace('_', ' ')), c='w')
        ax[1].set_ylabel('MB of {}'.format(df.name.replace('_', ' ')), c='w')

        for i in range(0, 2):
            ax[i].set_xlabel('2019 DOY', c='w')
            ax[i].spines['bottom'].set_color('white')
            ax[i].spines['left'].set_color('white')
            ax[i].xaxis.label.set_color('white')
            ax[i].yaxis.label.set_color('white')
            ax[i].tick_params(axis='x', colors='white')
            ax[i].tick_params(axis='y', colors='white')

        ax[0].plot(x, y, c='orange')
        ax[1].plot(x, z, c='turquoise')

        fig.suptitle(out_name, color='white')
        fig.savefig(workspace + "{}_{}.png".format(out_name, df.name), facecolor='k')


def split_by_products(df):
    # Clean up df and add date index
    stats['doy'] = stats['F2'].apply(lambda x: x[14:17])
    stats['year'] = stats['F2'].apply(lambda x: x[10:14])
    stats['doy'] = stats['doy'].astype(int)
    stats['year'] = stats['year'].astype(int)
    stats.sort_values(['doy'], inplace=True)
    stats.drop_duplicates(keep='first', inplace=True)
    stats.index = compose_date(stats['year'], days=stats['doy'])
    stats['MB'] = stats['Mean Bias F1 - F2']
    stats.drop(['Mean Bias F1 - F2'], axis=1, inplace=True)

    # Separate out the different sensors for comparison
    stats_mcd_vnp = stats[stats['F1'].str.contains('MCD')]
    stats_mcd_vnp = stats_mcd_vnp[stats_mcd_vnp['F2'].str.contains('VNP')]
    stats_mcd_vnp.name = 'MCD_vs_VNP'
    # print(stats_mcd_vnp.head())

    stats_mcd_vj1 = stats[stats['F1'].str.contains('MCD')]
    stats_mcd_vj1 = stats_mcd_vj1[stats_mcd_vj1['F2'].str.contains('VJ1')]
    stats_mcd_vj1.name = 'MCD_vs_VJ1'
    # print(stats_mcd_vj1.head())

    stats_vj1_vnp = stats[stats['F1'].str.contains('VJ1')]
    stats_vj1_vnp = stats_vj1_vnp[stats_vj1_vnp['F2'].str.contains('VNP')]
    stats_vj1_vnp.name = 'VJ1_vs_VNP'
    # print(stats_vj1_vnp.head())

    dfs = [stats_mcd_vnp, stats_mcd_vj1, stats_vj1_vnp]
    return dfs


workspace = '/home/arthur/Dropbox/projects/modis_viirs_continuity/sensor_intercompare/stats/'
os.chdir(workspace)

csvs = glob(workspace + "*stats.csv")

for csv in csvs:
    stats = pd.read_csv(csv)

    # Run everything
    dfs = split_by_products(stats)
    plot_stats(dfs, os.path.basename(csv)[:6])
