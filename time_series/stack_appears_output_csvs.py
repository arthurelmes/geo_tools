"""Combine a series of appears results into one big csv (due to appears request size limit)
Author: Arthur ELmes
Date: 2020-06-09"""

import os, glob
import pandas as pd

workspace = '/home/arthur/Dropbox/projects/greenland/transect_points/appears/'
os.chdir(workspace)

csv_file_names = glob.glob('russel-1-with-parallel*.csv')

combined_csv = pd.concat([pd.read_csv(f) for f in csv_file_names])
print(combined_csv.shape)
csv_name_all = 'russel-1-with-parallel-combined-MCD43A3-006-results.csv'
combined_csv.to_csv(csv_name_all, index=False)

