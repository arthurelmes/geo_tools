"""
1;5202;0cCreated on Wed Sep 19 10:04:10 2018
@author: aelmes

Taiga,AK,Delta Junction - DEJU,63.88112,-145.75136,Relocatable Terrestrial,Bureau of Land Management,Complete,Partially Available,h11v02
Taiga,AK,Caribou-Poker Creeks Research Watershed - BONA,65.15401,-147.50258,Core Terrestrial,University of Alaska,Complete,Partially Available,h11v02
Tundra,AK,Barrow Environmental Observatory - BARR,71.28241,-156.61936,Relocatable Terrestrial,Barrow Environmental Observatory,Complete,Partially Available,h12v01
Tundra,AK,Toolik - TOOL,68.66109,-149.37047,Core Terrestrial,Bureau of Land Management,Complete,Partially Available,h12v02
Taiga,AK,Healy - HEAL,63.87569,-149.21334,Relocatable Terrestrial,Alaska Department of Natural Resources,h11v02

Anaktuvuk River Fire: year 2007, 
smple1: 69.120186, -150.60678

Rock Fire: year 2015, 
orig_smpl: 66.012754 -154.162100

smpl1:  66.020665, -154.133065 
smpl2:  66.187050, -153.932029
smpl3:  65.979228, -154.049494  
smpl4:  65.920039, -154.040912 

"""
import os, glob, sys, pyproj, csv, statistics
from osgeo import gdal, osr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
from h5py import File

#years = [ "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019" ]

#TODO all these global variables gotta go
years = ["2018"]
tile = "12v04"
prdct = "VNP43MA3"
base_dir = "/muddy/data05/arthur.elmes/VNP43MA3/h5/"
sds_name_wsa_sw = "Albedo_WSA_shortwave"
sds_name_bsa_sw = "Albedo_BSA_shortwave"
sds_name_qa_sw = "BRDF_Albedo_Band_Mandatory_Quality_shortwave"

sites_dict = {
    "HF" : [(42.53691, -72.17265), "h12v04"]
    #"Summit" : [(72.57972, -38.50454), "h16v01"],
    #"NASA-U" : [(73.84189, -49.49831), "h16v01"],
    #"GITS":  [(77.13781, -61.04113), "h16v01"],
    #"Humboldt" : [(78.5266, -56.8305), "h16v01"],
    #"CP2" : [(69.87968, -46.98692), "h16v01"],
    #"South_Dome" : [(63.14889, -44.81717), "h16v02"],
    #"DYE-2" : [(66.48001, -46.27889), "h16v02"],
    #"Saddle" : [(65.99947, -44.50016), "h16v02"],
    #"NASA-SE" : [(66.4797, -42.5002), "h16v02"],
    #"Swiss_Camp" : [(69.56833, -49.31582), "h16v02"],
    #"JAR" : [(69.498358, -49.68156), "h16v02"],
    #"JAR_2" : [(69.42, -50.0575), "h16v02"],
    #"KAR" : [(69.69942, -33.00058), "h16v02"],
    #"NASA-E" : [(75, -29.99972), "h17v01"],
    #"NGRIP" : [(75.09975, -42.3325), "h17v01"],
    #"TUNU-N" : [(78.01677, -33.99387), "h17v01"]
}

#"Crawford_Pt" : [(69.87975, -46.98667), "h16v01"],
    
# sites_dict = {
#         "DEJU" : [(63.88112, -145.75136), "h11v02"],
#         "BONA" : [(65.15401,-147.50258), "h11v02"],
#         "BARR" : [(71.28241,-156.61936), "h12v01"],
#         "TOOL" : [(68.66109,-149.37047), "h12v02"],
#         "HEAL" : [(63.87569,-149.21334), "h11v02"],
#         "CARI" : [(65.15306, -147.502), "h11v02"]
#         }

def hdf_to_np(hdf_fname, sds):
    #TODO close the dataset, probably using 'with'
   hdf_ds = SD(hdf_fname, SDC.READ)
   dataset_3d = hdf_ds.select(sds)
   data_np = dataset_3d[:,:]
   return data_np

def h5_to_np(h5_fname, sds):
    h5_ds = File(h5_fname, 'r')
    data_np = h5_ds['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields'][sds].value
    return data_np

