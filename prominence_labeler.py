import os, re, random, argparse
import numpy as np


def calculate_percentiles(prominence_file_path):
    """Calculates 30, 60 and 90 percentiles from the prominence values of the whole data."""

    # Create an empty list to store the index 5 values, i.e. prominence.
    index_5_values = []

    # Iterate through all the .prom files in the directory
    for filename in os.listdir(prominence_file_path):
        if filename.endswith(".prom"):
            file_path = os.path.join(prominence_file_path, filename)
            with open(file_path) as f:
                prom_list_f = [x.split("\t") for x in list(f)]

                for i in prom_list_f:
                    index_5_values.append(float(i[5]))
                # Append the value at index 5 to the index_5_values list

    percentile_values = np.percentile(index_5_values, [30, 60, 90])
    return percentile_values



def remove_whitespace(s):
    """Removes excess white space."""

    s = re.sub(r'^\s*"', '"', s)

    inside_quote = False
    result = []
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i-1] != '\\'):
            inside_quote = not inside_quote
        elif inside_quote:
            if c == ' ' and s[i-1] == '"':
                continue  # skip whitespace after opening quote
            elif c == ' ' and s[i+1] == '"':
                continue  # skip whitespace before closing quote
        result.append(c)
    s = "".join(result)

    # remove excess whitespace
    s = re.sub(r'(?<=[\s?!])"+(?!\w)', '"', s)

    return s

def change_value(value):
    """
    Categorize a numeric value based on percentile ranking using three thresholds. Four categories.
    """
    if value < percentiles[0]:
        return 0
    elif value <= percentiles[1]:
        return 1
    elif value <= percentiles[2]:
        return 2
    else:
        return 3

def main():

    global percentiles

    """ Calculate the percentiles for the dataset. """
    percentiles = calculate_percentiles(prominence_file_path)

    modified_files = 0

    # Iterate through all files in the .txt directory
    for file_name in os.listdir(transcription_file_path):
        #if modified_files == 10:
            #break

        # Open text file.
        if file_name.endswith(".txt"):
            with open(os.path.join(transcription_file_path, file_name), "r") as txt_file:
                txt_line = txt_file.readline()
                txt_words_list = []

                # Open prominence file.
            with open(os.path.join(prominence_file_path, file_name[:-4] + ".prom"), "r") as prom_file:
                # Split the line into words and punctuation.
                txt_words = [w for w in re.findall(r'(?:[-:]\w+)*|\w+(?:[-:]\w*)*|\W', txt_line) if w.strip()]

                finnish_alphabet = re.compile(r'[A-Za-zÄäÖöÅå]')

                prom_list = [string.split("\t") for string in list(prom_file)]  # convert prom_file to a list
                #print(prom_list)

                past_words = []
                new_txt_words = []
                txt_word_count = 0
                # Iterate through the .txt file.
                for txt_word in txt_words:
                    txt_word_count +=1
                    # If word is punctuation then skip it.
                    if not finnish_alphabet.search(txt_word):
                        new_txt_words.append(txt_word)
                        continue


                    w_count = 0
                    past_words.append(txt_word)
                    word_instances = past_words.count(txt_word)
                    for i in prom_list:
                        if i[4] == txt_word:
                            w_count+=1
                            if w_count == word_instances:
                                #print(i[0])
                                new_value_5 = change_value(float(i[5]))


                    """ This randomises the possibility of labeling the word, 20% possibility of labeling the word. """

                    random_num = random.randint(0, 100)
                    # Append the modified value to the word.
                    if new_value_5 == 3:
                        if txt_word_count != 1:
                            if random_num > 66:
                                txt_word = str(new_value_5) + txt_word
                    elif random_num > 80:
                        txt_word = str(new_value_5) + txt_word

                    # Append the modified word to a new list.
                    new_txt_words.append(txt_word)

                    # check if this is the last word in the list and prepend value if it is
                    if txt_word == txt_words[-1]:
                        new_txt_words[-1] = str(new_value_5) + new_txt_words[-1]


                new_txt_line = " ".join(new_txt_words)
                new_txt_line = re.sub(r'(\w)\s+(?![\'":\-])([\W()])', r'\1\2', new_txt_line)
                txt_words_list.append(new_txt_line)

            final_text = remove_whitespace("\n".join(txt_words_list))
            # write the modified text to the file
            with open(os.path.join(output_file_path, file_name), "w") as txt_file:
                txt_file.write(final_text)

            modified_files += 1



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to label prominence categories on transcripts.')

    parser.add_argument('-t', '--transcription', type=str, help='Path to the transcription file')
    parser.add_argument('-p', '--prominence', type=str, help='Path to the prominence file')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file')

    args = parser.parse_args()

    transcription_file_path = args.transcription
    prominence_file_path = args.prominence
    output_file_path = args.output

    main()
