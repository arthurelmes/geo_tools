# make variograms of a set of tifs
library(raster)
library(usdm)

# set wd
setwd('/media/arthur/Windows/LinuxShare/LC08/greenland/tif/wsa/wgs84/')

# this will become a loop through all tifs in the wd
#tif_file <- system.file('/media/arthur/Windows/LinuxShare/LC08/greenland/tif/wsa/wgs84/LC08_L1TP_006013_20190610_20190619_01_T1_albedo_broad_wsa_broad_wgs84.tif', package="usdm")

tif_raster <- raster(x = 'LC08_L1TP_006013_20190610_20190619_01_T1_albedo_broad_wsa_broad_wgs84.tif')

print(tif_raster)
# check what this means
r <- brick(tif_raster)
#r
#mplot(r[[1]])
v1 <- Variogram(r[[1]])
plot(v1)