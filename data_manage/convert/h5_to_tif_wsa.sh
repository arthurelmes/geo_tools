#!/bin/bash

## WARNING: Currently only works with manual tile bounding coords (in meters from origin, I think?), which must be passed in manually. Get by looking at extent in QGIS or similar.
## TODO convert bounding coordinates from ll to meters so this is automated. Shortcut/hurry mode, just write them down in file for all tiles.

## h12v04 UL: -6671703.1179999997839332 5559752.5983330002054572 LR: -5559752.5983330002054572 4447802.0786669999361038
## h13v04 UL: -5559752.5983330002054572 5559752.5983330002054572 LR: -4447802.0786669999361038 4447802.0786669999361038 
## h16v01 UL: -2223901.0393329998478293 8895604.1573329996317625 LR: -1111950.5196670000441372 7783653.6376670002937317
## h16v02 UL: -2223901.0393329998478293 7783653.6376670002937317 LR: -1111950.5196670000441372 6671703.1179999997839332
## h11v04 UL: -7783653.6376670002937317 5559752.5983330002054572 LR: -6671703.1179999997839332 4447802.0786669999361038
## h10v04 UL: -8895604.1573329996317625 5559752.5983330002054572 LR: -7783653.6376670002937317 4447802.0786669999361038
in_dir=$1 
out_dir=$2

#TODO fix this so the single (or double?) quotes are actually stored in the string variable
srs_str='PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]'

ul_coord='-8895604.1573329996317625 5559752.5983330002054572'
lr_coord='-7783653.6376670002937317 4447802.0786669999361038'

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

if [ ! -d ${out_dir}/qa/ ]; then
    mkdir ${out_dir}/qa/
fi

if [ ! -d ${out_dir}/wsa/ ]; then
    mkdir ${out_dir}/wsa/
fi

if [ ! -d ${out_dir}/bsa/ ]; then
    mkdir ${out_dir}/bsa/
fi

if [ ! -d ${out_dir}/lwmask/ ]; then
    mkdir ${out_dir}/lwmask/
fi

for h5 in $in_dir/*.h5
do
    #echo $h5
    filename=$(basename -- $h5)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"

#    echo -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_WSA_shortwave ${out_dir}/wsa/${filename}_wsa_shortwave.tif


    #gdal_translate -a_nodata 255 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_LandWaterType ${out_dir}/lwmask/${filename}_lw_type.tif
    
    gdal_translate -a_nodata 32767 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_WSA_shortwave ${out_dir}/wsa/${filename}_wsa_shortwave.tif

    gdal_translate -a_nodata 32767 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_BSA_shortwave ${out_dir}/bsa/${filename}_bsa_shortwave.tif    

    gdal_translate -a_nodata 255 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/qa/${filename}_qa_shortwave.tif    

    #for VNP43IA3Albedo_WSA_I2
#    gdal_translate -a_nodata 32767 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not spAlbedo_WSA_I2ecified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_WSA_I2 ${out_dir}/wsa/${filename}_wsa_i2.tif

    #for VNP43MA1 BRDF_Albedo_Parameters_M4
#    gdal_translate -a_nodata 32767 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not spAlbedo_WSA_I2ecified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr $ul_coord $lr_coord -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Parameters_M4 ${out_dir}/${filename}_params_ma4.tif

done


