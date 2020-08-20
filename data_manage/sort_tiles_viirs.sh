#!/bin/bash

in_dir=$1

for h5 in ${in_dir}/*.h5 ; do
    h5_name=`echo $h5`
    IFS='.'
    read -ra ARR <<< $h5
    tile=${ARR[3]}
    IFS=''
    if [[ ${tile} == *"h"* ]]; then
	if [ ! -d ${in_dir}/${tile} ]; then
    	    mkdir ${in_dir}/${tile}
    	fi
    	mv ${h5_name} ${in_dir}/${tile}/
    fi
    
done
