"""Combine a series of appears results into one big csv (due to appears request size limit)
Author: Arthur Elmes
Date: 2020-06-09"""

import os, glob
import pandas as pd

workspace = '/home/arthur/Dropbox/projects/greenland/blue_sky_variables/SZA/h15v03/'
os.chdir(workspace)

csv_file_names = glob.glob('*.csv')

combined_csv = pd.concat([pd.read_csv(f) for f in csv_file_names])
print(combined_csv.shape)
csv_name_all = 'h15v03_AOD_2000_2020.csv'
combined_csv.to_csv(csv_name_all, index=False)

