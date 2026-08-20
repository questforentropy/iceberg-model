"""Tier 4: emergent spacetime (manifest P8, O3).

Q10 light cone     gossip reach after k rounds = exactly distance k
Q11 dilation       PRE-REGISTERED PREDICTION: budget model tau = T(1-v) MISMATCHES
                   Lorentz sqrt(1-v^2) (pass = predicted failure confirmed);
                   sprinkled-DAG longest chain: boost-invariant, linear in interval
Q12 photon         near-null pairs: chain length collapses vs timelike
"""

import hashlib
import math


def H(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def u01(seed_hex):
    return int(seed_hex, 16) / float(1 << 256)


def check(label, ok, detail):
    print("%-6s %-6s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def sprinkle(run, n):
    return [(u01(H("sprinkle", run, i, "t")), u01(H("sprinkle", run, i, "x")))
            for i in range(n)]


def longest_chain(points, p, q):
    tp, xp = p
    tq, xq = q
    interior = [(t, x) for t, x in points
                if (t - tp) > abs(x - xp) and (tq - t) > abs(x - xq)]
    interior.sort()
    L = [1] * len(interior)
    for i in range(len(interior)):
        ti, xi = interior[i]
        best = 0
        for j in range(i):
            tj, xj = interior[j]
            if (ti - tj) > abs(xi - xj) and L[j] > best:
                best = L[j]
        L[i] = best + 1
    return max(L) if L else 0


def main():
    R = []

    # Q10: sharp light cone from nearest-neighbor gossip
    N = 41
    src = N // 2
    informed = {src}
    sharp = True
    for k in range(1, 15):
        informed = informed | {i + 1 for i in informed if i + 1 < N} \
                            | {i - 1 for i in informed if i - 1 >= 0}
        if informed != {i for i in range(N) if abs(i - src) <= k}:
            sharp = False
    R.append(check("Q10", sharp, "reach after k rounds = exactly distance k, 14 rounds checked"))

    # Q11a: budget scheduler vs Lorentz (prediction: MISMATCH)
    T = 2000
    max_gap = 0.0
    rows = []
    for v10 in range(1, 10):
        v = v10 / 10.0
        hops = 0
        acc = 0.0
        for _ in range(T):
            acc += v
            if acc >= 1.0:
                acc -= 1.0
                hops += 1
        tau_budget = (T - hops) / T
        tau_lorentz = math.sqrt(1 - v * v)
        gap = abs(tau_budget - tau_lorentz)
        max_gap = max(max_gap, gap)
        if v10 in (3, 5, 7):
            rows.append("v=%.1f: budget %.3f vs Lorentz %.3f" % (v, tau_budget, tau_lorentz))
    R.append(check("Q11a", max_gap > 0.25,
                   "PREDICTED FAILURE CONFIRMED, max gap %.3f; %s" % (max_gap, "; ".join(rows))))

    # Q11b: sprinkled DAG - boost invariance and linearity in the interval
    NPTS, NRUNS = 5000, 5
    p = (0.05, 0.5)
    svals = [0.28, 0.42, 0.56]
    etas = [0.0, 0.4, 0.8]
    means = {}
    for s in svals:
        for eta in etas:
            q = (p[0] + s * math.cosh(eta), p[1] + s * math.sinh(eta))
            tot = 0
            for run in range(NRUNS):
                tot += longest_chain(sprinkle(run, NPTS), p, q)
            means[(s, eta)] = tot / NRUNS
    boost_ok = True
    spreads = []
    for s in svals:
        ls = [means[(s, e)] for e in etas]
        spread = (max(ls) - min(ls)) / (sum(ls) / len(ls))
        spreads.append("s=%.2f: L=%s spread %.1f%%" %
                       (s, "/".join("%.1f" % l for l in ls), 100 * spread))
        if spread > 0.15:
            boost_ok = False
    lbar = {s: sum(means[(s, e)] for e in etas) / len(etas) for s in svals}
    ratio = lbar[0.56] / lbar[0.28]
    linear_ok = abs(ratio - 2.0) < 0.3
    R.append(check("Q11b", boost_ok and linear_ok,
                   "boost invariance: %s; L(0.56)/L(0.28) = %.2f (linear target 2.0, area would be 4.0)"
                   % ("; ".join(spreads), ratio)))

    # Q12: photon - near-null pair collapses vs timelike of the same coordinate time
    tot_t = tot_n = 0
    for run in range(NRUNS):
        pts = sprinkle(run, NPTS)
        tot_t += longest_chain(pts, p, (p[0] + 0.5, p[1]))          # interval 0.50
        tot_n += longest_chain(pts, p, (p[0] + 0.5, p[1] + 0.49))   # interval 0.10
    ratio = tot_n / tot_t
    R.append(check("Q12", ratio < 0.40,
                   "same coordinate time: null-ish chain / timelike chain = %.2f (< 0.40)" % ratio))

    print()
    print("TIER 4: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
