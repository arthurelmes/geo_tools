
Created by Arthur Elmes 6/28/2018
arthur.elmes@gmail.com

## Introduction
This repo contains assorted tools (python and bash) used for EO data management and analysis. The tools are currently in development using
MODIS, VIIRS, Landsat, and Sentinel-2 data. Please report any problems you find, and feel free to submit pull requests if you would like to
contribute.

Note that many of these scripts are provisional and under development. Thus many still require manual modification of parameters prior to use.
Please note! The downloading tools require that you configure a .netrc file in your home directory, because the data require authorization to download.
You can get a free account here: https://go.nasa.gov/3ciWcUx
A .netrc file looks like this: machine urs.earthdata.nasa.gov login <enter your user name here> password <enter your password here>

## Purpose

This repo is designed to facilitate typical EO downloading, processing, and analytical workflows. These tools have been developed on an as-needed basis.
Please contact me if you have any doubt as to their intended purpose or design.

## How to Contribute

Pull requests are welcome! There is a lot still left to do. Please fork the repo, and make a pull request for review.