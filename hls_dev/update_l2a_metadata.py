# This is a stopgap script to update the Sentinel-2 L2A metadata that comes from Sen2Cor V 2.08.00, which
# added a new tag relative to version 2.4, and causes the L2A processing date to be used as the
# sentinel albedo output date, rather than the acquisition date

import xml.etree.ElementTree as ET
import os, sys


def update_date(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print("updating: {x}".format(x=xml_file))

    for item in root.findall('*'):
        for child in item:
            # Why do some of the names have a __???
            if "__" in child.text:
                index = 7
            else:
                index = 6

            if child.tag == 'L1C_TILE_ID':
                correct_date = child.text.split("_")[index]

            if child.tag == 'TILE_ID':
                # incorrect_date = str(child.text.split("_")[index])
                # print(incorrect_date)
                id_beginning = '_'.join(child.text.split("_")[:index])
                id_end = '_'.join(child.text.split("_")[index + 1:])
                correct_name = id_beginning + "_" + correct_date + "_" + id_end
                child.text = correct_name

            if child.tag == 'DATASTRIP_ID':
                child.text = correct_name

    tree.write(xml_file)


if __name__ == '__main__':
    wk_dir = '/lovells/data02/arthur.elmes/S2/HLS_comparison/22WFV/S2_albedo_test_new_name' #sys.argv[1]
    for root, dirs, files in os.walk(wk_dir):
        for file in files:
            if file == 'MTD_TL.xml':
                print(os.path.join(root, file))
                update_date(os.path.join(root, file))
