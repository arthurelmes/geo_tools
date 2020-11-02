#!/bin/bash

# QA screen the bsky outputs, by year and tile

tiles="h15v03" #$1
start_year=2020 #$2
end_year=2020 #$3

bsky_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/bsky_tif/" #$4
qa_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/QA_tif/qa/" #$5
sza_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/SZA_tif/sza/" #$6
out_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/bsky_qa_screened/" #$7


for tile in ${tiles};
do
    for year in $(seq ${start_year} ${end_year});
    do
	echo ${tile} ${year} ${year}
	/home/arthur.elmes/code/geo_tools/data_manage/qa_screen_mcd43.sh ${tile} ${year} ${year} ${bsky_dir} ${qa_dir} ${sza_dir} ${out_dir}
    done
done
