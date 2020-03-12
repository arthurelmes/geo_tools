"""
Created on Wed Sep 19 10:04:10 2018
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
prdct = "MCD43A3"
base_dir = "/muddy/data05/arthur.elmes/MCD43/hdf/"
copy_srs_dir = os.path.join(base_dir, "copy_srs")
sds_name_wsa_sw = "Albedo_WSA_shortwave"
sds_name_bsa_sw = "Albedo_BSA_shortwave"
sds_name_qa_sw = "BRDF_Albedo_Band_Mandatory_Quality_shortwave"

sites_dict = {
   "1" : [(42.9609762442872, -81.3596629348376), "h12v04"],
   "2" : [(44.5689795941181, -73.7731623736408), "h12v04"],
   "3" : [(41.428803003867, -67.7006269649778), "h12v04"],
   "4" : [(43.9628686972571, -72.4183557028722), "h12v04"],
   "5" : [(41.5699273613238, -75.0789318654518), "h12v04"],
   "6" : [(47.4933272906822, -83.0820816479422), "h12v04"],
   "7" : [(42.0994645249512, -70.8594387457314), "h12v04"],
   "8" : [(47.402824901915, -83.6793321743925), "h12v04"],
   "9" : [(41.8574958373491, -77.9091825977107), "h12v04"],
   "10" : [(40.0856687907483, -75.6677958974889), "h12v04"],
   "11" : [(47.5029849241722, -78.0248650055764), "h12v04"],
   "12" : [(45.254294651692, -74.1591285502442), "h12v04"],
   "13" : [(41.4489030591277, -78.1754440166343), "h12v04"],
   "14" : [(43.5758843117417, -74.3277162506381), "h12v04"],
   "15" : [(44.3104433857202, -74.1735683871707), "h12v04"],
   "16" : [(42.6230096103569, -71.0757415793904), "h12v04"],
   "17" : [(47.6923460121331, -84.5309227625609), "h12v04"],
   "18" : [(49.3575002185506, -81.1310104809029), "h12v04"],
   "19" : [(48.1643823700599, -89.0957889382612), "h12v04"],
   "20" : [(43.9150278254132, -83.0765157626539), "h12v04"],
   "21" : [(40.4802114782855, -69.6414767826865), "h12v04"],
   "22" : [(43.3316747269835, -80.1272192979383), "h12v04"],
   "23" : [(46.2218993651198, -80.9195294013382), "h12v04"],
   "24" : [(40.1674379488733, -68.4759805054746), "h12v04"],
   "25" : [(43.8894389786501, -75.3718194118338), "h12v04"],
   "26" : [(42.2491057621595, -75.0295630792861), "h12v04"],
   "27" : [(42.4394870115553, -78.0900578705234), "h12v04"],
   "28" : [(40.8355278648118, -78.3397303218876), "h12v04"],
   "29" : [(46.9991518538199, -81.6492956814841), "h12v04"],
   "30" : [(42.7445485707209, -72.2833301675428), "h12v04"],
   "31" : [(45.2245895174742, -79.8241479736104), "h12v04"],
   "32" : [(45.9751161775291, -74.3322056332669), "h12v04"],
   "33" : [(45.7744662725285, -72.6577029862445), "h12v04"],
   "34" : [(48.2168942157706, -77.6007332361689), "h12v04"],
   "35" : [(40.7039950495386, -68.2204245832199), "h12v04"],
   "36" : [(49.541861058892, -82.9621014439363), "h12v04"],
   "37" : [(41.621524266424, -71.8689326803879), "h12v04"],
   "38" : [(44.8815877066712, -72.1094999267144), "h12v04"],
   "39" : [(40.0575027089945, -70.8201294214986), "h12v04"],
   "40" : [(44.353195268873, -76.8950534759788), "h12v04"],
   "41" : [(41.1716876072191, -72.6158022680451), "h12v04"],
   "42" : [(49.3793289854609, -83.2979936665823), "h12v04"],
   "43" : [(49.7834029027317, -80.5410266927594), "h12v04"],
   "44" : [(42.8789422739013, -76.6063090767742), "h12v04"],
   "45" : [(40.8510571751412, -70.2767859840801), "h12v04"],
   "46" : [(47.9989284210628, -78.8502816116073), "h12v04"],
   "47" : [(47.5206733242827, -78.6435321776836), "h12v04"],
   "48" : [(46.6452952642064, -79.8934857477508), "h12v04"],
   "49" : [(45.5413654801563, -82.2698062033769), "h12v04"],
   "50" : [(45.4175058641709, -74.2052460495009), "h12v04"],
   "51" : [(45.3426960093274, -78.6915740365686), "h12v04"],
   "52" : [(44.6972260281395, -74.3240980242048), "h12v04"],
   "53" : [(44.4184082962773, -74.2633512202997), "h12v04"],
   "54" : [(43.7303084771034, -70.1593747032118), "h12v04"],
   "55" : [(45.6769491015939, -77.4844223240677), "h12v04"],
   "56" : [(48.1721542895407, -87.1557811534738), "h12v04"],
   "57" : [(45.3292862820756, -81.5994965405134), "h12v04"],
   "58" : [(46.9611693154808, -84.1770478936826), "h12v04"],
   "59" : [(45.9894786850275, -72.0371483480716), "h12v04"],
   "60" : [(41.7844831743042, -79.4615563404332), "h12v04"],
   "61" : [(41.5059473724118, -79.2539530715372), "h12v04"],
   "62" : [(41.4900623387685, -79.4321196609864), "h12v04"],
   "63" : [(43.2535124228648, -76.9469422205315), "h12v04"],
   "64" : [(47.6152454855985, -84.6936978911142), "h12v04"],
   "65" : [(41.5891185062877, -68.9337653582252), "h12v04"],
   "66" : [(44.3413726875828, -75.9699407204168), "h12v04"],
   "67" : [(44.1948149988828, -72.151206100508), "h12v04"],
   "68" : [(47.2270813704949, -78.7288215318993), "h12v04"],
   "69" : [(44.9341248517595, -84.6340150471842), "h12v04"],
   "70" : [(40.4827912231905, -71.9904715032474), "h12v04"],
   "71" : [(49.0419246794444, -87.686240124965), "h12v04"],
   "72" : [(48.2662514530604, -88.0455988736552), "h12v04"],
   "73" : [(41.2364283656025, -67.5203861002826), "h12v04"],
   "74" : [(49.5387982881903, -86.5266817539353), "h12v04"],
   "75" : [(44.1741331557231, -77.649425359314), "h12v04"],
   "76" : [(49.1000368937586, -78.2953524880394), "h12v04"],
   "77" : [(45.4614331648884, -73.5683058915726), "h12v04"],
   "78" : [(49.818201002388, -89.6236817650998), "h12v04"],
   "79" : [(42.1364892725282, -75.6645952862234), "h12v04"],
   "80" : [(43.3224503866647, -79.6433000733909), "h12v04"],
   "81" : [(49.3867497637347, -80.5524005781083), "h12v04"],
   "82" : [(47.3494640392623, -75.0241412855657), "h12v04"],
   "83" : [(43.0038469502306, -76.7513236236353), "h12v04"],
   "84" : [(47.6156951979867, -87.8746629247189), "h12v04"],
   "85" : [(47.2106424932864, -76.1210871430933), "h12v04"],
   "86" : [(46.0914113540768, -81.8901265344621), "h12v04"],
   "87" : [(49.4309712366572, -82.9477816715541), "h12v04"],
   "88" : [(40.3444119995582, -71.764794691116), "h12v04"],
   "89" : [(41.1809876826896, -76.9240838689791), "h12v04"],
   "90" : [(40.1294946331845, -76.8807513999062), "h12v04"],
   "91" : [(48.8078938217831, -89.9557259959862), "h12v04"],
   "92" : [(49.470270865351, -78.2381858641461), "h12v04"],
   "93" : [(41.5621906365231, -75.4010676703081), "h12v04"],
   "94" : [(45.3424659633383, -75.3464179121713), "h12v04"],
   "95" : [(41.6929476600918, -75.4824776292962), "h12v04"],
   "96" : [(49.2375673332796, -88.5887612018379), "h12v04"],
   "97" : [(48.1994121129235, -80.8640009759717), "h12v04"],
   "98" : [(45.0722395285579, -77.4944846067411), "h12v04"],
   "99" : [(48.9434887634467, -84.4230486702874), "h12v04"],
   "100" : [(45.8222150924491, -83.1320952062388), "h12v04"]
}
# sites_dict = {
#    "HF" : [(42.53691, -72.17265), "h12v04"]
#     "Summit" : [(72.57972, -38.50454), "h16v01"],
#     "NASA-U" : [(73.84189, -49.49831), "h16v01"],
#     "GITS":  [(77.13781, -61.04113), "h16v01"],
#     "Humboldt" : [(78.5266, -56.8305), "h16v01"],
#     "CP2" : [(69.87968, -46.98692), "h16v01"],
#     "South_Dome" : [(63.14889, -44.81717), "h16v02"],
#     "DYE-2" : [(66.48001, -46.27889), "h16v02"],
#     "Saddle" : [(65.99947, -44.50016), "h16v02"],
#     "NASA-SE" : [(66.4797, -42.5002), "h16v02"],
#     "Swiss_Camp" : [(69.56833, -49.31582), "h16v02"],
#     "JAR" : [(69.498358, -49.68156), "h16v02"],
#     "JAR_2" : [(69.42, -50.0575), "h16v02"],
#     "KAR" : [(69.69942, -33.00058), "h16v02"],
#     "NASA-E" : [(75, -29.99972), "h17v01"],
#     "NGRIP" : [(75.09975, -42.3325), "h17v01"],
#     "TUNU-N" : [(78.01677, -33.99387), "h17v01"]
# }

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
   with File(h5_fname, 'r') as h5_ds:
      data_np = h5_ds['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields'][sds][()]
   return data_np

def convert_ll_vnp(lat, lon, tile, in_dir):
   # Convert the lat/long point of interest to a row/col location
   template_h_list = \
                     glob.glob(os.path.join(copy_srs_dir,\
                     '*.A*{tile}*.h*'.format(tile=tile)))
   template_h_file = template_h_list[0]
   template_h_ds = gdal.Open(template_h_file, gdal.GA_ReadOnly)
   template_h_band = gdal.Open(template_h_ds.GetSubDatasets()[0][0], \
                               gdal.GA_ReadOnly)
   # Use pyproj to create a geotransform between
   # WGS84 geographic (lat/long; epsg 4326) and
   # the funky crs that modis/viirs use.
   # Note that this modis crs seems to have units
   # in meters from the geographic origin, i.e.
   # lat/long (0, 0), and has 2400 rows/cols per tile.
   # gdal does NOT read the corner coords correctly,
   # but they ARE stored correctly in the hdf metadata. Although slightly
   # difft than reported by gdal...

   # Using pyproj to transform coords of interes to meters
   in_proj = pyproj.Proj(init='epsg:4326')
   #out_proj = pyproj.Proj(template_h_band.GetProjection())
   out_proj = pyproj.Proj('+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs')
   
   # Current sample location convert from ll to m
   smpl_x, smpl_y = pyproj.transform(in_proj, out_proj, lon, lat)
   # print("Sample x, y: ")
   # print(str(smpl_x) + ", " + str(smpl_y))
   
   # FOR VIIRS, use manual
   #h12v04 UL: -6671703.1179999997839332 5559752.5983330002054572 LR: -5559752.5983330002054572 4447802.0786669999361038
   #out_proj = pyproj.Proj('+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs')

   # Getting bounding coords from meta
   # Perhaps no longer neededm but they're slilghtly difft than gdal geotransofrm
   # NOTE gdal works fine if you call the geotransform
   # on the BAND!!! (sds), not the DS
   meta = template_h_ds.GetMetadata_Dict()
   # FOR MODIS, us ALL CAPS
   y_origin_meta = float(meta['NORTHBOUNDINGCOORDINATE'])
   y_min_meta = float(meta['SOUTHBOUNDINGCOORDINATE'])
   x_max_meta = float(meta['EASTBOUNDINGCOORDINATE'])
   x_origin_meta = float(meta['WESTBOUNDINGCOORDINATE'])
   n_rows_meta = 1200 # int(meta['DATAROWS'])
   n_cols_meta = 1200 # int(meta['DATACOLUMNS'])
   pixel_height_meta_m = 926.6254330558330139 #(y_origin_meta - y_min_meta) / n_rows_meta
   pixel_width_meta_m = 926.6254330558330139 #pixel_height_meta_m

   # # Make calculations to get row/col value
   # # NOTE that for geotifs, it would also be possible
   # # to simply open with rasterio, then use .index()
   # # to return the row/col. This does not work for hdf
   x_origin_meta_m, y_origin_meta_m = pyproj.transform(in_proj, out_proj, x_origin_meta, y_origin_meta)
   x_max_meta_m, y_min_meta_m = pyproj.transform(in_proj, out_proj, x_max_meta, y_min_meta)

   col_m = int((smpl_x - x_origin_meta_m) / pixel_width_meta_m)
   row_m = int( -1 * (smpl_y - y_origin_meta_m) / pixel_height_meta_m)
   smp_rc = row_m, col_m
   # print("Geotransform-based extents: ")
   # print("pix height/width")
   # print(pixel_height_meta_m)
   # print(pixel_width_meta_m)
   # print("x max")
   # print(x_max_meta)
   # print("x origin")
   # print(x_origin_meta)
   # print("y min")
   # print(y_min_meta)
   # print("y origin")
   # print(y_origin_meta)
   # print()
   # print()
   # print("Sample location in LL:")
   # print(str(lon) + ", " + str(lat))
   # print("Sample location in map units (meters from origin): ")
   # print(str(smpl_x) + ", " + str(smpl_y))
   # print()
   # print()
   # print("Metadata-based row/col:")
   # print(smp_rc_meta)
   # print("Geotransform-based row/col:")
   return smp_rc

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
   # Use pyproj to create a geotransform between
   # WGS84 geographic (lat/long; epsg 4326) and
   # the funky crs that modis/viirs use.
   # Note that this modis crs seems to have units
   # in meters from the geographic origin, i.e.
   # lat/long (0, 0), and has 2400 rows/cols per tile.
   # gdal does NOT read the corner coords correctly,
   # but they ARE stored correctly in the hdf metadata. Although slightly
   # difft than reported by gdal...

   # # Using pyproj to transform coords of interes to meters
   in_proj = pyproj.Proj(init='epsg:4326')
   out_proj = pyproj.Proj(template_h_band.GetProjection())
   
   # # Current sample location convert from ll to m
   smpl_x, smpl_y = pyproj.transform(in_proj, out_proj, lon, lat)
 
   # Getting bounding coords from meta
   # Perhaps no longer neededm but they're slilghtly difft than gdal geotransofrm
   # NOTE gdal works fine if you call the geotransform
   # on the BAND!!! (sds), not the DS
   # meta = template_h_ds.GetMetadata_Dict()
   # FOR MODIS, us ALL CAPS
   # y_origin_meta = float(meta['NORTHBOUNDINGCOORDINATE'])
   # y_min_meta = float(meta['SOUTHBOUNDINGCOORDINATE'])
   # x_max_meta = float(meta['EASTBOUNDINGCOORDINATE'])
   # x_origin_meta = float(meta['WESTBOUNDINGCOORDINATE'])
   # n_rows_meta = int(meta['DATAROWS'])
   # n_cols_meta = int(meta['DATACOLUMNS'])
   # pixel_height_meta_m = float(meta['CHARACTERISTICBINSIZE'])
   # pixel_width_meta_m = float(meta['CHARACTERISTICBINSIZE'])

   # print("metadata bounding info: ")
   # print(y_origin_meta)
   # print(y_min_meta)
   # print(x_max_meta)
   # print(x_origin_meta)
   # print(n_rows_meta)
   # print(n_cols_meta)
   # print(pixel_height_meta_m)
   # print(pixel_width_meta_m)
   
   #TESTING these are conversions of the metadata extents to meters
   # x_origin_meta_m, y_origin_meta_m = pyproj.transform(in_proj, out_proj, x_origin_meta, y_origin_meta)
   # x_max_meta_m, y_min_meta_m= pyproj.transform(in_proj, out_proj, x_max_meta, y_min_meta)
   # print("calculating pixel height/width with metadata info: ")
   # print(str(x_max_meta_m) + " - " + str(x_origin_meta_m) + " / " + str(n_cols_meta))
   # print(str(y_origin_meta_m) + " - " + str(y_min_meta_m) + " / " + str(n_rows_meta))
   # pixel_width_meta_m = (x_max_meta_m - x_origin_meta_m) / n_cols_meta
   # pixel_height_meta_m = (y_origin_meta_m - y_min_meta_m) / n_rows_meta
   # col_meta_m = int((smpl_x - x_origin_meta_m) / pixel_width_meta_m)
   # row_meta_m = int(-1 * (smpl_y - y_origin_meta_m) / pixel_height_meta_m)
   # smp_rc_meta = row_meta_m, col_meta_m
   # print("Metadata-based extents in ll: ")
   # print(x_max_meta)
   # print(x_origin_meta)
   # print(y_min_meta)
   # print(y_origin_meta)
   # print("Metadata-based extents in meters: ")
   # print(pixel_height_meta_m)
   # print(pixel_width_meta_m)
   # print(x_max_meta_m)
   # print(x_origin_meta_m)
   # print(y_min_meta_m)
   # print(y_origin_meta_m)
   # print()

   #UNCOMMENT BELOW FOR MCD
   # Getting bounding coords etc from gdal geotransform
   n_cols = template_h_band.RasterXSize
   n_rows = template_h_band.RasterYSize
   x_origin, x_res, x_skew, y_origin, y_skew, y_res = template_h_band.GetGeoTransform()
   # Using the skew is in case there is any affine transformation
   # in place in the input raster. Not so for modis tiles, so not really necessary, but complete.
   x_max = x_origin + n_cols * x_res + n_cols * x_skew
   y_min = y_origin + n_rows * y_res + n_rows * y_skew
     
   # # Make calculations to get row/col value
   # # NOTE that for geotifs, it would also be possible
   # # to simply open with rasterio, then use .index()
   # # to return the row/col. This does not work for hdf
   pixel_width_m = (x_max - x_origin) / n_cols
   pixel_height_m = (y_origin - y_min) / n_rows
   col_m = int((smpl_x - x_origin) / pixel_width_m)
   row_m = int( -1 * (smpl_y - y_origin) / pixel_height_m)
   smp_rc = row_m, col_m
   # print("Geotransform-based extents: ")
   # print(pixel_height_m)
   # print(pixel_width_m)
   # print(x_max)
   # print(x_origin)
   # print(y_min)
   # print(y_origin)
   # print()
   # print()
   # print("Sample location in LL:")
   # print(str(lon) + ", " + str(lat))
   # print("Sample location in map units (meters from origin): ")
   # print(str(smpl_x) + ", " + str(smpl_y))
   # print()
   # print()
   # print("Metadata-based row/col:")
   # print(smp_rc)                
   # print("Geotransform-based row/col:")
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
       # Make a blank pandas dataframe that results will be appended to?
       
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
            wsa_swir_mean = []
            wsa_swir_sd = []
            bsa_swir_mean = []
            bsa_swir_sd = []

            # Keep track of doy for output CSV
            doy_list = []

            for day in doys:
                # Open the shortwave white sky albedo band.
                # The list approach is because of the processing date part of the file
                # name, which necessitates the wildcard -- this was just the easiest way.
                h_file_list = glob.glob(os.path.join(in_dir,
                                                      '{prdct}.A{year}{day:03d}*.h*'.format(prdct=prdct,
                                                                                            day=day, year=year)))
                # See if there is a raster for the date, if not use a fill value for the graph
                if len(h_file_list) == 0: # or len(bsa_tif_list) == 0 or len(qa_tif_list) == 0:
                    print('File not found: {prdct}.A{year}{day:03d}*.h*'.format(prdct=prdct,
                                                                                day=day, year=year))
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

                    # Open tifs as gdal ds
                    #print("Opening: " + h_file_day + " " + sds_name_wsa_sw)
                    if "VNP" in prdct:
                       #print("Found VIIRS product.")
                       wsa_band = h5_to_np(h_file_day, sds_name_wsa_sw)
                       bsa_band = h5_to_np(h_file_day, sds_name_bsa_sw)
                       qa_band = h5_to_np(h_file_day, sds_name_qa_sw)
                    elif "MCD" in prdct:
                       #print("Found MODIS product.")
                       wsa_band = hdf_to_np(h_file_day, sds_name_wsa_sw)
                       bsa_band = hdf_to_np(h_file_day, sds_name_bsa_sw)
                       qa_band = hdf_to_np(h_file_day, sds_name_qa_sw)
                    elif "LC08" in prdct:
                       #print("Found Landsat-8 product.")
                       wsa_band = hdf_to_np(h_file_day, sds_name_wsa_sw)
                       bsa_band = hdf_to_np(h_file_day, sds_name_bsa_sw)
                       qa_band = hdf_to_np(h_file_day, sds_name_qa_sw)
                    else:
                       print("Unknown product! This only works for MCD, VNP, or LC8/LC08 hdf or h5 files!")
                       sys.exit()
                       
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
                    if "VNP" in prdct:
                       smp_rc = convert_ll_vnp(site[1][0][0], site[1][0][1], site[1][1], in_dir)
                    
                    elif "MCD" in prdct:
                       smp_rc = convert_ll(site[1][0][0], site[1][0][1], site[1][1], in_dir)
                    
                    elif "LC08" in prdct:
                       sys.exit()
                    else:
                       print("Unknown product! This only works for MCD, VNP, or LC8/LC08 hdf or h5 files!")
                       sys.exit()

                    wsa_swir_subset = wsa_swir_masked_qa[smp_rc]
                    wsa_swir_subset_flt = np.multiply(wsa_swir_subset, 0.001)
                    bsa_swir_subset = bsa_swir_masked_qa[smp_rc]
                    bsa_swir_subset_flt = np.multiply(bsa_swir_subset, 0.001)
                    # Add each point to the temporary list
                    wsa_smpl_results.append(wsa_swir_subset_flt)
                    bsa_smpl_results.append(bsa_swir_subset_flt)
                    doy_list.append(day)
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
           doy_df = pd.DataFrame(doy_list)
           cmb_smpl_results_df = pd.concat([doy_df, wsa_smpl_results_df, bsa_smpl_results_df], axis=1, ignore_index=True)
           cmb_smpl_results_df.set_axis(['doy', 'wsa', 'bsa'], axis=1, inplace=True)
           

           
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
