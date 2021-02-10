#!/bin/bash

in_dir=$1
out_dir=$2

for rst in ${in_dir}/*.hdf;
do
    echo $rst
    out_name=${out_dir}/`basename ${rst}`_subset.tif
    echo $out_name
    gdal_translate -of GTiff -projwin -0.05 0.025 -0.037 0.013 ${rst} ${out_name}
    #gdal_translate -of GTiff -projwin -0.05 0.025 -0.037 0.013 HDF4_EOS:EOS_GRID:${rst}:"MCD_CMG_BRDF_30Arc Second":BRDF_Quality ${out_name} 
done
