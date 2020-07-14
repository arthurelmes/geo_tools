#!/bin/bash

dl_dir=/muddy/data05/arthur.elmes/lance
mcd43_a1_dir=$dl_dir/MCD43A1
mcd43_a2_dir=$dl_dir/MCD43A2
mcd43_a3_dir=$dl_dir/MCD43A3
mcd43_a4_dir=$dl_dir/MCD43A4
mod09_dir=$dl_dir/MOD09GA
myd09_dir=$dl_dir/MYD09GA
vnp43_a1_dir=$dl_dir/VNP43MA1
vnp43_a2_dir=$dl_dir/VNP43MA2
vnp43_a3_dir=$dl_dir/VNP43MA3
vnp43_a4_dir=$dl_dir/VNP43MA4
vnp09_dir=$dl_dir/VNP09GA

declare -a tiles=("h12v04" "h11v11" "h17v07" "h09v05" "h24v04" "h11v08")

#MODIS

# organize MCD43A1
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $mcd43_a1_dir/$tile/allData/6/MCD43A1N/Recent/ $mcd43_a1_dir/$tile/
done

# organize MCD43A2
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $mcd43_a2_dir/$tile/allData/6/MCD43A2N/Recent/ $mcd43_a2_dir/$tile/
done

# organize MCD43A3
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $mcd43_a3_dir/$tile/allData/6/MCD43A3N/Recent/ $mcd43_a3_dir/$tile/
done

# organize MCD43A4
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $mcd43_a4_dir/$tile/allData/6/MCD43A4N/Recent/ $mcd43_a4_dir/$tile/
done

# organize MOD09GA
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $mod09_dir/$tile/allData/6/MOD09GA/Recent/ $mod09_dir/$tile/
done

# organize MYD09GA
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $myd09_dir/$tile/allData/6/MYD09GA/Recent/ $myd09_dir/$tile/
done


#VIIRS

# organize VNP43A1
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $vnp43_a1_dir/$tile/allData/5000/VNP43MA1N/Recent/ $vnp43_a1_dir/$tile/
done

# organize VNP43A2
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $vnp43_a2_dir/$tile/allData/5000/VNP43MA2N/Recent/ $vnp43_a2_dir/$tile/
done

# organize VNP43A3
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $vnp43_a3_dir/$tile/allData/5000/VNP43MA3N/Recent/ $vnp43_a3_dir/$tile/
done

# organize VNP43A4
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $vnp43_a4_dir/$tile/allData/5000/VNP43MA4N/Recent/ $vnp43_a4_dir/$tile/
done

# organize VNP09GA
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $vnp09_dir/$tile/allData/5000/VNP09GA_NRT/Recent/ $vnp09_dir/$tile/
done
