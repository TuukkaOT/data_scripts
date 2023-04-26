#####################################################
# This script runs acoustic analyses on audiofiles  #
# using parselmouth that calls Praat and saves them #
# as CSV files.                                     #
#####################################################

import parselmouth.praat
import os, argparse, parselmouth, os.path, pandas as pd


def main():

    name = []
    txt_style = []
    mean = []
    deviation = []
    minimum = []
    maximum = []
    f0_range = []
    slope = []
    tilt = []
    mean_intensity = []
    f0min = 75
    f0max = 400
    unit = "semitones re 100 Hz"

    #for wave_file in glob.glob("/home/tt/Desktop/Työ/wavs/*.wav"):
    for wave_file in os.listdir(file_path):
        if wave_file.endswith(".wav"):
            print("Processing {}...".format(wave_file))
            sound = parselmouth.Sound(file_path+wave_file)
            duration = parselmouth.praat.call(sound, "Get total duration")  # duration
            pitch = parselmouth.praat.call(sound, "To Pitch", 0.0, f0min, f0max)  # create a praat pitch object
            intensity = parselmouth.praat.call(sound, "To Intensity", 100, 0.0)  # create a praat intensity object
            ltas = parselmouth.praat.call(sound, "To Ltas", 100)
            intensity_m = parselmouth.praat.call(intensity, "Get mean...", 0.0, 0.0)
            spectral_tilt = parselmouth.praat.call(ltas, "Get slope", 0,1000,1000,4000, 'energy')  # get mean pitch
            meanF0 = parselmouth.praat.call(pitch, "Get mean", 0, 0, unit)  # get mean pitch
            stdevF0 = parselmouth.praat.call(pitch, "Get standard deviation", 0, 0, "semitones")  # get standard deviation
            min_f0 = parselmouth.praat.call(pitch, "Get minimum", 0, 0, unit, 'Parabolic')  # get minimum pitch
            max_f0 = parselmouth.praat.call(pitch, "Get maximum", 0, 0, unit, 'Parabolic')  # get maximum pitch
            slope_f0 = parselmouth.praat.call(pitch, "Get mean absolute slope", "semitones")  # get mas

            txt_style.append((str(wave_file[26:].split("_")[0])))
            name.append(str(wave_file.split("/")[6:])[2:-6])

            mean.append(meanF0)
            tilt.append(spectral_tilt)
            deviation.append(stdevF0)
            minimum.append(min_f0)
            maximum.append(max_f0)
            f0_range.append(max_f0-min_f0)
            slope.append(slope_f0)
            mean_intensity.append(intensity_m)
    df = pd.DataFrame(list(zip(name, txt_style, mean, deviation, minimum, maximum, f0_range, slope, tilt, mean_intensity)),
                columns =['Name', "txt_style", 'F0 mean', 'F0 SD', 'Minimum F0', 'Maximum F0', 'F0 range', 'Mean absolute slope', 'Tilt', "Mean intensity"])
    df.to_csv("acoustic_values.csv", sep='\t', encoding='UTF-8', index=False)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to run acoustic analyses on audio files.')

    parser.add_argument('-f', '--folder', type=str, help='Path to the audio files')

    args = parser.parse_args()

    file_path = args.folder

    main()
