#!/bin/bash

### The purpose of this script is to merge all hdf files with the same date into a single geotiff for that date.
### Currently set up specifically for the output hdf from actual_albedo_hdf.exe (converted to tif), but can be easily modified.
### Author: Arthur Elmes 2020-07-29

# Currently these must be tifs
workspace=$1
output_dir=$2
start_year=$3
end_year=$4

if [ ! -d ${output_dir} ]; then
    mkdir ${output_dir}
fi

for yr in $( seq "${start_year}" "${end_year}" ); do
    for dt in $( seq 1 366); do
	if [ ${dt} -lt 10 ]; then
	    dt=00${dt}
	elif [ ${dt} -lt 100 ]; then
	    dt=0${dt}
	fi
	full_date=${yr}${dt}
	hdf_list=`find $workspace -type f -name "*${yr}${dt}*"`
	if [ ${#hdf_list} -gt 0 ]; then
	    #change the output name to draw from the input name
	    gdal_merge.py -o "${output_dir}MCD43_actual_albedo_greenland_entire_island_A${yr}${dt}.tif" -of GTiff -n 32767 -a_nodata 32767  ${hdf_list}
	fi
    done
done
