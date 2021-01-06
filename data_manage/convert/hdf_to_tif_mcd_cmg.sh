#!/bin/bash

in_dir=$1 
out_dir=$2

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -a_srs "+proj=longlat +ellps=clrk66 +no_defs" -a_nodata 32767 -of GTiff -sds ${in_dir}/${filename} ${out_dir}/${filename_bare}.tif
done