def convert_ll(lat, lon, tile, in_dir):
   
   # Convert the lat/long point of interest to a row/col location
   template_h_list = \
                     glob.glob(os.path.join(in_dir,\
                     '{prdct}.A*{tile}*.h*'.format(prdct=prdct,\
                                                   tile=tile)))
   template_h_file = template_h_list[0]
   template_h_ds = gdal.Open(template_h_file, gdal.GA_ReadOnly)
   template_h_band = gdal.Open(template_h_ds.GetSubDatasets()[0][0], \
                               gdal.GA_ReadOnly)
   
   # The below lines are the more verbose gdalish way
   # in_proj_gdal = osr.SpatialReference()
   # in_proj_gdal.ImportFromWkt(template_h_ds.GetProjectionRef())
   # lat_long_proj_gdal = osr.SpatialReference()
   # lat_long_proj_gdal.ImportFromEPSG(4326)
   
   # # create a transform object to convert between crss
   # transform = osr.CoordinateTransformation(in_proj_gdal, lat_long_proj_gdal)
   # x_min_gt = gt[0]
   # y_min_gt = gt[3] + cols*gt[4] + rows*gt[5]

   # print("gdal thinks x min (from geotransform) is:")
   # print(x_min_gt)
   # print("gdal thinks y min (from geotransform) is:")
   # print(y_min_gt)

#   x, y = transform.TransformPoint(x_min, y_min)
#   print(x)
#   print(y)
   
   # (x, y) = transform.TransformPoint(lon, lat)
   # print(x)
   # print(y)
   
   # print("Projection of lat/long will be WGS84, EPSG 4326: " + str(in_proj))
   # print("Projection read from file is: " + str(out_proj))
   # print("longitude: " + str(lon) + " latitude:" + str(lat))
   #template_h_rg = template_h_ds.GetRootGroup()
   
   # Use pyproj to create a geotransform between
   # WGS84 geographic (lat/long; epsg 4326) and
   # the funky crs that modis/viirs use.
   # Note that this modis crs seems to have units
   # in meters from the geographic origin, i.e.
   # lat/long (0, 0), and has 2400 rows/cols per tile.
   # gdal does NOT read the corner coords correctly,
   # but they ARE stored correctly in the hdf metadata.

   # Getting bounding coords from meta NO LONGER NEEDED
   # NOTE gdal works fine if you call the geotransform
   # on the BAND!!! (sds), not the DS
   meta = template_h_ds.GetMetadata_Dict()
   y_origin_meta = float(meta['NORTHBOUNDINGCOORDINATE'])
   y_min_meta = float(meta['SOUTHBOUNDINGCOORDINATE'])
   x_max_meta = float(meta['EASTBOUNDINGCOORDINATE'])
   x_origin_meta = float(meta['WESTBOUNDINGCOORDINATE'])
   n_rows_meta = int(meta['DATAROWS'])
   n_cols_meta = int(meta['DATACOLUMNS'])
   # print("metadata bounding info: ")
   # print(y_origin_meta)
   # print(y_min_meta)
   # print(x_max_meta)
   # print(x_origin_meta)
   # print(n_rows_meta)
   # print(n_cols_meta)
   
   # Getting bounding coords etc from gdal geotransform
   n_cols = template_h_band.RasterXSize
   n_rows = template_h_band.RasterYSize
   x_origin, x_res, x_skew, y_origin, y_skew, y_res = template_h_band.GetGeoTransform()

   # Using the skew is in case there is any affine transformation
   # in place in the input raster. Not so for modis tiles, so redundant.
   x_max = x_origin + n_cols * x_res + n_cols * x_skew
   y_min = y_origin + n_rows * y_res + n_rows * y_skew
   # print("gdal geotransform info: ")
   # print("y origin: " + str(y_origin))
   # print("y min: " + str(y_min))
   # print("x max: " + str(x_max))
   # print("x origin: " + str(x_origin))
   # print(n_rows)
   # print(n_cols)
   
   # Using pyproj to transform coords of interes to meters
   in_proj = pyproj.Proj(init='epsg:4326')
   out_proj = pyproj.Proj(template_h_band.GetProjection())
   #origin_m = pyproj.transform(in_proj, out_proj, x_origin, y_origin)
   #xy_max_m = pyproj.transform(in_proj, out_proj, x_max, y_min)

   # Current sample location convert from ll to m
   smpl_x, smpl_y = pyproj.transform(in_proj, out_proj, lon, lat)

   #TESTING these are conversions of the metadata extents to meters
   x_origin_meta_m, y_origin_meta_m = pyproj.transform(in_proj, out_proj, x_origin_meta, y_origin_meta)
   x_max_meta_m, y_min_meta_m= pyproj.transform(in_proj, out_proj, x_max_meta, y_min_meta)

   pixel_width_meta_m = (x_max_meta_m - x_origin_meta_m) / n_cols_meta
   pixel_height_meta_m = (y_origin_meta_m - y_min_meta_m) / n_rows_meta
   col_m = int((smpl_x - x_origin_meta_m) / pixel_width_meta_m)
   row_m = int( -1 * (smpl_y - y_origin_meta_m) / pixel_height_meta_m)
   smp_rc_meta = row_m, col_m
   print("Metadata-based extents: ")
   print(pixel_height_meta_m)
   print(pixel_width_meta_m)
   print(x_max_meta_m)
   print(x_origin_meta_m)
   print(y_min_meta_m)
   print(y_origin_meta_m)

   
   # Make calculations to get row/col value
   # NOTE that for geotifs, it would also be possible
   # to simply open with rasterio, then use .index()
   # to return the row/col. This does not work for hdf
   pixel_width_m = (x_max - x_origin) / n_cols
   pixel_height_m = (y_origin - y_min) / n_rows
   col_m = int((smpl_x - x_origin) / pixel_width_m)
   row_m = int( -1 * (smpl_y - y_origin) / pixel_height_m)
   smp_rc = row_m, col_m
   print("Geotransform-based extentds: ")
   print(pixel_height_m)
   print(pixel_width_m)
   print(x_max)
   print(x_origin)
   print(y_min)
   print(y_origin)
   
   print("")
   print("")
   print("Metadata-based row/col:")
   print(smp_rc_meta)
   print("Geotransform-based row/col:")
   print(smp_rc)
   sys.exit()
   return smp_rc

