#!/bin/bash

in_dir=$1

for filename in ${in_dir}/*.tar.gz
do
    tar zvxf $filename
done
