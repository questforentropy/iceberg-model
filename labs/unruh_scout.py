"""Unruh-in-toy (Dorau-Much bridge, 2026-08-20) - acceleration reads the
vacuum as heat.

The bridge note's lesson: in the QFT derivation the Unruh/Hawking temperature
is NOT an input - an observer confined to a causal wedge reads the vacuum as
thermal at T = a/2pi, forced by the structure of what they can access. Toy
version: the vacuum is a random-phase mode ensemble (zero-point spectrum
~ 1/sqrt(omega) IMPORTED, declared; Gaussian UV regulator declared); the
correlation of the field's proper-time derivative along a worldline is
evaluated ENSEMBLE-EXACT (the phase average is analytic per mode - a
quadrature instrument, no Monte-Carlo noise).

Instrument note (first cut, on record): a SHARP k-cutoff rings - the inertial
control showed dtau^-0.6 instead of the vacuum dtau^-2, failing its own known
law. The control caught the instrument; the regulator is now smooth.

U1  the accelerated worldline's correlation fits the THERMAL form
    [pi T / sinh(pi T dtau)]^2 with T = a/2pi: both tested accelerations
    within 15%, temperature ratio = acceleration ratio within 10%
U2  inertial control: the same field on an unaccelerated worldline shows the
    cold-vacuum 1/dtau^2 law (exponent -2 +/- 0.3) and the thermal fit pins
    to the scan floor - no acceleration, no temperature
"""

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


K_C = 60.0
DK = 0.0005
K = np.arange(DK / 2, 6 * K_C, DK)
W2 = DK / K * np.exp(-(K / K_C) ** 2) * K ** 2      # A^2 k^2 per mode


def corr_accel(a, dtau, a_tau_mid=2.0):
    """Exact ensemble correlation of dphi/dtau at symmetric pairs around
    tau_mid on the Rindler worldline u = e^(-a tau)/a, v = e^(a tau)/a."""
    tm = a_tau_mid / a
    ta, tb = tm - dtau / 2, tm + dtau / 2
    dua, dub = -np.exp(-a * ta), -np.exp(-a * tb)
    dva, dvb = np.exp(a * ta), np.exp(a * tb)
    Du = (np.exp(-a * ta) - np.exp(-a * tb)) / a
    Dv = (np.exp(a * tb) - np.exp(a * ta)) / a
    C = np.empty(len(dtau))
    for i in range(len(dtau)):
        C[i] = 0.5 * float((W2 * (dua[i] * dub[i] * np.cos(K * Du[i])
                                  + dva[i] * dvb[i] * np.cos(K * Dv[i]))).sum())
    return C


def corr_inertial(dtau):
    C = np.empty(len(dtau))
    for i in range(len(dtau)):
        C[i] = float((W2 * np.cos(K * dtau[i])).sum())
    return C


def fit_thermal(C, dtau, b_grid):
    # log-space fit: equal weight per point across the decades of decay
    ly = np.log(np.abs(C))
    best = (None, np.inf)
    for b in b_grid:
        lmod = -2 * np.log(np.sinh(b * dtau))
        lalpha = float((ly - lmod).mean())
        r = float(((ly - lmod - lalpha) ** 2).mean())
        if r < best[1]:
            best = (b, r)
    return best


def main():
    R = []
    dtau = np.linspace(1.5, 12.0, 60)
    b_grid = np.linspace(0.02, 0.8, 400)

    Ts, resids = {}, {}
    for a in (0.25, 0.5):
        C = corr_accel(a, dtau)
        b, r = fit_thermal(C, dtau, b_grid)
        Ts[a] = b / np.pi
        resids[a] = r
    pred1, pred2 = 0.25 / (2 * np.pi), 0.5 / (2 * np.pi)
    ratio = Ts[0.5] / Ts[0.25]
    R.append(check("U1", abs(Ts[0.25] / pred1 - 1) < 0.15
                   and abs(Ts[0.5] / pred2 - 1) < 0.15
                   and abs(ratio / 2.0 - 1) < 0.10,
                   "the accelerated observer reads the vacuum as HEAT: the correlation "
                   "fits [piT/sinh(piT dtau)]^2 (residuals %.1e / %.1e) with T = %.5f "
                   "at a=0.25 (Unruh a/2pi = %.5f) and T = %.5f at a=0.5 (predicted "
                   "%.5f); doubling the acceleration doubles the temperature (ratio "
                   "%.3f) - the temperature was never an input, only the worldline was"
                   % (resids[0.25], resids[0.5], Ts[0.25], pred1, Ts[0.5], pred2, ratio)))

    C0 = corr_inertial(dtau)
    slope = float(np.polyfit(np.log(dtau), np.log(np.abs(C0)), 1)[0])
    b0, _ = fit_thermal(C0, dtau, b_grid)
    R.append(check("U2", abs(slope + 2) < 0.3 and b0 <= b_grid[0] + 1e-12,
                   "inertial control: same field, unaccelerated worldline - correlation "
                   "falls as dtau^%.2f (the cold vacuum's 1/dtau^2) and the thermal fit "
                   "pins to the scan floor (b = %.3f): no acceleration, no temperature"
                   % (slope, b0)))

    print()
    print("UNRUH: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
