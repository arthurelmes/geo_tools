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


for bin in $in_dir/*broad.bin
do
    filename=$(basename -- $bin)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    
    gdal_translate -a_nodata 32767 -of GTiff -b 1 ${in_dir}/${filename} ${out_dir}/bsa/${filename}_bsa_shortwave.tif
    gdal_translate -a_nodata 32767 -of GTiff -b 2 ${in_dir}/${filename} ${out_dir}/wsa/${filename}_wsa_shortwave.tif

done


for bin in $in_dir/*broad_qa.bin
do
    filename=$(basename -- $bin)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"

    gdal_translate -a_nodata 32767 -of GTiff ${in_dir}/${filename} ${out_dir}/qa/${filename}_qa_shortwave.tif

done

