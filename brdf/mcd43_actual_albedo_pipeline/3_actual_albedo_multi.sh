#!/bin/bash

tiles=$1
isodate_start=$2
isodate_end=$3 
working_dir=$4 

mcd43a1_dir=${working_dir}/MCD43A1/
stats_dir=${working_dir}/out/stats/
out_dir=${working_dir}/out/bsky/
out_dir_tif=${working_dir}/out/bsky_tif/
exe="/home/arthur.elmes/code/actual_albedo_tool/actual_albedo_hdf.exe"


d="$isodate_start"
for tile in ${tiles};
do
    while [ "$d" != "$isodate_end" ];
    do
	year=`date -d $d +%Y`
	aod_tbl="${stats_dir}/AOD_${tile}_wgs84_stats.csv"
	sza_tbl="${stats_dir}/SZA_${tile}_stats.csv"
	mcd43a1_tbl="${stats_dir}/mcd43a1_${tile}_list.txt"

	date=`date -d $d +%m/%d/%Y`
	jdate=`date -d $date +%Y%j`
	
	aod=`awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $aod_tbl`
	sza=`awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $sza_tbl`
	params=`awk -v date_a="A$jdate" -F "," '$0~date_a { print $1 "\t" }' $mcd43a1_tbl`

	if [ ! -z "${aod}" ] && [ ! -z $"{sza}" ] && [ ! -z $"{params}" ]; then
	    cmd_string="${exe} -par ${mcd43a1_dir}/${year}/${tile}/${params} -od ${aod} -szn ${sza} -out ${out_dir}${params::-5}_bsky.hdf"
	    echo $cmd_string
	    # have to change dir to the actual albedo exe directory before running
	    cd `dirname ${exe}`
	    ${cmd_string}
	    cd -
	    # then revert to previous dir
	fi
	
	d=$(date -I -d "$d + 1 day")
    done
done


# now convert all the blue sky ouput hdfs to tif
/home/arthur.elmes/code/geo_tools/data_manage/convert/hdf_to_tif_mcd43_actual_albedo.sh ${out_dir} ${out_dir_tif}
