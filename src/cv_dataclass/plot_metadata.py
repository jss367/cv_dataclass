
from matplotlib import pyplot as plt



def plot_histo(lst):
    plt.hist(lst, bins=[0, .1, .2, .3, .40, .50,
                        1, 2, 3, 4, 5, 6], rwidth=0.75)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('GSD')
    plt.xticks(rotation=45)
    plt.savefig('test.png')
    #ps = pd.Series(lst)
    #fig = dxp.hist(val='gsd', data=ps)
    #fig.savefig('dxphisto.png')
