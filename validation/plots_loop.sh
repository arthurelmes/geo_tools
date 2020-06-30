#!/bin/bash
file_dir="/lovells/data02/arthur.elmes/j1_viirs/make_plot_two_tiles/h12v04"

# MCD43 vs VJ143
#python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020070.h12v04.001.2020078082637.h5 -f2 VJ143MA3.A2020070.h12v04.002.h5

for h_file in ${file_dir}/VNP43MA3*.h5; do
    IFS='.'
    read -ra ARR <<< "${h_file}"
    dt=`echo "${ARR[2]}"`
    IFS=' '

    mcd_mate=`find ${file_dir} -maxdepth 1 -type f -name MCD43A3*${dt}*`

    h_file_base="$(basename -- ${h_file})"
    mcd_mate_base="$(basename -- ${mcd_mate})"
    #echo $file_dir
    echo $h_file_base
    echo $mcd_mate_base
    #python plot_two_tiles.py -d ${file_dir}/ -f1 ${mcd_mate_base} -f2 ${h_file_base}
    
done

# VNP43 vs VJ143
#python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020070.h12v04.001.2020078082637.h5 -f2 VJ143MA3.A2020070.h12v04.002.h5

for h_file in ${file_dir}/VNP43MA3*.h5; do
    IFS='.'
    read -ra ARR <<< "${h_file}"
    dt=`echo "${ARR[2]}"`
    IFS=' '

    vj1_mate=`find ${file_dir} -maxdepth 1 -type f -name VJ143MA3*${dt}*`

    h_file_base="$(basename -- ${h_file})"
    vj1_mate_base="$(basename -- ${vj1_mate})"
    #echo $file_dir
    echo $h_file_base
    echo $vj1_mate_base
    #python plot_two_tiles.py -d ${file_dir}/ -f1 ${vj1_mate_base} -f2 ${h_file_base}
    
done

# MCD43 vs VNP43
#python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020070.h12v04.001.2020078082637.h5 -f2 VJ143MA3.A2020070.h12v04.002.h5

for h_file in ${file_dir}/MCD43A3*.hdf; do
    IFS='.'
    read -ra ARR <<< "${h_file}"
    dt=`echo "${ARR[2]}"`
    IFS=' '

    vnp_mate=`find ${file_dir} -maxdepth 1 -type f -name VJ143MA3*${dt}*`

    h_file_base="$(basename -- ${h_file})"
    vnp_mate_base="$(basename -- ${vnp_mate})"
    #echo $file_dir
    echo $h_file_base
    echo $vnp_mate_base

    python plot_two_tiles.py -d ${file_dir}/ -f1 ${h_file_base} -f2 ${vnp_mate_base}
    
done
