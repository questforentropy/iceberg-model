"""Dumb-hole thermodynamics (Dorau-Much bridge, 2026-08-20) - does the derived
hole obey a first law?

Pass marks DECLARED BEFORE the first run (tests/gr.md GR-34..36): the
Schwarzschild pattern r_h ~ M (p in [0.7,1.3]), T ~ 1/M (q in [-1.35,-0.65]),
and the Clausius entropy S = INT 2pi dJ/kappa ~ r_h^s with s in [1.5,2.5]
(the Bekenstein square assembled from measured scalings). PRE-REGISTERED
ALTERNATIVE: analog-gravity lore (Unruh) says horizon kinematics need not
bring Einstein dynamics - a FAIL is the kinematics-only verdict, a finding.

Instruments: the FLU-8 derived hole (telegraph_line, nothing painted);
J = flux crossing the horizon = b at the u=1 crossing; kappa = |du/dx| there
(the BH-3 surface-gravity read); r_h = distance sink-to-horizon.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluid_scouts2 import telegraph_line


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def hole_readings(lam):
    u, b, x = telegraph_line(lam)
    left = np.where((x < 1500) & (u >= 1.0))[0]
    if len(left) == 0:
        return None
    ih = int(left.min())                     # left horizon: u crosses c inbound
    r_h = 1500.0 - float(x[ih])
    J = float(b[ih])                         # flux through the horizon (u = 1)
    kappa = abs(float(u[ih + 3] - u[ih - 3]) / 6.0)
    return r_h, J, kappa


def powfit(lx, ly):
    p, c = np.polyfit(lx, ly, 1)
    resid = ly - (p * lx + c)
    r2 = 1.0 - float((resid ** 2).sum() / ((ly - ly.mean()) ** 2).sum())
    return float(p), r2


def main():
    R = []
    lams = (0.3, 0.45, 0.65, 1.0, 1.5)
    rows = []
    for lam in lams:
        h = hole_readings(lam)
        if h:
            rows.append((lam,) + h)
    rh = np.array([r[1] for r in rows])
    J = np.array([r[2] for r in rows])
    kap = np.array([r[3] for r in rows])
    order = np.argsort(J)
    rh, J, kap = rh[order], J[order], kap[order]

    p, r2p = powfit(np.log(J), np.log(rh))
    R.append(check("FL1", len(rows) >= 4 and 0.7 <= p <= 1.3 and r2p > 0.9,
                   "mass-radius on %d appetites: r_h ~ J^%.2f (R^2=%.3f; Schwarzschild "
                   "pattern r ~ M is exponent 1) - the bigger the appetite, the "
                   "proportionally bigger the hole" % (len(rows), p, r2p)))

    q, r2q = powfit(np.log(J), np.log(kap))
    R.append(check("FL2", -1.35 <= q <= -0.65 and r2q > 0.9,
                   "temperature-mass: kappa ~ J^%.2f (R^2=%.3f; Schwarzschild T ~ 1/M "
                   "is exponent -1) - bigger holes are COLDER, the black-hole "
                   "thermodynamic signature, from budget dynamics alone" % (q, r2q)))

    # FL3: Clausius entropy from the MEASURED kappa(J): dS = 2pi dJ / kappa
    T = kap / (2 * np.pi)
    S = np.concatenate([[0.0], np.cumsum(0.5 * (1 / T[1:] + 1 / T[:-1]) * np.diff(J))])
    S = S - S[0] + (J[0] / T[0])             # anchor: S(J0) ~ J0/T0 (power-law tail)
    s_exp, r2s = powfit(np.log(rh), np.log(S))
    R.append(check("FL3", 1.5 <= s_exp <= 2.5 and r2s > 0.9,
                   "the first law assembled: Clausius S = INT dJ/T from the measured "
                   "temperatures fits S ~ r_h^%.2f (R^2=%.3f) - the BEKENSTEIN SQUARE "
                   "(in 3D, S ~ area IS S ~ r^2): entropy-area emerges from two "
                   "measured scalings, nothing installed" % (s_exp, r2s)))

    print()
    for lam, r, j, k in rows:
        print("  appetite %.2f: r_h=%5.1f  J=%.4f  kappa=%.4f" % (lam, r, j, k))
    print("FIRST-LAW: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
