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
from datetime import datetime

# CLI args                                                                                                                        
parser = ArgumentParser()
parser.add_argument('-d', '--input-dir', dest='workspace', help='Directory containing tif data.', metavar='WORKSPACE')
parser.add_argument('-p', '--product', dest='product_name',
                    help='Product name, e.g. mcd, SZA, AOD, actual_albedo',
                    metavar='PRDCT')
parser.add_argument('-t', '--tile', dest='tile', help='Optional. Tile of interest. '
                                                      'Enter h00v00 for non-tile-based summary. ',
                    metavar='TILE')
parser.add_argument('-y', '--year', dest='year', help='Optional. Year to extract data for.',
                    metavar='YEAR')
parser.add_argument('-v', '--vector', dest='vector', help='Required. Shapefile defining AOI.')

args = parser.parse_args()

workspace = args.workspace
product_name = args.product_name
vector = args.vector
if args.tile:
    tile = args.tile
if args.year:
    year = args.year

def convert_doy(doy):
    date_complete = datetime.strptime(doy, '%Y%j').date()
    date_complete = date_complete.strftime('%m/%d/%Y')
    return date_complete


# Open AOI vector
with fiona.open(vector, 'r') as clip_shp:
    shapes = [feature["geometry"] for feature in clip_shp]

# List to hold outputs
stats_list = []
csv_header = ['date', 'product', 'mean', 'sd_dev', 'valid_pixels_count']

for tif in glob.glob(workspace + '/*.tif'):
    # Loop over all tifs in indir, clip each using clip_shp, and then calculate mean an sd, append to list
    with rio.open(tif) as src:
        try:
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
            else:
                print("Product not recognized!")
                sys.exit(1)
        except:
            print("fail")
            mean = None
            std = None
            count = None

        if mean is None:
            mean = ''
        else:
            if type(mean) == np.ma.core.MaskedConstant:
                mean = ''

        if std is None:
            std = ''
        else:
            if type(std) == np.ma.core.MaskedConstant:
                std = ''

        if count is None:
            count = ''
        else:
            if type(count) == np.ma.core.MaskedConstant:
                count = ''

        tif_name = ntpath.basename(tif)
        #TODO this is silly, and won't work when the file name changes. Fix it!
        # date = convert_doy(tif_name[9:16]) # this one is for the SZA tifs
        # date = convert_doy(tif_name[10:17]) # this one is for the AOD tifs like MOD08_D3.A2020098.061.2020099180515_wgs84.tif
        date = convert_doy(tif_name[-11:-4]) # this is for the actual_albedo_entire_islands... sigh.
        print(date)
        stats_list.append((date, tif_name, mean, std, count))


# Write stats_list to csv
os.chdir(workspace)
csv_name = str(product_name) + '_' + os.path.basename(str(vector[:-4])) + '_stats.csv'
print(csv_name)
with open(csv_name, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_header)
    writer.writerows(stats_list)
