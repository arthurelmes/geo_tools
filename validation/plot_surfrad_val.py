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
import os

#TODO change to CLI arg
workspace = '/home/arthur/Dropbox/projects/modis_viirs_continuity/in_situ/'

# SURFRAD data

# These should be the the SURFRAD standard abbreviations
stn_list = ['dra']

#TODO currenlty requires correct directory formatting... not ideal
os.chdir(os.path.join(workspace, 'surfrad'))
sfrd = pd.read_csv('dra_2019.csv')

# Extracted data from MODIS/VIIRS
mcd = pd.read_csv(os.path.join(workspace, 'extracted', 'mcd')
                  + '/surfrad_sites_subset_formatted_h08v05_extracted_values_MCD43A3.csv',
                  index_col=0)
vnp = pd.read_csv(os.path.join(workspace, 'extracted', 'vnp')
                  + '/surfrad_sites_subset_formatted_h08v05_extracted_values_VNP43MA3.csv',
                  index_col=0)
vj1 = pd.read_csv(os.path.join(workspace, 'extracted', 'vj1')
                  + '/surfrad_sites_subset_formatted_h08v05_extracted_values_VJ143MA3.csv',
                  index_col=0)

# Make the WSA variables distinguishable
mcd.rename(columns = {'drk_wsa':'drk_wsa_mcd',
                     'drk_bsa':'drk_bsa_mcd'}, inplace=True)
vnp.rename(columns = {'drk_wsa':'drk_wsa_vnp',
                     'drk_bsa':'drk_bsa_vnp'}, inplace=True)
vj1.rename(columns = {'drk_wsa':'drk_wsa_vj1',
                     'drk_bsa':'drk_bsa_vj1'}, inplace=True)

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

stn = sfrd['gnd_mean']
mcd = sfrd['drk_wsa_mcd']
vnp = sfrd['drk_wsa_vnp']
vj1 = sfrd['drk_wsa_vj1']

#TODO this should obviously be a function
# Calculate RMSE and Mean Bias
rmse_mcd_sfrd = ((stn - mcd) ** 2).mean() ** 0.5
mb_mcd_sfrd = stn.mean() - mcd.mean()
rmse_vnp_sfrd = ((stn - vnp) ** 2).mean() ** 0.5
mb_vnp_sfrd = stn.mean() - vnp.mean()
rmse_vj1_sfrd = ((stn - vj1) ** 2).mean() ** 0.5
mb_vj1_sfrd = stn.mean() - vj1.mean()

print(rmse_mcd_sfrd)
print(mb_mcd_sfrd)
print(rmse_vnp_sfrd)
print(mb_vnp_sfrd)
print(rmse_vj1_sfrd)
print(mb_vj1_sfrd)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10,3))
ax1.set_facecolor('k')
ax2.set_facecolor('k')
ax3.set_facecolor('k')

ax1.scatter(stn, mcd,color='#d95f02', marker='^', s=5, label='MCD43A3')
ax2.scatter(stn, vnp, color='#7570b3', marker='+', s=5, label='VNP43MA3')
ax3.scatter(stn, vj1, color='#e7298a', marker='d', s=5, label='VJ143MA3')

ax1.set_ylabel('Satellite Albedo')
fig.text(0.5, 0.0, 'SURFRAD Albedo', ha='center')

fig.legend(loc='lower right', bbox_to_anchor=(0.21, 0.68))

fig.tight_layout()
plt.savefig(workspace + 'test_scatters.png')
plt.show()

# This plots the satellite and SURFRAD data against DOY, so a time series
sfrd.reset_index(inplace=True)
doy = sfrd['doy']

fig2, ax = plt.subplots(figsize=(8, 6))
ax.set_facecolor('k')

ax.scatter(doy, stn, color='#1b9e77', marker='o', s=5, label='SURFRAD')
ax.scatter(doy, mcd, color='#d95f02', marker='^', s=5, label='MCD43A3')
ax.scatter(doy, vnp, color='#7570b3', marker='+', s=5, label='VNP43MA3')
ax.scatter(doy, vj1, color='#e7298a', marker='d', s=5, label='VJ143MA3')

ax.set_xlabel('DOY 2019')
ax.set_ylabel('Albedo')

ax.legend()
plt.savefig(workspace + 'test_timeseries.png')
plt.show()
