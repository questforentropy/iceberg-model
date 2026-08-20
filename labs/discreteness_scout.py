"""Discreteness scout: continuity is never required - but the grain must be random.

The user's claim (knowledge/discrete-vs-continuous-and-the-ruler.md): we don't need a
continuum; an arbitrarily fine grid that passes the rules suffices. Split and tested:

D1  counting layer   on a REGULAR lattice the longest chain between same-interval events
                     is T - X = s*exp(-eta): boost-broken by a factor INDEPENDENT of
                     resolution - fineness can never fix it. A sprinkled set at the same
                     job is boost-invariant. The cure is randomness, not fineness.
D2  dynamics layer   the budget-field rules (bending) CONVERGE under grid refinement -
                     here "arbitrarily fine grid passes the rules" is exactly right.
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spacetime_tests import longest_chain, sprinkle


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def lattice_chain(T, X):
    pts = [(float(t), float(x)) for t in range(T + 1) for x in range(-T, T + 1)
           if t > abs(x) and (T - t) > abs(X - x)]
    return longest_chain(pts, (0.0, 0.0), (float(T), float(X)))


def main():
    R = []
    eta = 0.5

    # D1: the counting layer - regular lattice broken at EVERY density
    ratios = []
    for L in (40, 80):
        T = int(round(L * math.cosh(eta)))
        X = int(round(L * math.sinh(eta)))
        straight = lattice_chain(L, 0)
        boosted = lattice_chain(T, X)
        ratios.append(boosted / straight)
    spr = []
    for run in range(3):
        pts = sprinkle(run, 5000)
        p = (0.15, 0.5)
        s = 0.4
        st = longest_chain(pts, p, (p[0] + s, p[1]))
        bo = longest_chain(pts, p, (p[0] + s * math.cosh(eta), p[1] + s * math.sinh(eta)))
        spr.append(bo / st)
    spr_ratio = sum(spr) / len(spr)
    broken = math.exp(-eta)
    ok1 = (abs(ratios[0] - broken) < 0.05 and abs(ratios[1] - broken) < 0.05
           and spr_ratio > 0.85)
    R.append(check("D1", ok1,
                   "lattice: boosted/straight chain = %.3f (L=40) and %.3f (L=80) - stuck at "
                   "e^-eta = %.3f at BOTH densities, fineness fixes nothing; sprinkled: %.3f "
                   "(boost-invariant). The cure is randomness, not resolution."
                   % (ratios[0], ratios[1], broken, spr_ratio)))

    # D2: the dynamics layer - bending converges under refinement
    def bend(N, iters):
        C = N / 2.0
        y, x = np.mgrid[0:N, 0:N]
        rho = np.zeros((N, N))
        rho[(x - C) ** 2 + (y - C) ** 2 <= (6.0 * N / 128) ** 2] = 1.0
        p = np.zeros((N, N))
        for _ in range(iters):
            p[1:-1, 1:-1] = 0.25 * (p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:]
                                    + p[1:-1, :-2] + rho[1:-1, 1:-1])
        n_field = 1.0 / (1 - 0.08 * p / p.max())
        gy, gx = np.gradient(n_field)

        def bil(a, xx, yy):
            x0, y0 = int(xx), int(yy)
            fx, fy = xx - x0, yy - y0
            return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy)
                    + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)

        ds = 0.1 * N / 128
        xx, yy = 10.0 * N / 128, C + 20.0 * N / 128
        vx, vy = 1.0, 0.0
        lim_lo, lim_hi = 6.0 * N / 128, N - 10.0 * N / 128
        while lim_lo < xx < lim_hi and lim_lo < yy < lim_hi:
            nn = bil(n_field, xx, yy)
            dnx, dny = bil(gx, xx, yy), bil(gy, xx, yy)
            dot = dnx * vx + dny * vy
            vx += ds * (dnx - dot * vx) / nn
            vy += ds * (dny - dot * vy) / nn
            nrm = math.hypot(vx, vy)
            vx, vy = vx / nrm, vy / nrm
            xx += vx * ds
            yy += vy * ds
        return math.atan2(vy, vx)

    a_coarse = bend(96, 9000)
    a_fine = bend(192, 25000)
    rel = abs(a_fine - a_coarse) / abs(a_fine)
    R.append(check("D2", a_coarse < 0 and a_fine < 0 and rel < 0.08,
                   "bending angle %.5f rad at N=96 vs %.5f at N=192 (rel diff %.1f%%) - the "
                   "dynamics rules converge with fineness, exactly as claimed"
                   % (a_coarse, a_fine, 100 * rel)))

    print()
    print("DISCRETENESS: %s (%d checks) - continuity never required; fineness cures dynamics, "
          "randomness cures counting" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
