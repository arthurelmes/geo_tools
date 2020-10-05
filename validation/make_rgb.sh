#!/bin/bash

in_dir=$1
out_dir=${in_dir}/rgb/

if [ ! -d ${out_dir} ];
then
    mkdir ${out_dir}
fi


for tif in ${in_dir}/*.tif;
do
    tif_base=$(basename -- $tif)
    IFS="_"
    read -ra tif_parts <<< ${tif_base}
    h5=${tif_parts[0]}
    IFS=" "
    if [[ $h5 == "VNP"* ]] || [[ $h5 == "VJ1"* ]]; then
	b_red=`find ${in_dir} -type f -name "$h5*b5*"`
	b_green=`find ${in_dir} -type f -name "$h5*b4*"`
	b_blue=`find ${in_dir} -type f -name "$h5*b3*"`
    
    elif [[ $h5 == "MCD"* ]]; then
	b_red=`find ${in_dir} -type f -name "$h5*b1*"`
	b_green=`find ${in_dir} -type f -name "$h5*b4*"`
	b_blue=`find ${in_dir} -type f -name "$h5*b3*"`
    fi
    
    gdal_merge.py -separate -init "0 0 0" -o ${out_dir}/${h5}_rgb.tif ${b_red} ${b_green} ${b_blue} -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB
	
done
