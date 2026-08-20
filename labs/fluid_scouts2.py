"""FLU round 2 - the flux DERIVED, not painted (V4 build campaign, 2026-08-17).

The budget is a telegraph fluid: db/dt = -dJ/dx + supply - decay - consumption,
tau * dJ/dt = -c_g^2 * tau * db/dx - J. Memory tau > 0 gives the exchange
inertia (the G6 wave-type channel); tau -> 0 at fixed D = c_g^2*tau is pure
diffusion.

F6  a moving demand drags a budget CIRCULATION: circ = -v * c_g^2 * tau^2 *
    Int (b'/b)^2 (derived + measured); pure diffusion drags NOTHING (u is then
    an exact gradient of -D ln b - zero circulation, a small theorem). Frame
    dragging requires memory. Statics never see tau; only dragging does.
F7  Sagnac: counter-propagating laps around the ring differ by 2*circ/c^2,
    with u taken from the budget dynamics (shape derived; coupling = 1
    declared). Static-crowd control: no asymmetry.
F8  dynamic horizon: a consuming sink builds its own inflow; steady drift
    u = J/b is NOT bounded by c_g, and above a critical appetite |u| crosses
    the wave speed at a radius that grows with the appetite.
"""

import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def telegraph_ring(vc, tau, cg2, lam=2e-3, T=5000.0, N=1000, dt=0.05,
                   s=0.01, mu=1e-3, sig=20.0):
    x = np.arange(N, dtype=float)
    b = np.full(N, s / mu)
    J = np.zeros(N)
    eps = 0.25                                   # numerical stabilizer (declared)
    for step in range(int(T / dt)):
        t = step * dt
        xc = (vc * t) % N
        d = (x - xc + N / 2) % N - N / 2
        rho = np.exp(-d * d / (2 * sig * sig))
        dbx = 0.5 * (np.roll(b, -1) - np.roll(b, 1))
        dJx = 0.5 * (np.roll(J, -1) - np.roll(J, 1))
        visc = np.roll(b, -1) + np.roll(b, 1) - 2 * b
        b = b + dt * (-dJx + s - mu * b - lam * rho * b) + eps * visc
        J = J + dt * (-cg2 * dbx - J / tau)
    return J / b, b


def lap_time(u_field, direction, N=1000, dt=0.1):
    # one-directional pulse on the ring; time of its return to the launch point
    x = np.arange(N, dtype=float)
    phi = np.exp(-((x - 0.0 + N / 2) % N - N / 2) ** 2 / (2 * 8.0 ** 2))
    # a pulse moving at +c satisfies phi(x, t-dt) = phi0(x + c*dt)
    prev = np.exp(-(((x + direction * dt) + N / 2) % N - N / 2) ** 2 / (2 * 8.0 ** 2))
    u = u_field
    det = []
    def Dx(f):
        return 0.5 * (np.roll(f, -1) - np.roll(f, 1))
    def Dxx(f):
        return np.roll(f, -1) - 2 * f + np.roll(f, 1)
    steps = int(1400 / dt)
    for sn in range(steps):
        nxt = (2 * phi - prev + dt * dt * (1.0 - u * u) * Dxx(phi)
               - 2 * u * dt * (Dx(phi) - Dx(prev)))
        prev, phi = phi, nxt
        det.append(float(phi[0]))
    det = np.array(det) ** 2
    w = np.arange(int(850 / dt), int(1150 / dt))
    wts = det[w]
    return float((w * wts).sum() / wts.sum()) * dt


def telegraph_line(lam_sink, tau=20.0, cg2=1.0, T=6000.0, N=3000, dt=0.05,
                   s=0.01, mu=1e-3, sig=10.0, x_sink=1500.0):
    x = np.arange(N, dtype=float)
    b = np.full(N, s / mu)
    J = np.zeros(N)
    g = np.exp(-(x - x_sink) ** 2 / (2 * sig * sig))
    eps = 0.25
    for _ in range(int(T / dt)):
        dbx = 0.5 * (np.roll(b, -1) - np.roll(b, 1))
        dJx = 0.5 * (np.roll(J, -1) - np.roll(J, 1))
        visc = np.roll(b, -1) + np.roll(b, 1) - 2 * b
        b = b + dt * (-dJx + s - mu * b - lam_sink * g * b) + eps * visc
        J = J + dt * (-cg2 * dbx - J / tau)
        b[:3] = s / mu
        b[-3:] = s / mu
        J[:3] = 0.0
        J[-3:] = 0.0
    return J / b, b, x


