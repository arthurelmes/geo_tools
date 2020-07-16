import numpy as np
import pandas as pd
from libpysal.weights.contiguity import Queen
from libpysal.weights import lat2W
import pysal as ps
import rasterio as rio
import rasterio.mask
import fiona
from esda.moran import Moran

np.random.seed(34539)

workspace = '/media/arthur/Windows/LinuxShare/S2/albedo/T22WEV/wsa/wgs84/'
tif = workspace + \
      'S2A_USER_MSI_L2A_TL_MTI__20190727T195520_A021386_T22WEV_N02.08_albedo_broad.bin_wsa_shortwave_wgs84.tif'

with fiona.open('/home/arthur/Dropbox/projects/greenland/sensor_intercompare/intersection_006013_T22WEV_h16v02_wgs84.shp',
                'r') as clip_shp:
    shapes = [feature["geometry"] for feature in clip_shp]

with rio.open(tif) as src:
    clipped_img, clipped_transform = rio.mask.mask(src, shapes, crop=True)
    clipped_meta = src.meta

# clipped_meta.update({"driver": "GTiff",
#                  "height": clipped_img.shape[1],
#                  "width": clipped_img.shape[2],
#                  "transform": clipped_transform})

# with rasterio.open("RGB.byte.masked.tif", "w", **clipped_meta) as dest:
#     dest.write(clipped_img)


print((clipped_img.shape[1], clipped_img.shape[2]))
#print((src.shape[0], src.shape[1]))

weights = lat2W(clipped_img.shape[1], clipped_img.shape[2], rook=False, id_type='int')
moran = Moran(clipped_img, weights)
print(moran.I)