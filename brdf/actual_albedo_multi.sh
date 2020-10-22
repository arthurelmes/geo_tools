#!/bin/bash

tiles="h15v02"
isodate_start=2020-01-01
isodate_end=2020-12-31
stats_dir="/lovells/data02/arthur.elmes/greenland/bsky_vars/"
mcd43a1_dir="/lovells/data02/arthur.elmes/greenland/MCD43A1/"
exe="/home/arthur.elmes/code/actual_albedo_tool/actual_albedo_hdf.exe"
out_dir="/ipswich/data01/arthur.elmes/bsky/"

d="$isodate_start"
for tile in ${tiles};
do
    while [ "$d" != "$enddate" ];
    do
	year=`date -d $d +%Y`
	aod_tbl="${stats_dir}/AOD/AOD_${year}_${tile}_stats.csv"
	sza_tbl="${stats_dir}/SZA/SZA_${year}_${tile}_stats.csv"
	mcd43a1_tbl="${stats_dir}/MCD43A1/mcd43a1_${tile}_list.txt"

	date=`date -d $d +%m/%d/%Y`
	jdate=`date -d $date +%Y%j`
	
	aod=`awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $aod_tbl`
	sza=`awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $sza_tbl`
	params=`awk -v date_a="A$jdate" -F "," '$0~date_a { print $1 "\t" }' $mcd43a1_tbl`
	if [ ! -z $aod ] && [ ! -z $sza ] && [ ! -z $params ]; then
	    cmd_string="${exe} -par ${mcd43a1_dir}/${year}/${tile}/${params} -od ${aod} -szn ${sza} -out ${out_dir}${params::-5}_bsky.tif"
	    #TODO I think I have to change dir to the actual albedo exe directory before running
	    cd `dirname ${exe}`
	    ${cmd_string}
	    cd -
	    #TODO then probably revert to previous dir after?
	fi
	
	d=$(date -I -d "$d + 1 day")
    done
done
