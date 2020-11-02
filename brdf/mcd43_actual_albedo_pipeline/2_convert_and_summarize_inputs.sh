#!/bin/bash

in_dir=$1
years=$2
tiles=$3
shp_dir=$4

out_dir=${in_dir}/out/

if [ ! -d ${out_dir} ];
then
    mkdir -p ${out_dir}
    mkdir -p ${out_dir}/AOD_tif/
    mkdir -p ${out_dir}/SZA_tif/
    mkdir -p ${out_dir}/QA_tif/
    mkdir -p ${out_dir}/AOD_tif_wgs84/
    mkdir -p ${out_dir}/stats/
    mkdir -p ${out_dir}/bsky/
fi

# make two loops, nested:
for year in ${years};
do
    for tile in ${tiles};
    do
	echo $year $tile
	# Convert AOD, SZA, and mandatory QA from MCD43A1 to tif, and project AOD to WGS84
	# AOD
	/home/arthur.elmes/code/geo_tools/data_manage/convert/hdf_to_tif_mod08.sh ${in_dir}/MOD08_D3/${year} ${out_dir}/AOD_tif/

	# SZA
	/home/arthur.elmes/code/geo_tools/data_manage/convert/hdf_to_tif_mcd43a2.sh ${in_dir}/MCD43A2/${year}/${tile}/ ${out_dir}/SZA_tif/

	# QA
	/home/arthur.elmes/code/geo_tools/data_manage/convert/hdf_to_tif_mcd43a1_3.sh ${in_dir}/MCD43A1/${year}/${tile}/ ${out_dir}/QA_tif/ 1


	# Project AOD
	/home/arthur.elmes/code/geo_tools/data_manage/convert/convert_to_wgs84.sh ${out_dir}/AOD_tif/ ${out_dir}/AOD_tif_wgs84/

	# Delete any previously made SZA tables for the tile/year
	if [ -f ${out_dir}/AOD_tif_wgs84/AOD_${tile}_wgs84_stats.csv ];
	then
	    rm ${out_dir}/AOD_tif_wgs84/AOD_${tile}_wgs84_stats.csv
	fi
	
	if [ -f ${out_dir}/SZA_tif/SZA_${tile}_stats.csv ];
	then
	    rm ${out_dir}/SZA_tif/SZA_${tile}_stats.csv
	fi

	# Now summarize the AOD and SZA into tables, one per tile
	# AOD
	python /home/arthur.elmes/code/geo_tools/time_series/summary_stats_box.py -d ${out_dir}/AOD_tif_wgs84/ -p AOD -t ${tile} -y ${year} -v ${shp_dir}${tile}_wgs84.shp

	# SZA
	python /home/arthur.elmes/code/geo_tools/time_series/summary_stats_box.py -d ${out_dir}/SZA_tif/sza/ -p SZA -t ${tile} -y ${year} -v ${shp_dir}${tile}.shp

	if [ -f ${out_dir}/AOD_tif_wgs84/AOD_${tile}_wgs84_stats.csv ];
	then
	    cp ${out_dir}/AOD_tif_wgs84/AOD_${tile}_wgs84_stats.csv ${out_dir}/stats
	fi

	if [ -f ${out_dir}/SZA_tif/sza/SZA_${tile}_stats.csv ];
	then
	    cp ${out_dir}/SZA_tif/sza/SZA_${tile}_stats.csv ${out_dir}/stats
	fi
	
	
    done
done


# Now make a txt file with a list of all MCD43A1 inputs

workspace=${in_dir}/MCD43A1/

if [ -f ${out_dir}/stats/mcd43a1_${tile}_list.txt ];
then
    rm ${out_dir}/stats/mcd43a1_${tile}_list.txt
fi


for tile in $tiles; do
    if [ -f ${workspace}/mcd43a1_${tile}_list.txt ]; then
        rm ${workspace}/mcd43a1_${tile}_list.txt
    fi

    for year in ${years}; do
        find ${workspace}/${year}/${tile}/ -type f -name "*.hdf"  -printf "%f\n" >> ${out_dir}/stats/mcd43a1_${tile}_list.txt
    done
done