def main():
    R = []

    # F6: circulation needs memory - measured vs the derived formula, per run
    def pred_circ(vc, tau, cg2, b):
        dlnb = 0.5 * (np.roll(b, -1) - np.roll(b, 1)) / b
        return -vc * cg2 * tau ** 2 * float((dlnb ** 2).sum())
    u_wave, b_wave = telegraph_ring(vc=0.3, tau=20.0, cg2=1.0, lam=0.01)
    u_2v, b_2v = telegraph_ring(vc=0.6, tau=20.0, cg2=1.0, lam=0.01)
    u_diff, _ = telegraph_ring(vc=0.3, tau=0.5, cg2=40.0, lam=0.01)  # same D, no memory
    u_stat, _ = telegraph_ring(vc=0.0, tau=20.0, cg2=1.0, lam=0.01)
    circ_w = float(u_wave.sum())
    circ_2v = float(u_2v.sum())
    circ_d = float(u_diff.sum())
    circ_s = float(u_stat.sum())
    pw = pred_circ(0.3, 20.0, 1.0, b_wave)
    p2 = pred_circ(0.6, 20.0, 1.0, b_2v)
    R.append(check("F6", abs(circ_w / pw - 1) < 0.35 and abs(circ_2v / p2 - 1) < 0.35
                   and abs(circ_d) < 0.15 * abs(circ_w)
                   and abs(circ_s) < 0.1 * abs(circ_w),
                   "budget circulation: wave-type exchange %.2f vs derived "
                   "-v*cg^2*tau^2*Int(lnb')^2 = %.2f (2x speed: %.2f vs %.2f - sublinear "
                   "because the wake shallows, per the same formula); pure DIFFUSION at "
                   "the same D: %.3f; static: %.3f - dragging requires the exchange to "
                   "have MEMORY; a diffusive fabric can never drag (small theorem)" %
                   (circ_w, pw, circ_2v, p2, circ_d, circ_s)))

    # F7: Sagnac on the derived u field
    tR = lap_time(u_wave, +1)
    tL = lap_time(u_wave, -1)
    dt_meas = tL - tR
    dt_pred = 2.0 * float((u_wave / (1.0 - u_wave ** 2)).sum())   # exact lap asymmetry, c = 1
    tRs = lap_time(u_stat, +1)
    tLs = lap_time(u_stat, -1)
    dt_stat = tLs - tRs
    R.append(check("F7", abs(dt_meas / dt_pred - 1) < 0.3
                   and abs(dt_stat) < 0.25 * abs(dt_meas),
                   "counter-propagating laps: dt = %.2f vs 2*circ/c^2 = %.2f (static-crowd "
                   "control %.2f) - the derived drag is REAL to waves: a Sagnac "
                   "interferometer around a moving mass reads its motion" %
                   (dt_meas, dt_pred, dt_stat)))

    # F8: a hungry sink builds its own horizon
    rows, maxu = [], {}
    rh = {}
    for lam in (0.005, 0.3, 1.0):
        u, b, x = telegraph_line(lam)
        au = np.abs(u)
        maxu[lam] = float(au.max())
        right = (x > 1500) & (x < 2600)
        cross = np.where(au[right] >= 1.0)[0]
        rh[lam] = float(x[right][cross].max() - 1500) if len(cross) else 0.0
        rows.append("appetite %.3f: max|u| %.2f, horizon radius %.0f" %
                    (lam, maxu[lam], rh[lam]))
    R.append(check("F8", maxu[0.005] < 1.0 and rh[0.3] > 0 and rh[1.0] > rh[0.3],
                   "the sink builds its own inflow: %s - below critical hunger no "
                   "horizon; above it the fabric falls faster than waves swim, at a "
                   "radius that grows with the appetite (the hole is DYNAMICAL, not "
                   "painted)" % "; ".join(rows)))

    print()
    print("FLU2: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
