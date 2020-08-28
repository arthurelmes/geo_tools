#!/bin/bash

# Credit: user Hastur, https://stackoverflow.com/questions/24641948/merging-csv-files-appending-instead-of-merging

in_dir=$1
out_file_name=$2      # Fix the output name
i=0                                       # Reset a counter
for filename in ${in_dir}/*.csv; do 
 if [ "$filename"  != "$out_file_name" ] ;      # Avoid recursion 
 then 
   if [[ $i -eq 0 ]] ; then 
      head -1  "$filename" >   "$out_file_name" # Copy header if it is the first file
   fi
   tail -n +2  "$filename" >>  "$out_file_name" # Append from the 2nd line each file
   i=$(( $i + 1 ))                            # Increase the counter
 fi
done
