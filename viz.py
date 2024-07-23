"""
Visualization of the network and several subgraphs.
"""
# %%
import json
import random

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

# %%
A = np.load('Data/A.npy')
pkgs = pd.read_csv('Data/package_list.csv')
with open('Data/clean.json') as f:
    clean = json.load(f)
with open('Data/clean_in.json') as f:
    clean_in = json.load(f)

# %%
def remove_edges(l: list) -> nx.DiGraph:
    A1 = A.copy()
    for e in l:
        idx = pkgs['Name'].to_list().index(e)
        A1 = np.delete(A1, idx, axis=0)
        A1 = np.delete(A1, idx, axis=1)
    G = nx.from_numpy_array(A1, create_using=nx.DiGraph)
    return G


# %%
# Full network visualization
G = nx.from_numpy_array(A, create_using=nx.DiGraph)
pos = nx.circular_layout(G)
fig, ax = plt.subplots(figsize=(40, 40))
nx.draw_networkx(G, pos=pos, ax=ax)
sns.despine(fig, left=True, bottom=True)
fig.tight_layout()
fig.savefig('Images/full.png', transparent=True)

# %%
l = pkgs['Name'].to_list()
# high k_in
for pkg in ['python', 'vc', 'vs2015_runtime', 
            'numpy', 'packaging']:
    print(pkg + ':', l.index(pkg))

# high k_out
for pkg in ['_anaconda_depends', 'spyder', 'imagecodecs',
            'streamlit', 'arrow-cpp']:
    print(pkg + ':', l.index(pkg))

# %%
# Remove all in-edges from python node
G1 = remove_edges(['python'])
pos = nx.circular_layout(G1)
fig, ax = plt.subplots(figsize=(40, 40))
sns.despine(fig, left=True, bottom=True)
nx.draw_networkx(G1, pos=pos, ax=ax)

# %%
# Discard
G2 = nx.from_numpy_array(A, create_using=nx.DiGraph)
out_degrees = G2.out_degree()
out_edges = list(G2.out_edges())
colors = ['r' if out_degrees[e[0]] >= 20 else 'gray' for e in out_edges] 
widths = [1.5 if out_degrees[e[0]] >= 20 else 0.25 for e in out_edges]

pos = nx.circular_layout(G2)
fig, ax = plt.subplots(figsize=(40, 40))
nx.draw_networkx(G2, pos=pos, ax=ax, 
                 edge_color=colors, width=widths
)

# %%
# numpy and its dependents
G = nx.DiGraph()
G.add_node('numpy')

for dep in clean_in['numpy']:
    if dep != '_anaconda_depends':
        G.add_edge(dep, 'numpy')
        for dep2 in clean[dep]:
            if dep2 in clean_in['numpy']:
                G.add_edge(dep, dep2)

def nudge(pos, x_shift, y_shift):
    return {n:(x + x_shift, y + y_shift) for n,(x,y) in pos.items()}

def plot(direction='out'):
    random.seed(12345)
    np.random.seed(12345)

    if direction == 'out':
        dir_degrees = G.out_degree()
    elif direction == 'in':
        dir_degrees = G.in_degree()

    nodes = G.nodes()
    n_color = np.asarray([dir_degrees[n] for n in nodes])
    labels = {n: n + ', ' + str(dir_degrees[n]) for n in nodes}
    fig, ax = plt.subplots(figsize=(20, 20))
                     
    pos = nx.spring_layout(G, k=0.3)
    pos_nodes = nudge(pos, 0, 0.05)

    nx.draw_networkx(G, pos=pos, arrowstyle='->',
                    edge_color='gray', node_color = n_color,
                    node_size =n_color*100+20, cmap='viridis',
                    style='--', with_labels=False,
                    ax=ax, width=0.5)
    nx.draw_networkx_labels(G, pos=pos_nodes, ax=ax,
                            labels=labels, font_size=22);
    sns.despine(left=True, bottom=True)
    fig.tight_layout()
    fig.savefig(f'Images/numpy_{direction}.png', 
                transparent=True)
    
