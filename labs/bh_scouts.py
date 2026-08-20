"""BH horizon scouts - on the hole the budget dynamics BUILT (2026-08-17).

The sink's inflow u(x) comes from fluid_scouts2.telegraph_line (FLU-8): nothing
here is painted. Transport instrument: characteristic families at u -/+ c,
certified against the full wave equation by FLU-4.

B1  one-way membrane: a pulse inside the horizon never crosses it outward and
    an outside observer hears nothing; the same pulse launched outside escapes
B2  nothing frozen, door open inward: signals from outside cross the horizon
    INWARD and reach the core on schedule; the budget inside stays alive
    (a frozen patch would block both directions)
B3  the frozen-star image: signals emitted closer and closer to the horizon
    arrive later and later outside - the gaps stretch without bound - and a
    signal from just inside never arrives at all
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluid_scouts2 import telegraph_line


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def transport(a, l0, steps, dt=0.2, probes=(), edge=6):
    a_f = 0.5 * (a + np.roll(a, -1))
    ap = np.maximum(a_f, 0.0)
    am = np.minimum(a_f, 0.0)
    l = l0.copy()
    probe_max = {p: 0.0 for p in probes}
    probe_t = {p: [] for p in probes}
    min_x, max_x = None, None
    for s in range(steps):
        F = ap * l + am * np.roll(l, -1)
        l = l - dt * (F - np.roll(F, 1))
        l[:edge] = 0.0
        l[-edge:] = 0.0
        live = np.where(l > 0.02)[0]
        if len(live):
            lo, hi = float(live[0]), float(live[-1])
            min_x = lo if min_x is None else min(min_x, lo)
            max_x = hi if max_x is None else max(max_x, hi)
        for p in probes:
            probe_max[p] = max(probe_max[p], float(l[p]))
            probe_t[p].append(float(l[p]))
        if not len(live):
            break
    return l, min_x, max_x, probe_max, probe_t


def arrival_time(series, dt=0.2):
    # median arrival: time at which half the received amplitude has passed
    a = np.array(series) ** 2
    if a.sum() < 1e-12:
        return None
    c = np.cumsum(a)
    return float(np.searchsorted(c, 0.5 * c[-1])) * dt


def gauss(x, x0, sig=6.0):
    return np.exp(-(x - x0) ** 2 / (2 * sig ** 2))


def main():
    R = []
    u, b, x = telegraph_line(1.0)                 # the FLU-8 supercritical hole
    left = np.where((x < 1500) & (u >= 1.0))[0]
    xh = float(x[left.min()])                     # left horizon: u crosses c going in
    a_out = u - 1.0                               # escaping family (leftward outside)
    a_in = u + 1.0                                # infalling family (rightward)
    b0 = float(b[100])

    # B1: one-way membrane
    _, mn_in, _, pm_in, _ = transport(a_out, gauss(x, xh + 15), 9000, probes=(400,))
    _, mn_out, _, pm_out, _ = transport(a_out, gauss(x, 800.0), 9000, probes=(400,))
    R.append(check("B1", mn_in > xh - 25 and mn_out < 450
                   and pm_in[400] < 0.05 * max(pm_out[400], 1e-9),
                   "horizon SELF-LOCATED at x=%.0f (u crosses c): inside launch reaches "
                   "min x=%.0f (never out), outside probe hears %.1e; the SAME pulse "
                   "launched outside escapes to %.0f (probe %.2f) - a one-way membrane "
                   "the budget dynamics built on its own" %
                   (xh, mn_in, pm_in[400], mn_out, pm_out[400])))

    # B2: door open inward, budget alive inside
    core = 1495
    _, _, _, _, pt = transport(a_in, gauss(x, 800.0), 6000, probes=(core,))
    t_arr = arrival_time(pt[core])
    seg = (x >= 800) & (x <= core)
    t_pred = float((1.0 / a_in[seg]).sum())
    R.append(check("B2", t_arr is not None and abs(t_arr / t_pred - 1) < 0.25
                   and float(b[1500]) > 0.0,
                   "infalling signal from x=800 crosses the horizon and reaches the core "
                   "at t=%.0f (schedule %.0f); budget at the center still %.2e (alive) - "
                   "the door is open INWARD and nothing inside is frozen; a halted patch "
                   "would block both ways" % (t_arr or -1, t_pred, float(b[1500]))))

    # B3: the frozen-star image - emission points marching toward the horizon
    times = {}
    for xe in (xh - 24, xh - 12, xh - 6, xh + 12):
        _, _, _, _, pt = transport(a_out, gauss(x, xe, 2.0), 20000, probes=(1000,))
        times[xe] = arrival_time(pt[1000])
    # log law: t(d) = A - ln(d)/kappa -> geometric steps toward the horizon give
    # EQUAL gaps ln2/kappa; kappa = surface gravity |da_out/dx| at the horizon
    g1 = times[xh - 12] - times[xh - 24]
    g2 = times[xh - 6] - times[xh - 12]
    ratio = g2 / g1
    kap_t = np.log(2.0) / (0.5 * (g1 + g2))
    ih = int(xh)
    kap_field = abs(float(a_out[ih + 3] - a_out[ih - 3]) / 6.0)
    R.append(check("B3", times[xh + 12] is None and 0.7 < ratio < 1.4
                   and 0.35 < kap_t / kap_field < 2.0,
                   "emission at 24/12/6 cells outside: t=%.0f/%.0f/%.0f - each HALVING "
                   "of the distance costs the same extra delay (%.0f, %.0f: the log-law "
                   "signature of a horizon), e-folding rate kappa=%.3f vs measured "
                   "surface gravity %.3f (the number that would set the Hawking "
                   "temperature; instrument reads low through upwind diffusion, "
                   "declared); emitted 12 cells INSIDE: never arrives - the frozen-star "
                   "image" % (times[xh - 24], times[xh - 12], times[xh - 6], g1, g2,
                              kap_t, kap_field)))

    print()
    print("BH: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
