# This script extracts all pixel values of two input files from the same MODIS grid tile, and plots the
# results. 

from argparse import ArgumentParser
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn.metrics import mean_squared_error
import numpy as np
from pyhdf.SD import SD, SDC
from h5py import File
import os, matplotlib, math, sys
import pandas as pd
matplotlib.rcParams['agg.path.chunksize'] = 100000
import csv


def determine_sensor(fname):
    if "MCD" in fname:
        return fname.split("/")[-1][17:23], fname.split("/")[-1][:16], fname.split("/")[-1][24:27]
    elif "VNP" in fname or "VJ1" in fname:
        return fname.split("/")[-1][18:24], fname.split("/")[-1][:17], fname.split("/")[-1][25:28]
    else:
        print("Check input data! Only MCD and VNP/VJ1 products work.")
        sys.exit()


def get_data(fname, sds):
    if "MCD" in fname:
        np_data = hdf_to_np(fname, sds)
    elif "VNP" in fname or "VJ1" in fname:
        np_data = h5_to_np(fname, sds)
    return np_data


def modis_process():
    #TODO fill in the processing chain for modis hdf products here, calling hdf_to_np etc
    pass


def viirs_process():
    #TODO mirror the modis processing chain that's already laid out and working, but with h5py
    pass


def hdf_to_np(hdf_fname, sds):
    #TODO close the dataset, probably using 'with'
    try:
        hdf_ds = SD(hdf_fname, SDC.READ)
        dataset_3d = hdf_ds.select(sds)
        data_np = dataset_3d[:,:]
        return data_np
    except:
        print("Failed to open HDF.")


def h5_to_np(h5_fname, sds):
    try:
        with File(h5_fname, 'r') as h5_ds:
            data_np = h5_ds['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields'][sds][()]
            return data_np
    except:
        print("Failed to open H5.")


def mask_qa(hdf_data, hdf_qa):
    # Mask the wsa values with QA to keep only value 0 (highest quality)
    # Also, mask out nodata values (32767)
    # wsa_swir_masked = np.ma.masked_array(wsa_band, wsa_band == 32767)
    # wsa_swir_masked_qa = np.ma.masked_array(wsa_swir_masked, qa_band > 1)

    nodata_masked = np.ma.masked_array(hdf_data, hdf_data == 32767)
    # NOTE: Uncomment below to also mask out all zeros. They seem to be mostly water pixels.
    # nodata_masked = np.ma.masked_array(nodata_masked, nodata_masked == 0)

    qa_masked = np.ma.masked_array(nodata_masked, hdf_qa > 0)
    qa_masked_float = np.multiply(qa_masked, 0.001)

    return qa_masked_float


def plot_data(cmb_data, labels, stats, workspace):
    # Using masked numpy arrays, create scatterplot of tile1 vs tile2

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    fig.tight_layout(pad=3)
    fig.set_facecolor('black')
    
    # Get rid of all the masked data by filling with nans and then removing them
    cmb_data_nans = np.ma.filled(cmb_data, np.nan)
    cmb_data_nans = cmb_data_nans[~np.isnan(cmb_data_nans).any(axis=1)]

    #hist = plt.hist2d(cmb_data_nans[:, 0], cmb_data_nans[:, 1], bins=50, norm=LogNorm())
    x = cmb_data_nans[:, 0]
    y = cmb_data_nans[:, 1]

    hist = plt.hist2d(cmb_data_nans[:, 0], cmb_data_nans[:, 1], bins=200, norm=LogNorm(),
                      range=[[0, 1.0], [0, 1.0]], cmap=plt.cm.YlGn)
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    cb = fig.colorbar(hist[3])
    cb.ax.yaxis.set_tick_params(color='white')
    cb.outline.set_edgecolor('white')
    plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='white')
    
    ax.set_title(labels[0] + "_" + labels[3][0] + " " + labels[3][1])
    ax.title.set_color('white')

    ax.set_xlabel(labels[1] + " " + labels[4] + ' ' + labels[3][0].replace('_', ' '))
    ax.set_ylabel(labels[2] + " " + labels[5] + ' ' + labels[3][1].replace('_', ' '))

    # Add text box with RMSE and mean bias
    textstr = '\n'.join((
        r'$\mathrm{RMSE}=%.4f$' % (stats[0], ),
        r'$\mathrm{MeanBias}=%.4f$' % (stats[1], )))

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.95, textstr, fontsize=14, verticalalignment='top', bbox=props)

    # Add x=y line
    lims = [
        np.min([plt.xlim(), plt.ylim()]),  # min of both axes
        np.max([plt.xlim(), plt.ylim()]),  # max of both axes
    ]

    # Plot limits against each other for 1:1 line
    ax.plot(lims, lims, 'y-', alpha=0.75, zorder=1)
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    # Export data as CSV in case needed
    hdrs = str(labels[1] + "." + labels[4] + "," + labels[2] + "." + labels[5])
    csv_name = os.path.join(workspace, labels[0] + "_" + labels[1] + "_" + labels[2] + "_" + labels[3][0] + "_" +
                            labels[3][1] + "_data.csv")
    np.savetxt(csv_name, cmb_data_nans, delimiter=",", header=hdrs, comments='')

    plt_name = os.path.join(workspace, labels[0] + "_" + labels[1] + "_" + labels[4] + "_vs_"
                            + labels[2] + "_" + labels[5] + "_" + labels[3][0] + "_vs_" + labels[3][1])
    print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=plt_name))
    fig.savefig('{plt_name}.png'.format(plt_name=plt_name), facecolor='black')


