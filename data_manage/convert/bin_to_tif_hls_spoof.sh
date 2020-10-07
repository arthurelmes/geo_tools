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

for safe in $in_dir/*.SAFE
do
    sw_bin=`find ${safe} -type f -name "*albedo_broad.bin"`
    qa_bin=`find ${safe} -type f -name "*albedo_broad_qa.bin"`

    filename=$(basename -- ${sw_bin})
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    
    gdal_translate -a_nodata 32767 -of GTiff -b 1 ${sw_bin} ${out_dir}/bsa/${filename}_bsa_shortwave.tif
    gdal_translate -a_nodata 32767 -of GTiff -b 2 ${sw_bin} ${out_dir}/wsa/${filename}_wsa_shortwave.tif
    gdal_translate -a_nodata 32767 -of GTiff ${qa_bin} ${out_dir}/qa/${filename}_qa_shortwave.tif
done
