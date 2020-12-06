"""This script will quickly make RGB and NIR composites of MCD43/VNP43/VJ143
Author: Arthur Elmes
Date: 2020-12-04

Great tips here:
https://lpdaac.usgs.gov/resources/e-learning/working-daily-nasa-viirs-surface-reflectance-data/"""

import h5py
import pyhdf
import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, gdal_array
import datetime as dt
import pandas as pd
from skimage import exposure
import sys
from pyhdf.SD import SD, SDC
import pprint

# set up workspace
workspace = '/home/arthur/Dropbox/projects/modis_viirs_continuity/sensor_intercompare/'
out_dir = os.path.join(workspace, 'output')
os.chdir(workspace)

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

# vnp_file = 'VNP43MA4.A2019150.h08v05.002.2020296231330.h5'
# mcd_file = 'MCD43A4.A2019150.h08v05.061.2020298033853.hdf'
img_file = 'MCD43A4.A2019150.h08v05.061.2020298033853.hdf'


def vnp(vnp_file):
    # get date in a nice print-able format
    yeardoy = vnp_file.split('.')[1][1:]
    date = dt.datetime.strptime(yeardoy, '%Y%j').strftime('%m/%d/%Y')

    h5 = h5py.File(vnp_file)
    # print(list(h5.keys()))

    # List contents of GRIDS directory
    grids = list(h5['HDFEOS']['GRIDS'])

    # add all objects in the h5 to a list
    h5_objs = []
    h5.visit(h5_objs.append)

    # get a list of all datasets. lol I did not do this double list comp.
    all_datasets = [obj for grid in grids for obj in h5_objs if isinstance(h5[obj], h5py.Dataset) and grid in obj]

    # assign the bands -- this is a less exact but more pythonic approach
    # r = h5[[a for a in all_datasets if 'M5' in a][0]]  # M5 = Red
    # g = h5[[a for a in all_datasets if 'M4' in a][0]]  # M4 = Green
    # b = h5[[a for a in all_datasets if 'M3' in a][0]]  # M3 = Blue
    # n = h5[[a for a in all_datasets if 'M7' in a][0]]  # M7  = NIR

    # This is a simpler but more hard-coded way
    r = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['Nadir_Reflectance_M5']
    g = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['Nadir_Reflectance_M4']
    b = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['Nadir_Reflectance_M3']
    n = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['Nadir_Reflectance_M7']

    # QA bands
    r_q = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['BRDF_Albedo_Band_Mandatory_Quality_M5']
    g_q = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['BRDF_Albedo_Band_Mandatory_Quality_M4']
    b_q = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['BRDF_Albedo_Band_Mandatory_Quality_M3']
    n_q = h5['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields']['BRDF_Albedo_Band_Mandatory_Quality_M7']

    bits = 8                          # Define number of bits
    vals = list(range(0, (2**bits)))  # Generate a list of all possible bit values
    goodQF = []                       # Create an empty list used to store bit values where bits 4-7 = 0

    for v in vals:
        bitVal = format(vals[v], 'b').zfill(bits)  # Convert to binary based on values and # of bits defined above:
        if bitVal[0:8] == '00000000':  # Keep if all bits = 0
            goodQF.append(vals[v])     # Append to list
            print('\n' + str(vals[v]) + ' = ' + str(bitVal))  # print good quality values

    # List attributes
    # print(list(r.attrs))
    # For some reason, there is no scale_factor stored in the H5 files
    scale_factor = 0.0001 #r.attrs['scaleFactor'][0]
    fill_value = r.attrs['_FillValue'][0]

    red = r[()] * scale_factor
    green = g[()] * scale_factor
    blue = b[()] * scale_factor
    nir = n[()] * scale_factor

    # Check that this is working -- on test scene I can't tell if QA mask is applied correctly
    red = np.ma.MaskedArray(red, np.in1d(r_q, goodQF, invert=True))
    green = np.ma.MaskedArray(green, np.in1d(g_q, goodQF, invert=True))
    blue = np.ma.MaskedArray(blue, np.in1d(b_q, goodQF, invert=True))
    nir = np.ma.MaskedArray(nir, np.in1d(n_q, goodQF, invert=True))

    rgb = np.dstack((red, green, blue))  # Create RGB array
    rgb[rgb == fill_value * scale_factor] = 0  # Set fill value equal to 0

    return rgb


