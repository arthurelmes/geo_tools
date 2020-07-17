# make variograms of a set of tifs
library(raster)
library(rgdal)
library(gstat)
#library(geoR)
#library(Formula)

# set wd
wd_path <-'/home/arthur/Dropbox/projects/greenland/sensor_intercompare/'
setwd(wd_path)

# shapefile to clip with  
clip_file_name <- readOGR('/home/arthur/Dropbox/projects/greenland/sensor_intercompare/intersection_006013_T22WEV_h16v02.shp')
#clip_file_name <- readOGR('/home/arthur/Dropbox/projects/greenland/sensor_intercompare/test_clip_wgs84.shp')


# this will become a loop through all tifs in the wd
file.names <- dir(wd_path, pattern=".tif")
for(i in 1:length(file.names)){
  tif_raster <- raster(x = file.names[i])
  tif_raster_variable <- tools::file_path_sans_ext(file.names[i])
  
  print("masking raster")  
  # clip the raster to the shapefile and its extent (trim)
  masked_raster <- mask(tif_raster, clip_file_name)
  non_na_raster <- trim(masked_raster)
  
  # construct a SpatailPointsDataFrame from a sample of the raster, because using all points, as in the commented out line,
  # is waaaay to resource intensive
  #point_data <- as(non_na_raster, 'SpatialPointsDataFrame')
  
  print("sampling raster")
  point_data <- as.data.frame(sampleRandom(x=non_na_raster, size = 500, na.rm = TRUE, ext = clip_file_name, xy = TRUE))
  xy <- cbind(point_data[1], point_data[2])
  
  print("masking spatialpointsdf")
  point_data <- SpatialPointsDataFrame(xy, point_data)
  
  # plot the layers to check
  #plot(non_na_raster)
  #plot(point_data, add=TRUE)
  
  #tif_raster_variable <- 'test'
  f <- paste(tif_raster_variable, "~ 1")
  h <- as.formula(f)
  
  
  print("running variogram")
  gstat_variogram <- variogram(h, data = point_data)
  plot(gstat_variogram)
}







### Extra stuff

#geor_variogram <- variog(as.geodata(point_data))
#plot(geor_variogram)

# Vario for entire area, not clipped
#point_data_big <- as.data.frame(sampleRandom(x=tif_raster, size = 5000, na.rm = TRUE, ext = tif_raster, xy = TRUE))
#xy <- cbind(point_data_big[1], point_data_big[2])
#point_data_big <- SpatialPointsDataFrame(xy, point_data_big)

# plot the layers to check
#plot(tif_raster)
#plot(point_data_big, add=TRUE)

#gstat_variogram_big <- variogram(LC08_L1TP_006013_20190610_20190619_01_T1_albedo_broad_wsa_broad ~ 1, data = point_data_big)
#plot(gstat_variogram)

#geor_variogram_big <- variog(as.geodata(point_data_big))
#plot(geor_variogram)
