"""V3 expansion scout: the storage bill as cosmology (entropy-first C3, in the toy).

Mechanism under test (user, 2026-08-15): node count fixed, space fixed; the growing
ledger (entropy S(t) = cumulative folds) loads the background; processing slows;
"expansion" is the feeling of c dropping - distances take longer to cross.

PRE-REGISTERED FORK (the sign test decides the model):
  hop-tax   the storage bill bites the MESSAGE fabric (light pays): c(t) falls,
            clocks untouched  -> prediction: REDSHIFT growing with distance (Hubble!)
  tick-tax  the bill bites local processing (clocks pay), light untouched
            -> prediction: BLUESHIFT (old light beats slowed clocks) - anti-cosmology
  uniform   both pay equally -> prediction: NO shift (episode #12's invisibility,
            to first order) - expansion unobservable

The model needs the hop-tax variant to be the physical one. Deterministic, no draws.

E1  apparent size: light-crossing time grows linearly with S(t)
E2  hop-tax: z > 0, z(d) linear (a Hubble law), slope matches analytic g*rho/c0
E3  tick-tax control: z < 0;  uniform control: z ~ 0
"""

import math


G_RHO = 2e-4       # load growth rate: g * (folds per substrate time)
C0 = 1.0
P = 50.0           # emitter period, local ticks


def c_of(t, hop_tax):
    return C0 / (1 + G_RHO * t) if hop_tax else C0


def rate_of(t, tick_tax):
    return 1 / (1 + G_RHO * t) if tick_tax else 1.0


def travel_time(t_emit, d, hop_tax, dt=0.05):
    x, t = 0.0, t_emit
    while x < d:
        x += c_of(t, hop_tax) * dt
        t += dt
    return t - t_emit


def redshift(d, hop_tax, tick_tax, t0=0.0):
    # two successive wavefronts, one emitter period apart in the EMITTER's local ticks
    dt_sub_1 = P / rate_of(t0, tick_tax)
    a1 = t0 + travel_time(t0, d, hop_tax)
    t1 = t0 + dt_sub_1
    a2 = t1 + travel_time(t1, d, hop_tax)
    arrival_spacing_sub = a2 - a1
    received_ticks = arrival_spacing_sub * rate_of(a1, tick_tax)
    return received_ticks / P - 1


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []

    # E1: apparent size of a fixed world grows with the ledger
    D = 500.0
    ts = [0, 2000, 4000, 8000]
    crossings = [travel_time(t, D, hop_tax=True) for t in ts]
    preds = [D / C0 * (1 + G_RHO * (t + D / (2 * C0))) for t in ts]
    dev = max(abs(c - p) / p for c, p in zip(crossings, preds))
    R.append(check("E1", crossings[-1] > 2.5 * crossings[0] and dev < 0.15,
                   "same 500-hop world takes %.0f ticks to cross at S=0 and %.0f at late S "
                   "(x%.2f) - fixed space FEELS bigger as the ledger grows"
                   % (crossings[0], crossings[-1], crossings[-1] / crossings[0])))

    # E2: hop-tax -> redshift, linear in distance (a Hubble law), slope matches analytic
    ds = [100, 200, 400, 800]
    zs = [redshift(d, hop_tax=True, tick_tax=False) for d in ds]
    slopes = [z / d for z, d in zip(zs, ds)]
    slope = sum(slopes) / len(slopes)
    spread = (max(slopes) - min(slopes)) / slope
    analytic = G_RHO / C0
    R.append(check("E2", all(z > 0 for z in zs) and spread < 0.15
                   and abs(slope / analytic - 1) < 0.15,
                   "REDSHIFT, z proportional to d (Hubble law): z = %s at d = %s; "
                   "slope %.2e vs analytic g*rho/c0 = %.2e"
                   % (["%.4f" % z for z in zs], ds, slope, analytic)))

    # E3: the fork's other tines - tick-tax blueshifts, uniform cancels
    z_tick = redshift(400, hop_tax=False, tick_tax=True)
    z_unif = redshift(400, hop_tax=True, tick_tax=True)
    z_hop = redshift(400, hop_tax=True, tick_tax=False)
    R.append(check("E3", z_tick < -0.01 and abs(z_unif) < 0.2 * abs(z_hop),
                   "tick-tax: z = %.4f (BLUEshift - anti-cosmology, falsified as expansion); "
                   "uniform: z = %.4f vs hop-tax %.4f (first-order cancellation - the "
                   "invisibility pillar, measured)" % (z_tick, z_unif, z_hop)))

    print()
    print("V3 EXPANSION: %s (%d checks) - expansion-feel requires the storage bill to "
          "bite the message fabric, not the clocks" % ("ALL PASS" if all(R) else "FAILURES", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
