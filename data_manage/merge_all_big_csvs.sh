#!/bin/bash

tiles="h08v05 h09v04 h11v04 h11v09 h12v04 h16v02 h26v04 h30v11"

for tile in ${tiles};
do   
    ./merge_csvs.sh /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/VJ1_VNP/ /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/${tile}_VJ1_VNP_2019_all.csv
    ./merge_csvs.sh /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/MCD_VNP/ /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/${tile}_MCD_VNP_2019_all.csv
    ./merge_csvs.sh /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/MCD_VJ1/ /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/${tile}_MCD_VJ1_2019_all.csv

done

