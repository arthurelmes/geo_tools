"""
Created Sep 19 10:04:10 2018
Significant updates March 17th 2020
@author: arthur elmes arthur.elmes@gmail.com

"""
import os, glob, sys, pyproj, csv, statistics
from argparse import ArgumentParser
from osgeo import gdal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
from h5py import File
from datetime import datetime
import seaborn as sns


def hdf_to_np(hdf_fname, sds):
    #TODO close the dataset, probably using 'with'
    hdf_ds = SD(hdf_fname, SDC.READ)
    dataset_3d = hdf_ds.select(sds)
    data_np = dataset_3d[:,:]
    return data_np


def h5_to_np(h5_fname, sds):
    with File(h5_fname, 'r') as h5_ds:
        data_np = h5_ds['HDFEOS']['GRIDS']['VIIRS_Grid_BRDF']['Data Fields'][sds][()]
    return data_np


def convert_ll_vnp(lat, lon, tile, in_dir, prdct):
    # prdct = prdct
    # Convert the lat/long point of interest to a row/col location
    template_h_list = glob.glob(os.path.join(in_dir, "*.A*{tile}*.h*".format(tile=tile)))
    template_h_file = template_h_list[0]
    template_h_ds = gdal.Open(template_h_file, gdal.GA_ReadOnly)
    template_h_band = gdal.Open(template_h_ds.GetSubDatasets()[0][0], gdal.GA_ReadOnly)
    # Use pyproj to create a geotransform between
    # WGS84 geographic (lat/long; epsg 4326) and
    # the funky crs that modis/viirs use.
    # Note that this modis crs seems to have units
    # in meters from the geographic origin, i.e.
    # lat/long (0, 0), and has 2400 rows/cols per tile.
    # gdal does NOT read the corner coords correctly,
    # but they ARE stored correctly in the hdf metadata. Although slightly
    # difft than reported by gdal...

    # Using pyproj to transform coords of interes to meters
    in_proj = pyproj.Proj(init='epsg:4326')
    # out_proj = pyproj.Proj(template_h_band.GetProjection())
    out_proj = pyproj.Proj('+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs')

    # Current sample location convert from ll to m
    smpl_x, smpl_y = pyproj.transform(in_proj, out_proj, lon, lat)

    # FOR VIIRS, use manual
    # h12v04 UL: -6671703.1179999997839332 5559752.5983330002054572 LR: -5559752.5983330002054572 4447802.0786669999361038
    # out_proj = pyproj.Proj('+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs')

    # Getting bounding coords from meta
    # Perhaps no longer neededm but they're slilghtly difft than gdal geotransofrm
    # NOTE gdal works fine if you call the geotransform
    # on the BAND!!! (sds), not the DS
    meta = template_h_ds.GetMetadata_Dict()
    # FOR MODIS, us ALL CAPS
    y_origin_meta = float(meta['NORTHBOUNDINGCOORDINATE'])
    y_min_meta = float(meta['SOUTHBOUNDINGCOORDINATE'])
    x_max_meta = float(meta['EASTBOUNDINGCOORDINATE'])
    x_origin_meta = float(meta['WESTBOUNDINGCOORDINATE'])
    # n_rows_meta = 1200 # int(meta['DATAROWS'])
    # n_cols_meta = 1200 # int(meta['DATACOLUMNS'])
    pixel_height_meta_m = 926.6254330558330139 #(y_origin_meta - y_min_meta) / n_rows_meta
    pixel_width_meta_m = 926.6254330558330139 #pixel_height_meta_m

    # # Make calculations to get row/col value
    # # NOTE that for geotifs, it would also be possible
    # # to simply open with rasterio, then use .index()
    # # to return the row/col. This does not work for hdf
    x_origin_meta_m, y_origin_meta_m = pyproj.transform(in_proj, out_proj, x_origin_meta, y_origin_meta)
    # x_max_meta_m, y_min_meta_m = pyproj.transform(in_proj, out_proj, x_max_meta, y_min_meta)

    col_m = int((smpl_x - x_origin_meta_m) / pixel_width_meta_m)
    row_m = int(-1 * (smpl_y - y_origin_meta_m) / pixel_height_meta_m)
    smp_rc = row_m, col_m
    return smp_rc