def draw_plot():
    plt.ion()
    # fig = plt.figure()
    # fig.suptitle('ABoVE Domain Albedo Time Series')
    # ax = fig.add_subplot(111)
    # fig.subplots_adjust(top=0.85)
    # ax.set_title(series_name)
    # ax.set_xlabel('DOY')
    # ax.set_ylabel('White Sky Albedo')
    # plt.xlim(0, 365)
    # plt.ylim(0.0, 1.0)
    # ax.plot(doys, wsa_swir_mean)
    # plt_name = str(year + '_' + series_name.replace(" ", ""))
    # print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=plt_name))
    # plt.savefig('{plt_name}.png'.format(plt_name=plt_name))


def main():
    for year in years:
        for site in sites_dict.items():
            #print("Processing " + str(year) + " at site: " + site[0])
            in_dir = os.path.join(base_dir, prdct, year, site[1][1])
            fig_dir = os.path.join(base_dir, 'figs')
            if not os.path.isdir(fig_dir):
               os.makedirs(fig_dir)
               print("Made new folder for figs: " + str(fig_dir))
            else:
               pass
            os.chdir(in_dir)

            # Set up graph days and time axis
            doys = range(1, 366)

            # Set up the pixel location manually FOR NOW
            location = str(site[0])
            #print(site)
            lat_long = (site[1][0][0], site[1][0][1])
            #print(lat_long)
            
            # Create empty arrays for mean, sd
            #TODO curently these aren't really needed
            wsa_swir_mean = []
            wsa_swir_sd = []
            bsa_swir_mean = []
            bsa_swir_sd = []
            
            for day in doys:
                # Open the shortwave white sky albedo band.
                # The list approach is because of the processing date part of the file
                # name, which necessitates the wildcard -- this was just the easiest way.
                h_file_list = glob.glob(os.path.join(in_dir,
                                                      '{prdct}.A{year}{day:03d}*.h*'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                # bsa_hdf_list = glob.glob(os.path.join(in_dir,
                #                                       'bsa',
                #                                       '{prdct}.A{year}{day:03d}*bsa_shortwave.tif'.format(prdct=prdct,
                #                                                                                           day=day, year=year)))
                # qa_hdf_list = glob.glob(os.path.join(in_dir,
                #                                      'qa',
                #                                      '{prdct}.A{year}{day:03d}*qa_shortwave.tif'.format(prdct=prdct,
                #                                                                                         day=day, year=year)))
                # See if there is a raster for the date, if not use a fill value for the graph
                if len(h_file_list) == 0: # or len(bsa_tif_list) == 0 or len(qa_tif_list) == 0:
                    print('File not found: MCD43A3.A{year}{day:03d}*.h*'.format(day=day, year=year))
                    wsa_swir_subset_flt = float('nan')
                    bsa_swir_subset_flt = float('nan')
                elif len(h_file_list) > 1:
                    print('Multiple matching files found for same date!')
                    sys.exit()
                else:
                    #print('Found file: ' + ' {prdct}.A{year}{day:03d}*.h*'.format(prdct=prdct, day=day, year=year))
                    h_file_day = h_file_list[0]
                    # bsa_tif = bsa_tif_list[0]
                    # qa_tif = qa_tif_list[0]

                    # Open tifs as gdal ds but using rasterio for simplicity
                    #print("Opening: " + h_file_day + " " + sds_name_wsa_sw)
                    wsa_band = hdf_to_np(h_file_day, sds_name_wsa_sw)
                    bsa_band = hdf_to_np(h_file_day, sds_name_bsa_sw)
                    qa_band = hdf_to_np(h_file_day, sds_name_qa_sw)
                    # wsa_raster = rasterio.open(wsa_tif)
                    # bsa_raster = rasterio.open(bsa_tif)
                    # qa_raster = rasterio.open(qa_tif)
                    # wsa_band = wsa_raster.read(1)
                    # bsa_band = bsa_raster.read(1)
                    # qa_band = qa_raster.read(1)

                    # Mask out nodata values
                    wsa_swir_masked = np.ma.masked_array(wsa_band, wsa_band == 32767)
                    wsa_swir_masked_qa = np.ma.masked_array(wsa_swir_masked, qa_band > 1)
                    bsa_swir_masked = np.ma.masked_array(bsa_band, bsa_band == 32767)
                    bsa_swir_masked_qa = np.ma.masked_array(bsa_swir_masked, qa_band > 1)

                    # Spatial subset based on coordinates of interest.
                    wsa_smpl_results = []
                    bsa_smpl_results = []
                    
                    #TODO this used to be an additional loop that would average the values over
                    #several locations to get one mean value, rather than get the value of a given
                    #tower's pixel. Maybe modifiy to average within a bounding box or something?
                    #for smpl in sites_dict.values():
                    smp_rc = convert_ll(site[1][0][0], site[1][0][1], site[1][1], in_dir)
                    #print("Sample row/col: " + str(smp_rc))
                    wsa_swir_subset = wsa_swir_masked_qa[smp_rc]
                    wsa_swir_subset_flt = np.multiply(wsa_swir_subset, 0.001)
                    bsa_swir_subset = bsa_swir_masked_qa[smp_rc]
                    bsa_swir_subset_flt = np.multiply(bsa_swir_subset, 0.001)
                    #print("Queried pixel value is: " + str(wsa_swir_subset))
                    
                    # Add each point to the temporary list
                    wsa_smpl_results.append(wsa_swir_subset_flt)
                    bsa_smpl_results.append(bsa_swir_subset_flt)
                    #TODO this try is not really needed, but it doesn't hurt to leave it in case
                    # I want to incorporate the multiple-points-per-sample idea
                    try:
                       wsa_tmp_mean = statistics.mean(wsa_smpl_results)
                       bsa_tmp_mean = statistics.mean(bsa_smpl_results)
                       wsa_swir_mean.append(wsa_tmp_mean)
                       bsa_swir_mean.append(bsa_tmp_mean)
                    except:
                       wsa_swir_mean.append(0.0)
                       bsa_swir_mean.append(0.0)

        wsa_smpl_results_df = pd.DataFrame(wsa_swir_mean)
        bsa_smpl_results_df = pd.DataFrame(bsa_swir_mean)
        cmb_smpl_results_df = pd.concat([wsa_smpl_results_df, bsa_smpl_results_df], axis=1, ignore_index=True)
        print("wsa results below:")
        print(wsa_swir_mean)
        print("Combined DF below")
        cmb_smpl_results_df.set_axis(['wsa', 'bsa'], axis=1, inplace=True)
        print(cmb_smpl_results_df.to_string())
        # Do plotting and save output
        #print(*doys)
        #print(*wsa_swir_mean)
        series_name = location + "_" + str(year)
        os.chdir(fig_dir)
        csv_name = str(series_name + "_" + prdct + ".csv")
        print("writing csv: " + csv_name)
        # export data to csv
        cmb_smpl_results_df.to_csv(csv_name, index=False)
        # with open(csv_name, "w") as export_file:
        #     wr = csv.writer(export_file, dialect='excel', lineterminator='\n')
        #     for index, row in cmb_smpl_results_df.iterrows():
        #         row_data = str(row['wsa'] + "," + row['bsa'])
        #         wr.writerow(row_data)


if __name__ == "__main__":
    main()
