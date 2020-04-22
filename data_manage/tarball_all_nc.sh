#!/bin/bash

in_dir=$1

for nc in ${in_dir}/*.nc
do
    base=$(basename "$nc")
    echo "Compressing ${base}..."
    tar czfv ${in_dir}/${base}.tar.gz -C ${in_dir} ${base}
done
