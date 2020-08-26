'''
Created Sep 19 10:04:10 2018
Significant updates March 17th 2020
@author: arthur elmes arthur.elmes@gmail.com

'''
import os, glob, sys, pyproj, csv, statistics
from argparse import ArgumentParser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import rasterio as rio
import timeit


def tif_to_np(tif_fname):
    with rio.open(tif_fname,
                  'r',
                  driver='GTiff') as tif:
        data_np = tif.read()
        return data_np


def make_prod_list(in_dir, prdct, year, day):
    if 'MCD' in prdct or 'VNP' in prdct or 'VJ1' in prdct:
        t_file_list = glob.glob(os.path.join(in_dir,
                                             '{prdct}*{year}{day:03d}*.tif'.format(prdct=prdct,
                                                                                   day=day, year=year)))
    elif 'LC08' in prdct:
        dt_string = str(year) + '-' + str(day)
        date_complete = datetime.strptime(dt_string, '%Y-%j')
        mm = date_complete.strftime('%m')
        dd = date_complete.strftime('%d')
        t_file_list = glob.glob(os.path.join(in_dir, '{prdct}*_{year}{month}{day}_*.h*'.format(prdct=prdct,
                                                                                                     month=mm,
                                                                                                     day=dd,
                                                                                                     year=year)))
    else:
        print('Product type unknown! Please check that input is MCD, VNP, VJ1 or LC08.')
        sys.exit()

    #print('{prdct}*{year}{day:03d}*.tif'.format(prdct=prdct, day=day, year=year))
    return t_file_list


def extract_pixel_values(sites_dict, t_file_day):
    # Open tifs with rasterio

    with rio.open(t_file_day,
                  'r',
                  driver='GTiff') as tif:

        rc_list = []
        for site in sites_dict.items():
            col, row = tif.index(float(site[1][1]), float(site[1][0]))
            rc_list.append((col, row))

        tif_np = tif.read(1)
        tif_np_masked = np.ma.masked_array(tif_np, tif_np == 32767)

        results = []
        for rc in rc_list:
            try:
                result = tif_np_masked[rc]
                results.append(result)
            except IndexError:
                print('No raster value for this pixel/date')
                results.append(np.nan)
    results = np.ma.filled(results, fill_value=np.nan)
    return results


def draw_plot(year, smpl_results_df, fig_dir, prdct, sites_dict):
    sns.set_style('darkgrid')
    smpl_results_df.rename(columns={0: 'id_0', 1: 'id_1', 2: 'id_2', 3: 'id_3', 4: 'id_4'}, inplace=True)

    for site in smpl_results_df.columns.tolist():
        if site != 'doy':

            print(site)
            # Create a seaborn scatterplot (or replot for now, small differences)
            #sct = sns.scatterplot(x='doy', y=site, data=smpl_results_df)
            sct = sns.regplot(x='doy', y=site, data=smpl_results_df, marker='o', label='sw ' ,
                              fit_reg=False, scatter_kws={'color':'darkblue', 'alpha':0.3,'s':20})
            sct.set_ylim(0, 1.0)
            sct.set_xlim(1, 366)
            sct.legend(loc='best')

            # Access the figure, add title
            plt_name = str(year + ' ' + prdct )
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
    #TODO to avoid egregious geolocation errors, I should require the csv to have headers (currently it cannot)
    #and the headers should be id,lat,long, so I can check that the latitude and longitude cols are correct by
    #their name in the csv
    prdct = args.prdct
    base_dir = args.base_dir
    fig_dir = os.path.join(base_dir, "fig")

    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    years = [args.years]
    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    sites_csv_input = os.path.join(base_dir, args.sites_csv_fname)
    sites_dict = {}
    with open(sites_csv_input, mode='r') as sites_csv:
        reader = csv.reader(sites_csv)
        for row in reader:
            key = row[0]
            sites_dict[key] = row[1:]

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

        # Create empty array for mean
        tif_mean = []
        for day in doy_list:
            # Open the ONLY BAND IN THE TIF! Cannot currently deal with multiband tifs
            t_file_list = make_prod_list(base_dir, prdct, year, day)
            file_name = '{in_dir}/{prdct}*{year}{day:03d}*.tif'.format(in_dir=base_dir,
                                                                       prdct=prdct,
                                                                       day=day,
                                                                       year=year)
            # See if there is a raster for the date, if not use a fill value for the graph
            if len(t_file_list) == 0:
                #print('File not found: ' + file_name)
                pixel_values = [np.nan] * len(sites_dict)
            elif len(t_file_list) > 1:
                print('Multiple matching files found for same date! Please remove one.')
                sys.exit()
            else:
                #print('Found file: ' + file_name)
                t_file_day = t_file_list[0]
                # Extract pixel values and append to dataframe
                try:
                    pixel_values = extract_pixel_values(sites_dict, t_file_day)
                    #print(pixel_values)
                except:
                    print('Warning! Pixel out of raster boundaries!')
                    pixel_values = [np.nan] * len(sites_dict)

            tif_mean.append(pixel_values)

        smpl_results_df = pd.DataFrame(tif_mean)
        smpl_results_df['doy'] = doy_list
        cols = smpl_results_df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        smpl_results_df = smpl_results_df[cols]
        smpl_results_df = smpl_results_df * 0.001

        # Do plotting and save output PER YEAR (individual csv per year)
        #TODO this does not work!
        #draw_plot(year, smpl_results_df, fig_dir, prdct, sites_dict)

        # Export data to csv
        os.chdir(fig_dir)
        output_name = str(sites_csv_input[:-4] + '_extracted_values')
        csv_name = str(output_name + '_' + prdct + '.csv')
        #print('writing csv: ' + csv_name)
        #print(year_smpl_cmb_df)
        smpl_results_df.to_csv(csv_name, index=False)


if __name__ == '__main__':
    main()
