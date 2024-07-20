"""
Creates adjacency matrix and edgelists from raw.json.

Outputs:
--------
* A.py: adjacency matrix
* clean.json: out-edge list
* clean_in.json: in-edge list

Cleans the raw package info from raw.json,
stripping away any version-specific info.
Maps the clean package name to its raw name,
and creates a clean out-edge list.
Creates the adjacency matrix.
Creates a clean in-edge list.
"""
import json

import numpy as np
import pandas as pd

with open('Data/raw.json') as f:
    data = json.load(f)

pkgs = pd.read_csv('Data/package_list.csv')

print(len(pkgs)) # 491
print(sum([len(v) for v in data.values()])) # 1882

raw = list(data.keys())
raw.sort()

clean = pkgs['Name'].to_list()
clean.sort()

# Double-check that (sorted) clean
# corresponds to (sorted) raw
print(all([c in r for c, r in zip(clean, raw)]))

clean_to_raw = {k: v for k, v in zip(clean, raw)}

# Double check that clean packages map to the dirty dependencies
lst = [l for ls in data.values() for l in ls]

# Split on space and take the first element
c = set([l.split()[0] for l in lst])

# 8 packages not in dependecies
# '_anaconda_depends',
#  'anaconda-catalogs',
#  'anaconda-navigator',
#  'anaconda-project',
#  'conda-build',
#  'conda-verify',
#  'console_shortcut',
#  'powershell_shortcut
print(set(clean) - c)

# python is a requirement of 411 of the packages
# actually there's some duplicate links
# so this is overstated
count = 0
for v in data.values():
    for _ in v:
        if 'python' in _:
            count += 1
print(count)

out = {}
for c in clean:
    l = []
    for e in data[clean_to_raw[c]]:
        l.append(e.split()[0])
    out[c] = l

with open('Data/clean.json', 'w') as f:
    json.dump(out, f)

# Aij is 1 if there is a dependency of i on j
# Opposite of Newman book but what networkx expects
A = np.zeros((len(clean), len(clean)))
for k, v in out.items():
    j = clean.index(k)
    for _ in v:
        i = clean.index(_)
        A[i, j] = 1

np.save('Data/A.npy', A)

# find duplicate dependencies
for k, v in out.items():
    if len(v) != len(set(v)):
        print(k, v)

clean_in = {}
for pkg in pkgs['Name']:
    clean_in[pkg] = []

for k, v in clean.items():
    for val in v:
        clean_in[val].append(k)

with open('Data/clean_in.json', 'w') as f:
    json.dump(clean_in, f)