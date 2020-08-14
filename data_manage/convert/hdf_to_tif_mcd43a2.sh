#!/bin/bash
in_dir=$1 
out_dir=$2

srs_str="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

if [ ! -d ${out_dir}/sza/ ]; then
    mkdir ${out_dir}/sza/
fi


for hdf in $in_dir/*.hdf
do
    #echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:"${in_dir}${filename}":MOD_Grid_BRDF:BRDF_Albedo_LocalSolarNoon ${out_dir}/sza/${filename_bare}_sza.tif

done
