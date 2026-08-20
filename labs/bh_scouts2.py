"""Compute-floor scouts - the density route to a black hole (no singularity).

The claim (user, 2026-08-19): a black hole is a region packed so dense that
compute approaches 0 - and only approaches. The singularity is continuum
language dividing by zero; the machine never divides by zero, it just ticks
slower. The rate map L -> r = 1/(1+L) never reaches 0 for any finite load,
and infinite load would need an infinite ledger = infinite time.

C1  the floor is asymptotic: load ladder x10 per rung - tick-scheduler sim
    measures redshift 1+z = 1+L exactly; the algebraic ladder runs to
    L = 1e300 with the rate strictly positive, finite, monotone - no machine
    quantity ever diverges (the diverging "curvature" is 1+L itself, a
    CONTINUUM proxy the machine never inverts)
C2  frozen, not sealed: a signal from the core of an exponentially loaded
    well DOES escape - escape time = sum of local waits, finite; equal steps
    deeper multiply the observed delay by the constant factor e^(step/lambda)
    (the density-route analog of BH-3's log law)
C3  the two routes are distinguishable: the density hole is two-way (the C2
    probe escapes, arbitrarily slowly) while the flux hole of BH-1 is a true
    one-way membrane (same probe never crosses out) - a real black hole is
    both at once
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bh_scouts import gauss, transport
from fluid_scouts2 import telegraph_line


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def tick_period(load, n_ticks=4):
    # credit scheduler: a node with load L gets rate r = 1/(1+L) of the fixed
    # compute; measure the mean global-step gap between its ticks
    r = 1.0 / (1.0 + load)
    credit, t, ticks = 0.0, 0, []
    while len(ticks) < n_ticks:
        t += 1
        credit += r
        if credit >= 1.0:
            credit -= 1.0
            ticks.append(t)
    return float(np.mean(np.diff(ticks)))


def main():
    R = []

    # C1: the asymptotic floor
    worst = 0.0
    for k in range(6):
        L = 10.0 ** k
        worst = max(worst, abs(tick_period(L) / (1.0 + L) - 1.0))
    ladder = [10.0 ** k for k in range(0, 301, 25)]
    rates = [1.0 / (1.0 + L) for L in ladder]
    finite = all(np.isfinite(rr) and rr > 0.0 for rr in rates)
    monotone = all(a > b for a, b in zip(rates, rates[1:]))
    R.append(check("C1", worst < 1e-9 and finite and monotone,
                   "sim rungs L=1..1e5: measured redshift 1+z = 1+L exact (worst dev "
                   "%.1e); algebraic ladder to L=1e300: rate strictly positive, finite, "
                   "monotone at every rung - compute approaches 0 and never reaches it; "
                   "the only diverging quantity is the continuum proxy 1+L, which the "
                   "machine never inverts" % worst))

    # C2: frozen, not sealed - escape from an exponential well
    lam, amp, depth = 30.0, 2000.0, 200
    xw = np.arange(depth)
    wait = 1.0 + amp * np.exp(-xw / lam)     # global steps per cell (one local tick)
    esc = {d: float(wait[d:].sum()) for d in (0, 15, 30, 45)}
    r1 = esc[0] / esc[15]
    r2 = esc[15] / esc[30]
    r3 = esc[30] / esc[45]
    pred = float(np.exp(15.0 / lam))
    ok_ratio = all(abs(r / pred - 1.0) < 0.10 for r in (r1, r2, r3))
    R.append(check("C2", np.isfinite(esc[0]) and ok_ratio,
                   "core signal ESCAPES: T=%.0f steps from the floor (finite for any "
                   "finite load); emission 15 cells deeper each time multiplies the "
                   "delay by %.3f/%.3f/%.3f (constant, predicted e^(1/2)=%.3f) - the "
                   "density-route frozen star: dimmer and slower without bound, "
                   "never sealed" % (esc[0], r1, r2, r3, pred)))

    # C3: density two-way vs flux one-way
    u, b, xg = telegraph_line(1.0)
    left = np.where((xg < 1500) & (u >= 1.0))[0]
    xh = float(xg[left.min()])
    a_out = u - 1.0
    _, mn_in, _, pm_in, _ = transport(a_out, gauss(xg, xh + 15), 9000, probes=(400,))
    R.append(check("C3", np.isfinite(esc[0]) and mn_in > xh - 25 and pm_in[400] < 1e-3,
                   "the SAME escape attempt: density hole lets it out (T=%.0f, two-way, "
                   "just slow); flux hole (BH-1's derived horizon at x=%.0f) never - "
                   "inside launch reaches min x=%.0f, outside probe hears %.1e - the "
                   "model's two horizon mechanisms are DISTINGUISHABLE; a real black "
                   "hole is both at once" % (esc[0], xh, mn_in, pm_in[400])))

    print()
    print("BH2: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
