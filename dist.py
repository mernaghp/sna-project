# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# %%
A = np.load('Data/A.npy')

def dist(axis: int, title: str) -> plt.Axes:
    unique, counts = np.unique(A.sum(axis=axis), 
                               return_counts=True)
    df = pd.DataFrame({'Vals': unique, 'Counts': counts})
    df['Percent'] = df['Counts'].div(df['Counts'].sum())
    df['Vals'] = df['Vals'].astype(int)

    fig, ax = plt.subplots()
    df.plot.bar(x='Vals', y='Percent', ax=ax, 
                legend=False, width=1, xlabel='x',
                ylabel='P(x)')
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    ax.set_title(title)
    sns.despine()
    return ax


# %%
# From the perspective
# that x number of other packages depend 
# on any given package 
# in-edges
dist(1, 'Probability Distribution: # of in-edges');

# %%
# From the perspective
# What is the probability that any given package
# has x number of dependents
# out-edges
dist(0, 'Probability Distribution: # of out-edges');