#!/bin/bash

# QA screen the bsky outputs, by year and tile

tiles=$1
start_year=$2
end_year=$3
working_dir=$4

bsky_dir=${working_dir}/bsky_tif/
qa_dir=${working_dir}/QA_tif/qa/
sza_dir=${working_dir}/SZA_tif/sza/
out_dir=${working_dir}/bsky_qa_screened/


for tile in ${tiles};
do
    for year in $(seq ${start_year} ${end_year});
    do
	echo ${tile} ${year} ${year}
	/home/arthur.elmes/code/geo_tools/data_manage/qa_screen_mcd43.sh ${tile} ${year} ${year} ${bsky_dir} ${qa_dir} ${sza_dir} ${out_dir}
    done
done
