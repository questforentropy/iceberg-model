"""H1 - edges of the visible universe on an edgeless fabric (user point 3).

The fabric is a closed ring (circumference L): no center, no edges. The stretch
(v3: causal speed declining as the ledger grows) can outrun light: if the reach
integral of c(t) converges, regions exist that are out of even THEORETICAL reach -
the visible universe acquires edges although the fabric has none.

Dichotomy, pre-registered: the horizon's existence depends on the ENTROPY
PRODUCTION CURVE.
  constant load        c = 1               reach ~ t          full contact, fast
  linear ledger growth c = 1/(1+at)        reach ~ ln t       full contact, slow
  exponential growth   c = e^(-bt)         reach -> 1/b       PERMANENT EDGE

H1a  constant and linear laws: every point of the fabric eventually reachable
H1b  exponential law: reach saturates below L/2 - a permanent horizon; the visible
     patch is a fixed fraction of a fabric that has no boundary at all
H1c  no center: with an inhomogeneous fabric, every observer gets the same-SIZED
     patch, but a DIFFERENT one, centered on themselves - the edge is relational
"""

import math


L = 1000.0
ALPHA = 0.01
BETA = 0.01


def c_of(law, t):
    if law == "const":
        return 1.0
    if law == "linear":
        return 1.0 / (1 + ALPHA * t)
    return math.exp(-BETA * t)


def reach(law, T, dt=0.05):
    r, t = 0.0, 0.0
    hit = None
    while t < T:
        r += c_of(law, t) * dt
        t += dt
        if hit is None and r >= L / 2:
            hit = t
    return r, hit


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []
    T = 30000.0

    r_c, hit_c = reach("const", T)
    r_l, hit_l = reach("linear", T)
    R.append(check("H1a", hit_c is not None and hit_l is not None and hit_l > 10 * hit_c,
                   "constant law covers the fabric at t = %.0f; linear ledger growth still "
                   "covers it, but at t = %.0f (x%.0f later) - slower entropy production "
                   "keeps the whole fabric in reach" % (hit_c, hit_l, hit_l / hit_c)))

    r_e, hit_e = reach("exp", T)
    r_half, _ = reach("exp", T / 2)
    frac = 2 * r_e / L
    R.append(check("H1b", hit_e is None and r_e < L / 2 and (r_e - r_half) < 0.1,
                   "exponential ledger growth: reach saturates at %.1f (analytic 1/b = %.0f) "
                   "< L/2 = %.0f - a PERMANENT horizon; visible patch = %.0f%% of an "
                   "edgeless fabric; %.0f%% is out of even theoretical reach"
                   % (r_e, 1 / BETA, L / 2, 100 * frac, 100 * (1 - frac))))

    # H1c: inhomogeneous fabric - every observer gets an equal-sized, DIFFERENT patch
    def patch(x0, amp, T=20000.0, dt=0.05):
        xr = xl = x0
        t = 0.0
        while t < T:
            cr = c_of("exp", t) * (1 + amp * math.sin(2 * math.pi * xr / L))
            cl = c_of("exp", t) * (1 + amp * math.sin(2 * math.pi * xl / L))
            xr += cr * dt
            xl -= cl * dt
            t += dt
        return xl, xr, xr - xl

    def spread_of(amp):
        ps = [patch(x0, amp) for x0 in (0.0, 300.0, 700.0)]
        sizes = [p[2] for p in ps]
        centers = [((p[0] + p[1]) / 2) % L for p in ps]
        return sizes, centers, (max(sizes) - min(sizes)) / (sum(sizes) / len(sizes))

    sizes_h, _, spread_h = spread_of(0.0)          # homogeneous control: exactly equal
    sizes, centers, spread = spread_of(0.05)       # 5% lumpy fabric: spread bounded by it
    distinct = (max(centers) - min(centers)) > 100
    R.append(check("H1c", spread_h < 1e-9 and spread < 0.10 and distinct
                   and all(s < L for s in sizes),
                   "homogeneous fabric: identical patches (spread %.1e); 5%%-lumpy fabric: "
                   "sizes %.0f/%.0f/%.0f (spread %.1f%% - bounded by the lumpiness), centers "
                   "%.0f/%.0f/%.0f - equal horizons, each centered on its observer; the "
                   "fabric has no edge, every observer has their own"
                   % (spread_h, sizes[0], sizes[1], sizes[2], 100 * spread,
                      centers[0], centers[1], centers[2])))

    print()
    print("H1: %s (%d checks) - whether the universe has edges is a property of the "
          "entropy production curve, not of the fabric"
          % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
