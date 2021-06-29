# This script plots out the summary stats created during plot_two_tiles.py
# The idea is to run that script on a long time series of data, then use this
# one to sumamrize the results.
# Author: Arthur Elmes
# Date: 2020-12-11

import pandas as pd
import os, sys
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import csv


def write_csv(tile_n, m, v, rmse, mb, sns, product):
    # if no csv exists, create it, otherwise append stats
    stats_csv_name = (os.path.join(workspace, "summary_stats.csv"))
    print('Writing stats to: {}'.format(stats_csv_name))
    stats_write = (rmse, mb)
    header = ['Product', 'Tile', 'RMSE grand mean', 'Mean Bias F1 - F2 _grand_mean', 'Band 1', 'Band 2', 'Sensor vs Sensor']

    if os.path.isfile(stats_csv_name):
        with open(stats_csv_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.DictWriter(write_obj, fieldnames=header)

            # Add contents of list as last row in the csv file
            csv_writer.writerow({'Product': product,
                                 'Tile': tile_n,
                                 'RMSE grand mean': stats_write[0],
                                 'Mean Bias F1 - F2 _grand_mean': stats_write[1],
                                 'Band 1': m,
                                 'Band 2': v,
                                 'Sensor vs Sensor': sns})
    else:
        with open(stats_csv_name, 'w', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.DictWriter(write_obj, fieldnames=header)

            # Initialize the new file with headers
            csv_writer.writeheader()

            # Add contents of list as last row in the csv file
            csv_writer.writerow({'Product': product,
                                 'Tile': tile_n,
                                 'RMSE grand mean': stats_write[0],
                                 'Mean Bias F1 - F2 _grand_mean': stats_write[1],
                                 'Band 1': m,
                                 'Band 2': v,
                                 'Sensor vs Sensor': sns})


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
        ax[1].axhline(0, c='white', ls='--')

        fig.suptitle(' '.join(out_name.split('_')), color='white')
        #TODO make this dir if it doesn't exist or the script cries
        fig.savefig(workspace + "/png/{}_{}.png".format(out_name, df.name), facecolor='k')
        plt.close()


def modis_viirs_band(modis_band):
    bands = {'Band1': 'M5',
             'Band2': 'M7',
             'Band3': 'M3',
             'Band4': 'M4',
             'Band5': 'M8',
             'Band6': 'M10',
             'Band7': 'M11',
             'nir': 'nir',
             'shortwave': 'shortwave',
             'vis': 'vis'}
    viirs_band = bands[modis_band]
    return viirs_band


def split_by_products(stats, band, tile_n, product):
    # Subset by band
    v_band = modis_viirs_band(band_name)
    m_band = band

    stats = stats.loc[(stats['B1'] == m_band) | (stats['B1'] == v_band)].copy()
    stats = stats[stats['F1'].str.contains(product)].copy()
    
    # Clean up df and add date index
    #TODO THIS NEEDS TO BE CHANGED TO ACCOMODATE EITHER MCD-MCD OR MCD-V?? or VNP-VJ1 comparisons due to file name diffncs
    stats['doy'] = stats['F2'].apply(lambda x: x[13:16])
    stats['year'] = stats['F2'].apply(lambda x: x[9:13])
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

    # Append results to an aggregate csv
    write_csv(tile_n, m_band, v_band, stats_mcd_vnp['RMSE'].mean(), stats_mcd_vnp['MB'].mean(), stats_mcd_vnp.name, product)
    write_csv(tile_n, m_band, v_band, stats_mcd_vj1['RMSE'].mean(), stats_mcd_vj1['MB'].mean(), stats_mcd_vj1.name, product)
    write_csv(tile_n, m_band, v_band, stats_vj1_vnp['RMSE'].mean(), stats_vj1_vnp['MB'].mean(), stats_vj1_vnp.name, product)

    dfs = [stats_mcd_vnp, stats_mcd_vj1, stats_vj1_vnp]
    return dfs


workspace = '/ipswich/data01/arthur.elmes/test_C61/'
os.chdir(workspace)
bands = ['shortwave']
#bands = ['Band1', 'Band2', 'Band3', 'Band4', 'Band5', 'Band6', 'Band7', 'nir', 'shortwave', 'vis']
csvs = glob(workspace + "h*stats.csv")
#products = ['A3', 'A4']
products = ['A3']

if os.path.isfile((os.path.join(workspace, "summary_stats.csv"))):
    os.remove((os.path.join(workspace, "summary_stats.csv")))

for product in products:
    for band_name in bands:
        for csv_n in csvs:
            stats_csv = pd.read_csv(csv_n)
            v_band = modis_viirs_band(band_name)
            tile = csv_n.split('/')[-1][:6]

            # Run everything
            dfs = split_by_products(stats_csv, band_name, tile, product)
            plot_stats(dfs, os.path.basename(csv_n)[:6] + "_" + product + '_' + band_name + "_" + v_band)
