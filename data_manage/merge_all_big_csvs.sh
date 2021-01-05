#!/bin/bash

tiles="h08v05 h09v04 h11v04 h11v09 h12v04 h16v02 h26v04 h30v11"
m_bands="Band1 Band2 Band3 Band4 Band5 Band6 Band7 vis nir shortwave"
v_bands="M3 M4 M5 M7 M8 M10 M11 vis nir shortwave"
product='A4'

for m_band in ${m_bands};
do    
    for tile in ${tiles};
    do   
	./merge_csvs.sh /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/MCD_VNP/${product}/${m_band}/ /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/${tile}_MCD_VNP_2019_all_with_nbar_${m_band}.csv
	./merge_csvs.sh /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/MCD_VJ1/${product}/${m_band}/ /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/${tile}_MCD_VJ1_2019_all_with_nbar_${m_band}.csv
    done
done

for v_band in ${v_bands};
do  
    for tile in ${tiles};
    do   
	./merge_csvs.sh /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/VJ1_VNP/${product}/${v_band}/ /ipswich/data02/arthur.elmes/comparo_results/csv/${tile}/${tile}_VJ1_VNP_2019_all_with_nbar_${v_band}.csv
    done
done
