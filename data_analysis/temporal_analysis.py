############################################################
# The script extracts temporal values from TextGrid files: #
# Filename, the onset of the utterance, speaking rate, and #
# pause to speech ratio.                                   #
############################################################

import argparse, glob, pandas as pd

def durations_extract(filepath):
    Name = []
    onset = []
    pauses = []
    rate = []
    for time_file in glob.glob(filepath+"*.TextGrid"):
        print("Processing duration {}...".format(time_file))
        Name.append(time_file.split("/")[-1][:-9])

        with open(time_file) as f:
            lines = f.readlines()
            file_text = "".join(lines)
            intervals = file_text.split("item")[2].split("intervals")
            duration = float(intervals[-1].split("\n")[2].split(" ")[-1])
            begin = intervals[2].split()[-4]
            #end = lines[4].split()[2]
            #duration = float(end) - float(begin)
            ortographic_len = sum([len(i.split("\"")[1]) for i in intervals[2:]])
            onset.append(begin)
            quiet_words = []
            spoken_words = []
            for i in intervals[2:]:
                text = i.split()
                #print(len(text))
                #if len(text) > 1:
                if text[9] == "\"\"":
                    quiet_words.append(float(text[6])-float(text[3]))
                else:
                    spoken_words.append(float(text[6])-float(text[3]))
            quiet_time = sum(quiet_words)
            spoken_time = sum(spoken_words)
            rate.append(ortographic_len / duration)
            if quiet_time != 0.0:
                pause_ratio = quiet_time / spoken_time
            elif quiet_time == 0.0:
                pause_ratio = 0.0
            pauses.append(pause_ratio)

    dataset = list(zip(Name, rate, onset, pauses))
    df = pd.DataFrame(dataset, columns=['name', 'speechrate', 'onset', 'totalpauses'])
    df.to_csv("temporal_values.csv", sep='\t', encoding='UTF-8', index=False)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to run acoustic analyses on audio files.')

    parser.add_argument('-f', '--folder', type=str, help='Path to the audio files')

    args = parser.parse_args()

    file_path = args.folder

    durations_extract(file_path)
