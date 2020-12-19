#!/bin/bash

products=$1
AS=$2
year=$3
start_day=$4
end_day=$5
tiles=$6
dl_root_dir=$7

for product in ${products};
do
    for tile in ${tiles};
    do
	out_dir=${dl_root_dir}/${product}/${tile}/
	if [ ! -d "${out_dir}" ];
	then
	    mkdir -p ${out_dir}
	fi
		
	for doy in $(seq ${start_day} ${end_day});
	do
	    if [ "$doy" -le 9 ];
	    then
		doy=00${doy}
	    elif [ "$doy" -le 99 ];
	    then
		doy=0${doy}
	    fi
	    
	    wget -e robots=off -m -np -A "*${tile}*" -R "*.html" -R "*.tmp" -nH --cut-dirs=6 https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/${AS}/${product}/${year}/${doy}/ --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298"  -P ${out_dir}

	done
    done
done
