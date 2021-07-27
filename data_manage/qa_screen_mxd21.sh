#!/bin/bash

# This masks input TIF mcd43 files with the TIF version of the mandatory qa, max value only
# Should be improved in many ways, e.g. specify more than qa=0, intake the HDFs, etc
# Author: Arthur Elmes 2020-08-01

in_dir=$1
qa_dir=$2
out_dir=$3
product=$4

# for MxD21A1D products, 40960 is lowest value for good perf in emis and lst retrieval 
if [ "${product}" == "MOD21A1D" ] || [ "${product}" == "MYD21A1D" ];
then
    qa_clear_value=40960
fi

# for MxD21A2 8Day products, >= 176 is good quality
if [ "${product}" == "MOD21A2" ] || [ "${product}" == "MYD21A2" ];
then
    qa_clear_value=176
fi
 
if [ ! -d ${out_dir} ]; then
    mkdir $out_dir
fi

for tif in ${in_dir}/*.tif; do
    filename=$(basename -- ${tif})
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    # band=`echo "${filename_bare}" | tail -c 4`
    date=`echo ${filename_bare} | awk -F . '{print $2}' | awk -F 'A' '{print $2}'`
    tmp_name_0=${tif}_temp0.tif
    tmp_name_1=${tif}_temp1.tif
    out_name=${out_dir}/${filename_bare}_high_qa.tif
    
    # Find matching qa file
    qa_tif=`find ${qa_dir} -type f -name "*A${date}*qa*"`
    # This could probably be one step
    # for debug
    # echo "Procesing:"
    # echo $tif
    # echo $tmp_name_0
    # echo $tmp_name_1
    # echo $qa_tif
    
    # first make a boolean mask; check this qa value -- probably there are others that should be let through also
    gdal_calc.py --format GTiff -A ${qa_tif} --outfile=${tmp_name_0} --calc="(A>=${qa_clear_value})" --quiet

    # get rid of poor qa pixels; 0.02 is the scaling factor for this product
    gdal_calc.py --format GTiff -A ${tif} -B ${tmp_name_0} --outfile=${tmp_name_1} --calc="A*B*0.02" --NoDataValue=0 --quiet

    # finish up by setting correct data range and nodata value
    gdal_calc.py --format GTiff -A ${tmp_name_1} --outfile=${out_name} --calc="A*(A>0)" --NoDataValue=32767 --quiet
    
    # vrt format is not implemented for gdal_calc, so delete the temporary tifs (this is super non-optimal)
    if [ -f ${tmp_name_0} ]; then
	rm ${tmp_name_0}
    fi
    if [ -f ${tmp_name_1} ]; then
	rm ${tmp_name_1}
    fi    
done

