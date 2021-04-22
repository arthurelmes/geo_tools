#!/bin/bash
# Script to download TILED MODIS or VIIRS data products from Terra (MOD), Aqua (MYD), combined Terra Aqua (MCD), or SNPP-VIIRS (VNP)
# Does not currenty work for CMG products, future revision will
# Arthur Elmes
# Created 2019-05-01
# Updated to add version option on 2021-04-22 by afme

usage="Usage: ./download_modis.sh [-s start date (YYYY-MM-DD)] [-e end date (YYYY-MM-DD)] [-n product short name e.g. MCD43A3] [-t tile e.g. h12v04] [-d download dir] [-v version]"
while getopts ":s:e:n:t:d:v:" arg; do
    case $arg in
	s) start_date=$OPTARG;;
	e) end_date=$OPTARG;;
	n) short_name=$OPTARG;;
	t) tile=$OPTARG;;
	d) dl_dir=$OPTARG;;
	v) vers=$OPTARG;;
	\?) echo $usage
    esac
done

if [ "${tile}" = "h00v00" ];
then
    tile=""
fi

url_base=https://e4ftl01.cr.usgs.gov/

if [ -z $start_date ] || [ -z $end_date ] || [ -z $short_name ] || [ -z $tile ] || \
       [ -z $dl_dir ]; then
    echo $usage
    exit
else
    echo "All args ok"
fi

# Check if the download dir has a trailing slash, add if not
case "$dl_dir" in
    */)
	echo
	;;
    *)
	echo "Adding trailing slash to dl_dir"
	dl_dir=${dl_dir}/
	;;
    esac

# Check which product was specified to select the right URL
case ${short_name} in
    "MOD"*) echo "Found Terra Product"
	    url_prod=${url_base}"MOLT/${short_name}.${vers}/"
	    fmt="hdf";;
    "MYD"*) echo "Found Aqua Product"
	    url_prod=${url_base}"MOLA/${short_name}.${vers}/"
	    fmt="hdf";;
    "MCD"*) echo "Found Combined Terra Aqua Product" 
	    url_prod=${url_base}"MOTA/${short_name}.${vers}/"
	    fmt="hdf";;
    "VNP"*) echo "Found SNPP Product"
	    url_prod=${url_base}"VIIRS/${short_name}.${vers}/"
	    fmt="h5";;
esac

cur_date=${start_date}
end_date=$(date -I -d "$end_date+1 day")

# Loop through all dates in year, download with full url
while [[ "$cur_date" < "$end_date" ]]; do 
    dl_dir_out=$dl_dir
    year=`date --date="$cur_date" '+%Y'`
    cur_date_url=${cur_date:0:4}.${cur_date:5:2}.${cur_date:8:2}
    dl_url=${url_prod}${cur_date_url}/
    file="${short_name}*${tile}*.${fmt}"
    cur_date=$(date -I -d "$cur_date+1 day")
    dl_dir_out=${dl_dir_out}${short_name}/${year}/${tile}
    if [ ! -r $dl_dir_out ]; then
	mkdir -p $dl_dir_out
    fi
    echo "Downloading from:" ${dl_url}
    echo "File: " ${file}
    echo "Saving to: " ${dl_dir_out}
    wget -N --load-cookies ~/.urs_cookies -c --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on \
    	 -r --reject "index.html*" --accept "${file}" -l1 -np -e robots=off --no-directories --waitretry=300 -t 100 \
     	 --directory-prefix=${dl_dir_out} --secure-protocol=TLSv1 ${dl_url}
done
