################################################################
# This script runs a dimensionality reduction algorithm on     #
# the latent prosody space output of a Tacotron 2, or similar, #
# speech synthesiser and outputs the first three components on #
# a CSV file. You can choose between PCA, T-SNE and UMAP       #
# algorithms.                                                  #
################################################################


import os, argparse, re, seaborn as sns, numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
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

def dimensionality_reduction(processed_vectors, model_method):
    """ Run the algorithm. """
    if model_method == "PCA":
        method = PCA(n_components=3)
    elif model_method == "TSNE":
        method = TSNE(n_components=3)
    elif model_method == "UMAP":
        method = umap.UMAP(n_components=3)
    processed_vectors = processed_vectors.astype(np.float64)
    method.fit(processed_vectors)
    # If you want to store the PCA model, uncomment the following pickle dump and add a filepath.
    """import pickle as pk
    with open(###, 'wb') as f:
        pk.dump(pca, f)"""
    if model_method == "PCA":
        model = method.transform(processed_vectors)
        variance_ratio = method.explained_variance_ratio_ * 100
        print("Variance explained by the first 1 component: ",
            "{:.2f}".format(np.cumsum(method.explained_variance_ratio_ * 100)[0]), "%")
        print("Variance explained by the first 2 components: ",
            "{:.2f}".format(np.cumsum(method.explained_variance_ratio_ * 100)[1]), "%", '\t(', "PC 2",
            "{:.2f}".format(variance_ratio[1]), ') %')
        print("Variance explained by the first 3 components: ",
            "{:.2f}".format(np.cumsum(method.explained_variance_ratio_ * 100)[2]), "%", '\t(', "PC 3",
            "{:.2f}".format(variance_ratio[2]), ') %')
    else:
        model = method.fit_transform(processed_vectors)

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
                      columns=['Name', 'txt_style', 'set', 'pos', 'textlength', 'Component 1', 'Component 2', 'Component 3'])

    return df

def main():
    # open the embedding files
    with open(os.path.join(embedding_file_path), "r") as f_data:
        processed_vectors = process_vectors(f_data)

    # Open the label files
    with open(os.path.join(label_file_path), "r") as f_meta:
        labels = process_labels(f_meta)


    model = dimensionality_reduction(processed_vectors, model_method)
    dataset = create_data_set(model, labels)
    dfin = create_data_frame(dataset)

    dfin.to_csv("reduced_embeddings.csv", sep='\t', encoding='UTF-8', index=False)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to run PCA dimensionality reduction and write results to a CSV file.')

    parser.add_argument('-e', '--embedding', type=str, help='Path to the embedding file')
    parser.add_argument('-l', '--label', type=str, help='Path to the label file')
    parser.add_argument('-m', '--method', choices=['PCA', 'TSNE', 'UMAP'], type=str, help='Choose method: PCA, TSNE or UMAP (case sensitive)')

    args = parser.parse_args()

    embedding_file_path = args.embedding
    label_file_path = args.label
    model_method = args.method

    main()
