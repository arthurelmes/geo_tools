#!/bin/bash

# This masks input TIF mcd43 files with the TIF version of the mandatory qa, max value only (qa==0).
# Should be improved in many ways, e.g. specify more than qa==0, intake the HDFs, etc
# Author: Arthur Elmes 2020-08-01

tile=$1
start_year=$2
end_year=$3
in_dir=$4 #"/ipswich/data01/arthur.elmes/bsky/tif/${tile}_2020/"
qa_dir=$5 #"/lovells/data02/arthur.elmes/greenland/MCD43A1/tif/${tile}"
sza_dir=$6 #"/ipswich/data01/arthur.elmes/MCD43A2/all/${tile}"
out_dir=$7 #"/ipswich/data01/arthur.elmes/bsky/tif/qa_screened/"

if [ ! -d ${out_dir} ]; then
    mkdir $out_dir
fi

rm ${in_dir}*temp*

for year in $(seq ${start_year} ${end_year}); do    
    for tif in ${in_dir}/*A${year}*.tif; do 
	filename=$(basename -- ${tif})
	extension="${filename##*.}"
	filename_bare="${filename%.*}"
	date=${filename_bare:9:14}
	tmp_name=${tif}_temp.tif
	tmp_name_2=${tif}_temp2.tif
	tmp_name_3=${tif}_temp3.tif
	out_name=${out_dir}/${filename_bare}_high_qa.tif

	# Find matching qa file
	qa_tif=`find ${qa_dir} -type f -name "*${date}*qa*"`

	# Find previously extracted SZA file
	sza_tif=`find ${sza_dir} -type f -name "*${date}*sza*"`
	
	# This could probably be one step
	echo "Procesing:"
	echo $tif
	echo $qa_tif
	echo $sza_tif

	gdal_calc.py --format GTiff -A ${tif} -B ${qa_tif} --outfile=${tmp_name} --calc="A*(B==0)" --NoDataValue=0 --quiet 
	gdal_calc.py --format GTiff -A ${tmp_name} --outfile=${tmp_name_2} --calc="A*(A>0)" --NoDataValue=32767 --quiet 
	gdal_calc.py --format GTiff -A ${tmp_name_2} -B ${sza_tif} --outfile=${tmp_name_3} --calc="A*(B<72.0)" --NoDataValue=0 --quiet
	gdal_calc.py --format GTiff -A ${tmp_name_3} --outfile=${out_name} --calc="A*(A>0)" --NoDataValue=32767 --quiet

	# delete the temporary tifs (this is a wonky way of doing it, but VRT is not supported for the CLI gdal_calc.py)
	if [ -f ${tmp_name} ]; then
	    rm ${tmp_name}
	fi
	if [ -f ${tmp_name_2} ]; then
	    rm ${tmp_name_2}
	fi
	if [ -f ${tmp_name_3} ]; then
	    rm ${tmp_name_3}
	fi
    done
done
