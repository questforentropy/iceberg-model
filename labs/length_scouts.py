"""Length scouts (user challenge + thought, 2026-08-16).

L1  gravitational wavelength compression - the user's sketch, measured: in a busy
    (slow) region a wave keeps its frequency, loses speed, so its wavelength
    shrinks - the pattern occupies FEWER NODES. (Distinct from SR contraction.)
L2  Lorentz contraction with no rule - a sine-Gordon kink (episode #7's beast) is
    launched with the WRONG (rest) width at speed v; the lattice wave dynamics
    itself squeezes it to width w0/gamma. Contraction is a property of Lorentzian
    wave equations, not something a grid must be told.
Q1  quasicrystal ruler test (the thought) - is aperiodicity enough for the
    counting layer, or does it take randomness? Lattice vs Fibonacci-product
    quasicrystal vs Poisson sprinkle on the boosted-chain ratio.
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


def main():
    R = []

    # L1: wavelength compression in a slow region (frequency fixed, lambda ~ c)
    Nx, dx, dt = 3000, 0.5, 0.2
    x = np.arange(Nx) * dx
    c = np.where((x > 700) & (x < 1100), 0.7, 1.0)
    phi = np.zeros(Nx)
    prev = np.zeros(Nx)
    period = 40.0
    for s in range(12000):
        t = s * dt
        lap = np.zeros(Nx)
        lap[1:-1] = phi[2:] - 2 * phi[1:-1] + phi[:-2]
        nxt = 2 * phi - prev + (c * dt / dx) ** 2 * lap
        nxt[0] = math.sin(2 * math.pi * t / period)
        nxt[-1] = 0.0
        sponge = x > 1300
        nxt[sponge] = nxt[sponge] * 0.98
        prev, phi = phi, nxt

    def wavelength(lo, hi):
        seg = phi[int(lo / dx):int(hi / dx)]
        zc = np.where(np.diff(np.sign(seg)) != 0)[0]
        return 2 * dx * np.diff(zc).mean()

    lam_fast = wavelength(300, 650)
    lam_slow = wavelength(750, 1050)
    ratio = lam_slow / lam_fast
    R.append(check("L1", abs(ratio - 0.7) < 0.03,
                   "wavelength in the busy region / outside = %.3f (c ratio 0.700) - the "
                   "pattern occupies fewer nodes where compute is busy, exactly the user's "
                   "sketch (gravitational compression, not SR contraction)" % ratio))

    # L2: the lattice enforces Lorentz contraction on a kink launched at the WRONG width
    def kink_width(v_inject):
        N, dxk, dtk = 4000, 0.1, 0.05
        xs = np.arange(N) * dxk
        x0, w0 = 120.0, 1.0
        phi0 = 4 * np.arctan(np.exp((xs - x0) / w0))          # REST profile, width w0
        dphi = np.gradient(phi0, dxk)
        prev = phi0 + dtk * v_inject * dphi                    # moving, uncontracted
        phik = phi0.copy()
        gam = np.zeros(N)
        gam[xs < 30] = 0.2
        gam[xs > 370] = 0.2
        centers = []
        widths = []
        for s in range(int(200 / dtk)):
            lap = np.zeros(N)
            lap[1:-1] = phik[2:] - 2 * phik[1:-1] + phik[:-2]
            nxt = (2 * phik - prev + (dtk / dxk) ** 2 * lap
                   - dtk ** 2 * np.sin(phik) - gam * dtk * (phik - prev))
            nxt[0], nxt[-1] = 0.0, 2 * math.pi
            prev, phik = phik, nxt
            t = s * dtk
            if t > 120:
                i = int(np.argmin(np.abs(phik - math.pi)))
                centers.append((t, xs[i]))
                widths.append(2.0 / np.abs(np.gradient(phik, dxk)).max())
        ts, cs = zip(*centers)
        v_meas = np.polyfit(ts, cs, 1)[0]
        return v_meas, float(np.mean(widths))

    worst = 0.0
    rows = []
    for v in (0.3, 0.5, 0.7):
        v_meas, w = kink_width(v)
        inv = w * (1 / math.sqrt(1 - v_meas ** 2))
        worst = max(worst, abs(inv - 1.0))
        rows.append("v=%.2f: width %.3f, w*gamma = %.3f" % (v_meas, w, inv))
    R.append(check("L2", worst < 0.06,
                   "kink launched at rest-width relaxes to w0/gamma by itself: %s "
                   "(invariant w*gamma = 1 within %.1f%%) - Lorentz contraction with no rule"
                   % ("; ".join(rows), 100 * worst)))

    # Q1: is aperiodicity enough for the ruler? (lattice vs quasicrystal vs sprinkle)
    eta = 0.5
    # product sets in light-cone coordinates: longest chain = min(#u-points, #v-points)
    def fib_positions(n_iters=18):
        word = "A"
        for _ in range(n_iters):
            word = "".join("AB" if ch == "A" else "A" for ch in word)
        steps = [(1 + math.sqrt(5)) / 2 if ch == "A" else 1.0 for ch in word]
        pos = np.cumsum([0.0] + steps)
        return pos / pos[-1]                     # normalized to [0, 1]

    def count_in(positions, span):
        return int((positions < span).sum())

    fib = fib_positions()
    K = count_in(fib, 1.0 / math.cosh(eta) ** 2)  # straight diamond u,v spans
    ratios = {}
    for name, pts in (("lattice", np.linspace(0, 1, len(fib))), ("fibonacci", fib)):
        straight = min(count_in(pts, 0.5), count_in(pts, 0.5))
        span_u = min(0.5 * math.exp(eta), 1.0)
        span_v = 0.5 * math.exp(-eta)
        boosted = min(count_in(pts, span_u), count_in(pts, span_v))
        ratios[name] = boosted / straight
    spr = []
    for run in range(3):
        pts = sprinkle(run, 5000)
        p, s = (0.15, 0.5), 0.4
        st = longest_chain(pts, p, (p[0] + s, p[1]))
        bo = longest_chain(pts, p, (p[0] + s * math.cosh(eta), p[1] + s * math.sinh(eta)))
        spr.append(bo / st)
    spr_ratio = sum(spr) / len(spr)
    broken = math.exp(-eta)
    ok = (abs(ratios["lattice"] - broken) < 0.05 and abs(ratios["fibonacci"] - broken) < 0.05
          and spr_ratio > 0.85)
    R.append(check("Q1", ok,
                   "boosted/straight chain: lattice %.3f, Fibonacci quasicrystal %.3f - BOTH "
                   "stuck at e^-eta = %.3f; sprinkle %.3f. Aperiodicity is not the cure; the "
                   "ruler needs randomness. (Caveat: product construction; 8-fold tilings "
                   "conjectured same - discrete orientational symmetry obstructs boosts.)"
                   % (ratios["lattice"], ratios["fibonacci"], broken, spr_ratio)))

    print()
    print("LENGTH: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
