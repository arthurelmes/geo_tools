#!/home/arthur.elmes/software/anaconda3/envs/geo/bin/python

import os, matplotlib, math, sys
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn.metrics import mean_squared_error
import numpy as np
from pyhdf.SD import SD, SDC
from h5py import File

matplotlib.rcParams['agg.path.chunksize'] = 100000

## h12v04 UL: -6671703.1179999997839332 5559752.5983330002054572 LR: -5559752.5983330002054572 4447802.0786669999361038
## h16v01 UL: -2223901.0393329998478293 8895604.1573329996317625 LR: -1111950.5196670000441372 7783653.6376670002937317
## h16v02 UL: -2223901.0393329998478293 7783653.6376670002937317 LR: -1111950.5196670000441372 6671703.1179999997839332
# h09v05 -10007554.6769999992102385,3335851.5589999998919666 : -8895604.1573329996317625,4447802.0786669999361038
# h11v03 -7783653.6376670002937317,5559752.5983330002054572 : -6671703.1179999997839332,6671703.1179999997839332
# h11v08 -7783653.6376670002937317,0.0000000000000000 : -6671703.1179999997839332,1111950.5196670000441372
# h11v11 -7783653.6376670002937317,-3335851.5589999998919666 : -6671703.1179999997839332,-2223901.0393329998478293
# h17v07 -1111950.5196670000441372,1111950.5196670000441372 : 0.0000000000000000,2223901.0393329998478293
# h20v11 2223901.0393329998478293,-3335851.5589999998919666 : 3335851.5589999998919666,-2223901.0393329998478293
# h24v04 6671703.1179999997839332,4447802.0786669999361038 : 7783653.6376670002937317,5559752.5983330002054572
# h26v04 8895604.1573329996317625,4447802.0786669999361038 : 10007554.6769999992102385,5559752.5983330002054572
# h30v11 13343406.2359999995678663,-3335851.5589999998919666 : 14455356.7556669991463423,-2223901.0393329998478293

def determine_sensor(fname):
    if "MCD" in fname:
        return fname.split("/")[-1][17:23], fname.split("/")[-1][:16], fname.split("/")[-1][24:27]
    elif "VNP" in fname:
        return fname.split("/")[-1][18:24], fname.split("/")[-1][:17], fname.split("/")[-1][25:28]
    else:
        print("Check input data! Only MCD and VNP products work.")
        sys.exit()


def get_data(fname, sds):
    if "MCD" in fname:
        np_data = hdf_to_np(fname, sds)
    elif "VNP" in fname:
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

    qa_masked = np.ma.masked_array(nodata_masked, hdf_qa > 1)
    qa_masked_float = np.multiply(qa_masked, 0.001)

    return qa_masked_float


def plot_data(cmb_data, labels, stats, workspace):
    # Using masked numpy arrays, create scatterplot of tile1 vs tile2

    # Get rid of all the masked data by filling with nans and then removing them
    cmb_data_nans = np.ma.filled(cmb_data, np.nan)
    cmb_data_nans = cmb_data_nans[~np.isnan(cmb_data_nans).any(axis=1)]

    #hist = plt.hist2d(cmb_data_nans[:, 0], cmb_data_nans[:, 1], bins=50, norm=LogNorm())
    x = cmb_data_nans[:, 0]
    y = cmb_data_nans[:, 1]

    hist = plt.hist2d(cmb_data_nans[:, 0], cmb_data_nans[:, 1], bins=200, norm=LogNorm(),
                      cmap=plt.cm.YlOrRd)
    plt.colorbar(hist[3])
    plt.title(labels[0] + '_' + labels[1] + "_"+ labels[3])

    plt.xlabel(labels[1] + " " + labels[4] + ' (scaled)')
    plt.ylabel(labels[2] + " " + labels[5] + ' (scaled)')

    # # Add text box with RMSE and mean bias
    textstr = '\n'.join((
        r'$\mathrm{RMSE}=%.2f$' % (stats[0], ),
        r'$\mathrm{MeanBias}=%.2f$' % (stats[1], )))

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    plt.text(0.05, 0.95, textstr, fontsize=14, verticalalignment='top', bbox=props)

    # Add x=y line
    lims = [
        np.min([plt.xlim(), plt.ylim()]),  # min of both axes
        np.max([plt.xlim(), plt.ylim()]),  # max of both axes
    ]

    # Plot limits against each other for 1:1 line
    plt.plot(lims, lims, 'k-', alpha=0.75, zorder=1)
    plt.xlim(lims)
    plt.ylim(lims)

    #plt.show()

    # Export data as CSV in case needed
    hdrs = str(labels[1] + "." + labels[4] + "," + labels[2] + "." + labels[5])
    csv_name = os.path.join(workspace, labels[0] + "_" + labels[1] + "_" + labels[2] + "_" + labels[3] + "_data.csv")
    np.savetxt(csv_name, cmb_data, delimiter=",", header=hdrs)

    plt_name = os.path.join(workspace, labels[0] + "_" + labels[1] + "_" + labels[4] + "_vs_" \
                            + labels[2] + "_" + labels[5] + "_" + labels[3])
    print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=plt_name))
    plt.savefig('{plt_name}.png'.format(plt_name=plt_name))

