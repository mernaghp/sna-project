"""
Visualization and analysis of degree distribution
"""
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

A = np.load('Data/A.npy')
with open('Data/clean.json') as f:
    clean = json.load(f)


def summary_df(axis: int) -> pd.DataFrame:
    unique, counts = np.unique(A.sum(axis=axis), 
                               return_counts=True)    
    df = pd.DataFrame({'Vals': unique, 'Counts': counts})
    df['Percent'] = df['Counts'].div(df['Counts'].sum())
    df['Vals'] = df['Vals'].astype(int)
    return df


def dist(axis: int, xlabel: str) -> plt.Axes:
    df = summary_df(axis)

    fig, ax = plt.subplots()
    df.plot.bar(x='Vals', y='Percent', ax=ax, 
                legend=False, width=1, 
                ylabel='Fraction of nodes', 
                edgecolor='k', linewidth=0.1)
    ax.set_xlabel(xlabel)
    sns.despine()
    return ax


# In-degree: # of pkgs that depend on a given pkg
ax = dist(1, 'In-Degree')
plt.savefig('Images/in-degree.png')


# Out-degree: # of pkgs that a given pkg depends on
ax = dist(0, 'Out-Degree')
plt.savefig('Images/out-degree.png')

# Bullet points for in-degree
df = summary_df(axis=0)
print(df[df['Vals'].between(0, 8)]['Percent'].sum()) # 0.9613

# highest k-in
# python: 378
# vc: 175
# vs2015_runtime: 174
# numpy: 35
# packaging: 33
# zlib: 24

# Bullet points for out-degree
df = summary_df(axis=1)
print(df[df['Vals'].between(0, 11)]['Percent'].sum()) # 0.9511


# highest k-out
print([(k, len(clean[k])) for k in clean.keys() if len(clean[k]) >= 20])
# [('_anaconda_depends', 62),
#  ('anaconda-navigator', 21),
#  ('arrow-cpp', 22),
#  ('conda-build', 20),
#  ('imagecodecs', 29),
#  ('jupyter_server', 20),
#  ('scrapy', 20),
#  ('spyder', 41),
#  ('streamlit', 24)]

print([k for k in clean.keys() if len(clean[k]) == 0])
# k-out == 0
# ['blas',
#  'ca-certificates',
#  'icc_rt',
#  'msys2-conda-epoch',
#  'pybind11-abi',
#  'tzdata',
#  'vs2015_runtime',
#  'winpty']