plot()
plot('in')

# %%
# Degree correlation - unused
k_in = A.sum(axis=1)
k_out = A.sum(axis=0)
fig, ax = plt.subplots()
ax.scatter(k_in, k_out);

# %%
# AWS
aws = pkgs[pkgs['Name'].str[:3].eq('aws')]['Name'].to_list()
G = nx.DiGraph()

for pkg in aws:
    for dep in clean[pkg]:
        G.add_edge(pkg, dep)

random.seed(12345)
np.random.seed(12345)

pos = nx.circular_layout(G)
pos_nodes = nudge(pos, 0, 0.05)

def adjust_pos(pos) -> dict:
    # move all y-positions up
    # adjust x-positions to left or right depending on quadrant
    return

fig, ax = plt.subplots(figsize=(20, 20))
edges = list(G.edges())
colors = ['orange' if (e[0][:3] == 'aws' and e[1][:3] == 'aws') 
          else 'gray' for e in edges]
widths = [2 if color == 'orange' else 0.5 for color in colors]
node_colors = ['orange' if n[:3] == 'aws' else 'gray' for n in G.nodes()]

nx.draw_networkx(G, pos=pos, ax=ax, with_labels=False,
                 edge_color=colors,
                 width=widths,
                 node_color=node_colors)
nx.draw_networkx_labels(G, pos=pos_nodes, ax=ax,
                        font_size=22)
fig.tight_layout()
sns.despine(fig, left=True, bottom=True)
fig.savefig('Images/aws.png', transparent=True)

# %%
# sphinx
sphinx = pkgs[pkgs['Name'].str[:6].eq('sphinx')]['Name'].to_list()

G = nx.DiGraph()

for pkg in sphinx:
    for dep in clean[pkg]:
        G.add_edge(pkg, dep)

random.seed(54321)
np.random.seed(54321)
pos = nx.spring_layout(G, k=0.5)
node_pos = nudge(pos, 0, 0.05)

edges = G.edges()
node_colors = ['b' if n[:6] == 'sphinx' else 'gray' for n in G.nodes()]
colors = ['b' if (e[0][:6] == 'sphinx' and e[1][:6] == 'sphinx') 
          else 'gray' for e in edges]
widths = [2 if color == 'b' else 0.5 for color in colors]


fig, ax = plt.subplots(figsize=(20, 20))
nx.draw_networkx(G, pos, ax=ax, with_labels=False,
                 node_color=node_colors,
                 edge_color=colors,
                 width=widths)
nx.draw_networkx_labels(G, node_pos, ax=ax,
                        font_size=22)
fig.tight_layout()
sns.despine(fig, left=True, bottom=True)
fig.savefig('Images/sphinx.png', transparent=True)

# %%
# jupyter
jup = pkgs[pkgs['Name'].str[:7].eq('jupyter')]['Name'].to_list()

for pkg in jup:
    for dep in clean[pkg]:
        G.add_edge(pkg, dep)
random.seed(12345)
np.random.seed(12345)
G.remove_node('python')
pos = nx.spring_layout(G, k=0.9)
node_pos = nudge(pos, 0, 0.05)
fig, ax = plt.subplots(figsize=(20, 20))
node_colors = ['darkorange' if n[:7] == 'jupyter' 
               else 'gray' for n in G.nodes()]
edges = G.edges()
colors = ['darkorange' if (e[0][:7] == 'jupyter' and e[1][:7] == 'jupyter') 
          else 'gray' for e in edges]
widths = [2 if color == 'darkorange' else 0.5 for color in colors]
in_degrees = G.in_degree()
node_size = np.asarray([in_degrees[n] for n in G.nodes()])
nx.draw_networkx(G, pos, ax=ax, with_labels=False,
                 node_color=node_colors,
                 node_size=node_size*100 + 100,
                 edge_color=colors,
                 width=widths)
nx.draw_networkx_labels(G, node_pos, font_size=22)
sns.despine(fig, left=True, bottom=True)
fig.tight_layout()
fig.savefig('Images/jupyter.png', transparent=True)