def main():
    # CLI args
    parser = ArgumentParser()
    parser.add_argument("-d", "--input-dir", dest="base_dir",
                        help="Base directory containing sample and imagery data",
                        metavar="IN_DIR")
    parser.add_argument("-f1", "--file1", dest="file1", help="First image to compare.", metavar="FILE1")
    parser.add_argument("-f2", "--file2", dest="file2", help="Second image to compare.", metavar="FILE2")
    args = parser.parse_args()

    workspace = args.base_dir

    # Set input hdf/h5 filenames
    tile1_fname = args.file1
    tile2_fname = args.file2

    # Set workspace IO dirs
    workspace_out = workspace
    os.chdir(workspace)

    #TODO these shouldn't just be wsa, should be able to do
    # any band, selected as argument they should be args so
    # that different bands can be selected. Right now these are manually set
    # to reflect the band of interest
    # sds_name_wsa = "Albedo_WSA_shortwave"
    # sds_name_qa = "BRDF_Albedo_Band_Mandatory_Quality_shortwave"
    sds_name_wsa = "Albedo_WSA_nir"
    sds_name_qa = "BRDF_Albedo_Band_Mandatory_Quality_nir"
    # Extract identifying information from filenames
    tile1_deets = determine_sensor(tile1_fname.split("/")[-1])
    tile2_deets = determine_sensor(tile2_fname.split("/")[-1])
    labels = (tile1_deets[0], tile1_deets[1], tile2_deets[1], sds_name_wsa, tile1_deets[2], tile2_deets[2])

    # Convert both tiles' data and qa to numpy arrays for plotting
    tile1_data_wsa = get_data(os.path.join(workspace, tile1_fname), sds_name_wsa)
    tile1_data_qa = get_data(os.path.join(workspace, tile1_fname), sds_name_qa)
    tile2_data_wsa = get_data(os.path.join(workspace, tile2_fname), sds_name_wsa)
    tile2_data_qa = get_data(os.path.join(workspace, tile2_fname), sds_name_qa)

    # Call masking function to cleanup data
    tile1_data_qa_masked = mask_qa(tile1_data_wsa, tile1_data_qa)
    tile2_data_qa_masked = mask_qa(tile2_data_wsa, tile2_data_qa)

    #every other pixel. If both datasets are the same, do nothing.
    if ("MCD" in labels[2] and "VNP" in labels[3]) or ("MCD" in labels[2] and "VNP" in labels[3]):
        tile1_data_qa_masked = tile1_data_qa_masked[::2, ::2]
    else:
        pass
    # Flatten np arrays into single column
    x = tile1_data_qa_masked.flatten()
    y = tile2_data_qa_masked.flatten()
    cmb_data = np.ma.column_stack((x, y))

    # Calculate RMSE and Mean Bias, multiply by 0.001, which is the scale factor for MCD43/VNP43
    rmse = math.sqrt(mean_squared_error(x, y)) * 0.001
    mb = np.sum(x - y) / x.size * 0.001
    stats = (rmse, mb)

    # Call plotting function
    plot_data(cmb_data, labels, stats, workspace_out)


if __name__ == "__main__":
    main()
