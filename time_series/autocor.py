import numpy as np
import pandas as pd
from libpysal.weights.contiguity import Queen
from libpysal.weights import lat2W
import pysal as ps
import rasterio as rio
import rasterio.mask
import fiona
from esda.moran import Moran
import timeit


np.random.seed(34539)

workspace = '/lovells/data02/arthur.elmes/greenland/sensor_intercompare/tif/LC8/wsa_wgs84/'
tif = workspace + \
      'LC08_L1TP_006013_20190610_20190619_01_T1_albedo_broad_wsa_broad_wgs84.tif'

with fiona.open('/lovells/data02/arthur.elmes/greenland/sensor_intercompare/shp/intersection_006013_T22WEV_h16v02_wgs84.shp',
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


#print((clipped_img.shape[1], clipped_img.shape[2]))
#print((src.shape[0], src.shape[1]))

masked_clipped_img = np.ma.masked_array(clipped_img, clipped_img == 32767)

print(masked_clipped_img.shape)

#2004, 4640

weights = lat2W(2004, 4640, rook=False, id_type='int')
moran = Moran(masked_clipped_img, weights)
print(moran.I)


#print(timeit.timeit(test_code), number = 1)
