"""
Network summary measures
"""
import json

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

A = np.load('Data/A.npy')
pkgs = pd.read_csv('Data/package_list.csv')
with open('Data/clean.json') as f:
    clean = json.load(f)
with open('Data/clean_in.json') as f:
    clean_in = json.load(f)


def idx_to_pkg(idx: int) -> str:
    return pkgs['Name'].iloc[idx]


def pkg_to_idx(pkg: str):
    return np.argwhere(pkgs['Name'].eq(pkg)).flatten()[0]


G = nx.from_numpy_array(A, create_using=nx.DiGraph)

# NetworkXError: Graph is not strongly connected.
print(nx.average_shortest_path_length(G))

# NetworkXError: Found infinite path length 
# because the digraph is not strongly connected
print(nx.diameter(G))

print(nx.is_directed_acyclic_graph(G)) # False
print(nx.find_cycle(G)) # [(81, 85), (85, 81)

# crude way to find all cycles
# conda <-> conda-libmamba-solver
# numpy <-> mkl_fft
# numpy <-> mkl_random
for pkg in clean.keys():
    for pkg2 in clean[pkg]:
        if pkg in clean[pkg2]:
            print(pkg, pkg2)

# Clustering coefficient
# Recall that typically the directed nature
# of the network is ignored
print(nx.transitivity(G)) # 0.01115298237600396

# Reciprocity
print(nx.reciprocity(G)) #0.003215434083601286

clustering = nx.clustering(G)
idx_to_pkg(max(clustering, key=clustering.get)) # boltons

mins = [k for k in clustering.keys() 
        if clustering[k] == min(clustering.values())]
for m in mins:
    print(idx_to_pkg(m))

# ca-certificates
# console_shortcut
# icc_rt
# importlib_metadata
# jq
# m2w64-libwinpthread-git
# powershell_shortcut
# pybind11-abi
# tzdata
# winpty

# Local Clustering
for pkg in ['_anaconda_depends', 'anaconda-catalogs', 'anaconda-navigator',
            'anaconda-project', 'conda-build', 'conda-verify', 
            'console_shortcut', 'powershell_shortcut',
            'blas', 'ca-certificates', 'icc_rt', 'msys2-conda-epoch',
            'pybind11-abi', 'tzdata', 'vs2015_runtime', 'winpty']:
    print(pkg, round(clustering[pkg_to_idx(pkg)], 2))

# _anaconda_depends 0.03
# anaconda-catalogs 0.33
# anaconda-navigator 0.11
# anaconda-project 0.16
# conda-build 0.07
# conda-verify 0.1
# console_shortcut 0
# powershell_shortcut 0
# blas 0.23
# ca-certificates 0
# icc_rt 0
# msys2-conda-epoch 0.17
# pybind11-abi 0
# tzdata 0
# vs2015_runtime 0.02
# winpty 0

# k_out
for pkg in ['_anaconda_depends', 'anaconda-catalogs', 'anaconda-navigator',
            'anaconda-project', 'conda-build', 'conda-verify', 
            'console_shortcut', 'powershell_shortcut']:
    print(pkg, len(clean[pkg]))

# _anaconda_depends 62
# anaconda-catalogs 4
# anaconda-navigator 21
# anaconda-project 8
# conda-build 20
# conda-verify 10
# console_shortcut 1
# powershell_shortcut 1

# k_in
for pkg in ['blas', 'ca-certificates', 'icc_rt', 'msys2-conda-epoch',
            'pybind11-abi', 'tzdata', 'vs2015_runtime', 'winpty']:
    print(pkg, len(clean_in[pkg]))

# blas 6
# ca-certificates 1
# icc_rt 2
# msys2-conda-epoch 3
# pybind11-abi 1
# tzdata 1
# vs2015_runtime 174
# winpty 1

# Watts and Strogatz clustering coefficient
# 0.34, signficantly higher than transitivity
print(nx.average_clustering(G)) # 0.34

# Betweenness Centrality
bc = nx.betweenness_centrality(G)
bc_pkg = {idx_to_pkg(k): v for k, v in bc.items()}
bc_sorted = dict(sorted(bc_pkg.items(), key=lambda item: item[1]))

# Eigenvector Centrality
