#!/bin/bash

in_dir=$1 
out_dir=$2

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -sds -of GTiff ${in_dir}/${filename} ${out_dir}/${filename_bare}.tif
done
