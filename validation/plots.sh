#!/bin/bash
file_dir="/lovells/data02/arthur.elmes/j1_viirs/make_plot_two_tiles"

python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020070.h12v04.001.2020078082637.h5 -f2 VJ143MA3.A2020070.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020080.h12v04.001.2020114050010.h5 -f2 VJ143MA3.A2020080.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020090.h12v04.001.2020120191037.h5 -f2 VJ143MA3.A2020090.h12v04.002.h5
python plot_two_tiles.py -d ${file_dir}/h12v04 -f1 VNP43MA3.A2020100.h12v04.001.2020122190946.h5 -f2 VJ143MA3.A2020100.h12v04.002.h5

python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020070.h16v01.001.2020078084615.h5  -f2 VJ143MA3.A2020070.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020080.h16v01.001.2020114150644.h5  -f2 VJ143MA3.A2020080.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020090.h16v01.001.2020121044822.h5  -f2 VJ143MA3.A2020090.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020100.h16v01.001.2020122213708.h5  -f2 VJ143MA3.A2020100.h16v01.002.h5
python plot_two_tiles.py -d ${file_dir}/h16v01 -f1 VNP43MA3.A2020110.h16v01.001.2020123063830.h5  -f2 VJ143MA3.A2020110.h16v01.002.h5
