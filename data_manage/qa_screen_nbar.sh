#!/bin/bash

# This masks input TIF mcd43 files with the TIF version of the mandatory qa, max value only
# Should be improved in many ways, e.g. specify more than qa=0, intake the HDFs, etc
# Author: Arthur Elmes 2020-08-01

# Set these
# in_dir="/media/arthur/linux_data/compare_MCD_VNP_VJ1/MCD43/nbar/"
# qa_dir="/media/arthur/linux_data/compare_MCD_VNP_VJ1/MCD43/qa/"
# out_dir="/media/arthur/linux_data/compare_MCD_VNP_VJ1/MCD43/nbar_screened/"
in_dir=$1
qa_dir=$2
out_dir=$3

if [ ! -d ${out_dir} ]; then
    mkdir $out_dir
fi

for tif in ${in_dir}/*.tif; do 
    filename=$(basename -- ${tif})
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    date=${filename_bare:9:15}
    IFS="_"
    read -ra tif_parts <<< ${filename_bare}
    band=${tif_parts[2]}
    IFS=" "
    
    # temp processing files
    tmp_name=${tif}_temp.tif
    tmp_name_2=${tif}_temp2.tif
    out_name=${out_dir}/${filename_bare}_high_qa.tif

    # Find matching qa file
    qa_tif=`find ${qa_dir} -type f -name "*${date}*qa*${band}.tif"`

    # This could probably be one step
    echo "Procesing:"
    echo $tif
    # echo $qa_tif
    # echo $date
    # echo $band
    # echo $qa_tif
    
    gdal_calc.py --format GTiff -A ${tif} -B ${qa_tif} --outfile=${tmp_name} --calc="A*(B==0)" --NoDataValue=0 --quiet
    gdal_calc.py --format GTiff -A ${tmp_name} --outfile=${out_name} --calc="A*(A>0)" --NoDataValue=0 --quiet
    #gdal_translate -of GTiff -a_nodata 0 ${tmp_name_2} ${out_name}
    
    # For some reason the vrt format is not working, so delete the temporary tifs (this is super non-optimal)
    if [ -f ${tmp_name} ]; then
	rm ${tmp_name}
    fi
    if [ -f ${tmp_name_2} ]; then
	rm ${tmp_name_2}
    fi
done
