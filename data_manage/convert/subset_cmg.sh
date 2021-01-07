#!/bin/bash

in_dir="/ipswich/data02/arthur.elmes/MCD43D61/h00v00"
out_dir="/ipswich/data02/arthur.elmes/MCD43D61/ak_subset_tif"

for rst in ${in_dir}/*.hdf;
do
    echo $rst
    out_name=${out_dir}/`basename ${rst}`_subset.tif
    echo $out_name
    gdal_translate -of GTiff -projwin -0.05 0.025 -0.037 0.013 ${rst} ${out_name}

done
