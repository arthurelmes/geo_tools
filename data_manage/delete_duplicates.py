# simple script to delete duplicated LC8 scenes based on scene id
# Author: Arthur Elmes, 2020-02-25

import os, glob, sys

def main(wkdir):
    print("Deleting duplicates in: " + str(wkdir))
    while True:
        num_files = 0
        num_dupes = 0
        dupe_state = 1

        for root, dirs, files in os.walk(wkdir):
            num_files = len(files)
            for file_name in files:
                # Strip off the end of the file name, since it is always different
                file_name = str(file_name[:22] + "*")

                # Find any identical product ids
                file_name_list = glob.glob(os.path.join(root, file_name))

                # Count up how many files there are, including duplicates
                num_dupes = num_dupes + len(file_name_list)

                # If there are duplicates, delete the second (could be first,
                # doesn't matter.
                if len(file_name_list) > 1:
                    os.remove(file_name_list[1])

        # Keep looping until the number of files and 'duplicates' is
        # equal, in case of multiple duplicates
        if num_files == num_dupes:
            break

if __name__ == "__main__":
    main(sys.argv[1])
