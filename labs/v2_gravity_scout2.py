"""V2-2 gravity scouts, round 2: orbits and gravity-at-c.

G5  orbits          a packet with the right tangential momentum CIRCLES the crowd
                    (celestial mechanics from scheduling); at rest it falls; too
                    fast it escapes
G6  gravity at c    budget exchanged by WAVE-type neighbor signalling: field changes
                    arrive ballistically (t ~ d, the causal cone), unlike diffusion
                    (t ~ d^2); and the settled field still matches the Poisson one
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2_gravity_scout import C, N, bilinear, crowd_density, solve_field

G = 0.3


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def evolve_traj(V, m, x0, y0, px, py, t_total, dt=0.02):
    k = 2 * np.pi * np.fft.fftfreq(N)
    kx, ky = np.meshgrid(k, k)
    kin = np.exp(-1j * (kx ** 2 + ky ** 2) * dt / (2 * m))
    pot = np.exp(-1j * V * dt / 2)
    y, x = np.mgrid[0:N, 0:N]
    sig = 6.0
    psi = np.exp(-(((x - x0) ** 2 + (y - y0) ** 2) / (4 * sig ** 2))).astype(complex)
    psi *= np.exp(1j * (px * x + py * y))
    psi /= np.sqrt((np.abs(psi) ** 2).sum())
    traj = []
    for s in range(int(t_total / dt)):
        psi = pot * psi
        psi = np.fft.ifft2(kin * np.fft.fft2(psi))
        psi = pot * psi
        if s % 100 == 0:
            w = np.abs(psi) ** 2
            traj.append(((w * x).sum(), (w * y).sum()))
    return np.array(traj)


def main():
    R = []
    phi, _ = solve_field(crowd_density(1.0))
    phi_n = phi / phi.max()
    gyp, gxp = np.gradient(phi_n)

    # G5: orbits - v_orb = sqrt(a * r) from the measured field, mass-independent (Compton)
    r0, m, T = 25.0, 4.0, 150.0
    a = G * abs(bilinear(gxp, C + r0, C))
    v_orb = math.sqrt(a * r0)
    V = -m * G * phi_n
    runs = {
        "orbit": evolve_traj(V, m, C + r0, C, 0.0, m * v_orb, T),
        "rest": evolve_traj(V, m, C + r0, C, 0.0, 0.0, T),
        "fast": evolve_traj(V, m, C + r0, C, 0.0, 1.5 * m * v_orb, T),
    }
    rad = {k: np.hypot(t[:, 0] - C, t[:, 1] - C) for k, t in runs.items()}
    ang = np.unwrap(np.arctan2(runs["orbit"][:, 1] - C, runs["orbit"][:, 0] - C))
    swept = math.degrees(abs(ang[-1] - ang[0]))
    ok5 = (rad["orbit"].min() > 0.75 * r0 and rad["orbit"].max() < 1.30 * r0
           and swept > 80 and rad["rest"].min() < 0.6 * r0 and rad["fast"].max() > 1.35 * r0)
    R.append(check("G5", ok5,
                   "v_orb from the field: radius held in [%.1f, %.1f] (r0 = %d), swept %.0f deg; "
                   "at rest falls to r = %.1f; at 1.5x escapes to r = %.1f"
                   % (rad["orbit"].min(), rad["orbit"].max(), int(r0), swept,
                      rad["rest"].min(), rad["fast"].max())))

    # G6: wave-type budget exchange - ballistic arrival, then the same static field
    rho = crowd_density(1.0)
    dt, gamma = 0.5, 0.02
    dets = [20, 30, 40, 50]
    eps = 0.05

    def laplace(p):
        out = np.zeros_like(p)
        out[1:-1, 1:-1] = (p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:] + p[1:-1, :-2]
                           - 4 * p[1:-1, 1:-1])
        return out

    p_now = np.zeros((N, N))
    p_old = np.zeros((N, N))
    arrive_w = {}
    for s in range(20000):
        p_new = (2 * p_now - p_old + dt * dt * (laplace(p_now) + rho)
                 - gamma * dt * (p_now - p_old))
        p_new[0, :] = p_new[-1, :] = p_new[:, 0] = p_new[:, -1] = 0
        p_old, p_now = p_now, p_new
        t = (s + 1) * dt
        for d in dets:
            if d not in arrive_w and p_now[int(C), int(C + d)] > eps:
                arrive_w[d] = t
    slope_w = np.polyfit(dets, [arrive_w[d] for d in dets], 1)[0]

    p_h = np.zeros((N, N))
    dth = 0.2
    arrive_d = {}
    s = 0
    while len(arrive_d) < len(dets) and s < 400000:
        p_h += dth * (laplace(p_h) + rho)
        s += 1
        for d in dets:
            if d not in arrive_d and p_h[int(C), int(C + d)] > eps:
                arrive_d[d] = s * dth
    logfit = np.polyfit(np.log(dets), np.log([arrive_d[d] for d in dets]), 1)[0]

    prof_w = np.array([p_now[int(C), int(C + d)] for d in range(10, 46)])
    prof_p = np.array([phi[int(C), int(C + d)] for d in range(10, 46)])
    static_dev = np.abs(prof_w - prof_p).max() / prof_p.max()

    ok6 = 0.8 < slope_w < 1.6 and logfit > 1.6 and static_dev < 0.08
    R.append(check("G6", ok6,
                   "wave exchange: arrival t ~ %.2f * d (ballistic - the field change rides the "
                   "causal cone); diffusion control: t ~ d^%.2f; settled wave field matches the "
                   "Poisson field to %.1f%%" % (slope_w, logfit, 100 * static_dev)))

    print()
    print("V2-2 ROUND 2: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
