#!/bin/bash

# This masks input TIF mcd43 files with the TIF version of the mandatory qa, max value only (qa==0).
# Should be improved in many ways, e.g. specify more than qa==0, intake the HDFs, etc
# Author: Arthur Elmes 2020-08-01

start_year=$1
end_year=$2
in_dir=$3
qa_dir=$4
out_dir=$5
if [ ! -d ${out_dir} ]; then
    mkdir $out_dir
fi

rm ${in_dir}*temp*

for year in $(seq ${start_year} ${end_year}); do    
    for tif in ${in_dir}/*A${year}*.tif; do 
	filename=$(basename -- ${tif})
	extension="${filename##*.}"
	filename_bare="${filename%.*}"
	date=${filename_bare:9:8}
	tmp_name=${tif}_temp.tif
	out_name=${out_dir}/${filename_bare}_high_qa.tif

	# Find matching qa file
	qa_tif=`find ${qa_dir} -type f -name "*${date}*.tif"`

	# This could probably be one step
	echo "Procesing:"
	echo $tif
	echo $qa_tif

	gdal_calc.py --format GTiff -A ${tif} -B ${qa_tif} --outfile=${tmp_name} --calc="A*(B==0)" --NoDataValue=0 --quiet 
	gdal_calc.py --format GTiff -A ${tmp_name} --outfile=${out_name} --calc="A*(A>0)" --NoDataValue=32767 --quiet 

	# delete the temporary tifs (this is a wonky way of doing it, but VRT is not supported for the CLI gdal_calc.py)
	if [ -f ${tmp_name} ]; then
	    rm ${tmp_name}
	fi
    done
done
