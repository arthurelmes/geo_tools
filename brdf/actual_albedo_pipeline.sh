#!/bin/bash

aod_tbl="/home/arthur/Dropbox/projects/greenland/blue_sky_variables/AOD/AOD_h15v03_wgs84_stats.csv"
sza_tbl="/home/arthur/Dropbox/projects/greenland/blue_sky_variables/SZA/SZA_h15v03_stats.csv"
mcd43a1_tbl="/home/arthur/Dropbox/projects/greenland/blue_sky_variables/MCD43A1/2020/2020_all_h15v03.csv"

date="01/10/2020"
echo $date

awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $aod_tbl
awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $sza_tbl
awk -v date_a="$date" -F "," '$0~date_a { print $3 "\t" }' $mcd43a1_tbl
