"""This script will quickly make RGB and NIR composites of MCD43/VNP43/VJ143
Author: Arthur Elmes
Date: 2020-12-04

Great tips here:
https://lpdaac.usgs.gov/resources/e-learning/working-daily-nasa-viirs-surface-reflectance-data/"""

import h5py
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime as dt
from skimage import exposure
import sys
from pyhdf.SD import SD, SDC
import pprint
from glob import glob
import argparse


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

    # Define number of bits
    bits = 8
    # Generate a list of all possible bit values
    vals = list(range(0, (2**bits)))
    # Create an empty list used to store bit values where bits 1-7 = 0
    goodQF = []

    for v in vals:
        # Convert to binary based on values and # of bits defined above:
        bitVal = format(vals[v], 'b').zfill(bits)
        # Keep if all bits = 0
        if bitVal[0:8] == '00000000':
            # Append to list
            goodQF.append(vals[v])
            # DEV: print good quality values
            # print('\n' + str(vals[v]) + ' = ' + str(bitVal))

    # List attributes
    # print(list(r.attrs))
    # For some reason, there is no scale_factor stored in the VNP43MA4 files
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

    # DEV: check attr
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

    # Define number of bits
    bits = 8
    # Generate a list of all possible bit values
    vals = list(range(0, (2**bits)))
    # Create an empty list used to store bit values where bits 1-7 = 0
    goodQF = []

    for v in vals:
        # Convert to binary based on values and # of bits defined above:
        bitVal = format(vals[v], 'b').zfill(bits)
        # Keep if all bits = 0
        if bitVal[0:8] == '00000000':
            # Append to list
            goodQF.append(vals[v])
            # DEV: print good quality values
            # print('\n' + str(vals[v]) + ' = ' + str(bitVal))

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

    return rgb, img


def do_plot(rgb, img_file, out_dir, contrast_stretch):
    # Calculate 2nd,98th percentile for updating min/max vals
    p2, p98 = np.percentile(rgb, (2, 98))

    # Perform contrast stretch on RGB range
    if contrast_stretch == True:
        rgb_stretched = exposure.rescale_intensity(rgb, in_range=(p2, p98))

    # Perform Gamma Correction
    # rgb_stretched = exposure.adjust_gamma(rgb_stretched, 0.5)
    rgb_stretched = exposure.adjust_gamma(rgb, 0.5)

    # Set the figure size
    fig = plt.figure(figsize=(10, 10))
    ax = plt.Axes(fig, [0, 0, 1, 1])

    # Turn off axes
    #ax.set_axis_off()
    fig.add_axes(ax)

    fp = FontProperties(family='DejaVu Sans', size=16, weight='bold')
    fig.suptitle(os.path.basename(img_file), fontproperties=fp, color='white')

    # Plot a natural color RGB
    ax.imshow(rgb_stretched, interpolation='bilinear', alpha=0.9)

    plt.show()
    # Export natural color RGB as png
    fig.savefig('{}{}_RGB.png'.format(out_dir + '/', os.path.basename(img_file[:-3])))


def main():
    parser = argparse.ArgumentParser(description='Make NBAR pngs from directory '
                                                 'of hdf or h5 files for V**43MA4 '
                                                 'or MCD43A4')
    parser.add_argument('-w', metavar='workspace', type=str, dest="workspace",
                        help='Enter a workspace containing one or more VNP43MA4, VJ143MA4, or MCD43A4 files.')
    parser.add_argument('-p', metavar='product', type=str, dest="product",
                        help='Specify MCD, VNP, or VJ1')
    parser.add_argument('-c', metavar='contrast_stretch', type=bool, default=False, dest="contrast_stretch",
                        help='Enter True to perform a contrast stretch using 2nd - 98th percentile.')
    args = parser.parse_args()

    workspace = args.workspace
    product = args.product
    contrast_strech = args.contrast_stretch

    os.chdir(workspace)
    out_dir = os.path.join(workspace, 'output')
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    h_file_list = glob(workspace + '/' + product + '*A4*.h*')
    for h_file in h_file_list:
        print(h_file)
        rgb, img = img_2_numpy(h_file)
        do_plot(rgb, img, out_dir, contrast_strech)


if __name__ == '__main__':
    main()
