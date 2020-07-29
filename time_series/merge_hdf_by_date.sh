#!/bin/bash

### The purpose of this script is to merge all hdf files with the same date into a single geotiff for that date.
### Currently set up specifically for the output hdf from actual_albedo_hdf.exe, but can be easily modified.
### Author: Arthur Elmes 2020-07-29

workspace="/media/arthur/Windows/LinuxShare/bsky_test/tif/"
output_dir="/media/arthur/Windows/LinuxShare/bsky_test/tif/merged/"

if [ ! -d ${output_dir} ]; then
    mkdir ${output_dir}
fi

for yr in $( seq 2000 2020); do
    for dt in $( seq 1 366); do
	if [ ${dt} -lt 10 ]; then
	    dt=00${dt}
	elif [ ${dt} -lt 100 ]; then
	    dt=0${dt}
	fi
	full_date=${yr}${dt}
	hdf_list=`find $workspace -type f -name "*${yr}${dt}*"`
	if [ ${#hdf_list} -gt 0 ]; then
	    gdal_merge.py -o "${output_dir}MCD43_actual_albedo_greenland_west_coast_${yr}${dt}.tif" -of GTiff ${hdf_list}
	fi
    done
done
