#!/bin/bash

# This masks input TIF mcd43 files with the TIF version of the mandatory qa, max value only
# Should be improved in many ways, e.g. specify more than qa=0, intake the HDFs, etc
# Author: Arthur Elmes 2020-08-01

# Set these
in_dir="/media/arthur/Windows/LinuxShare/screen_qa/bluesky/"
qa_dir="/media/arthur/Windows/LinuxShare/screen_qa/qa/"
sza_dir="/media/arthur/Windows/LinuxShare/screen_qa/sza/"
out_dir="/media/arthur/Windows/LinuxShare/screen_qa/bluesky_screened/"

for tif in ${in_dir}/*.tif; do 
    filename=$(basename -- ${tif})
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    date=${filename_bare:9:14}
    tmp_name=${tif}.vrt
    out_name=${out_dir}/${filename_bare}_high_qa.tif

    # Find matching qa file
    qa_tif=`find ${qa_dir} -type f -name "*${date}*qa*"`

    # Find previously extracted SZA file
    sza_tif=`find ${sza_dir} -type f -name "*${date}*sza*"`
    
    # This could probably be one step
    gdal_calc.py -A ${tif} -B ${qa_tif} --outfile=${tmp_name} --calc="A*(B==0)"
    gdal_calc.py -A ${tmp_name} --outfile=${tmp_name} --calc="A*(A>0)" --NoDataValue=0
    gdal_calc.py -A ${tmp_name} -B ${sza_tif} --outfile=${out_name} --calc="A*(B<72.0)"

done
