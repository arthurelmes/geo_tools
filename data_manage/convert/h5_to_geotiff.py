"""
Created Apr 17 2020
@author: arthur elmes arthur.elmes@gmail.com
With significant guidance from Cole Krehbiel
Contact: LPDAAC@usgs.gov Voice: +1-866-573-3222
Organization: Land Processes Distributed Active Archive Center (LP DAAC)
Website: https://lpdaac.usgs.gov/
"""

import h5py, os, sys
import numpy as np
from osgeo import gdal, gdal_array
import datetime as dt
import pandas as pd

in_dir = "/home/arthur/data/h5_convert_dev/"
out_dir = os.path.join(in_dir, "tif")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

os.chdir(in_dir)

in_file = "VNP09GA.A2018001.h30v11.002.2020021214039.h5"

# Using h5py for heavy lifting
f = h5py.File(in_file)

# Create a list of the grids -- do we care about this here?
grids = list(f['HDFEOS']['GRIDS'])

# Get a list of the metadata and clean it up
# The following two lines could be combined into one
file_metadata = f['HDFEOS INFORMATION']['StructMetadata.0']
file_metadata = file_metadata[()].split()
file_metadata = [m.decode('utf-8') for m in file_metadata]

# Gather up all the h5's objects in a list
h5_objs = []
f.visit(h5_objs.append)

# List all the sdss
# The first way is way more concise, but a little mind warping at first
# so I separated it out for now
#datasets = [obj for grid in grids for obj in h5_objs if isinstance(f[obj], h5py.Dataset) and grid in obj]
datasets = []
for grid in grids:
    for obj in h5_objs:
        if isinstance(f[obj], h5py.Dataset) and grid in obj:
            datasets.append(obj)

# Such list comprehension...
r = f[[a for a in datasets if 'M5' in a][0]] #M5 is red
g = f[[a for a in datasets if 'M4' in a][0]] #M4 is green
b = f[[a for a in datasets if 'M3' in a][0]] #M3 is blue
n = f[[a for a in datasets if 'M7' in a][0]] #M7 is nir

# Get scale factor and fill value
scale_factor = r.attrs['Scale']
fill_value = r.attrs['_FillValue']

# Use the scale factor to scale all the bands to their real values
red = r[()] * scale_factor
green = g[()] * scale_factor
blue = b[()] * scale_factor
nir = n[()] * scale_factor

# For visualization, create RGB array
rgb = np.dstack((red,green,blue))
rgb[rgb == fill_value * scale_factor] = 0

