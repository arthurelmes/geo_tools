""" This script plots NEON albedo against extracted satellite data (use ../time_series/extract_samples_modisviirs43.py)
 and the pre-exisiting IDL NEON formatting code (readgroundmeasurement_surfrad.pro and calaveragep.pro, currently
 in Arthur's neponset homedir: /home/arthur.elmes/code/val_data/). These format data correctly for ingestion into
 this script.
 Author: Arthur Elmes
 Date: 2020-12-11
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, sys, csv


#TODO change to CLI arg
workspace = '/home/arthur/Dropbox/projects/modis_viirs_continuity/in_situ/'

# These should be the the NEON standard abbreviations
stn_list = ['HARV']

# make csv to hold stats
stats_fields = ['stn', 'rmse_mcd_neon', 'mb_mcd_neon', 'rmse_vnp_neon', 'mb_vnp_neon', 'rmse_vj1_neon', 'mb_vj1_neon']
csv_fname = workspace + '/neon_stats.csv'

with open(csv_fname, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(stats_fields)


for stn in stn_list:
    os.chdir(os.path.join(workspace, 'neon'))
    neon = pd.read_csv(stn + '_2019.csv', index_col=0, parse_dates=True)
    neon.reset_index(inplace=True)

    # Extracted data from MODIS/VIIRS
    mcd = pd.read_csv(os.path.join(workspace, 'extracted', 'mcd')
                      + '/hf_neon_tower_extracted_values_MCD43A3.csv',
                      index_col=0)
    vnp = pd.read_csv(os.path.join(workspace, 'extracted', 'vnp')
                      + '/hf_neon_tower_extracted_values_VNP43MA3.csv',
                      index_col=0)
    vj1 = pd.read_csv(os.path.join(workspace, 'extracted', 'vj1')
                      + '/hf_neon_tower_extracted_values_VJ143MA3.csv',
                      index_col=0)
    # wsa = stn + '_wsa'
    # bsa = stn + '_bsa'
    wsa = '1_wsa'
    bsa = '1_bsa'
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
    #neon['Date'] = pd.to_datetime(neon['year'].map(str) + '-' + neon['month'].map(str) + '-' + neon['day'].map(str))
    neon['doy'] = neon['date'].dt.dayofyear

    # Then get julian date from it, to use as a join field
    neon.set_index('doy', inplace=True)
    neon.drop(columns=['date'],
              axis=1, inplace=True)

    # This plots the set of scatterlpots against the SURFRAD (x) and satellite (y)
    #TODO this whole section should automatically have the number of figs as input datasets, e.g. just MCD, or MCD and VNP, etc
    neon = neon.join(mcd,  lsuffix='_neon', rsuffix='_snsr')
    neon = neon.join(vnp,  lsuffix='_neon', rsuffix='_snsr')
    neon = neon.join(vj1,  lsuffix='_neon', rsuffix='_snsr')


    stn_wsa_col = neon['albedo']
    mcd = neon[stn + '_wsa_mcd']
    vnp = neon[stn + '_wsa_vnp']
    vj1 = neon[stn + '_wsa_vj1']

    #TODO this should obviously be a function
    # Calculate RMSE and Mean Bias
    rmse_mcd_neon = ((stn_wsa_col - mcd) ** 2).mean() ** 0.5
    mb_mcd_neon = stn_wsa_col.mean() - mcd.mean()
    rmse_vnp_neon = ((stn_wsa_col - vnp) ** 2).mean() ** 0.5
    mb_vnp_neon = stn_wsa_col.mean() - vnp.mean()
    rmse_vj1_neon = ((stn_wsa_col - vj1) ** 2).mean() ** 0.5
    mb_vj1_neon = stn_wsa_col.mean() - vj1.mean()

    stats_row = [stn, rmse_mcd_neon, mb_mcd_neon, rmse_vnp_neon, mb_vnp_neon, rmse_vj1_neon, mb_vj1_neon]
    with open(csv_fname, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(stats_row)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3))
    fig.tight_layout(pad=3)
    fig.set_facecolor('black')

    # Add x=y line
    lims = [
        np.min([plt.xlim(), plt.ylim()]),  # min of both axes
        np.max([plt.xlim(), plt.ylim()]),  # max of both axes
    ]

    for i in (ax1, ax2, ax3):
        i.set_facecolor('k')
        i.set_facecolor('k')
        i.set_facecolor('k')
        i.xaxis.label.set_color('white')
        i.yaxis.label.set_color('white')
        i.spines['bottom'].set_color('white')
        i.spines['left'].set_color('white')
        i.tick_params(colors='white')

        # Plot limits against each other for 1:1 line
        i.plot(lims, lims, 'deeppink', alpha=0.5, zorder=1)
        i.set_xlim(lims)
        i.set_ylim(lims)

    ax1.scatter(stn_wsa_col, mcd, color='#e6ab02', marker='^', s=5, label='MCD43A3', facecolors='none')
    ax2.scatter(stn_wsa_col, vnp, color='#d95f02', marker='s', s=5, label='VNP43MA3', facecolors='none')
    ax3.scatter(stn_wsa_col, vj1, color='#66a61e', marker='d', s=5, label='VJ143MA3', facecolors='none')

    ax1.set_ylabel('Satellite Albedo', color='white')
    fig.text(0.5, 0.0, 'SURFRAD Albedo', ha='center', color='white')

    fig.legend(loc='lower right', bbox_to_anchor=(0.21, 0.68))
    fig.tight_layout()
    plt.savefig(workspace + stn + '_sat_vs_surfrad_scatters.png')
    plt.show()

    # This plots the satellite and SURFRAD data against DOY, so a time series
    neon.reset_index(inplace=True)
    doy = neon['doy']

    # Slapdash conversion between stn abbr and full namm
    #TODO this should be done with a dictionary instead, way above, that is iterated over


    if stn == 'HARV':
        stn_full = 'Harvard Forest, MA'
    else:
        print('Station name error!')
        sys.exit(1)

    fig2, ax = plt.subplots(figsize=(8, 6))
    fig2.set_facecolor('black')
    fig2.tight_layout(pad=3)

    ax.set_title(stn_full, fontsize=16, color='white')
    ax.set_facecolor('black')

    ax.scatter(doy, stn_wsa_col, color='#7570b3', marker='o', s=20, label='SURFRAD', facecolors='none')
    ax.scatter(doy, mcd, color='#e6ab02', marker='^', s=20, label='MCD43A3', facecolors='none')
    ax.scatter(doy, vnp, color='#d95f02', marker='s', s=20, label='VNP43MA3', facecolors='none')
    ax.scatter(doy, vj1, color='#66a61e', marker='d', s=20, label='VJ143MA3', facecolors='none')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(colors='white')
    ax.set_xlabel('DOY 2019', size=14)
    ax.set_ylabel('Albedo', size=14)

    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)

    ax.legend(prop={'size': 12})
    # txt_rmse = 'RMSE=' + str(round(rmse_mcd_neon, 4))
    # txt_mb = 'MB = ' + str(round(mb_mcd_neon, 4))
    # fig2.text(0.8, 0.85, txt_rmse, color='white')
    plt.savefig(workspace + stn + '_timeseries.png')
    plt.show()
