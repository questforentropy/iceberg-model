"""DS-3: the last grain tell - statistical blur - fades with fineness
(V3 completion campaign, 2026-08-17).

A sprinkled grain has no preferred frame (D1/Q1), but it still jitters travel
times statistically. The tell is harmless only if it SHRINKS as the grain
refines: measure the relative travel-distance jitter at two densities.
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sphere_gr_scout import adjacency, dijkstra, knn_edges, sphere_points


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def jitter(n, runs=2, k=14):
    spreads = []
    for run in range(runs):
        pts = sphere_points(10 + run, n)
        ang = np.arccos(np.clip(pts @ pts.T, -1.0, 1.0))
        ei, ej, elen = knn_edges(ang, k)
        adj = adjacency(n, ei, ej, elen)
        d = dijkstra(adj, n, 0)
        m = (ang[0] > 0.5) & (ang[0] < 2.5)
        eta = (d[m] * ang[0][m]).sum() / (ang[0][m] ** 2).sum()
        spreads.append(float(np.std(d[m] / (eta * ang[0][m]) - 1.0)))
    return float(np.mean(spreads))


def main():
    R = []
    j_coarse = jitter(1000)
    j_fine = jitter(4000)
    expo = math.log(j_coarse / j_fine) / math.log(4.0)
    R.append(check("DS3", j_fine < 0.8 * j_coarse,
                   "travel-time jitter: %.4f at n=1000 -> %.4f at n=4000 (falls as "
                   "density^-%.2f) - the last grain tell is statistical blur, and it "
                   "fades with fineness: any finite observational precision can be "
                   "out-run by a finer sprinkle" % (j_coarse, j_fine, expo)))
    print()
    print("DS-BLUR: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
