"""
Use this on the output of extract_samples_tif.py to create a new table where
all of the transect points are stacked vertically, with their correct doy.
"""

import pandas as pd
import sys

workspace = '/media/arthur/Windows/LinuxShare/actual_albedo/wgs84/fig/'
csv_name = '65_deg_north_ice_clip_wgs84_pts.csv_extracted_values_MCD43_actual_albedo_2020.csv'
raw_df = pd.read_csv(workspace + csv_name )


stacked_df = pd.DataFrame(columns=['Category', 'Date', 'Value'])

for id in raw_df.columns.tolist():
    if id != 'doy':
        #tmp_df = None
        tmp_df = pd.DataFrame(raw_df[['doy', id]])
        tmp_df['Category'] = str(id)
        tmp_df.rename(columns={'doy':'Date', id:'Value'}, inplace=True)
        tmp_df = tmp_df[['Category', 'Date', 'Value']]
        stacked_df = stacked_df.append(tmp_df, sort=False)


stacked_df.to_csv(workspace + csv_name[:-4] + '_stacked.csv', index=False)
