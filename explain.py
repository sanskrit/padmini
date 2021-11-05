#!/usr/bin/env python
import itertools
import sys
from padmini.constants import Tag as T
from padmini.prakarana import tin_pratyaya as tin
from test.utils import run_all_permutations


code = sys.argv[1]
try:
    target = sys.argv[2]
except IndexError:
    target = None

LA = [
    "la~w",
    "li~w",
    "lu~w",
    "lf~w",
    "lo~w",
    "la~N",
    "ashirlin",
    "li~N",
    "lu~N",
    "lf~N",
]
all_prakriyas = {}
for la, purusha, vacana in itertools.product(LA, tin.PURUSHA, tin.VACANA):
    tags = {purusha, vacana}
    if la == "ashirlin":
        la = "li~N"
        tags.add(T.ASHIH)

    all_prakriyas.setdefault(la, [])
    all_prakriyas[la].extend(run_all_permutations(code, la, tags))

for la in all_prakriyas:
    for p in all_prakriyas[la]:
        if not target or p.text == target:
            print(la, tags)
            p.debug_print()

for la, prakriyas in all_prakriyas.items():
    print(la, [p.text for p in prakriyas])
