#############################################################
# This script goes through prominence files that            #
# contain all the text from transcripts and every syllable's#
# prominence values. It checks the two first syllables      #
# of a word and takes the higher prominence value.          #
# It then overwrites the original prominence file           #
# to only contain the highest value for every               #
# word. This prominence file is then used by                #
# the prominence_labeller.py script to label                #
# the transcripts with prominence categories.               #
#############################################################

import os, argparse, numpy as np

# Iterate through the prominence files

def main(prominence_file_path):
    for filename in os.listdir(prominence_file_path):
        if filename.endswith(".prom"):
            file_path = os.path.join(prominence_file_path, filename)
            with open(file_path) as f:

                # Delete silences
                prominence_list_f = [x for x in list(f) if not x.strip().split("\t")[3] == "<p:>"]
                list_of_lists_f = [string.split("\t") for string in prominence_list_f]

                """ Make a nested list that keeps the order intact and groups syllables by word. """
                prom_list_f = []
                temp_list_f = []
                prev_val_f = None

                for item in list_of_lists_f:
                    if prev_val_f != item[4] and temp_list_f:
                        prom_list_f.append(temp_list_f)
                        temp_list_f = []
                    temp_list_f.append(item)
                    prev_val_f = item[4]
                if temp_list_f:
                    prom_list_f.append(temp_list_f)

                """ Take first two syllables. """
                prom_list_f = [x[:2] for x in prom_list_f]

                """ Take the syllable with the higher prominence value. """
                for i in range(len(prom_list_f)):
                    sublist_1 = prom_list_f[i][0]
                    if len(prom_list_f[i]) == 1:
                        prom_list_f[i] = [sublist_1]
                        continue
                    sublist_2 = prom_list_f[i][1]
                    if sublist_1[5] >= sublist_2[5]:
                        prom_list_f[i] = [sublist_1]
                    else:
                        prom_list_f[i] = [sublist_2]

                flattened_list = [value for sublist in prom_list_f for value in sublist]
                final_flattened_list = ["\t".join(i) for i in flattened_list]
                final_text = "".join(final_flattened_list)

                # write the modified text to the file
                with open(os.path.join(output_file_path, filename), "w") as prom_file:
                    prom_file.write(final_text)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to label prominence categories on transcripts.')

    parser.add_argument('-p', '--prominence', type=str, help='Path to the prominence file')
    parser.add_argument('-o', '--output', type=str, help='Path to the output folder')
    args = parser.parse_args()
    prominence_file_path = args.prominence
    output_file_path = args.output
    main(prominence_file_path)
