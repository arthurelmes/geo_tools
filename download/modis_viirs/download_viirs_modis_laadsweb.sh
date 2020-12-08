#!/bin/bash

AS="3339"
products="VNP43MA3 VJ143MA3"
year=2019
start_day=1
end_day=365
#tiles="h08v05 h09v04 h11v04 h11v09 h12v04 h16v02 h26v04 h30v11"
tiles="h09v04 h11v04"

for product in ${products};
do
    for tile in ${tiles};
    do
	out_dir="/ipswich/data02/arthur.elmes/${product}/${tile}/"

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
