#!/bin/bash

in_dir=$1

for hdf in ${in_dir}/*.hdf ; do
    hdf_name=`echo $hdf`
    IFS='.'
    read -ra ARR <<< $hdf
    tile=${ARR[3]}
    IFS=''
    if [[ ${tile} == *"h"* ]]; then
	if [ ! -d ${in_dir}/${tile} ]; then
    	    mkdir ${in_dir}/${tile}
    	fi
    	mv ${hdf_name} ${in_dir}/${tile}/
    fi
    
done
