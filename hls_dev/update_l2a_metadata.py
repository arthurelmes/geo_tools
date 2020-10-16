# This is a stopgap script to update the Sentinel-2 L2A metadata that comes from Sen2Cor V 2.08.00, which
# added a new tag relative to version 2.4, and causes the L2A processing date to be used as the
# sentinel albedo output date, rather than the acquisition date

import xml.etree.ElementTree as ET
import os

xml_file = "/media/arthur/Windows/LinuxShare/S2/L2A/" \
           "S2A_MSIL2A_20200502T213531_N9999_R086_T05WPM_20201002T225054.SAFE/GRANULE/" \
           "L2A_T05WPM_A025394_20200502T213532/MTD_TL.xml"

os.chdir('/media/arthur/Windows/LinuxShare/S2/L2A/'
         'S2A_MSIL2A_20200502T213531_N9999_R086_T05WPM_20201002T225054.SAFE/GRANULE/')

tree = ET.parse(xml_file)
root = tree.getroot()


for item in root.findall('*'):
    for child in item:
        #print(child.tag)
        if child.tag == 'L1C_TILE_ID':
            correct_date = child.text.split("_")[7]
        elif child.tag == 'TILE_ID':
            incorrect_date = str(child.text.split("_")[7])
            id_beginning = '_'.join(child.text.split("_")[:7])
            id_end = '_'.join(child.text.split("_")[8:])
            print(child.text)
            child.text = id_beginning + "_" + correct_date + "_" + id_end
            print(child.text)
