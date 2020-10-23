#!/bin/bash

tiles="h15v03"
isodate_start=2020-01-01
isodate_end=2020-12-31
stats_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/stats/"
mcd43a1_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/MCD43A1/"
exe="/home/arthur.elmes/code/actual_albedo_tool/actual_albedo_hdf.exe"
out_dir="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/bsky/"
out_dir_tif="/lovells/data02/arthur.elmes/test_blue_sky_multi/out/bsky_tif/"

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
	if [ ! -z $aod ] && [ ! -z $sza ] && [ ! -z $params ]; then
	    cmd_string="${exe} -par ${mcd43a1_dir}/${year}/${tile}/${params} -od ${aod} -szn ${sza} -out ${out_dir}${params::-5}_bsky.hdf"
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