def main():
    # CLI args
    parser = ArgumentParser()
    parser.add_argument("-d", "--output-dir", dest="base_dir",
                        help="Directory to store outputs",
                        metavar="IN_DIR")
    parser.add_argument("-f1", "--file1", dest="file1", help="Complete path of "
                                                             "First image to compare.", metavar="FILE1")
    parser.add_argument("-f2", "--file2", dest="file2", help="Complete path of "
                                                             "Second image to compare.", metavar="FILE2")
    parser.add_argument("-b1", "--band1", dest="band1", default="sw",
                        help="Specify the band from the first file to compare, e.g. shortwave, nir, Band3, M4,")
    parser.add_argument("-b2", "--band2", dest="band2", default="shortwave",
                        help="Specify the band from the second file to compare, e.g. shortwave, nir, 3, M3,")
    parser.add_argument("-p", "--product", dest="product", default="WSA",
                        help="Specify the product to compare, i.e. WSA or BSA.")

    args = parser.parse_args()

    # Set workspace IO dir
    workspace_out = args.base_dir

    # Set input hdf/h5 filenames
    tile1_fname = args.file1
    tile2_fname = args.file2
    band1 = args.band1
    band2 = args.band2
    product = args.product

    # Check that MCD is the f1 if f2 is VIIRS, because of silly way of handling resolution mismatch currently
    if "MCD" in tile2_fname:
        if "VNP" in tile1_fname or "VJ1" in tile1_fname:
            print("MCD file must be file1 if a MODIS/VIIRS comparison is being made!")
            sys.exit(1)

    os.chdir(workspace_out)

    # Will need different style sds names for modis vs viirs
    sds1_name = "Albedo_{}_{}".format(product, band1)
    qa1_name = "BRDF_Albedo_Band_Mandatory_Quality_{}".format(band1)
    sds2_name = "Albedo_{}_{}".format(product, band2)
    qa2_name = "BRDF_Albedo_Band_Mandatory_Quality_{}".format(band2)

    # Extract identifying information from filenames
    tile1_deets = determine_sensor(tile1_fname.split("/")[-1])
    tile2_deets = determine_sensor(tile2_fname.split("/")[-1])
    labels = (tile1_deets[0], tile1_deets[1], tile2_deets[1], (sds1_name, sds2_name), tile1_deets[2], tile2_deets[2])


    # Convert both tiles' data and qa to numpy arrays for plotting
    tile1_data = get_data(os.path.join(tile1_fname), sds1_name)
    tile1_qa = get_data(os.path.join(tile1_fname), qa1_name)
    tile2_data = get_data(os.path.join(tile2_fname), sds2_name)
    tile2_qa = get_data(os.path.join(tile2_fname), qa2_name)

    # Call masking function to cleanup data
    tile1_qa_masked = mask_qa(tile1_data, tile1_qa)
    tile2_qa_masked = mask_qa(tile2_data, tile2_qa)


    # Take every other pixel if comparing MCD (500m) and VNP/VJ1 (1km). If both datasets are the same, do nothing.
    #TODO This is janky because it requires that the MCD is entered first, right? Add some thing to fix this
    if ("MCD" in labels[1] and "VNP" in labels[2] and "MA" in labels[2]) or \
            ("MCD" in labels[1] and "VJ1" in labels[2] and "MA" in labels[2]):
        print('Subsampling every other pixel in MCD because of resolution mismatch.')
        tile1_qa_masked = tile1_qa_masked[::2, ::2]
    else:
        pass

    # Flatten np arrays into single column
    x = tile1_qa_masked.flatten()
    y = tile2_qa_masked.flatten()
    cmb_data = np.ma.column_stack((x, y))
    cmb_data_df = pd.DataFrame(cmb_data)
    rmse = ((cmb_data_df[0] - cmb_data_df[1]) ** 2).mean() ** 0.5
    mb = cmb_data_df[0].mean() - cmb_data_df[1].mean()
    stats_csv_name = (os.path.join(workspace_out, tile1_deets[0] + "_stats.csv"))
    print('Writing stats to: {}'.format(stats_csv_name))
    stats = (rmse, mb)
    header = ['RMSE', 'Mean Bias F1 - F2', 'F1', 'F2', 'B1', 'B2']

    if os.path.isfile(stats_csv_name):       
        with open(stats_csv_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.DictWriter(write_obj, fieldnames=header)

            # Add contents of list as last row in the csv file
            csv_writer.writerow({'RMSE': stats[0],
                                 'Mean Bias F1 - F2': stats[1],
                                 'F1': os.path.basename(tile1_fname),
                                 'F2': os.path.basename(tile2_fname),
                                 'B1': band1,
                                 'B2': band2})
    else:
        with open(stats_csv_name, 'w', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.DictWriter(write_obj, fieldnames=header)

            # Initialize the new file with headers
            csv_writer.writeheader()
            
            # Add contents of list as last row in the csv file
            csv_writer.writerow({'RMSE': stats[0],
                                 'Mean Bias F1 - F2': stats[1],
                                 'F1': os.path.basename(tile1_fname),
                                 'F2': os.path.basename(tile2_fname),
                                 'B1': band1,
                                 'B2': band2})
        
    # Call plotting function
    plot_data(cmb_data, labels, stats, workspace_out)


if __name__ == "__main__":
    main()
