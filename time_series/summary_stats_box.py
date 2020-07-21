"""This script provides summary statistics for a time stack of rasters within a specified box. The user
indicates the imagery directory and a constraining shapefile.
Note: as of this version, only GeoTiff inputs are accepted. Future development will include HDF4/HDF5.
Author: Arthur Elmes
7/15/2020"""

import pandas as pd
import rasterio as rio
import rasterio.mask
import fiona
import csv
import numpy as np
import glob
import ntpath

# Set workspaces etc
#workspace = '/media/arthur/Windows/LinuxShare/MCD43A2/'
workspace = '/ipswich/data01/arthur.elmes/MCD43A2/2019/h16v02/sza/'
product_name = 'SZA'

with fiona.open('/lovells/data02/arthur.elmes/greenland/tile_extents/h16v02.shp',
                'r') as clip_shp:
    shapes = [feature["geometry"] for feature in clip_shp]

# List to hold outputs
stats_list = []
csv_header = ['product', 'mean', 'sd_dev']

for tif in glob.glob(workspace + '*.tif'):
    # Loop over all tifs in indir, clip each using clip_shp, and then calculate mean an sd, append to list
    with rio.open(tif) as src:
        clipped_img, clipped_transform = rio.mask.mask(src, shapes, crop=True)
        clipped_meta = src.meta

    masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 255)

    if 'mcd' in product_name or 'MCD' in product_name:
        mean = masked_clipped_img.mean() * 0.001
        std = masked_clipped_img.std() * 0.001
    elif 'lc' in product_name or 's2' in product_name or 'LC' in product_name or 'S2' in product_name:
        mean = masked_clipped_img.mean() * 0.0001
        std = masked_clipped_img.std() * 0.0001
    else:
        mean = masked_clipped_img.mean()
        std = masked_clipped_img.std()

    tif_name = ntpath.basename(tif)

    stats_list.append((tif_name, mean, std))

# Write stats_list to csv
with open(workspace + product_name + '_stats.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_header)
    writer.writerows(stats_list)
