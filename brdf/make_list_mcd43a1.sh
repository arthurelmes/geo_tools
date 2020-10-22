#!/bin/bash

tiles="h15v02 h15v03 h16v00 h16v01 h16v02 h17v00 h17v01 h17v02"
workspace="/lovells/data02/arthur.elmes/greenland/MCD43A1/"

for tile in $tiles; do
    if [ -f ${workspace}/mcd43a1_${tile}_list.txt ]; then
	rm ${workspace}/mcd43a1_${tile}_list.txt
    fi
    
    for year in $(seq 2020 2020); do
	find ${workspace}/${year}/${tile}/ -type f -name "*.hdf"  -printf "%f\n" >> ${workspace}/mcd43a1_${tile}_list.txt
    done
done

