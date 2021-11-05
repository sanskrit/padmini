import sys

import pstats
from pstats import SortKey


try:
    order = sys.argv[2]
except IndexError:
    order = "tottime"

p = pstats.Stats(sys.argv[1])
p.strip_dirs().sort_stats(order).print_stats(20)
