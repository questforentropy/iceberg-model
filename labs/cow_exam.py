"""COW exam: quantum interference in the scheduler gravity field.

The Colella-Overhauser-Werner experiment (1975), in the toy: an interferometer whose
two arms sit at different depths in the budget field. Clock rates differ between arms
(V2-2's G1), phase advances per LOCAL tick with the Compton scaling (G3/G4's declared
bridge), so the counted fringes shift by delta_phi = m * g * dPhi * T.

This is the first exam that needs BOTH halves of the model at once: the contract
engine (superposition, interference) and the congested grid (the field).

COW-1  fringes oscillate in T at the field-predicted frequency
COW-2  frequency scales with arm separation (dPhi ratio)
COW-3  frequency doubles with mass (Compton clock)
COW-4  no crowd -> no shift (control)
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qm_tests import QContract, H, HAD, RZ
from v2_gravity_scout import C, crowd_density, solve_field

G = 0.3
STEPS = 40


def fringe_curve(tag, phi_n, dA, dB, m, Ts, n):
    dphi_field = phi_n[int(C), int(C + dA)] - phi_n[int(C), int(C + dB)]
    domega = m * G * dphi_field
    ps = []
    for T in Ts:
        k = 0
        for t in range(n):
            c = QContract(H(tag, T, t), [1, 0])
            c.apply1(HAD, 0)
            for _ in range(STEPS):                      # phase accrues per local tick
                c.apply1(RZ(domega * T / STEPS), 0)
            c.apply1(HAD, 0)
            k += c.measure_z(0) == 1
        ps.append(k / n)
    return np.array(ps), domega


def fit_omega(Ts, ps, w_lo, w_hi):
    ws = np.linspace(w_lo, w_hi, 600)
    sse = [((ps - 0.5 * (1 + np.cos(w * Ts))) ** 2).sum() for w in ws]
    return ws[int(np.argmin(sse))]


def check(label, ok, detail):
    print("%-6s %-6s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []
    phi, _ = solve_field(crowd_density(1.0))
    phi_n = phi / phi.max()

    n = 1500
    Ts = np.linspace(4, 170, 24)

    ps1, w_pred1 = fringe_curve("cow1", phi_n, 12, 32, 1.0, Ts, n)
    w1 = fit_omega(Ts, ps1, 0.3 * w_pred1, 2.5 * w_pred1)
    R.append(check("COW-1", abs(w1 / w_pred1 - 1) < 0.10,
                   "fringe frequency %.5f vs field prediction %.5f (ratio %.3f) - the two arms' "
                   "clock-rate gap, read out as counted fringes" % (w1, w_pred1, w1 / w_pred1)))

    ps2, w_pred2 = fringe_curve("cow2", phi_n, 12, 20, 1.0, Ts, n)
    w2 = fit_omega(Ts, ps2, 0.2 * w_pred1, 2.5 * w_pred1)
    R.append(check("COW-2", abs((w2 / w1) / (w_pred2 / w_pred1) - 1) < 0.12,
                   "narrower arms: frequency ratio %.3f vs dPhi ratio %.3f" %
                   (w2 / w1, w_pred2 / w_pred1)))

    ps3, _ = fringe_curve("cow3", phi_n, 12, 32, 2.0, Ts, n)
    w3 = fit_omega(Ts, ps3, 0.3 * w_pred1, 4.5 * w_pred1)
    R.append(check("COW-3", abs(w3 / w1 - 2) < 0.2,
                   "double mass: frequency x%.3f (Compton clock: rest frequency ~ mass)" % (w3 / w1)))

    flat = np.zeros((128, 128))
    ps4, _ = fringe_curve("cow4", flat, 12, 32, 1.0, Ts, n)
    R.append(check("COW-4", ps4.min() > 0.97,
                   "no crowd: fringes flat (min P0 = %.3f) - no field, no shift" % ps4.min()))

    print()
    print("COW: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
