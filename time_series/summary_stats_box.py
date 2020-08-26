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
import sys, os
from argparse import ArgumentParser

#TODO sort out these. e.g. year and tile are not always needed, so make them optional.
# CLI args                                                                                                                        
parser = ArgumentParser()
parser.add_argument('-i', '--input-dir', dest='workspace', help='Directory containing tif data.', metavar='WORKSPACE')
parser.add_argument('-p', '--product', dest='product_name',
                    help='Product name, e.g. mcd, SZA, AOD, actual_albedo',
                    metavar='PRDCT')
parser.add_argument('-t', '--tile', dest='tile', help='Tile of interest. Enter h00v00 for non-tile-based summary. ',
                    metavar='TILE')
parser.add_argument('-y', '--year', dest='year', help='Year to extract data for.',
                    metavar='YEAR')
args = parser.parse_args()

workspace = args.workspace
product_name = args.product_name
tile = args.tile
year = args.year

#TODO this should be changed as it relies on dir structure
#TODO and really, there's no reason to not just have the AOI shp be an input arg
if 'SZA' in product_name:
    year = workspace[-16:-12]
    with fiona.open('/lovells/data02/arthur.elmes/greenland/tile_extents/{x}.shp'.format(x=tile), 'r') as clip_shp:
        shapes = [feature["geometry"] for feature in clip_shp]

elif 'AOD' in product_name:
    year = workspace[-5:-1]
    with fiona.open('/lovells/data02/arthur.elmes/greenland/tile_extents/{x}_wgs84.shp'.format(x=tile), 'r') as clip_shp:
        shapes = [feature["geometry"] for feature in clip_shp]
else:
    with fiona.open('/lovells/data02/arthur.elmes/greenland/vector/catchments_top_level_w_coast_ekholm_polys_dissolve_sinusoidal.shp',
                    'r') as clip_shp:
        shapes = [feature["geometry"] for feature in clip_shp]


# List to hold outputs
stats_list = []
csv_header = ['product', 'mean', 'sd_dev', 'valid_pixels_count']

for tif in glob.glob(workspace + '/*.tif'):
    # Loop over all tifs in indir, clip each using clip_shp, and then calculate mean an sd, append to list
    with rio.open(tif) as src:
        clipped_img, clipped_transform = rio.mask.mask(src, shapes, crop=True)
        clipped_meta = src.meta

    
    if 'mcd' in product_name or 'MCD' in product_name:
        masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 32767)
        mean = masked_clipped_img.mean() * 0.001
        std = masked_clipped_img.std() * 0.001
        count = masked_clipped_img.count()
    elif 'lc' in product_name or 's2' in product_name or 'LC' in product_name or 'S2' in product_name:
        masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 32767)
        mean = masked_clipped_img.mean() * 0.0001
        std = masked_clipped_img.std() * 0.0001
        count = masked_clipped_img.count()
    elif 'AOD' in product_name:
        masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == -9999)
        mean = masked_clipped_img.mean() * 0.001
        std = masked_clipped_img.std() * 0.001
        count = masked_clipped_img.count()
    elif 'SZA' in product_name:
        masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 255)
        mean = masked_clipped_img.mean()
        std = masked_clipped_img.std()
        count = masked_clipped_img.count()
    elif 'actual_albedo' in product_name:
        masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 32767)
        mean = masked_clipped_img.mean() * 0.001
        std = masked_clipped_img.std() * 0.001
        count = masked_clipped_img.count()
        print(str(tif) + ": mean = " + str(mean) + " count = " + str(count))
        
    else:
        print("Product not recognized!")
        sys.exit(1)
        
    tif_name = ntpath.basename(tif)

    stats_list.append((tif_name, mean, std, count))

# Write stats_list to csv
os.chdir(workspace)
csv_name = str(product_name + '_' + year + '_' + tile[1:] + '_stats.csv')
#csv_name = str(product_name + '_' + '_stats.csv')
print(csv_name)
with open(csv_name, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_header)
    writer.writerows(stats_list)
