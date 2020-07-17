# make variograms of a set of tifs
library(raster)
library(gstat)

# set wd
setwd('/media/arthur/Windows/LinuxShare/LC08/greenland/tif/wsa/wgs84/')

# shapefile to clip with
clip_file_name <- getData('/home/arthur/Dropbox/projects/greenland/sensor_intercompare/intersection_006013_T22WEV_h16v02_wgs84.shp')
plot(clip_file_name)

# this will become a loop through all tifs in the wd
tif_raster <- raster(x = 'LC08_L1TP_006013_20190610_20190619_01_T1_albedo_broad_wsa_broad_wgs84.tif')

# clip the raster
masked_raster <- mask(tif_raster, clip_file_name)

plot(masked_raster)

point_data <- as(tif_raster, 'SpatialPointsDataFrame')
gstat_variogram <- variogram(band1 ~ 1, data = point_data)