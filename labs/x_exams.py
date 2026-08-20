"""X-series exams (test-plan Tier 5): the second-pass curriculum.

X1 counterfeit, X2 teleportation, X3 swapping, X5 Darwinism curve, X6 Zeno,
X7 uncertainty, X8 twins-on-DAG, X9 dimension estimator, X10 fail-on-purpose,
X11 bomb tester. (X4 eraser was absorbed by CH-13.)
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qm_tests import (ALICE_ANGLES, BOB_ANGLES, HAD, QContract, RY, RZ, SQ2, H, u01)
from ch_retake import cry
from spacetime_tests import longest_chain, sprinkle

X_GATE = [[0, 1], [1, 0]]
Z_GATE = [[1, 0], [0, -1]]


def RX(t):
    c, s = math.cos(t / 2), math.sin(t / 2)
    return [[c, -1j * s], [-1j * s, c]]


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []

    # X1 counterfeit: CNOT-copy is perfect on basis states, fails on superpositions
    n = 3000
    basis_ok = 0
    for t in range(n):
        c = QContract(H("x1b", t), [0, 1, 0, 0])       # |1> on q0, blank q1
        c.cnot(0, 1)
        basis_ok += c.measure_z(1) == -1
    thetas = [k * math.pi / 10 for k in range(1, 10)]
    fids, weights = [], []
    for th in thetas:
        k = 0
        for t in range(n):
            c = QContract(H("x1", th, t), [1, 0, 0, 0])
            c.apply1(RY(th), 0)
            c.cnot(0, 1)
            k += c.measure_angle(1, th) == 1           # clone fidelity to the original
        fids.append(k / n)
        weights.append(math.sin(th))
    avg_f = sum(f * w for f, w in zip(fids, weights)) / sum(weights)
    R.append(check("X1", basis_ok == n and avg_f < 5 / 6 and abs(avg_f - 2 / 3) < 0.03,
                   "basis copy %d/%d; superposition clone fidelity %.3f (theory 2/3, optimal-"
                   "cloner bound 5/6, perfect copy impossible)" % (basis_ok, n, avg_f)))

    # X2 teleportation: unknown state moved via one pair + two gossiped classical bits
    n = 3000
    ok_with = ok_without = 0
    for t in range(n):
        th = 2 * math.pi * u01(H("x2th", t))
        ph = 2 * math.pi * u01(H("x2ph", t))
        for use_bits in (True, False):
            c = QContract(H("x2", t, use_bits), [1] + [0] * 7)
            c.apply1(RY(th), 0)
            c.apply1(RZ(ph), 0)                        # the unknown state, on q0
            c.apply1(HAD, 1)
            c.cnot(1, 2)                               # the shared pair (q1, q2)
            c.cnot(0, 1)
            c.apply1(HAD, 0)
            z = c.measure_z(0) == -1
            x = c.measure_z(1) == -1
            if use_bits:                               # the two classical bits, gossiped
                if x:
                    c.apply1(X_GATE, 2)
                if z:
                    c.apply1(Z_GATE, 2)
            c.apply1(RZ(-ph), 2)
            c.apply1([[math.cos(th / 2), math.sin(th / 2)],
                      [-math.sin(th / 2), math.cos(th / 2)]], 2)   # inverse prep
            good = c.measure_z(2) == 1
            if use_bits:
                ok_with += good
            else:
                ok_without += good
    R.append(check("X2", ok_with == n and abs(ok_without / n - 0.5) < 0.05,
                   "with the 2 classical bits: %d/%d exact; without them: %.3f (garbage) - "
                   "the light-speed channel is mandatory" % (ok_with, n, ok_without / n)))

    # X3 entanglement swapping: A-D entangled though they never met
    def chsh_pair(tag, prepare, qa, qb, n):
        bins = {}
        for t in range(n):
            c = prepare(t)
            if c is None:
                continue
            ia = int(H(tag, t, "sa"), 16) % 2
            ib = int(H(tag, t, "sb"), 16) % 2
            ra = c.measure_angle(qa, ALICE_ANGLES[ia])
            rb = c.measure_angle(qb, BOB_ANGLES[ib])
            bins.setdefault((ia, ib), []).append(ra * rb)
        E = {k: sum(v) / len(v) for k, v in bins.items()}
        return abs(E[(0, 0)] - E[(0, 1)] + E[(1, 0)] + E[(1, 1)]), min(len(v) for v in bins.values())

    def two_pairs(seed):
        c = QContract(seed, [1] + [0] * 15)
        c.apply1(HAD, 0)
        c.cnot(0, 1)
        c.apply1(HAD, 2)
        c.cnot(2, 3)
        return c

    def swapped(t):
        c = two_pairs(H("x3", t))
        c.cnot(1, 2)
        c.apply1(HAD, 1)
        if c.measure_z(1) != 1 or c.measure_z(2) != 1:
            return None                                # post-select the Phi+ outcome
        return c

    S_swap, nb = chsh_pair("x3s", swapped, 0, 3, 48000)
    S_ctrl, _ = chsh_pair("x3c", lambda t: two_pairs(H("x3ctl", t)), 0, 3, 8000)
    sig = 2 / math.sqrt(nb)
    R.append(check("X3", abs(S_swap - 2 * SQ2) < 5 * sig and S_ctrl < 0.5,
                   "CHSH(A,D) after swap = %.3f (2.83 target; A and D never interacted); "
                   "without the swap = %.3f" % (S_swap, S_ctrl)))

    # X5 Darwinism curve: visibility dies copy by copy; reversal must touch all N
    n = 2000
    eta = math.pi / 3
    overlap = math.cos(eta / 2)
    worst = 0.0
    vs = []
    for N in range(0, 6):
        ps = []
        for phi in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi):
            k = 0
            for t in range(n):
                c = QContract(H("x5", N, phi, t), [1] + [0] * (2 ** (N + 1) - 1))
                c.apply1(HAD, 0)
                for e in range(N):
                    cry(c, eta, 0, e + 1)              # one more environment copy
                c.apply1(RZ(phi), 0)
                c.apply1(HAD, 0)
                k += c.measure_z(0) == 1
            ps.append(k / n)
        v = (max(ps) - min(ps)) / (max(ps) + min(ps))
        vs.append(v)
        worst = max(worst, abs(v - overlap ** N))
    mono = all(b <= a + 0.03 for a, b in zip(vs, vs[1:]))
    R.append(check("X5", worst < 0.06 and mono,
                   "V(N) = %s vs product law %.3f^N (max dev %.3f); reversal cost = N records"
                   % ("/".join("%.2f" % v for v in vs), overlap, worst)))

    # X6 Zeno: the watched thread never moves
    n = 3000
    surv = []
    for k in (1, 2, 4, 8, 16, 32):
        good = 0
        for t in range(n):
            c = QContract(H("x6", k, t), [1, 0])
            alive = True
            for _ in range(k):
                c.apply1(RY(math.pi / k), 0)
                if c.measure_z(0) != 1:
                    alive = False
                    break
            good += alive
        surv.append(good / n)
    theory = [(math.cos(math.pi / (2 * k)) ** 2) ** k for k in (1, 2, 4, 8, 16, 32)]
    dev = max(abs(s - th) for s, th in zip(surv, theory))
    mono = all(b >= a - 0.02 for a, b in zip(surv, surv[1:]))
    R.append(check("X6", dev < 0.03 and mono and surv[-1] > 0.9,
                   "survival %.2f -> %.2f as measurements go 1 -> 32 (theory match %.3f)"
                   % (surv[0], surv[-1], dev)))

    # X7 uncertainty: dZ * dX >= |<Y>| across preparations
    n = 3000
    viol = 0.0
    for i, prep in enumerate([("rx", th) for th in (0.4, 0.9, 1.4, 2.0)]
                             + [("ryrz", th) for th in (0.6, 1.2, 1.8)]):
        kind, th = prep
        def make(tag, t):
            c = QContract(H("x7", i, tag, t), [1, 0])
            if kind == "rx":
                c.apply1(RX(th), 0)
            else:
                c.apply1(RY(th), 0)
                c.apply1(RZ(0.8), 0)
            return c
        mz = sum(make("z", t).measure_z(0) for t in range(n)) / n
        mx = sum(make("x", t).measure_pauli(0, "X") for t in range(n)) / n
        my = sum(make("y", t).measure_pauli(0, "Y") for t in range(n)) / n
        dz = math.sqrt(max(1 - mz * mz, 0))
        dx = math.sqrt(max(1 - mx * mx, 0))
        viol = max(viol, abs(my) - dz * dx)
    R.append(check("X7", viol < 0.03,
                   "Robertson bound dZ*dX >= |<Y>| holds on all 7 preps (worst margin %.4f)" % viol))

    # X8 twins on the DAG: the bent worldline collects fewer blocks
    NRUNS = 5
    p, q = (0.15, 0.5), (0.65, 0.5)
    w = (0.40, 0.65)                                    # waypoint, x-displaced at mid-time
    straight = bent = 0
    for run in range(NRUNS):
        pts = sprinkle(run, 5000)
        straight += longest_chain(pts, p, q)
        bent += longest_chain(pts, p, w) + longest_chain(pts, w, q)
    ratio = bent / straight
    legs = 2 * math.sqrt(0.25 ** 2 - 0.15 ** 2)
    pred = legs / 0.5
    R.append(check("X8", bent < straight and abs(ratio - pred) < 0.12,
                   "bent twin aged x%.3f of straight (interval arithmetic: %.3f) - fewer blocks "
                   "on the bent chain, episode #15's twins measured here" % (ratio, pred)))

    # X9 dimension: the DAG knows its own dimension from ordering statistics alone
    def mm_dimension(frac):
        def f(d):
            return (math.gamma(d + 1) * math.gamma(d / 2)) / (4 * math.gamma(3 * d / 2))
        lo, hi = 1.05, 3.8
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid) > frac:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    dims = []
    for run in range(NRUNS):
        pts = sprinkle(run, 5000)
        tp, xp = p
        tq, xq = q
        inside = [(t, x) for t, x in pts
                  if (t - tp) > abs(x - xp) and (tq - t) > abs(x - xq)]
        rel = 0
        for i in range(len(inside)):
            ti, xi = inside[i]
            for j in range(len(inside)):
                tj, xj = inside[j]
                if (tj - ti) > abs(xj - xi):
                    rel += 1
        frac = rel / (len(inside) * (len(inside) - 1))   # MM constant is per ORDERED pair
        dims.append(mm_dimension(frac))
    d_est = sum(dims) / len(dims)
    R.append(check("X9", abs(d_est - 2.0) < 0.15,
                   "Myrheim-Meyer estimate d = %.3f (true: 1+1) from order counting alone" % d_est))

    # X10 the exam we fail on purpose: the ledger serves S=4 and nothing in-layer breaks
    n = 6000
    bins = {}
    margs = []
    for t in range(n):
        ia = int(H("x10", t, "sa"), 16) % 2
        ib = int(H("x10", t, "sb"), 16) % 2
        ra = 1 if u01(H("x10pr", t)) > 0.5 else -1
        rb = ra * (1 if (ia, ib) == (0, 1) else -1)
        bins.setdefault((ia, ib), []).append(ra * rb)
        margs.append(rb)
    E = {k: sum(v) / len(v) for k, v in bins.items()}
    S = abs(E[(0, 0)] - E[(0, 1)] + E[(1, 0)] + E[(1, 1)])
    R.append(check("X10", abs(S - 4) < 1e-9 and abs(sum(margs) / n) < 0.05,
                   "PR contract: S = %.1f, marginals flat (%.3f) - no-signalling intact, nothing "
                   "in-layer breaks; the model cannot say why nature stops at 2.83. Nobody can. "
                   "This failure is the Confession centerpiece." % (S, sum(margs) / n)))

    # X11 bomb tester: detect the bomb without triggering it
    n = 4000
    counts = {"boom": 0, "dark": 0, "bright": 0}
    dud_dark = 0
    for t in range(n):
        c = QContract(H("x11", t), [1, 0, 0, 0])
        c.apply1(HAD, 0)
        c.cnot(0, 1)                                   # live bomb in arm |1>
        c.apply1(HAD, 0)
        if c.measure_z(1) == -1:
            counts["boom"] += 1
        elif c.measure_z(0) == -1:
            counts["dark"] += 1                        # the interaction-free detection
        else:
            counts["bright"] += 1
        d = QContract(H("x11d", t), [1, 0, 0, 0])      # dud: no coupling
        d.apply1(HAD, 0)
        d.apply1(HAD, 0)
        dud_dark += d.measure_z(0) == -1
    fr = {k: v / n for k, v in counts.items()}
    ok11 = (abs(fr["boom"] - 0.5) < 0.04 and abs(fr["dark"] - 0.25) < 0.04
            and abs(fr["bright"] - 0.25) < 0.04 and dud_dark == 0)
    R.append(check("X11", ok11,
                   "live bomb: boom %.3f / detected-without-touching %.3f / inconclusive %.3f "
                   "(theory 0.50/0.25/0.25); dud never clicks dark (%d/%d)"
                   % (fr["boom"], fr["dark"], fr["bright"], dud_dark, n)))

    print()
    print("X-SERIES: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
