#!/bin/bash

in_dir=$1


for tif in $1/*.tif ; do
    tif_name=`echo $tif`
    IFS='.'
    read -ra ARR <<< $tif
    tile=${ARR[2]}
    IFS=''
    if [[ ${tile} == *"h"* ]]; then
    	if [ ! -d ./${tile} ]; then
    	    mkdir ${in_dir}/${tile}
    	fi
    	mv ${tif_name} ${in_dir}/${tile}
    fi
    
done
