#######################################################
# This script visualises PCA components with seaborn. #
#######################################################


import re, argparse, os
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
import sys




def visualize(no_comps_calculate, dfin):
    """  Visualizations of the principal components """

    cmap = ListedColormap(sns.color_palette('tab10'))
    sns.set_palette(sns.color_palette('tab10'))
    sns.set(rc={'figure.figsize': (15, 15)})

    if no_comps_calculate == 1:
        components = []
        ax = sns.kdeplot(data=dfin, x="Component 1", hue='style_label', fill=True,
                    alpha=.6, common_norm=False)  # plot a histogram with kernel density estimation
        ax.get_legend().set_title("Text style")
        plt.setp(ax.get_legend().get_texts(), fontsize='32') # for legend text
        plt.setp(ax.get_legend().get_title(), fontsize='32') # for legend title

    elif no_comps_calculate == 2:
        # Plot 2D scatterplot with Component 1 at x axis and Component 2 at y axis
        sns.scatterplot(data=dfin, x='Component 1', y='Component 2', hue='txt_style', alpha=0.6, size='textlength')

    elif no_comps_calculate == 3:
        # Plot 3D scatterplot
        plot_labels = ['forum', 'caps', 'prose', 'wiki', 'blog', 'fact', 'rich', 'parl']
        fig = plt.figure()
        fig.set_size_inches(15, 15)
        ax = plt.axes(projection='3d')
        xdata = [float(i) for i in dfin['Component 1']]
        ydata = [float(i) for i in dfin['Component 2']]
        zdata = [float(i) for i in dfin['Component 3']]
        scatter = ax.scatter3D(xdata, ydata, zdata, c=dfin.txt_style.astype('category').cat.codes, cmap=cmap,
                               alpha=0.6, depthshade=True)
        plt.legend(handles=scatter.legend_elements()[0],
                   title="txt_styles", labels=plot_labels, loc=1)
    plt.show()


""" Speaking styles divided by formality """

lab_speech = ['richperso', 'richopensub', 'richopensub2', 'richopensub3', 'richmv', 'richnews']

written_informal = ['blogholiday', 'forum1', 'forumecars', 'forumwiki', 'forumwiki2', 'blogbooks', 'blogbooks2', 'blogcorona', 'blogtech', 'factcolor', 'factcopyright', 'factempathy', 'factenvironment', 'factfear', 'facthumanitas', 'factmedia', 'facttheology', 'wikiarts', 'wikibiology', 'wikiblogs', 'wikigeography', 'wikihistory', 'wikijunior']

spoken_informal = ['capsgames', 'capshakanen', 'capsideal', 'capsselko', 'capssome', 'capssexism',  'capswritten',  'parl1', 'parl3']

prose = ['proseaho1', 'prosecarroll', 'prosedoyle', 'prosedumas', 'proseesseys', 'prosefinne', 'prosegogol', 'prosehamsun', 'prosekallas', 'prosekianto', 'prosekrohn', 'prosemontgomery',  'prosetshehov']

fairytales = ['prosetales', 'prosetales2', 'prosetales3']

def calc_new_col(row):
   if row['true_style'] in spoken_informal:
        return 'spoken'
   #elif row['true_style'] in spoken_formal:
    #    return 'spoken_formal'
   elif row['true_style'] in written_informal:
        return 'written'
   elif row['true_style'] in prose:
        return 'Prose'
   #elif row['true_style'] in written_formal:
    #    return 'written_formal'
   elif row['true_style'] in fairytales:
        return 'fairytales'
   elif row['true_style'] in lab_speech:
        return 'lab_speech'




def main(no_comps_calculate, file_path):
    df = pd.read_csv(file_path, sep='\t')
    df["true_style"] = df["txt_style"]+df["set"]
    df["style_label"] = df.apply(calc_new_col, axis=1)
    visualize(no_comps_calculate, df)





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Command line tool to visualize PCA components.')

    parser.add_argument('-f', '--file', type=str, help='Path to the CSV file')
    parser.add_argument('-c', '--components', choices=['1', '2', '3'], type=str, help='Number of components to visualize, 1, 2, or 3')

    args = parser.parse_args()

    file_path = args.file

    no_comps_calculate = int(args.components)

    main(no_comps_calculate, file_path)
