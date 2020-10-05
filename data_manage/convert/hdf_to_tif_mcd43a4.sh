#!/bin/bash

in_dir=$1 
out_dir=$2

srs_str="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

if [ ! -d ${out_dir}/qa/ ]; then
    mkdir ${out_dir}/qa/
fi

if [ ! -d ${out_dir}/nbar/ ]; then
    mkdir ${out_dir}/nbar/
fi

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"

    # for nbar
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band1 ${out_dir}/nbar/${filename_bare}_nbar_b1.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band2 ${out_dir}/nbar/${filename_bare}_nbar_b2.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band3 ${out_dir}/nbar/${filename_bare}_nbar_b3.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band4 ${out_dir}/nbar/${filename_bare}_nbar_b4.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band5 ${out_dir}/nbar/${filename_bare}_nbar_b5.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band6 ${out_dir}/nbar/${filename_bare}_nbar_b6.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 32767 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Nadir_Reflectance_Band7 ${out_dir}/nbar/${filename_bare}_nbar_b7.tif

    # for qa
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band1 ${out_dir}/qa/${filename_bare}_qa_b1.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band2 ${out_dir}/qa/${filename_bare}_qa_b2.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band3 ${out_dir}/qa/${filename_bare}_qa_b3.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band4 ${out_dir}/qa/${filename_bare}_qa_b4.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band5 ${out_dir}/qa/${filename_bare}_qa_b5.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band6 ${out_dir}/qa/${filename_bare}_qa_b6.tif
    gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_Band7 ${out_dir}/qa/${filename_bare}_qa_b7.tif

    # gdal_translate -a_srs "${srs_str}" -a_nodata 255 -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/qa/${filename_bare}_qa_shortwave.tif


done
