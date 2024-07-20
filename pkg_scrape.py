"""
Scrapes package dependencies from /info/index.json

Each conda package has an index.json file, in which
the "depends" entry contains that package's dependencies.
These are aggregated for all packages, 
and stored as Data/raw.json.
"""
import json
import os
from pathlib import Path

p = Path('C:/users/patri/anaconda3/pkgs')

folders = [f for f in p.iterdir() if  f.is_dir()]
pkgs_paths = [os.path.join(f, 'info', 'index.json')
        for f in folders if os.path.isfile(os.path.join(f, 'info', 'index.json'))]

data = {}
for pkg_path in pkgs_paths:
    p = Path(pkg_path)
    pkg = p.parts[-3]
    with open(pkg_path) as f:
        data[pkg] = json.load(f)['depends']

with open('Data/raw.json', 'w') as f:
    json.dump(data, f)