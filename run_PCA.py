import os, argparse, re, seaborn as sns, numpy as np
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Create an array of the vectors
def process_vectors(f_data):
    vectors = []
    for line in f_data:
        line = re.sub(r'\n', '', line) # remove newlines
        vectors.append(line.split('\t')) # add lines on vectors list as nested lists split by tab
    X = np.array(vectors)
    return X

# Create a list from the labels
def process_labels(f_meta):
    labels = []
    for line in f_meta:
        line = re.sub(r'\t', ',', line)
#        print(line.split("\n")[0])
        #print(",".join(
        #print("original", line)
        line = str(line.split("\n")[0].split(",")[0])+","+str(",".join(line.split("\n")[0].split(",")[1:]))
        #print("target", line)
        labels.append(line.split('\n'))
    return labels

def dimensionality_reduction(processed_vectors):
    """ Run the algorithm. """
    pca = PCA(n_components=128)
    processed_vectors = processed_vectors.astype(np.float64)
    pca.fit(processed_vectors)
    # If you want to store the PCA model, uncomment the following pickle dump and add a filepath.
    """import pickle as pk
    with open(###, 'wb') as f:
        pk.dump(pca, f)"""

    model = pca.transform(processed_vectors)
    variance_ratio = pca.explained_variance_ratio_ * 100
    print("Variance explained by the first 1 component: ",
          "{:.2f}".format(np.cumsum(pca.explained_variance_ratio_ * 100)[0]), "%")
    print("Variance explained by the first 2 components: ",
          "{:.2f}".format(np.cumsum(pca.explained_variance_ratio_ * 100)[1]), "%", '\t(', "PC 2",
          "{:.2f}".format(variance_ratio[1]), ') %')
    print("Variance explained by the first 3 components: ",
          "{:.2f}".format(np.cumsum(pca.explained_variance_ratio_ * 100)[2]), "%", '\t(', "PC 3",
          "{:.2f}".format(variance_ratio[2]), ') %')

    """ Uncomment if you want to standardize"""
    #model = StandardScaler().fit_transform(model)"""

    return model

def create_data_set(model, labels):
    """This combines the labels and the model components."""

    model_output = model.tolist() # convert PCA output into list

    # Combine labels and principal components
    pre_dataset = []
    for a, b in zip(labels[1:], model_output):
        pre_dataset.append(a[0]+","+",".join(str(x) for x in b))

    # Create a dataset with a nested list of labels and principal components
    dataset = [i.split(",") for i in pre_dataset]

    return dataset

def create_data_frame(dataset):
    

    # Create a Pandas dataframe
    df = pd.DataFrame(dataset,
                      columns=['Name', 'txt_style', 'set', 'pos', 'textlength', 'Component 1', 'Component 2', 'Component 3', 'Component 4', 'Component 5',
                               'Component 6', 'Component 7', 'Component 8', 'Component 9', 'Component 10', 'Component 11',
                               'Component 12', 'Component 13', 'Component 14', 'Component 15', 'Component 16', 'Component 17',
                               'Component 18', 'Component 19', 'Component 20', 'Component 21', 'Component 22', 'Component 23',
                               'Component 24', 'Component 25', 'Component 26', 'Component 27', 'Component 28', 'Component 29',
                               'Component 30', 'Component 31', 'Component 32', 'Component 33', 'Component 34', 'Component 35',
                               'Component 36', 'Component 37', 'Component 38', 'Component 39', 'Component 40', 'Component 41',
                               'Component 42', 'Component 43', 'Component 44', 'Component 45', 'Component 46', 'Component 47',
                               'Component 48', 'Component 49', 'Component 50', 'Component 51', 'Component 52', 'Component 53',
                               'Component 54', 'Component 55', 'Component 56', 'Component 57', 'Component 58', 'Component 59',
                               'Component 60', 'Component 61', 'Component 62', 'Component 63', 'Component 64', 'Component 65',
                               'Component 66', 'Component 67', 'Component 68', 'Component 69', 'Component 70', 'Component 71',
                               'Component 72', 'Component 73', 'Component 74', 'Component 75', 'Component 76', 'Component 77',
                               'Component 78', 'Component 79', 'Component 80', 'Component 81', 'Component 82', 'Component 83',
                               'Component 84', 'Component 85', 'Component 86', 'Component 87', 'Component 88', 'Component 89',
                               'Component 90', 'Component 91', 'Component 92', 'Component 93', 'Component 94', 'Component 95',
                               'Component 96', 'Component 97', 'Component 98', 'Component 99', 'Component 100', 'Component 101',
                               'Component 102', 'Component 103', 'Component 104', 'Component 105', 'Component 106', 'Component 107',
                               'Component 108', 'Component 109', 'Component 110', 'Component 111', 'Component 112', 'Component 113',
                               'Component 114', 'Component 115', 'Component 116', 'Component 117', 'Component 118', 'Component 119',
                               'Component 120', 'Component 121', 'Component 122', 'Component 123', 'Component 124', 'Component 125',
                               'Component 126', 'Component 127', 'Component 128'])

    return df

def main():
    # open the embedding files
    with open(os.path.join(embedding_file_path), "r") as f_data:
        processed_vectors = process_vectors(f_data)

    # Open the label files
    with open(os.path.join(label_file_path), "r") as f_meta:
        labels = process_labels(f_meta)


    model = dimensionality_reduction(processed_vectors)
    dataset = create_data_set(model, labels)
    dfin = create_data_frame(dataset)

    dfin.to_csv("PCA_embeddings.csv", sep='\t', encoding='UTF-8', index=False)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to run PCA dimensionality reduction and write results to a CSV file.')

    parser.add_argument('-e', '--embedding', type=str, help='Path to the embedding file')
    parser.add_argument('-l', '--label', type=str, help='Path to the label file')

    args = parser.parse_args()

    embedding_file_path = args.embedding
    label_file_path = args.label

    main()