def convert_ll(lat, lon, tile, in_dir, prdct):
    prdct = prdct
   # Convert the lat/long point of interest to a row/col location
    if "h" in tile:
        template_h_list = glob.glob(os.path.join(in_dir,
                                                 '{prdct}.A*{tile}*.h*'.format(prdct=prdct,
                                                                               tile=tile)))
    else:
        template_h_list = glob.glob(os.path.join(in_dir, '{prdct}*{tile}*.h*'.format(prdct=prdct,
                                                                                     tile=tile)))
    template_h_file = template_h_list[0]
    template_h_ds = gdal.Open(template_h_file, gdal.GA_ReadOnly)
    template_h_band = gdal.Open(template_h_ds.GetSubDatasets()[0][0],
                               gdal.GA_ReadOnly)
    # Use pyproj to create a geotransform betweensds
    # WGS84 geographic (lat/l1200ong; epsg 4326) and
    # the funky crs that modis/viirs use.
    # Note that this modis crs seems to have units
    # in meters from the geographic origin, i.e.
    # lat/long (0, 0), and has 2400 rows/cols per tile.
    # gdal does NOT read the corner coords correctly,
    # but they ARE stored correctly in the hdf metadata. Although slightly
    # difft than reported by gdal, which is odd.

    # # Using pyproj to transform coords of interes to meters
    in_proj = pyproj.Proj(init='epsg:4326')
    out_proj = pyproj.Proj(template_h_band.GetProjection())

    # # Current sample location convert from ll to m
    smpl_x, smpl_y = pyproj.transform(in_proj, out_proj, lon, lat)

    # Getting bounding coords from meta
    # Perhaps no longer neededm but they're slilghtly difft than gdal geotransofrm
    # NOTE gdal works fine if you call the geotransform
    # on the BAND!!! (sds), not the DS
    # meta = template_h_ds.GetMetadata_Dict()
    # FOR MODIS, us ALL CAPS
    # y_origin_meta = float(meta['NORTHBOUNDINGCOORDINATE'])
    # y_min_meta = float(meta['SOUTHBOUNDINGCOORDINATE'])
    # x_max_meta = float(meta['EASTBOUNDINGCOORDINATE'])
    # x_origin_meta = float(meta['WESTBOUNDINGCOORDINATE'])
    # n_rows_meta = int(meta['DATAROWS'])
    # n_cols_meta = int(meta['DATACOLUMNS'])
    # pixel_height_meta_m = float(meta['CHARACTERISTICBINSIZE'])
    # pixel_width_meta_m = float(meta['CHARACTERISTICBINSIZE'])

    #TESTING these are conversions of the metadata extents to meters
    # x_origin_meta_m, y_origin_meta_m = pyproj.transform(in_proj, out_proj, x_origin_meta, y_origin_meta)
    # x_max_meta_m, y_min_meta_m= pyproj.transform(in_proj, out_proj, x_max_meta, y_min_meta)
    # pixel_width_meta_m = (x_max_meta_m - x_origin_meta_m) / n_cols_meta
    # pixel_height_meta_m = (y_origin_meta_m - y_min_meta_m) / n_rows_meta
    # col_meta_m = int((smpl_x - x_origin_meta_m) / pixel_width_meta_m)
    # row_meta_m = int(-1 * (smpl_y - y_origin_meta_m) / pixel_height_meta_m)
    # smp_rc_meta = row_meta_m, col_meta_m

    # Getting bounding coords etc from gdal geotransform
    n_cols = template_h_band.RasterXSize
    n_rows = template_h_band.RasterYSize
    x_origin, x_res, x_skew, y_origin, y_skew, y_res = template_h_band.GetGeoTransform()
    # Using the skew is in case there is any affine transformation
    # in place in the input raster. Not so for modis tiles, so not really necessary, but complete.
    x_max = x_origin + n_cols * x_res + n_cols * x_skew
    y_min = y_origin + n_rows * y_res + n_rows * y_skew

    # # Make calculations to get row/col value
    # # NOTE that for geotifs, it would also be possible
    # # to simply open with rasterio, then use .index()
    # # to return the row/col. This does not work for hdf
    pixel_width_m = (x_max - x_origin) / n_cols
    pixel_height_m = (y_origin - y_min) / n_rows
    col_m = int((smpl_x - x_origin) / pixel_width_m)
    row_m = int( -1 * (smpl_y - y_origin) / pixel_height_m)
    smp_rc = row_m, col_m
    return smp_rc


