#!/bin/bash

start_date=$1
end_date=$2
tile=$3
out_dir=$4

# call /home/arthur.elmes/code/geo_tools/download/modis_viirs/download_viirs_modis.sh -s -e -n -t -d

# AOD (need to test that the script will work, because these are global, so no tile would be
# passed in -- maybe just leave that arg empty

# SZA
# /home/arthur.elmes/code/geo_tools/download/modis_viirs/download_viirs_modis.sh -s ${start_date} -e ${end_date} -n MCD43A2 -t ${tile} -d ${out_dir}

# MCD43A1
# /home/arthur.elmes/code/geo_tools/download/modis_viirs/download_viirs_modis.sh -s ${start_date} -e ${end_date} -n MCD43A1 -t ${tile} -d ${out_dir}
