#!/bin/bash

# this structure isn't good -- should generalize into function to make less ambiguous

in_dir="/ipswich/data02/arthur.elmes/"
out_dir="/ipswich/data02/arthur.elmes/comparo_results/"

tiles="h09v04"

if [ ! -d "${out_dir}" ];
then
    mkdir -p ${out_dir}
fi

for tile in ${tiles};
do
    # MCD43 vs VJ143
    for h_file in ${in_dir}/VNP43MA3/${tile}/VNP43MA3*.h5; do
	# first grab the date portion to find matching file
	IFS='.'
	read -ra ARR <<< "${h_file}"
	dt=`echo "${ARR[2]}"`
	IFS=' '
	mcd_mate=`find ${in_dir}/MCD43A3/2019/${tile}/ -maxdepth 1 -type f -name MCD43A3*${dt}*`
	if [ ! -z "${mcd_mate}" ] && [ ! -z "${h_file}" ];
	then
	    python plot_two_tiles.py -d ${out_dir}/ -f1 ${mcd_mate} -f2 ${h_file}
	fi
    done

    # VNP43 vs VJ143
    for h_file in ${in_dir}/VNP43MA3/${tile}/VNP43MA3*.h5; do
	IFS='.'
	read -ra ARR <<< "${h_file}"
	dt=`echo "${ARR[2]}"`
	IFS=' '
	vj1_mate=`find ${in_dir}/VJ143MA3/2019/${tile}/ -maxdepth 1 -type f -name VJ143MA3*${dt}*`
	if [ ! -z "${vj1_mate}" ] && [ ! -z "${h_file}" ];
	then
	    python plot_two_tiles.py -d ${out_dir}/ -f1 ${vj1_mate} -f2 ${h_file}
	fi
	
    done

    # MCD43 vs VNP43
    for h_file in ${in_dir}/MCD43A3/${tile}/MCD43A3*.hdf; do
	IFS='.'
	read -ra ARR <<< "${h_file}"
	dt=`echo "${ARR[2]}"`
	IFS=' '
	vnp_mate=`find ${in_dir}/VJ143MA3/2019/${tile}/ -maxdepth 1 -type f -name VJ143MA3*${dt}*`
	if [ ! -z "${vnp_mate}" ]  && [ ! -z "${h_file}" ];
	then
	    python plot_two_tiles.py -d ${out_dir}/ -f1 ${h_file} -f2 ${vnp_mate}
	fi
    done
done
