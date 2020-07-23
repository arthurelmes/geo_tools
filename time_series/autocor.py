import numpy as np
import pandas as pd
from libpysal.weights.contiguity import Queen
from libpysal.weights import lat2W
import pysal as ps
import rasterio as rio
import rasterio.mask
import fiona
from esda.moran import Moran
import ntpath
import csv
import glob


np.random.seed(34539)
workspace = '/lovells/data02/arthur.elmes/greenland/sensor_intercompare/tif/S2/wsa_wgs84/'
#workspace = '/lovells/data02/arthur.elmes/greenland/sensor_intercompare/tif/MCD43A3/wsa_wgs84/'
#workspace = '/lovells/data02/arthur.elmes/greenland/sensor_intercompare/tif/LC8/wsa_wgs84/'
#workspace = '/media/arthur/Windows/LinuxShare/LC08/greenland/tif/wsa/wgs84/'
#clip_file_name = '/home/arthur/Dropbox/projects/greenland/sensor_intercompare/intersection_006013_T22WEV_h16v02_wgs84.shp'
clip_file_name = '/lovells/data02/arthur.elmes/greenland/sensor_intercompare/shp/intersection_006013_T22WEV_h16v02_wgs84.shp'
tif = workspace + \
      'LC08_L1TP_006013_20190610_20190619_01_T1_albedo_broad_wsa_broad_wgs84.tif'






# List to hold outputs
stats_list = []
csv_header = ['image', 'morans_i']

for tif in glob.glob(workspace + '*.tif'):
    tif_name = ntpath.basename(tif)

    # Loop over all tifs in indir, clip each using clip_shp, and then calculate moran's i, append to list
    with fiona.open(clip_file_name, 'r') as clip_shp:
        shapes = [feature["geometry"] for feature in clip_shp]

    with rio.open(tif) as src:
        clipped_img, clipped_transform = rio.mask.mask(src, shapes, crop=True)
        clipped_meta = src.meta

    # Mask out nodata
    masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 32767)
    # print(masked_clipped_img.shape[1])
    # print(masked_clipped_img.shape[2])

    # Calculate weights matrix for the raster, and calculate Moran's i
    print("Building weights matrix for {x}".format(x=tif))
    weights = lat2W(masked_clipped_img.shape[1], masked_clipped_img.shape[2], rook=False, id_type='int')
    print("Calculating Moran's i for {x}".format(x=tif))
    moran = Moran(masked_clipped_img, weights)

    # Add moran's i to csv
    stats_list.append((tif_name, moran.I))

# Write stats_list to csv
with open(workspace + '_morani.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_header)
    writer.writerows(stats_list)