def make_prod_list(in_dir, prdct, year, day, tile):
    if "MCD" in prdct or "VNP" in prdct:
        h_file_list = glob.glob(os.path.join(in_dir,
                                             '{prdct}.A{year}{day:03d}*.h*'.format(prdct=prdct,
                                                                                   day=day, year=year)))
    elif "LC08" in prdct:
        dt_string = str(year) + "-" + str(day)
        date_complete = datetime.strptime(dt_string, "%Y-%j")
        mm = date_complete.strftime("%m")
        dd = date_complete.strftime("%d")
        h_file_list = glob.glob(os.path.join(in_dir, '{prdct}*{tile}_{year}{month}{day}_*.h*'.format(prdct=prdct,
                                                                                                     tile=tile,
                                                                                                     month=mm,
                                                                                                     day=dd,
                                                                                                     year=year)))
    else:
        print("Product type unknown! Please check that input is MCD, VNP, or LC08.")
        sys.exit()

    return h_file_list


def extract_pixel_value(in_dir, site, prdct, h_file_day, sds_names, base_dir):
    # Open tifs as gdal ds
    # print("Opening: " + h_file_day + " " + sds_name_wsa_sw)
    if "VNP" in prdct:
        # print("Found VIIRS product.")
        copy_srs_dir = os.path.join(base_dir, "copy_srs")
        wsa_band = h5_to_np(h_file_day, sds_names[0])
        bsa_band = h5_to_np(h_file_day, sds_names[1])
        qa_band = h5_to_np(h_file_day, sds_names[2])
    elif "MCD" in prdct or "LC08" in prdct:
        # print("Found MODIS product.")
        wsa_band = hdf_to_np(h_file_day, sds_names[0])
        bsa_band = hdf_to_np(h_file_day, sds_names[1])
        qa_band = hdf_to_np(h_file_day, sds_names[2])
    else:
        print("Unknown product! This only works for MCD, VNP, or LC8/LC08 hdf or h5 files!")
        sys.exit()

    # Mask out nodata values
    wsa_swir_masked = np.ma.masked_array(wsa_band, wsa_band == 32767)
    wsa_swir_masked_qa = np.ma.masked_array(wsa_swir_masked, qa_band > 1)
    bsa_swir_masked = np.ma.masked_array(bsa_band, bsa_band == 32767)
    bsa_swir_masked_qa = np.ma.masked_array(bsa_swir_masked, qa_band > 1)

    # Extract pixel value from product by converting lat/lon to row/col
    if "VNP" in prdct:
        smp_rc = convert_ll_vnp(site[1][0], site[1][1], site[1][2], copy_srs_dir, prdct)
    elif "MCD" in prdct:
        smp_rc = convert_ll(site[1][0], site[1][1], site[1][2], in_dir, prdct)
    elif "LC08" in prdct:
        smp_rc = convert_ll(site[1][0], site[1][1], site[1][2], in_dir, prdct)
    else:
        print("Unknown product! This only works for MCD, VNP, or LC8/LC08 hdf or h5 files!")
        sys.exit()

    # Take just the sampled location's value, and scale to float
    wsa_swir_subset = wsa_swir_masked_qa[smp_rc]
    wsa_swir_subset_flt = np.multiply(wsa_swir_subset, 0.001)
    plotbsa_swir_subset = bsa_swir_masked_qa[smp_rc]
    bsa_swir_subset_flt = np.multiply(bsa_swir_subset, 0.001)

    # Return a tuple of numpy arrays for wsa and bsa (and probably also qa?)
    return wsa_swir_subset_flt, bsa_swir_subset_flt


