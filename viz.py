# %%
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

# %%
A = np.load('Data/A.npy')
pkgs = pd.read_csv('Data/package_list.csv')

# %%
G = nx.from_numpy_array(A, create_using=nx.DiGraph)

# %%
fig, ax = plt.subplots()
nx.draw_networkx(G, ax=ax)

# %%
idx = pkgs['Name'].to_list().index('python')

A1 = np.delete(A, idx, axis=0)
A1 = np.delete(A1, idx, axis=1)

# %%
G1 = nx.from_numpy_array(A1, create_using=nx.DiGraph)

# %%
pos = nx.spring_layout(G, k=0.3)
fig, ax = plt.subplots(figsize=(20, 20))
nx.draw_networkx(G1, pos=pos, ax=ax)

# %%
pos = nx.circular_layout(G)
fig, ax = plt.subplots(figsize=(40, 40))
nx.draw_networkx(G, pos=pos, ax=ax)

# %%
pos = nx.circular_layout(G1)
fig, ax = plt.subplots(figsize=(40, 40))
nx.draw_networkx(G1, pos=pos, ax=ax)

# %%
idxs = np.where(A.sum(axis=1) > 20)
A2 = A.copy()
A2[idxs, :] = 0
A2[:, idxs] = 0
G2 = nx.from_numpy_array(A2, create_using=nx.DiGraph)
pos = nx.circular_layout(G2)
fig, ax = plt.subplots(figsize=(40, 40))
nx.draw_networkx(G2, pos=pos, ax=ax)

# %%
# highest number of in-edges
# python: 378
# vc: 175
# vs2015_runtime: 174
# numpy: 35
# packaging: 33
# zlib: 24