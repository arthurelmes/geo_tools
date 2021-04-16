#!/bin/bash

# Pass in the yyyy as arg1
start_date=${1}-01-01
end_date=$(date -I -d "$start_date +192 days")
cur_date=$start_date
url_base=https://e4ftl01.cr.usgs.gov/MOTA/MCD43D
vers=.006
dl_dir=/merrimack/data02/arthur.elmes/orig/v6/$1

echo "Downloading to: " $dl_dir
echo "Downloading from: "$start_date "to: ":$end_date


# Loop through D31 and D40
# Each band has the three params: geo, iso, vol
#declare -a arr=("31"  "40")
#for i in "${arr[@]}"

for i in 31 40;
do
    band=$(($(($i+2))/3))
    if [ $i -le 9 ]; then
	i=0$i
    fi
    
    # Loop through all dates in year, pass to download script with full url
    while [[ "$cur_date" < "$end_date" ]]; do
	cur_date_url=${cur_date:0:4}.${cur_date:5:2}.${cur_date:8:2}
	dl_url=${url_base}${i}${vers}/${cur_date_url}
	cur_date=$(date -I -d "$cur_date+1 day")
	
	if [ ! -r $dl_dir ]; then
	    mkdir -p $dl_dir
	fi
	
	echo "Downloading :"  $dl_url $dl_dir
        bash ./download.sh $dl_url $dl_dir
    done
    cur_date=$start_date
done 




# call downloader script with 2 args: url and dl_dir
#bash ./download.sh $url .
#echo 
