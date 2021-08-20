#!/bin/bash

## Script to download MODIS/VIIRS products from LADSWEB, a good backup for when LPDAAC is offline
## Inputs are as below -- note that the tiles var is designed to intake a list in "" double quotes
## Also note that for CMG products, enter h00v00 for the tiles arguemnt, since these products have no tiles
## Author: Arthur Elmes, Dec 2020

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
	    if [ "$tile" == "h00v00" ];
	    then
		wget -e robots=off -m -np -R "*.html" -R "*.tmp" -nH --cut-dirs=6 https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/${AS}/${product}/${year}/${doy}/ --header "Authorization: Bearer YXJ0aHVyLmVsbWVzOllYSjBhSFZ5TG1Wc2JXVnpRR2R0WVdsc0xtTnZiUT09OjE2MjYyODg5ODY6MGRjNTg0ZjE2N2IyMjkwZWFkOWQxNTcxYWUyMWMyNDIzYTMyZTA4ZA"  -P ${out_dir}
	    else
		wget -e robots=off -m -np -A "*${tile}*" -R "*.html" -R "*.tmp" -nH --cut-dirs=6 https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/${AS}/${product}/${year}/${doy}/ --header "Authorization: Bearer YXJ0aHVyLmVsbWVzOllYSjBhSFZ5TG1Wc2JXVnpRR2R0WVdsc0xtTnZiUT09OjE2MjYyODg5ODY6MGRjNTg0ZjE2N2IyMjkwZWFkOWQxNTcxYWUyMWMyNDIzYTMyZTA4ZA"  -P ${out_dir}
	    fi
	done
    done
done
