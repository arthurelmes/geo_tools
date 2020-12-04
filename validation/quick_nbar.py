"""This script will quickly make RGB and NIR composites of MCD43/VNP43/VJ143
Author: Arthur Elmes
Date: 2020-12-04

Great tips here:
https://lpdaac.usgs.gov/resources/e-learning/working-daily-nasa-viirs-surface-reflectance-data/"""

import h5py
import pyhdf
import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, gdal_array
import datetime as dt
import pandas as pd
from skimage import exposure

# set up workspace
workspace = '/home/arthur/Dropbox/projects/modis_viirs_continuity/sensor_intercompare/'
out_dir = os.path.join(workspace, 'output')
os.chdir(workspace)

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

vnp_file = 'VNP43MA3.A2019100.h08v05.002.2020295081219.h5'
mcd_file = 'MCD43A3.A2019100.h08v05.061.2020292121126.hdf'


def vnp(file_name):
    # get date in a nice print-able format
    yeardoy = vnp_file.split('.')[1][1:]
    date = dt.datetime.strptime(yeardoy, '%Y%j').strftime('%m/%d/%Y')

    h5 = h5py.File(vnp_file)
    print(list(h5.keys()))

    # List contents of GRIDS directory
    grids = list(f['HDFEOS']['GRIDS'])

    # add all objects in the h5 to a list
    h5_objs = []
    h5.visit(h5_objs.append)

    # get a list of all datasets. lol I did not do this double list comp.
    all_datasets = [obj for grid in grids for obj in h5_objs if isinstance(h5[obj], h5py.Dataset) and grid in obj]

    # assign the bands
    r = h5[[a for a in all_datasets if 'M5' in a][0]]  # M5 = Red
    g = h5[[a for a in all_datasets if 'M4' in a][0]]  # M4 = Green
    b = h5[[a for a in all_datasets if 'M3' in a][0]]  # M3 = Blue
    n = h5[[a for a in all_datasets if 'M7' in a][0]]  # M7  = NIR


vnp(vnp_file)