def draw_plot(year, year_smpl_cmb_df, fig_dir, prdct, sites_dict):
    sns.set_style("darkgrid")

    for site in sites_dict.keys():
        for sds in ["wsa", "bsa"]:
            col_name = str(site) + "_" + str(sds)

            # Create a seaborn scatterplot (or replot for now, small differences)
            sct = sns.regplot(x="doy", y=col_name, data=year_smpl_cmb_df, marker="o", label="sw " + str(sds),
                              fit_reg=False, scatter_kws={"color":"darkblue", "alpha":0.3,"s":20})
            sct.set_ylim(0, 1.0)
            sct.set_xlim(1, 366)
            sct.legend(loc="best")

            # Access the figure, add title
            plt_name = str(year + " " + prdct + " SW " + str(sds))
            plt.title(plt_name)
            #plt.show()

            plt_name = plt_name.replace(" ", "_") + "_" + str(site)
            # Save each plot to figs dir
            print('Saving plot to: ' + '{fig_dir}/{plt_name}.png'.format(fig_dir=fig_dir, plt_name=plt_name))
            plt.savefig('{fig_dir}/{plt_name}.png'.format(fig_dir=fig_dir, plt_name=plt_name))
            plt.clf()


def check_leap(year):
    leap_status = False
    year = int(year)
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                leap_status = True
            else:
                leap_status = False
        else:
            leap_status = True
    else:
        leap_status = False

    return leap_status


