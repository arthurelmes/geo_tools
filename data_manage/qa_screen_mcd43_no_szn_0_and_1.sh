#!/bin/bash

# This masks input TIF mcd43 files with the TIF version of the mandatory qa, max value only
# Should be improved in many ways, e.g. specify more than qa=0, intake the HDFs, etc
# Author: Arthur Elmes 2020-08-01

tile=$1
start_year=$2
end_year=$3

# Set these
in_dir="/lovells/data02/arthur.elmes/greenland/VNP43MA3/2019/tif/wsa/${tile}/"
qa_dir="/lovells/data02/arthur.elmes/greenland/VNP43MA3/2019/tif/qa/${tile}"
out_dir="/lovells/data02/arthur.elmes/greenland/VNP43MA3/2019/tif/wsa_qa_lite_screened/"

if [ ! -d ${out_dir} ]; then
    mkdir $out_dir
fi

for year in $(seq ${start_year} ${end_year}); do    
    for tif in ${in_dir}/*A${year}*.tif; do 
	filename=$(basename -- ${tif})
	extension="${filename##*.}"
	filename_bare="${filename%.*}"
	date=${filename_bare:9:14}
	tmp_name=${tif}_temp.tif
	out_name=${out_dir}/${filename_bare}_0_or_1_qa.tif

	# Find matching qa file
	qa_tif=`find ${qa_dir} -type f -name "*${date}*qa*"`

	# This could probably be one step
	echo "Procesing:"
	echo $tif
	echo $qa_tif
	echo $sza_tif
	
	gdal_calc.py --format GTiff -A ${tif} -B ${qa_tif} --outfile=${tmp_name} --calc="A*logical_or(B==0,B==1)" --NoDataValue=0 --quiet
	gdal_calc.py --format GTiff -A ${tmp_name} --outfile=${out_name} --calc="A*(A>0)" --NoDataValue=32767 --quiet

	# For some reason the vrt format is not working, so delete the temporary tifs (this is super non-optimal)
	if [ -f ${tmp_name} ]; then
	    rm ${tmp_name}
	fi
    done
done
