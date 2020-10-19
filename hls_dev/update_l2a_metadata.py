# This is a stopgap script to update the Sentinel-2 L2A metadata that comes from Sen2Cor V 2.08.00, which
# added a new tag relative to version 2.4, and causes the L2A processing date to be used as the
# sentinel albedo output date, rather than the acquisition date

import xml.etree.ElementTree as ET
import os


def update_date(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print("updating: {x}".format(x=xml_file))
    for item in root.findall('*'):
        for child in item:
            if child.tag == 'L1C_TILE_ID':
                correct_date = child.text.split("_")[6]
            elif child.tag == 'TILE_ID':
                incorrect_date = str(child.text.split("_")[6])
                id_beginning = '_'.join(child.text.split("_")[:6])
                id_end = '_'.join(child.text.split("_")[7:])
                print(incorrect_date)
                print(correct_date)

                child.text = id_beginning + "_" + correct_date + "_" + id_end

                print(id_beginning + "_" + correct_date + "_" + id_end)
    tree.write(xml_file)
    print()


if __name__ == '__main__':
    wk_dir = '/home/arthur/Desktop/S2_meta/'
    for root, dirs, files in os.walk(wk_dir):
        for file in files:
            if file == 'MTD_TL.xml':
                print(os.path.join(root, file))
                update_date(os.path.join(root, file))
