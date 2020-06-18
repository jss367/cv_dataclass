
from matplotlib import pyplot as plt
import numpy as np
import pickle


def plot_histo(lst, max_padding=0.1):
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 12)
    bins = np.arange(0, max(lst) + max_padding, 0.1)
    plt.hist(lst, bins=bins, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('GSD (in meters)')
    plt.xticks(rotation=45)
    plt.savefig('test.png')


def plot_boxplot(lst):
    plt.boxplot(lst, vert=False)
    plt.savefig('boxplot.png')


if __name__ == "__main__":

    with open('gsd.pkl', 'rb') as f:
        gsd = pickle.load(f)

    plot_histo(gsd)