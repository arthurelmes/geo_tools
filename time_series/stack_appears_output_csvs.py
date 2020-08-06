"""Combine a series of appears results into one big csv (due to appears request size limit)
Author: Arthur ELmes
Date: 2020-06-09"""

import os, glob
import pandas as pd

workspace = '/home/arthur/Dropbox/projects/greenland/aoi_albedo_time_series/appears/west_coast_add_2020/'
os.chdir(workspace)

csv_file_names = glob.glob('west*.csv')

combined_csv = pd.concat([pd.read_csv(f) for f in csv_file_names])
print(combined_csv.shape)
csv_name_all = 'west-coast-combined-MCD43A3-006-results-2000-2020.csv'
combined_csv.to_csv(csv_name_all, index=False)

