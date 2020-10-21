#!/bin/bash

tiles="h15v02"
isodate_start=2020-01-01
isodate_end=2020-12-31
working_dir="/home/arthur/Dropbox/projects/greenland/blue_sky_variables/"
exe="/arthur.elmes/code/actual_albedo_tool/actual_albedo_hdf.exe"
out_dir="/ipswich/data01/arthur.elmes/bsky/"

d="$isodate_start"
for tile in ${tiles};
do
    while [ "$d" != "$enddate" ];
    do
	aod_tbl="${working_dir}/AOD/AOD_${tile}_wgs84_stats.csv"
	sza_tbl="${working_dir}/SZA/SZA_${tile}_stats.csv"
	mcd43a1_tbl="${working_dir}/MCD43A1/2020/mcd43a1_${tile}_list.csv"

	date=`date -d $d +%m/%d/%Y`
	jdate=`date -d $date +%Y%j`
	
	aod=`awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $aod_tbl`
	sza=`awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $sza_tbl`
	params=`awk -v date_a="A$jdate" -F "," '$0~date_a { print $1 "\t" }' $mcd43a1_tbl`
	if [ ! -z $aod ] && [ ! -z $sza ] && [ ! -z $params ]; then
	    cmd_string="${exe} -par ${working_dir}${params} -od ${aod} -szn ${sza} -out ${out_dir}${params::-5}_bsky.tif"
	    echo $cmd_string
	fi
	
	d=$(date -I -d "$d + 1 day")
    done
done

/home/arthur.elmes/code/actual_albedo_tool/actual_albedo_hdf.exe -par /lovells/data02/arthur.elmes/greenland/MCD43A1/2014/h16v01/MCD43A1.A2014005.h16v01.006.2016146130845.hdf -od  -szn  -out /ipswich/data01/arthur.elmes/bsky/MCD43A1.A2014005.h16v01.006.blsky.hdf
