#!/bin/bash

in_dir=$1 
out_dir=$2
product=$3

if [ "${product}" == "MOD21A1D" ] || [ "${product}" == "MYD21A1D" ];
then
    sds_name_0="MODIS_Grid_Daily_1km_LST21"
    nodata=0
    sds_name_lst="LST_1KM"
    sds_name_qa="QC"
fi

if [ "${product}" == "MOD21A2" ] || [ "${product}" == "MYD21A2" ];
then
    sds_name_0="MODIS_Grid_8Day_1km_LST21"
    nodata=0
    sds_name_lst="LST_Day_1KM"
    sds_name_qa="QC_Day"
fi

srs_str="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

if [ ! -d ${out_dir}/qa/ ]; then
    mkdir ${out_dir}/qa/
fi

if [ ! -d ${out_dir}/lst/ ]; then
    mkdir ${out_dir}/lst/
fi

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"

    # for lst
    gdal_translate -a_srs "${srs_str}" -a_nodata ${nodata} -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':${sds_name_0}:${sds_name_lst} ${out_dir}/lst/${filename_bare}_lst.tif

    # for qa
    gdal_translate -a_srs "${srs_str}" -a_nodata ${nodata} -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':${sds_name_0}:${sds_name_qa} ${out_dir}/qa/${filename_bare}_qa_lst.tif
done
