'''
Created Sep 19 10:04:10 2018
Significant updates March 17th 2020
@author: arthur elmes arthur.elmes@gmail.com

'''
import os, glob, sys, pyproj, csv, statistics
from argparse import ArgumentParser
from osgeo import gdal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import rasterio as rio


def tif_to_np(tif_fname):
    with rio.open(tif_fname,
                  'r',
                  driver='GTiff') as tif:
        data_np = tif.read()
        return data_np


def make_prod_list(in_dir, prdct, year, day):
    if 'MCD' in prdct or 'VNP' in prdct or 'VJ1' in prdct:
        h_file_list = glob.glob(os.path.join(in_dir,
                                             '{prdct}*{year}{day:03d}*.tif'.format(prdct=prdct,
                                                                                   day=day, year=year)))
    elif 'LC08' in prdct:
        dt_string = str(year) + '-' + str(day)
        date_complete = datetime.strptime(dt_string, '%Y-%j')
        mm = date_complete.strftime('%m')
        dd = date_complete.strftime('%d')
        h_file_list = glob.glob(os.path.join(in_dir, '{prdct}*_{year}{month}{day}_*.h*'.format(prdct=prdct,
                                                                                                     month=mm,
                                                                                                     day=dd,
                                                                                                     year=year)))
    else:
        print('Product type unknown! Please check that input is MCD, VNP, VJ1 or LC08.')
        sys.exit()

    #print('{prdct}*{year}{day:03d}*.tif'.format(prdct=prdct, day=day, year=year))
    return h_file_list


def extract_pixel_value(in_dir, site, prdct, t_file_day, base_dir):
    # Open tifs with rasterio
    #print('Opening: ' + t_file_day)

    with rio.open(t_file_day,
                  'r',
                  driver='GTiff') as tif:

        #print("lon/lat are: ")
        lon, lat = (float(site[1][1]), float(site[1][0]))
        #print((lon, lat))

        #print("col/row are: ")
        col, row = tif.index(lon, lat)
        #print((col, row))

        tif_np = tif.read(1)
        tif_np_masked = np.ma.masked_array(tif_np, tif_np == 32767)
        result = tif_np_masked[(col, row)]

        return result


def draw_plot(year, year_smpl_cmb_df, fig_dir, prdct, sites_dict):
    sns.set_style('darkgrid')

    for site in sites_dict.keys():
        for sds in ['wsa', 'bsa']:
            col_name = str(site) + '_' + str(sds)

            # Create a seaborn scatterplot (or replot for now, small differences)
            sct = sns.regplot(x='doy', y=col_name, data=year_smpl_cmb_df, marker='o', label='sw ' + str(sds),
                              fit_reg=False, scatter_kws={'color':'darkblue', 'alpha':0.3,'s':20})
            sct.set_ylim(0, 1.0)
            sct.set_xlim(1, 366)
            sct.legend(loc='best')

            # Access the figure, add title
            plt_name = str(year + ' ' + prdct + ' SW ' + str(sds))
            plt.title(plt_name)
            #plt.show()

            plt_name = plt_name.replace(' ', '_') + '_' + str(site)
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
    parser.add_argument('-y', '--years', dest='years', help='Years to extract data for.', metavar='YEARS')

    parser.add_argument('-d', '--input-dir', dest='base_dir',
                        help='Base directory containing sample and dir of imagery data called the product name'
                             ', e.g. ../MCD43A3/',
                        metavar='IN_DIR')
    parser.add_argument('-s', '--sites', dest='sites_csv_fname', help='CSV with no headings containing smpls. '+\
                        'must look like: id,lat,long',
                        metavar='SITES')
    parser.add_argument('-p', '--product', dest='prdct', help='Imagery product to be input, e.g. LC08, MCD43A3.',
                        metavar='PRODUCT')
    args = parser.parse_args()

    # Note: I have chosen to call the landsat product LC08, rather than LC8, due to the file naming convention
    # of the inputs specific to the albedo code. LC8 is also used in different Landsat data products, annoyingly.
    prdct = args.prdct
    base_dir = args.base_dir
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
            in_dir = base_dir
            fig_dir = os.path.join(base_dir, 'figs')
            if not os.path.isdir(fig_dir):
               os.makedirs(fig_dir)
               print('Made new folder for figs: ' + str(fig_dir))
            else:
               pass
            try:
                os.chdir(in_dir)
            except FileNotFoundError:
                print('Sorry, data directory not found!')
                sys.exit(1)
            #print('Processing site: ' + str(site))

            # Create empty array for mean
            tif_mean = []
            for day in doy_list:
                # Open the ONLY BAND IN THE TIF! Cannot currently deal with multiband tifs
                h_file_list = make_prod_list(in_dir, prdct, year, day)
                file_name = '{in_dir}/{prdct}*{year}{day:03d}*.tif'.format(in_dir=in_dir, prdct=prdct, day=day,
                                                                           year=year)
                # See if there is a raster for the date, if not use a fill value for the graph
                if len(h_file_list) == 0:
                    #print('File not found: ' + file_name)
                    pixel_value = np.nan
                elif len(h_file_list) > 1:
                    print('Multiple matching files found for same date! Please remove one.')
                    sys.exit()
                else:
                    # print('Found file: ' + file_name)
                    h_file_day = h_file_list[0]
                    # Extract pixel values and append to dataframe
                    try:
                        pixel_value = extract_pixel_value(in_dir, site, prdct, h_file_day, base_dir)

                    except:
                         print('Warning! Pixel out of raster boundaries!')
                         pixel_value = np.nan

                # Add each point to a temporary list
                pixel_value = pixel_value * 0.001
                smpl_results = []
                smpl_results.append(pixel_value)
                try:
                    tmp_mean = statistics.mean(smpl_results)
                    tif_mean.append(tmp_mean)
                except:
                    tif_mean.append(np.nan)
            cols = str((site[0][0]))

            smpl_results_df = pd.DataFrame(tif_mean, columns=[cols])
            print(smpl_results_df.head())

            # Append the site's results to the existing yearly dataframe, initiated above
            year_smpl_cmb_df = pd.concat([year_smpl_cmb_df, smpl_results_df], axis=1)

        # Do plotting and save output PER YEAR (individual csv per year)
        #draw_plot(year, year_smpl_cmb_df, fig_dir, prdct, sites_dict)

        # Export data to csv
        os.chdir(fig_dir)
        output_name = str(sites_csv_input[:-4] + '_extracted_values')
        csv_name = str(output_name + '_' + prdct + '.csv')
        print('writing csv: ' + csv_name)
        year_smpl_cmb_df.to_csv(csv_name, index=False)


if __name__ == '__main__':
    main()
