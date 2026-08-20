"""The compounding rate law (Dorau-Much bridge, 2026-08-20) - beta = 1 from
composition, not from a new dictionary.

GR-33 measured the model's named deviation: the installed LINEAR rate law
c = 1 - GM/r gives beta = 1/2 (Mercury +17%). The first-law lesson (Jacobson /
Dorau-Much): the field equation must be self-consistent - load slows the very
fabric that carries load. The minimal ledger-native form of that self-coupling
is COMPOUNDING: slowdowns multiply (each shell taxes the already-taxed rate,
exactly how time-dilation factors compose), so

    d ln c = -dPhi   =>   rate = e^(-Phi)   instead of   1 - Phi.

Same dictionary as gr_3d (rate slows clocks AND hops): g00 = -e^(-2GM/r),
grr = e^(+2GM/r), light index n = e^(+2GM/r). This is the exponential
(Yilmaz-type) metric, known to match GR at first post-Newtonian order.
The scout MEASURES; adoption into the manifest is a user decision.

FE1  perihelion via the SAME certified integrator as GR-33: ratio to GR
     within 0.03 of the Schwarzschild control -> beta = 1 measured
FE2  bending unchanged: leading coefficient 4GM/b (gamma = 1 preserved)
FE3  no coordinate horizon: e^(-GM/r) finite/positive/monotone at all r > 0
     (Schwarzschild control hits zero at 2GM) - the metric-level echo of the
     BH-4 compute floor
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gr_3d import metric_apsidal


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def trace_ray_exp(GM, b, ds=0.25, span=1600.0):
    # gradient-index ray in n = e^(+2GM/r): grad ln n = -2GM/r^2 rhat
    pos = np.array([-span, b])
    t = np.array([1.0, 0.0])
    for _ in range(int(2 * span / ds) + 10):
        rad = math.hypot(pos[0], pos[1])
        rhat = pos / rad
        grad = -2 * (GM / rad ** 2) * rhat
        perp = grad - (grad @ t) * t
        t = t + perp * ds
        t /= math.hypot(t[0], t[1])
        pos = pos + t * ds
        if pos[0] > span:
            break
    return abs(math.atan2(t[1], t[0]))


def main():
    R = []
    GM = 1.0

    # FE1: perihelion with the compounded metric, Schwarzschild control alongside
    r1, r2 = 400.0, 800.0
    p = 2 * r1 * r2 / (r1 + r2)
    gr = 6 * math.pi * GM / p
    A_exp = lambda r: np.exp(-2 * GM / r)
    B_exp = lambda r: np.exp(+2 * GM / r)
    A_schw = lambda r: ((1 - GM / (2 * r)) / (1 + GM / (2 * r))) ** 2
    B_schw = lambda r: (1 + GM / (2 * r)) ** 4
    prec_e = 2 * metric_apsidal(A_exp, B_exp, r1, r2) - 2 * math.pi
    prec_s = 2 * metric_apsidal(A_schw, B_schw, r1, r2) - 2 * math.pi
    ratio_e, ratio_s = prec_e / gr, prec_s / gr
    beta = 4 - 3 * ratio_e                       # (2 + 2*gamma - beta)/3, gamma = 1
    R.append(check("FE1", abs(ratio_e - ratio_s) < 0.03,
                   "perihelion, same certified integrator as GR-33: compounded metric "
                   "%.4f x GR vs Schwarzschild control %.4f x GR (the linear law gave "
                   "1.179) - beta = %.3f: THE GR-33 DEVIATION CLOSES when slowdowns "
                   "COMPOUND instead of add; the dictionary never changes, only the "
                   "composition law" % (ratio_e, ratio_s, beta)))

    # FE2: bending with the compounded index
    bs = np.array([40.0, 60.0, 90.0, 135.0, 200.0])
    als = np.array([trace_ray_exp(GM, b) for b in bs])
    X = np.stack([1.0 / bs, 1.0 / bs ** 2], axis=1)
    c1, c2 = np.linalg.lstsq(X, als, rcond=None)[0]
    lead = c1 / (4 * GM)
    R.append(check("FE2", abs(lead - 1) < 0.05,
                   "bending: deflection fits c1/b with c1 = %.3f x 4GM - gamma = 1 "
                   "preserved (weak field identical to the linear law; only the second "
                   "order moved, which is exactly where beta lives)" % lead))

    # FE3: no coordinate horizon - the compute floor in the metric
    r = np.geomspace(0.05 * GM, 10 * GM, 400)
    red_e = np.exp(-GM / r)
    schw_zero = 1 - 2 * GM / (2 * GM)
    ok3 = (np.all(np.isfinite(red_e)) and np.all(red_e > 0)
           and np.all(np.diff(red_e) > 0) and abs(schw_zero) < 1e-12)
    R.append(check("FE3", ok3,
                   "the compounded redshift e^(-GM/r): finite, positive, monotone at "
                   "every sampled r down to 0.05 GM (min %.1e) while the Schwarzschild "
                   "factor hits ZERO at r = 2GM - the metric-level echo of the compute "
                   "floor (BH-4): the rate approaches zero and never arrives"
                   % float(red_e.min())))

    print()
    print("COMPOUND: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