def main():
    # CLI args
    parser = ArgumentParser()
    parser.add_argument("-y", "--years", dest="years", help="Years to extract data for.", metavar="YEARS")
    parser.add_argument("-t", "--tile", dest="tile", help="Tile the sample points are in.", metavar="TILE")
    parser.add_argument("-d", "--input-dir", dest="base_dir",
                        help="Base directory containing sample and imagery data",
                        metavar="IN_DIR")
    parser.add_argument("-s", "--sites", dest="sites_csv_fname", help="CSV with no headings containing smpls",
                        metavar="SITES")
    parser.add_argument("-p", "--product", dest="prdct", help="Imagery product to be input, e.g. LC08, MCD43A3.",
                        metavar="PRODUCT")
    args = parser.parse_args()

    # Note: I have chosen to call the landsat product LC08, rather than LC8, due to the file naming convention
    # of the inputs specific to the albedo code. LC8 is also used in different Landsat data products, annoyingly.
    prdct = args.prdct
    base_dir = args.base_dir
    tile = args.tile
    years = [args.years]
    sites_csv_input = os.path.join(base_dir, args.sites_csv_fname)
    sites_dict = {}
    with open(sites_csv_input, mode='r') as sites_csv:
        reader = csv.reader(sites_csv)
        for row in reader:
            key = row[0]
            sites_dict[key] = row[1:]

    # TODO this 'copy_srs_dir' location is here because currently VNP43 has broken spatial reference
    # TODO information. Check V002 and remove this if it has been fixed, as this is ludicrously clunky.

    sds_name_wsa_sw = "Albedo_WSA_shortwave"
    sds_name_bsa_sw = "Albedo_BSA_shortwave"
    # Note: the LC08 hdfs have a differently named qa sds. yaay.
    sds_name_qa_sw = "BRDF_Albedo_Band_Mandatory_Quality_shortwave"
    # sds_name_qa_sw = "Albedo_Band_Quality_shortwave"
    sds_names = [sds_name_wsa_sw, sds_name_bsa_sw, sds_name_qa_sw]

    # Loop through the years provided, and extract the pixel values at the provided coordinates. Outputs CSV and figs.
    for year in years:
        doy_list = []
        if check_leap(year):
            for i in range(1, 367):
                doy_list.append(i)
        else:
            for i in range(1, 366):
                doy_list.append(i)

        # Make a blank pandas dataframe that results will be appended to,
        # and start it off with all possible doys (366)
        year_smpl_cmb_df = pd.DataFrame(doy_list, columns=['doy'])
        # Loop through each site and extract the pixel values
        for site in sites_dict.items():
            in_dir = os.path.join(base_dir, prdct, year, site[1][2])
            fig_dir = os.path.join(base_dir, 'figs')
            if not os.path.isdir(fig_dir):
               os.makedirs(fig_dir)
               print("Made new folder for figs: " + str(fig_dir))
            else:
               pass
            os.chdir(in_dir)
            print("Processing site: " + str(site))

            # Create empty arrays for mean, sd
            wsa_swir_mean = []
            wsa_swir_sd = []
            bsa_swir_mean = []
            bsa_swir_sd = []
            for day in doy_list:
                # Open the shortwave white sky albedo band.
                # The list approach is because of the processing date part of the file
                # name, which necessitates the wildcard -- this was just the easiest way.
                h_file_list = make_prod_list(in_dir, prdct, year, day, tile)
                file_name = "{prdct}.A{year}{day:03d}*.h*".format(prdct=prdct, day=day, year=year)
                # See if there is a raster for the date, if not use a fill value for the graph
                if len(h_file_list) == 0: # or len(bsa_tif_list) == 0 or len(qa_tif_list) == 0:
                    # print('File not found: ' + file_name)
                    wsa_swir_subset_flt = float('nan')
                    bsa_swir_subset_flt = float('nan')
                elif len(h_file_list) > 1:
                    print('Multiple matching files found for same date! Please remove one.')
                    sys.exit()
                else:
                    # print('Found file: ' + file_name)
                    h_file_day = h_file_list[0]
                    # Extract pixel values and append to dataframe
                    # Note the base_dir argument should go away when the correctly georeferenced VNP43 are available,
                    # because I can likely eliminate the vnp-specific value extractor function
                    pixel_values = extract_pixel_value(in_dir, site, prdct, h_file_day, sds_names, base_dir)

                # Add each point to a temporary list
                wsa_smpl_results = []
                bsa_smpl_results = []
                wsa_smpl_results.append(pixel_values[0])
                bsa_smpl_results.append(pixel_values[1])
                #TODO this is currently silly, but ultimately will be replaced by an averaging
                #TODO function for points of the same sample area
                try:
                    wsa_tmp_mean = statistics.mean(wsa_smpl_results)
                    wsa_swir_mean.append(wsa_tmp_mean)
                    bsa_tmp_mean = statistics.mean(bsa_smpl_results)
                    bsa_swir_mean.append(bsa_tmp_mean)
                except:
                    wsa_swir_mean.append(np.nan)
                    bsa_swir_mean.append(np.nan)

            wsa_smpl_results_df = pd.DataFrame(wsa_swir_mean)
            bsa_smpl_results_df = pd.DataFrame(bsa_swir_mean)
            cmb_smpl_results_df = pd.concat([wsa_smpl_results_df, bsa_smpl_results_df], axis=1, ignore_index=True)
            cmb_smpl_results_df.set_axis([str(site[0]) +'_wsa', str(site[0]) + '_bsa'], axis=1, inplace=True)

            # Append the site's results to the existing yearly dataframe, initiated above
            year_smpl_cmb_df = pd.concat([year_smpl_cmb_df, cmb_smpl_results_df], axis=1)

        # Do plotting and save output PER YEAR (individual csv per year)
        draw_plot(year, year_smpl_cmb_df, fig_dir, prdct, sites_dict)

        # Export data to csv
        os.chdir(fig_dir)
        output_name = str(sites_csv_input[:-4] + "_extracted_values")
        csv_name = str(output_name + "_" + prdct + ".csv")
        print("writing csv: " + csv_name)
        year_smpl_cmb_df.to_csv(csv_name, index=False)


if __name__ == "__main__":
    main()
