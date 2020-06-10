"""Convert NOAA/ESRL/GMD/GRAD Radiation Archive .dat files into nicely formatted .csv
Author: Arthur ELmes
Date: 2020-06-09"""

import os, glob
import pandas as pd

workspace = '/home/arthur/Dropbox/projects/greenland/aoi_albedo_time_series/w_coast_merge/'
os.chdir(workspace)

csv_file_names = glob.glob('west-coast*.csv')

combined_csv = pd.concat([pd.read_csv(f) for f in csv_file_names])
print(combined_csv.shape)
csv_name_all = 'west-coast-combined-MCD43A3-006-results.csv'
combined_csv.to_csv(csv_name_all, index=False)

