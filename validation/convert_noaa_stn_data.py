'''Convert NOAA/ESRL/GMD/GRAD Radiation Archive .dat files into nicely formatted .csv
Author: Arthur ELmes
Date: 2020-05-27'''

import os, glob

workspace = '/home/arthur/Dropbox/projects/greenland/station_data/noaa_summit_data'
os.chdir(workspace)

dat_file_names = glob.glob('*.dat')

# For now, headers are hard coded, since they're always the same for the files I care about, and are otherwise
# annoyingly messy to automatically extract
# headers = content[:4]
headers = 'Year,Mn,Dy,Hr,Mi,D_GLOBAL,D_IR,U_GLOBAL,U_IR,Zenith\n'

csv_name_all = 'noaa_summit_all.csv'
csv_out_all = open(csv_name_all, 'w')
csv_out_all.write(headers)

for dat_file_name in dat_file_names:
    with open(dat_file_name) as dat_file:
        lines = dat_file.readlines()

    # Remove trailing/leading blank spaces
    content = [x.strip() for x in lines]

    # This removes the headers, which take up the top 0:4 lines and are very messy (multi-line interleved. whyyyy?)
    content = content[4:]

    # Read the contents line at a time and replace empty space with commas for easier ingestion
    csv_name = dat_file_name + '.csv'
    csv_out = open(csv_name, 'w')
    csv_out.write(headers)
    for line in content:
        line_parts = line.split(' ')
        new_line = ''
        for part in line_parts:
            if part == '':
                new_line = new_line
            else:
                new_line = new_line + str(part) + ','
        new_line = new_line[:-1] + '\n'
        csv_out.write(new_line)
        csv_out_all.write(new_line)
    csv_out.close()

csv_out_all.close()

