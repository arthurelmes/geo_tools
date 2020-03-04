#!/bin/bash

for dir in */
do
    base=$(basename "$dir")
    echo "Compressing ${base}..."
    tar -czf "${base}.tar.gz" "$dir"
done
