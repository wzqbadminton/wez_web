import os, glob, imagehash
from PIL import Image
from collections import defaultdict

paths = sorted(glob.glob('pic/*.jpg'))
hashes = {}
for p in paths:
    try:
        h = imagehash.phash(Image.open(p))
        hashes[p] = h
    except Exception as e:
        print('ERR', p, e)

THRESH = 8  # Hamming distance; <=8 = visually very similar
groups = []
used = set()
items = list(hashes.items())
for i, (p1, h1) in enumerate(items):
    if p1 in used:
        continue
    grp = [p1]
    for p2, h2 in items[i+1:]:
        if p2 in used:
            continue
        d = h1 - h2
        if d <= THRESH:
            grp.append(p2)
            used.add(p2)
    if len(grp) > 1:
        used.add(p1)
        groups.append(grp)

if not groups:
    print('No visually similar pairs (phash distance <= {}).'.format(THRESH))
else:
    print(f'Found {len(groups)} similar group(s):\n')
    for i, g in enumerate(groups, 1):
        print(f'Group {i}:')
        for p in g:
            print('  ', os.path.basename(p))
        print()
