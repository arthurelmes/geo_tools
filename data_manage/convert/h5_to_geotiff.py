"""
Created Apr 17 2020
@author: arthur elmes arthur.elmes@gmail.com
With significant guidance from Cole Krehbiel
Contact: LPDAAC@usgs.gov Voice: +1-866-573-3222
Organization: Land Processes Distributed Active Archive Center (LP DAAC)
Website: https://lpdaac.usgs.gov/
"""

import h5py, os, sys
import numpy as np
from osgeo import gdal, gdal_array
import datetime as dt
import pandas as pd

in_dir = "/home/arthur/data/h5_convert_dev/"
out_dir = os.path.join(in_dir, "tif")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

os.chdir(in_dir)

in_file = "VNP09GA.A2018185.h17v07.002.2020024191127.h5"
out_name = in_file.rsplit('.', 1)[0]

# Using h5py for heavy lifting
f = h5py.File(in_file)

# Create a list of the grids -- do we care about this here?
grids = list(f['HDFEOS']['GRIDS'])

# Get a list of the metadata and clean it up
# The following two lines could be combined into one
file_metadata = f['HDFEOS INFORMATION']['StructMetadata.0']
file_metadata = file_metadata[()].split()
file_metadata = [m.decode('utf-8') for m in file_metadata]

# Gather up all the h5's objects in a list
h5_objs = []
f.visit(h5_objs.append)

# List all the sdss
# The first way is way more concise, but a little mind warping at first
# so I separated it out for now
#datasets = [obj for grid in grids for obj in h5_objs if isinstance(f[obj], h5py.Dataset) and grid in obj]
datasets = []
for grid in grids:
    for obj in h5_objs:
        if isinstance(f[obj], h5py.Dataset) and grid in obj:
            datasets.append(obj)

# Such list comprehension...
r = f[[a for a in datasets if 'M5' in a][0]] #M5 is red
g = f[[a for a in datasets if 'M4' in a][0]] #M4 is green
b = f[[a for a in datasets if 'M3' in a][0]] #M3 is blue
n = f[[a for a in datasets if 'M7' in a][0]] #M7 is nir

#TODO Update this to use dataset[()] instead of dataset.value
qf1 = f[[a for a in datasets if 'QF1' in a][0]].value # Import QF1 SDS
qf7 = f[[a for a in datasets if 'QF7' in a][0]].value # Import QF7 SDS

# Unpack QA bits for aero quantity and cloud confidence

# The QA SDSs of interest both have 8 bits
bits = 8

# Populate a list with all possible values, raise 2 to the power of however many bits you specified
vals = list(range(0, (2**bits)))

# Create a list to store 'good' bit values, i.e. those that match the binary pattern we specify below
good_qf = []

for v in vals:
    bit_val = format(vals[v], 'b').zfill(bits) # converting to binary, zfill pads with 0
    # Narrow to our bit pattern of interest, for the bit numbers of interest.
    # Remember the index in the list of bit_value starts left to right as usual, but bits are
    # numbered right to left, since least significant is farthest right. So to get bits 2 and 3, as
    # defined in user guide, use index values 4:6.
    if bit_val[4:6] == '11':
        good_qf.append(vals[v])
        print('\n' + str(vals[v]) + ' = ' + str(bit_val))


# Mask the bands using the bit values defined above.
#TODO Unpacking the bit flags from the QA bands is similar maybe? Mask themselves rather than the spectral bands, then relcassify???

# Maybe this is clunky.. but this should work for a SINGLE bit value, but not yet a range
qf7_unpacked = np.ma.MaskedArray(qf7, np.in1d(qf7, good_qf, invert=True))
unique_vals = np.unique(qf7_unpacked)
for u in unique_vals:
    if u > 0:
        qf7_unpacked[qf7_unpacked == u] = 1

qf7_unpacked = np.where(qf7_unpacked == 1, 1, np.NaN)

# Get scale factor and fill value
scale_factor = r.attrs['Scale']
fill_value = r.attrs['_FillValue']

# Use the scale factor to scale all the bands to their real values
red = r[()] * scale_factor
green = g[()] * scale_factor
blue = b[()] * scale_factor
nir = n[()] * scale_factor

# For visualization, create RGB array
rgb = np.dstack((red,green,blue))
rgb[rgb == fill_value * scale_factor] = 0

# Come back to section 3b of the jupyter notebook guide to make viz, skipping for now
# And also section 4 for QA unpacking and masking
# 5 and 6 are probably less useful

# Pluck upper left corner from meta, split into lat and lon components
ul = [i for i in file_metadata if 'UpperLeftPointMtrs' in i][0]
ul_lon = float(ul.split('=(')[-1].replace(')', '').split(',')[0])
ul_lat = float(ul.split('=(')[-1].replace(')', '').split(',')[1])

# "Currently, VIIRS HDF-EOS5 files do not contain information regarding the spatial"
# resolution of the dataset within, so here set to the standard nominal resolution "
# of 1 km for this product."

y_res, x_res = -926.6254330555555,  926.6254330555555
geotransform = (ul_lon, x_res, 0, ul_lat, 0, y_res)

# I tried the proj4 string, but ONLY WKT WORKS FOR TIFS WHHYYYYY.
prj = 'PROJCS["unnamed",\
GEOGCS["Unknown datum based upon the custom spheroid", \
DATUM["Not specified (based on custom spheroid)", \
SPHEROID["Custom spheroid",6371007.181,0]], \
PRIMEM["Greenwich",0],\
UNIT["degree",0.0174532925199433]],\
PROJECTION["Sinusoidal"], \
PARAMETER["longitude_of_center",0], \
PARAMETER["false_easting",0], \
PARAMETER["false_northing",0], \
UNIT["Meter",1]]'

# This is a dictionary of all the bands to be exported. Modify this to be the wsa/bsa/qa bands for VNP43
#export_dict = {'red':{'data':red, 'band': 'M5'}, 'green':{'data':green, 'band': 'M4'},'blue':{'data':blue, 'band': 'M3'}}
export_dict = {'qf7':{'data':qf7_unpacked, 'band': 'QF7'}}


for e in export_dict:
    try:
        data = export_dict[e]['data']
        sys.exit()
        #data[data.mask == True] = fill_value
    except: AttributeError
    output_name = os.path.normpath('{}{}_{}.tif'.format(out_dir, out_name, export_dict[e]['band']))
    n_row, n_col = data.shape[0], data.shape[1]
    data_type = gdal_array.NumericTypeCodeToGDALTypeCode(data.dtype)
    driver = gdal.GetDriverByName('GTiff')

    # Left out the rgb export here, but would be interesting to revisit
    out_file = driver.Create(output_name, n_col, n_row, 1, data_type)
    band = out_file.GetRasterBand(1)
    print(data)
    band.WriteArray(data)
    band.FlushCache
    band.SetNoDataValue(float(fill_value))

    out_file.SetGeoTransform(geotransform)
    out_file.SetProjection(prj)
    out_file = None
    print('Processing: {}'.format(output_name))

    #NOTE Need to fix the output directory, but otherwise this works for VNP09 RGBN bands.
    #TODO Add CLI args to select SDSs desired, IO dirs, etc