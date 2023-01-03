#!/usr/bin/env python3

import sys
from itertools import combinations_with_replacement, permutations
combis=([''.join(p) for p in combinations_with_replacement(sys.argv[1], int(sys.argv[2]))])
print("%d combis" % len(combis))
for combi in combis:
    perms=([''.join(p) for p in permutations(combi)])
    for word in perms:
        start = word[0].upper()
        print(word)
        print(start + word[1:])