def mcd(mcd_file):
    # get date in a nice print-able format
    yeardoy = mcd_file.split('.')[1][1:]
    date = dt.datetime.strptime(yeardoy, '%Y%j').strftime('%m/%d/%Y')

    hdf_ds = SD(mcd_file, SDC.READ)
    # print(hdf_ds.info())

    # datasets_dict = hdf_ds.datasets()
    # for idx, sds in enumerate(datasets_dict.keys()):
    #     print(idx, sds)

    # This reads in the SDSs by name, and converts them
    # to numpy arrays. Get data and QA bands.
    r_3d = hdf_ds.select("Nadir_Reflectance_Band1")
    n_3d = hdf_ds.select("Nadir_Reflectance_Band2")
    b_3d = hdf_ds.select("Nadir_Reflectance_Band3")
    g_3d = hdf_ds.select("Nadir_Reflectance_Band4")
    r_q_3d = hdf_ds.select("BRDF_Albedo_Band_Mandatory_Quality_Band1")
    n_q_3d = hdf_ds.select("BRDF_Albedo_Band_Mandatory_Quality_Band2")
    b_q_3d = hdf_ds.select("BRDF_Albedo_Band_Mandatory_Quality_Band3")
    g_q_3d = hdf_ds.select("BRDF_Albedo_Band_Mandatory_Quality_Band4")
    r = r_3d[:, :]
    n = n_3d[:, :]
    b = b_3d[:, :]
    g = g_3d[:, :]
    r_q = r_3d[:, :]
    n_q = n_3d[:, :]
    b_q = b_3d[:, :]
    g_q = g_3d[:, :]

    # DEV: check attr
    # pprint.pprint(r_3d.attributes())

    scale_factor = 0
    fill_value = 0
    # Get scale factor and fill value
    for key, value in r_3d.attributes().items():
        if key == 'scale_factor':
            scale_factor = value
        if key == '_FillValue':
            fill_value = value


    bits = 8                          # Define number of bits
    vals = list(range(0, (2**bits)))  # Generate a list of all possible bit values
    goodQF = []                       # Create an empty list used to store bit values where bits 4-7 = 0

    for v in vals:
        bitVal = format(vals[v], 'b').zfill(bits)  # Convert to binary based on values and # of bits defined above:
        if bitVal[0:8] == '00000000':  # Keep if all bits = 0
            goodQF.append(vals[v])     # Append to list
            print('\n' + str(vals[v]) + ' = ' + str(bitVal))  # print good quality values


    red = r * scale_factor
    green = g * scale_factor
    blue = b * scale_factor
    nir = n * scale_factor

    # Check that this is working -- on test scene I can't tell if QA mask is applied correctly
    red = np.ma.MaskedArray(red, np.in1d(r_q, goodQF, invert=True))
    green = np.ma.MaskedArray(green, np.in1d(g_q, goodQF, invert=True))
    blue = np.ma.MaskedArray(blue, np.in1d(b_q, goodQF, invert=True))
    nir = np.ma.MaskedArray(nir, np.in1d(n_q, goodQF, invert=True))

    rgb = np.dstack((red, green, blue))  # Create RGB array
    rgb[rgb == fill_value * scale_factor] = 0  # Set fill value equal to 0

    return rgb


def img_2_numpy(img):
    if 'MCD' in img:
        rgb = mcd(img)
    elif 'VNP' in img or 'VJ1' in img:
        rgb = vnp(img)
    else:
        print("This file isn't MCD or VNP or VJ1! Exiting.")
        sys.exit(1)

    return rgb


rgb = img_2_numpy(img_file)

p2, p98 = np.percentile(rgb, (2, 98))  # Calculate 2nd,98th percentile for updating min/max vals
rgbStretched = exposure.rescale_intensity(rgb, in_range=(p2, p98))  # Perform contrast stretch on RGB range
rgbStretched = exposure.adjust_gamma(rgbStretched, 0.5)  # Perform Gamma Correction

fig = plt.figure(figsize=(10, 10))  # Set the figure size
ax = plt.Axes(fig, [0, 0, 1, 1])
ax.set_axis_off()  # Turn off axes
fig.add_axes(ax)
ax.imshow(rgbStretched, interpolation='bilinear', alpha=0.9)  # Plot a natural color RGB
plt.show()
fig.savefig('{}{}_RGB.png'.format(out_dir, img_file[:-3] + '_RGB.png'))  # Export natural color RGB as png


