#!/bin/bash

in_dir=$1

for dir in ${in_dir}/*
do
    base=$(basename "$dir")
    echo "Compressing ${base}..."
    tar -czfv "${in_dir}/${base}.tar.gz" "$dir"
done
