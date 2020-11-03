#!/bin/bash

in_dir="/ipswich/data01/arthur.elmes/bsky/tif/qa_screened_merged/test/"
out_dir="/ipswich/data01/arthur.elmes/bsky/tif/qa_screened_merged/test/samesize/"

if [ ! -d "${out_dir}" ];
then
    mkdir -p ${out_dir}
fi

for tif in ${in_dir}/*.tif;
do
    gdalinfo ${tif} > temp.txt
    img_size=`grep "Size is" temp.txt`
    if [[ "$img_size" == *"7200, 9600"* ]];
    then
	new_tif=$(basename "${tif}")
	cp ${tif} ${out_dir}/${new_tif}
    fi
    
done
