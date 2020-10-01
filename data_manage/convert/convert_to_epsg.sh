#!/bin/bash

in_dir=$1 
out_dir=$2
epsg_code=$3

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

for hdf in $in_dir/*.tif
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    echo ${in_dir}/${filename} ${out_dir}/${filename_bare}.tif
    gdalwarp -t_srs EPSG:${epsg_code} -overwrite ${in_dir}/${filename} ${out_dir}/${filename_bare}_${epsg_code}.tif
    
done
