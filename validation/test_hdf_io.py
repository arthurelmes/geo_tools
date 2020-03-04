#test rasterio's handling of hdf and h5 files

import sys
import rasterio as rio
import numpy as np
import os, math
from pyhdf.SD import SD, SDC
from sklearn.metrics import mean_squared_error
import pprint
from osgeo import gdal
import pyproj

# Open HDF4 file with pyhdf
#hdf_fname = "/penobscot/data01/arthur.elmes/painted_roads/lc8_alb/LC080410362019010601T1/LC08_L1TP_041036_20190106_20190130_01_T1_albedo_broad.hdf"
hdf_fname = "/muddy/data05/arthur.elmes/MCD43/hdf/MCD43A3/2018/h12v04/MCD43A3.A2018358.h12v04.006.2019009030957.hdf"

# using pyhdf
hdf_ds_pyhdf = SD(hdf_fname, SDC.READ)

# using gdal
hdf_ds_gdal = gdal.Open(hdf_fname, gdal.GA_ReadOnly)
band_ds_gdal = gdal.Open(hdf_ds_gdal.GetSubDatasets()[0][0], gdal.GA_ReadOnly)

crs = band_ds_gdal.GetProjection()
#print(crs)

in_proj = pyproj.Proj(init='epsg:4326')
out_proj = pyproj.Proj(crs)

# test point in LA: -118.4052, 34.1421
# print(in_proj.crs)
# print(out_proj.crs)

x, y = pyproj.transform(in_proj, out_proj,-118.4052, 34.1421)
#print(x)
#print(y)


upx, xres, xskew, upy, yskew, yres = band_ds_gdal.GetGeoTransform()
cols = band_ds_gdal.RasterXSize
rows = band_ds_gdal.RasterYSize

print("gdal geotransform info: ")
print(upx)
print(upy)
print(xres)
print(yres)
print(cols)
print(rows)
# Print SDSs
# print("datasets: ")
# print(hdf_ds.datasets())

# Print crs
# print("attributes: ")
# hdf_atts = hdf_ds.attributes()
# pprint.pprint(hdf_atts)

# Read dataset
# sds_name_wsa = 'Albedo_WSA_shortwave'
# data3d_wsa = hdf_ds.select(sds_name_wsa)

# The below step returns a numpy array. coolio.
# data = data3d_wsa[:,:]
# print(data)

# Open same dataset with rasterio and make sure they're identical by plotting
# tif_fname = "/muddy/data05/arthur.elmes/MCD43/MCD43A3/h12v04/wsa/MCD43A3.A2016366.h12v04.006.2017014050856_wsa_shortwave.tif"
# tif_ds = rio.open(tif_fname)
# tif_band_wsa = tif_ds.read(1)
# #print(tif_band_wsa)

# x = data.flatten()
# y = tif_band_wsa.flatten()
# test_data = np.column_stack((x,y,))

# rmse = math.sqrt(mean_squared_error(x,y))
# mb = np.sum(x - y) / x.size

# print(rmse)
# print(mb)
