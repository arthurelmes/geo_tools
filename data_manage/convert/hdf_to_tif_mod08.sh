#!/bin/bash

in_dir=$1 
out_dir=$2

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -a_srs "+proj=longlat +ellps=clrk66 +no_defs" -a_nodata -9999 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':mod08:AOD_550_Dark_Target_Deep_Blue_Combined_Mean ${out_dir}/${filename_bare}.tif
done

