#!/bin/bash

in_dir=$1

# loop over all h5 files in input dir
# use unpack_sds_bits to get the aerosol bits 2-3 from SurfReflect_QF7
# and cloud bits 2-3 from SurfRefelct_QF1
# e.g.:

for  h5 in ${in_dir}/*.h5;
do
    aero_dir=${in_dir}/aero
    cloud_dir=${in_dir}/cloud
    if [ ! -d ${aero_dir} ]; then
	mkdir ${aero_dir}
    fi
    if [ ! -d ${cloud_dir} ]; then
	mkdir ${cloud_dir} 
    fi
			    
    h5_name=$(basename ${h5})
    unpack_sds_bits -of=${aero_dir}/${h5_name}_aero_quant.tif ${h5} -sds="SurfReflect_QF7_1" -bn=2-3 ${h5}
    unpack_sds_bits -of=${cloud_dir}/${h5_name}_cloud_conf.tif -sds="SurfReflect_QF1_1" -bn=2-3 ${h5}

done


