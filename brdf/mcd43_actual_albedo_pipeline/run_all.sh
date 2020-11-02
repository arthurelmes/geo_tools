#!/bin/bash

start_date=$1
end_date=$2
tiles=$3
raw_data_dir=$4
shp_dir=$5

# calculate years from input dates
start_year=`date -d ${start_date} "+%Y"`
end_year=`date -d ${end_date} "+%Y"`
years=`echo $(seq ${start_year} ${end_year})`

for tile in ${tiles};
do
    echo ./1_download_bsky_inputs.sh ${start_date} ${end_date} ${tile} ${raw_data_dir}
done

echo ./2_convert_and_summarize_inputs.sh ${raw_data_dir} ${years} """${tiles}""" ${shp_dir}
echo ./3_actual_albedo_multi.sh """${tiles}""" ${start_date} ${end_date} ${raw_data_dir}
echo ./4_screen_and_merge_bsky.sh ${tiles} ${start_year} ${end_year} ${raw_data_dir}/out/
