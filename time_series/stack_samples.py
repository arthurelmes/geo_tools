"""
Use this on the output of extract_samples_tif.py to create a new table where
all of the transect points are stacked vertically, with their correct doy.
"""

import pandas as pd
import glob, os

workspace = '/home/arthur/Dropbox/projects/greenland/transect_points/extracted/72_5/'
for year in range(2000, 2020):
    csv_name = '72_5_deg_north_land_clip_wgs84_1km_pts_extracted_values_MCD43_actual_albedo_' + str(year) + '.csv'
    raw_df = pd.read_csv(workspace + csv_name)
    stacked_df = pd.DataFrame(columns=['Category', 'Date', 'Value'])

    for id in raw_df.columns.tolist():
        if id != 'doy':
            tmp_df = pd.DataFrame(raw_df[['doy', id]])
            tmp_df['Category'] = str(id)
            tmp_df.rename(columns={'doy':'Date', id:'Value'}, inplace=True)
            tmp_df = tmp_df[['Category', 'Date', 'Value']]
            stacked_df = stacked_df.append(tmp_df, sort=False)

    stacked_df.to_csv(workspace + csv_name[:-4] + '_stacked.csv', index=False)

# csv_name_all = ''

# for stacked in glob.glob(workspace + "*stacked*"):
#     df_merged = (pd.read_csv(f, sep=',') for f in all_files)
#     df_merged = pd.concat(df_from_each_file, ignore_index=True)
#     df_merged.to_csv("merged.csv")