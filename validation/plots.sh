#!/bin/bash
file_dir="/lovells/data02/arthur.elmes/j1_viirs/make_plot_two_tiles"

# VNP43 vs VJ143
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020070.h12v04.001.2020078082637.h5 -f2 VJ143MA3.A2020070.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020080.h12v04.001.2020114050010.h5 -f2 VJ143MA3.A2020080.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020090.h12v04.001.2020120191037.h5 -f2 VJ143MA3.A2020090.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020100.h12v04.001.2020122190946.h5 -f2 VJ143MA3.A2020100.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020110.h12v04.001.2020078082637.h5 -f2 VJ143MA3.A2020110.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020120.h12v04.001.2020128120805.h5 -f2 VJ143MA3.A2020120.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020130.h12v04.001.2020138082725.h5 -f2 VJ143MA3.A2020130.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020140.h12v04.001.2020148092439.h5 -f2 VJ143MA3.A2020140.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020150.h12v04.001.2020158100142.h5 -f2 VJ143MA3.A2020150.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020160.h12v04.001.2020168100557.h5 -f2 VJ143MA3.A2020160.h12v04.002.h5


python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020070.h16v01.001.2020078084615.h5  -f2 VJ143MA3.A2020070.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020080.h16v01.001.2020114150644.h5  -f2 VJ143MA3.A2020080.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020090.h16v01.001.2020121044822.h5  -f2 VJ143MA3.A2020090.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020100.h16v01.001.2020122213708.h5  -f2 VJ143MA3.A2020100.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020110.h16v01.001.2020123063830.h5  -f2 VJ143MA3.A2020110.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020120.h16v01.001.2020128125024.h5  -f2 VJ143MA3.A2020120.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020130.h16v01.001.2020138092239.h5  -f2 VJ143MA3.A2020130.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020140.h16v01.001.2020148100441.h5  -f2 VJ143MA3.A2020140.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020150.h16v01.001.2020158105629.h5  -f2 VJ143MA3.A2020150.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020160.h16v01.001.2020168105341.h5  -f2 VJ143MA3.A2020160.h16v01.002.h5


# MCD43 vs VJ143
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020070.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020080.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020090.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020100.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020110.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020120.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020130.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020140.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020150.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020160.h12v04.002.h5


python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020070.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020080.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020090.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020100.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020110.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020120.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020130.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020140.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020150.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1   -f2 VJ143MA3.A2020160.h16v01.002.h5


# MCD43 vs VJ143
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020070.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020080.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020090.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020100.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020110.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020120.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020130.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020140.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020150.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1  -f2 VJ143MA3.A2020160.h12v04.002.h5


python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020070.h16v01.001.2020078084615.h5  -f2 VJ143MA3.A2020070.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020080.h16v01.001.2020114150644.h5  -f2 VJ143MA3.A2020080.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020090.h16v01.001.2020121044822.h5  -f2 VJ143MA3.A2020090.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020100.h16v01.001.2020122213708.h5  -f2 VJ143MA3.A2020100.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020110.h16v01.001.2020123063830.h5  -f2 VJ143MA3.A2020110.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020120.h16v01.001.2020128125024.h5  -f2 VJ143MA3.A2020120.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020130.h16v01.001.2020138092239.h5  -f2 VJ143MA3.A2020130.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020140.h16v01.001.2020148100441.h5  -f2 VJ143MA3.A2020140.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020150.h16v01.001.2020158105629.h5  -f2 VJ143MA3.A2020150.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020160.h16v01.001.2020168105341.h5  -f2 VJ143MA3.A2020160.h16v01.002.h5



