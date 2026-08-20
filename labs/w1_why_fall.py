"""W1 - why things fall toward busy compute (user question, 2026-08-16).

Claim: NO steering rule is needed - but only because particles are extended waves.
A wave's two flanks are processed at different rates; the resulting phase tilt IS
momentum toward the slow side (Huygens). A POINT particle, by contrast, has no
flanks: local slowdown scales its speed but has no lever on its direction - a point
with no bolted-on rule does not fall and does not deflect.

W1a  at rest: point particle stays forever; wave packet falls toward the crowd
W1b  passing by: point particle crosses dead straight; wave packet deflects toward
     the crowd - gravity in this model is an interference effect
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2_gravity_scout import C, N, bilinear, crowd_density, evolve_packet, solve_field

G = 0.3


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def point_particle(phi_n, x0, y0, vx, vy, T, dt=0.02):
    # a point with position+direction; local slowdown scales SPEED only (no flanks,
    # no phase, nothing to tilt); direction has no coupling to the field
    x, y = x0, y0
    for _ in range(int(T / dt)):
        r = 1 - G * bilinear(phi_n, x, y)
        x += vx * r * dt
        y += vy * r * dt
        if not (2 < x < N - 2 and 2 < y < N - 2):
            break
    return x, y


def wave_transverse(phi_n, b, v, m, T, dt=0.02):
    # reuse the engine: packet crossing at impact parameter b; measure transverse drift
    k = 2 * np.pi * np.fft.fftfreq(N)
    kx, ky = np.meshgrid(k, k)
    kin = np.exp(-1j * (kx ** 2 + ky ** 2) * dt / (2 * m))
    V = -m * G * phi_n
    pot = np.exp(-1j * V * dt / 2)
    yy, xx = np.mgrid[0:N, 0:N]
    sig = 5.0
    psi = np.exp(-(((xx - 20.0) ** 2 + (yy - (C + b)) ** 2) / (4 * sig ** 2))).astype(complex)
    psi *= np.exp(1j * (m * v) * xx)
    psi /= np.sqrt((np.abs(psi) ** 2).sum())
    for _ in range(int(T / dt)):
        psi = pot * psi
        psi = np.fft.ifft2(kin * np.fft.fft2(psi))
        psi = pot * psi
    w = np.abs(psi) ** 2
    return (w * xx).sum(), (w * yy).sum()


def main():
    R = []
    phi, _ = solve_field(crowd_density(1.0))
    phi_n = phi / phi.max()

    # W1a: at rest in the gradient
    d0 = 25.0
    px, py = point_particle(phi_n, C + d0, C, 0.0, 0.0, T=150.0)
    point_moved = math.hypot(px - (C + d0), py - C)
    traj = evolve_packet(-4.0 * G * phi_n, 4.0, C + d0, 150.0)
    wave_fall = (C + d0) - traj[-1]
    R.append(check("W1a", point_moved < 1e-9 and wave_fall > 5,
                   "at rest: point particle moves %.1e cells (slowdown has no lever on it); "
                   "wave packet falls %.1f cells toward the crowd - no rule, just flanks"
                   % (point_moved, wave_fall)))

    # W1b: passing the crowd at the same impact parameter and speed
    b, v, m, T = 18.0, 1.5, 1.0, 42.0                  # m*v < pi (grid Nyquist)
    pxx, pyy = point_particle(phi_n, 20.0, C + b, v, 0.0, T)
    point_trans = pyy - (C + b)
    wx, wy = wave_transverse(phi_n, b, v, m, T)
    wave_trans = wy - (C + b)
    R.append(check("W1b", abs(point_trans) < 1e-9 and wave_trans < -1.5,
                   "passing at b = %.0f: point deflects %.1e (dead straight); wave deflects "
                   "%.1f cells toward the crowd - gravity here is an interference effect"
                   % (b, point_trans, wave_trans)))

    print()
    print("W1: %s (%d checks) - slowdown steers nothing pointlike; the wave's two flanks "
          "disagree about elapsed time, and that disagreement IS the fall"
          % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
