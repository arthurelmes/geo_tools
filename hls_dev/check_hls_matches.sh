#!/bin/bash

# loop through L2A_HLS dir, see which have matching HLS scene in HLS dir.
# if no match, mv the L2A safe to a different dir for SAFEkeeping

L2A_HLS_dir=/lovells/data02/arthur.elmes/S2/HLS_comparison/22WFV/L2A_HLS/
HLS_dir=/lovells/data01/arthur.elmes/HLS/sample_hls/S30/2020/22/W/F/V/
holding_dir=/lovells/data02/arthur.elmes/S2/HLS_comparison/22WFV/L2A_HLS/not_run/

if [ ! -d ${holding_dir} ]
then
    mkdir ${holding_dir}
fi

for safe in ${L2A_HLS_dir}*.SAFE
do
    # Pull of date from L2A SAFE, conv to doy
    # Also get tile (use sorting script example)
    safe=$(basename -- $safe)
    IFS="_"
    read -ra file_parts <<< "${safe}"
    date=${file_parts[2]::8}
    img_date=`date +"%Y%j" --date="${date}"`
    tile=${file_parts[5]}
    IFS=" "
    match=`find ${HLS_dir} -type f -name "HLS.S30.${tile}.${img_date}*.hdf"`
    if [ -z $match ]; then
    	echo "No match found, removing file from dir."
    	mv ${L2A_HLS_dir}${safe} ${holding_dir}
    else
    	    echo "Match is: ${match}"
    fi
done
