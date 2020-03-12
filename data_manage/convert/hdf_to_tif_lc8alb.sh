#!/bin/bash

in_dir=$1 
out_dir=$2

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

for hdf in $in_dir/*broad.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':Grid_Landsat_30m:Albedo_WSA_shortwave ${out_dir}/wsa/${filename_bare}_wsa_broad.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':Grid_Landsat_30m:Albedo_BSA_shortwave ${out_dir}/bsa/${filename_bare}_bsa_broad.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':Grid_Landsat_30m:Albedo_Band_Quality_shortwave ${out_dir}/qa/${filename_bare}_qa_broad.tif
    
done
