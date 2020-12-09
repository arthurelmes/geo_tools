""" This script plots SURFRAD albedo against extracted satellite data (use ../time_series/extract_samples_modisviirs43.py)
 and the pre-exisiting IDL SURFRAD formatting code (readgroundmeasurement_surfrad.pro and calaveragep.pro, currently
 in Arthur's neponset homedir: /home/arthur.elmes/code/val_data/). These format data correctly for ingestion into
 this script.
 Author: Arthur Elmes
 Date: 2020-12-4
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys, csv


#TODO change to CLI arg
workspace = '/home/arthur/Dropbox/projects/modis_viirs_continuity/in_situ/'

# SURFRAD data

# These should be the the SURFRAD standard abbreviations
stn_list = ['drk', 'tbl', 'ftp', 'sxf']

# make csv to hold stats
stats_fields = ['stn', 'rmse_mcd_sfrd', 'mb_mcd_sfrd', 'rmse_vnp_sfrd', 'mb_vnp_sfrd', 'rmse_vj1_sfrd', 'mb_vj1_sfrd']
csv_fname = workspace + '/sfrd_stats.csv'

with open(csv_fname, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(stats_fields)


for stn in stn_list:
    os.chdir(os.path.join(workspace, 'surfrad'))
    sfrd = pd.read_csv(stn + '_2019.csv')

    # Extracted data from MODIS/VIIRS
    mcd = pd.read_csv(os.path.join(workspace, 'extracted', 'mcd')
                      + '/surfrad_sites_subset_formatted_extracted_values_MCD43A3.csv',
                      index_col=0)
    vnp = pd.read_csv(os.path.join(workspace, 'extracted', 'vnp')
                      + '/surfrad_sites_subset_formatted_extracted_values_VNP43MA3.csv',
                      index_col=0)
    vj1 = pd.read_csv(os.path.join(workspace, 'extracted', 'vj1')
                      + '/surfrad_sites_subset_formatted_extracted_values_VJ143MA3.csv',
                      index_col=0)
    wsa = stn + '_wsa'
    bsa = stn + '_bsa'
    wsa_mcd = stn + '_wsa_mcd'
    bsa_mcd = stn + '_bsa_mcd'
    wsa_vnp = stn + '_wsa_vnp'
    bsa_vnp = stn + '_bsa_vnp'
    wsa_vj1 = stn + '_wsa_vj1'
    bsa_vj1 = stn + '_bsa_vj1'

    # Make the WSA variables distinguishable
    mcd.rename(columns={wsa: wsa_mcd,
                        bsa: bsa_mcd}, inplace=True)
    vnp.rename(columns={wsa: wsa_vnp,
                        bsa: bsa_vnp}, inplace=True)
    vj1.rename(columns={wsa: wsa_vj1,
                        bsa: bsa_vj1}, inplace=True)

    # Convert the individual data fields to datetime field
    sfrd['Date'] = pd.to_datetime(sfrd['year'].map(str) + '-' + sfrd['month'].map(str) + '-' + sfrd['day'].map(str))
    sfrd['doy'] = sfrd['Date'].dt.dayofyear

    # Then get julian date from it, to use as a join field
    sfrd.set_index('doy', inplace=True)
    sfrd.drop(columns=['month', 'day', 'year', 'gnd_sdev', 'dir/dif_ratio', 'diffuse/(dir+diff)', 'zen', 'Date'],
              axis=1, inplace=True)

    # This plots the set of scatterlpots against the SURFRAD (x) and satellite (y)
    #TODO this whole section should automatically have the number of figs as input datasets, e.g. just MCD, or MCD and VNP, etc
    sfrd = sfrd.join(mcd,  lsuffix='_sfrd', rsuffix='_snsr')
    sfrd = sfrd.join(vnp,  lsuffix='_sfrd', rsuffix='_snsr')
    sfrd = sfrd.join(vj1,  lsuffix='_sfrd', rsuffix='_snsr')

    stn_wsa_col = sfrd['gnd_mean']
    mcd = sfrd[stn + '_wsa_mcd']
    vnp = sfrd[stn + '_wsa_vnp']
    vj1 = sfrd[stn + '_wsa_vj1']

    #TODO this should obviously be a function
    # Calculate RMSE and Mean Bias
    rmse_mcd_sfrd = ((stn_wsa_col - mcd) ** 2).mean() ** 0.5
    mb_mcd_sfrd = stn_wsa_col.mean() - mcd.mean()
    rmse_vnp_sfrd = ((stn_wsa_col - vnp) ** 2).mean() ** 0.5
    mb_vnp_sfrd = stn_wsa_col.mean() - vnp.mean()
    rmse_vj1_sfrd = ((stn_wsa_col - vj1) ** 2).mean() ** 0.5
    mb_vj1_sfrd = stn_wsa_col.mean() - vj1.mean()

    stats_row = [stn, rmse_mcd_sfrd, mb_mcd_sfrd, rmse_vnp_sfrd, mb_vnp_sfrd, rmse_vj1_sfrd, mb_vj1_sfrd]
    with open(csv_fname, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(stats_row)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10,3))
    ax1.set_facecolor('k')
    ax2.set_facecolor('k')
    ax3.set_facecolor('k')

    ax1.scatter(stn_wsa_col, mcd, color='#d95f02', marker='^', s=5, label='MCD43A3')
    ax2.scatter(stn_wsa_col, vnp, color='#7570b3', marker='+', s=5, label='VNP43MA3')
    ax3.scatter(stn_wsa_col, vj1, color='#e7298a', marker='d', s=5, label='VJ143MA3')

    ax1.set_ylabel('Satellite Albedo')
    fig.text(0.5, 0.0, 'SURFRAD Albedo', ha='center')

    fig.legend(loc='lower right', bbox_to_anchor=(0.21, 0.68))
    fig.tight_layout()
    plt.savefig(workspace + stn + '_sat_vs_surfrad_scatters.png')
    plt.show()

    # This plots the satellite and SURFRAD data against DOY, so a time series
    sfrd.reset_index(inplace=True)
    doy = sfrd['doy']

    # Slapdash conversion between stn abbr and full namm
    #TODO this should be done with a dictionary instead, way above, that is iterated over

    ['drk', 'tbl', 'ftp', 'sxf']
    if stn == 'drk':
        stn_full = 'Desert Rock, NV'
    elif stn == 'tbl':
        stn_full = 'Table Mountain, CO'
    elif stn == 'ftp':
        stn_full = 'Fort Peck, MT'
    elif stn == 'sxf':
        stn_full = 'Sioux Falls, SD'
    else:
        print('Station name error!')
        sys.exit(1)

    fig2, ax = plt.subplots(figsize=(8, 6))

    ax.set_title(stn_full)
    ax.set_facecolor('k')

    ax.scatter(doy, stn_wsa_col, color='#1b9e77', marker='o', s=5, label='SURFRAD')
    ax.scatter(doy, mcd, color='#d95f02', marker='^', s=5, label='MCD43A3')
    ax.scatter(doy, vnp, color='#7570b3', marker='+', s=5, label='VNP43MA3')
    ax.scatter(doy, vj1, color='#e7298a', marker='d', s=5, label='VJ143MA3')

    ax.set_xlabel('DOY 2019')
    ax.set_ylabel('Albedo')

    ax.legend()
    # txt_rmse = 'RMSE=' + str(round(rmse_mcd_sfrd, 4))
    # txt_mb = 'MB = ' + str(round(mb_mcd_sfrd, 4))
    # fig2.text(0.8, 0.85, txt_rmse, color='white')
    plt.savefig(workspace + stn + '_timeseries.png')
    plt.show()
