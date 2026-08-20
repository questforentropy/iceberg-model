"""Noether/energy scouts (user questions 2026-08-17).

N1  Noether alive locally - a STATIC congestion well conserves <E> (time
    symmetry -> conservation); an oscillating well pumps energy (symmetry
    broken -> conservation broken). Same engine, one moving dial.
N2  the energy audit - a wave on a slowly-taxed fabric (c: 1.0 -> 0.7) loses
    energy at EXACTLY the redshift rate: dE/E = domega/omega = dc/c.
    The leak equals the bill.
N3  Ehrenfest - E/omega is an adiabatic invariant: slow tax pins it (hbar
    constant DURING expansion); a sudden tax breaks it by the predicted
    (w1^2+w2^2)/(2 w1 w2) = 1.25 factor - quanta created from nothing
    (cosmological particle production, toy form).
"""

import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def schrodinger_energy_run(move_amp):
    Nx, dx, dt = 512, 0.5, 0.01
    x = (np.arange(Nx) - Nx / 2) * dx
    kk = 2 * np.pi * np.fft.fftfreq(Nx, dx)
    kin_half = np.exp(-1j * kk ** 2 * dt / 4)
    psi = np.exp(-(x + 20.0) ** 2 / (4 * 4.0 ** 2)).astype(complex)
    psi /= math.sqrt((np.abs(psi) ** 2).sum() * dx)
    energies = []
    for s in range(30000):
        t = s * dt
        V = -0.5 * np.exp(-(x - move_amp * math.sin(0.2 * t)) ** 2 / (2 * 12.0 ** 2))
        pot = np.exp(-1j * V * dt)
        psi = np.fft.ifft(kin_half * np.fft.fft(psi))
        psi = pot * psi
        psi = np.fft.ifft(kin_half * np.fft.fft(psi))
        if s % 50 == 0:
            pk = np.fft.fft(psi)
            T = (np.abs(pk) ** 2 * kk ** 2 / 2).sum() / (np.abs(pk) ** 2).sum()
            U = (V * np.abs(psi) ** 2).sum() * dx
            energies.append(T + U)
    e = np.array(energies)
    scale = abs(e[0]) + 0.5
    return (e.max() - e.min()) / scale


def mode_run(c_profile, T, dt=0.05, Nx=256):
    dx = 1.0
    x = np.arange(Nx) * dx
    k = 2 * np.pi * 8 / (Nx * dx)
    phi = np.cos(k * x)
    w0 = c_profile(0.0) * k
    prev = np.cos(k * x) * math.cos(w0 * dt)      # standing mode, one step back
    cosk, sink = np.cos(k * x), np.sin(k * x)
    ts, a_s, adot_s, E_s = [], [], [], []
    steps = int(T / dt)
    for s in range(steps):
        t = s * dt
        c = c_profile(t)
        lap = np.roll(phi, 1) - 2 * phi + np.roll(phi, -1)
        nxt = 2 * phi - prev + (c * dt / dx) ** 2 * lap
        prev, phi = phi, nxt
        dphi_t = (phi - prev) / dt
        dphi_x = (np.roll(phi, -1) - np.roll(phi, 1)) / (2 * dx)
        ts.append(t)
        a_s.append(2 * (phi * cosk).mean())
        adot_s.append(2 * (dphi_t * cosk).mean())
        E_s.append(0.5 * (dphi_t ** 2 + (c * dphi_x) ** 2).sum() * dx)
    return np.array(ts), np.array(a_s), np.array(adot_s), np.array(E_s)


def window_stats(ts, a_s, adot_s, E_s, t_lo, t_hi):
    m = (ts >= t_lo) & (ts < t_hi)
    omega = math.sqrt((adot_s[m] ** 2).mean() / (a_s[m] ** 2).mean())
    return omega, float(E_s[m].mean())


def main():
    R = []

    # N1: static well conserves energy; oscillating well does not
    drift_static = schrodinger_energy_run(0.0)
    drift_moving = schrodinger_energy_run(8.0)
    R.append(check("N1", drift_static < 1e-4 and drift_moving > 100 * drift_static,
                   "<E> drift: static well %.1e vs oscillating well %.1e (x%.0f) - "
                   "conservation holds exactly where time symmetry holds, Noether in-toy"
                   % (drift_static, drift_moving, drift_moving / max(drift_static, 1e-300))))

    # N2 + N3a: slow uniform tax c 1.0 -> 0.7 over ~90 periods
    T_ramp, T_end = 3000.0, 3600.0
    def c_slow(t):
        return 1.0 - 0.3 * min(t, T_ramp) / T_ramp
    ts, a_s, adot_s, E_s = mode_run(c_slow, T_end)
    w1, E1 = window_stats(ts, a_s, adot_s, E_s, 5.0, 200.0)
    w2, E2 = window_stats(ts, a_s, adot_s, E_s, T_ramp + 100, T_end)
    zrate = w2 / w1
    erate = E2 / E1
    inv = (E2 / w2) / (E1 / w1)
    R.append(check("N2", abs(zrate - 0.7) < 0.01 and abs(erate - zrate) < 0.02,
                   "slow tax: frequency ratio %.3f (tax 0.700), energy ratio %.3f - the "
                   "photon's energy leaks at EXACTLY the redshift rate; the leak equals "
                   "the bill" % (zrate, erate)))
    R.append(check("N3a", abs(inv - 1.0) < 0.01,
                   "E/omega before vs after the slow 30%% tax: ratio %.4f - the quantum "
                   "of action rides through expansion untouched (Ehrenfest adiabatic "
                   "invariant = hbar looks constant)" % inv))

    # N3b: SUDDEN tax c 1.0 -> 0.5; phase-averaged E/omega jump = (w1^2+w2^2)/(2 w1 w2)
    period = 2 * math.pi / (1.0 * 2 * np.pi * 8 / 256)
    jumps = []
    for ph in range(12):
        t_sw = 200.0 + ph * period / 12
        def c_sudden(t, t_sw=t_sw):
            return 1.0 if t < t_sw else 0.5
        ts, a_s, adot_s, E_s = mode_run(c_sudden, 500.0)
        w1s, E1s = window_stats(ts, a_s, adot_s, E_s, 5.0, 195.0)
        w2s, E2s = window_stats(ts, a_s, adot_s, E_s, t_sw + 30, 500.0)
        jumps.append((E2s / w2s) / (E1s / w1s))
    jump = float(np.mean(jumps))
    pred = (1.0 ** 2 + 0.5 ** 2) / (2 * 1.0 * 0.5)
    R.append(check("N3b", abs(jump - pred) < 0.04,
                   "sudden halving of c: E/omega jumps x%.3f (predicted (w1^2+w2^2)/"
                   "(2 w1 w2) = %.3f) - quanta created from nothing when the change "
                   "outruns adiabaticity: cosmological particle production, toy form"
                   % (jump, pred)))

    print()
    print("NOETHER: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
