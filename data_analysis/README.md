All of the scripts take arguments. Check the arguments by running the script with -h flag. Small example datasets are located in the datasets folder.

- *acoustic_analysis.py* runs a set of prosodically linked acoustic analyses on a speech corpus. It takes .wav audio files as input. An example dataset is in datasets/wavs/ folder
- *temporal_analysis.py* analyses temporal features of audio files. It requires TextGrid files as input. E.g., aligned with [WebMAUS](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSBasic). Example dataset is located in the datasets/TextGrids/ folder
- *extract_prominent_syllables.py* looks for the most prominent syllables in prominence files that have been extracted with the [Wavelet Prosody Toolkit](https://github.com/asuni/wavelet_prosody_toolkit) by Suni et al.
- *prominence_labeler.py* annotates transcripts according to the prominence files.
- *dimensionality_reduction.py* runs a dimensionality reduction algorith, PCA, T-SNE, or UMAP, on the latent space of a neural speech synthesizer and outputs the three first components. Takes two files as its input, one with a set of 128-dimensional vectors and one with metadata on the vectors, such as style of the utterance. You can use the tiny example dasasets: example_metalabels.lab and example_embeddings.lab as input.
- *pca_visualization.py* plots the three first components on a 1-3 dimensional plane. Takes the dataframe created by dimensionality_reduction.py as input.
