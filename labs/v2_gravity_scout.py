"""V2-2 gravity scouts: compute-in-the-grid (design: v2/design-notes.md).

Mechanism under test: grid nodes exchange signals (the cameras); the exchange carries
the compute-budget field; a crowd of particles raises local demand; the region's tick
rate drops; events go slower there. Deterministic PDE scouts - no randomness anywhere.

G1  field shape      budget field from LOCAL exchange only -> log(d) far field in 2D
                     (Newton's Poisson equation from neighbor equilibration), and
                     dilation in EMPTY space (field, not contact effect)
G2  light bending    rays refract TOWARD the crowd; 2D signature: deflection ~ flat in
                     impact parameter; deflection doubles when the crowd mass doubles
G3  free fall        a packet AT REST drifts toward the crowd (slow region = lower
                     local phase rate = potential well); displacement ~ (1/2) a t^2
G4  equivalence      with the Compton clock (internal frequency ~ mass), trajectories
                     are MASS-INDEPENDENT; control without the scaling breaks it
"""

import math

import numpy as np

N = 128
C = 64.0
CROWD_R = 6.0


def crowd_density(scale=1.0):
    y, x = np.mgrid[0:N, 0:N]
    rho = np.zeros((N, N))
    rho[(x - C) ** 2 + (y - C) ** 2 <= CROWD_R ** 2] = scale
    return rho


def solve_field(rho, iters=15000):
    # budget equilibration by NEIGHBOR EXCHANGE ONLY (Jacobi) = Poisson with Phi=0 far away
    p = np.zeros((N, N))
    for _ in range(iters):
        p[1:-1, 1:-1] = 0.25 * (p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:] + p[1:-1, :-2]
                                + rho[1:-1, 1:-1])
    res = np.abs(0.25 * (p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:] + p[1:-1, :-2]
                         + rho[1:-1, 1:-1]) - p[1:-1, 1:-1]).max()
    return p, res


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def bilinear(a, x, y):
    x0, y0 = int(x), int(y)
    fx, fy = x - x0, y - y0
    return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy)
            + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)


def trace_ray(n_field, b, ds=0.1):
    gy, gx = np.gradient(n_field)
    x, y = 10.0, C + b
    vx, vy = 1.0, 0.0
    while 8.0 < x < 118.0 and 8.0 < y < 118.0:
        nn = bilinear(n_field, x, y)
        dnx, dny = bilinear(gx, x, y), bilinear(gy, x, y)
        dot = dnx * vx + dny * vy
        vx += ds * (dnx - dot * vx) / nn
        vy += ds * (dny - dot * vy) / nn
        norm = math.hypot(vx, vy)
        vx, vy = vx / norm, vy / norm
        x += vx * ds
        y += vy * ds
    return math.atan2(vy, vx)


def evolve_packet(V, m, x0, t_total, dt=0.02):
    k = 2 * np.pi * np.fft.fftfreq(N)
    kx, ky = np.meshgrid(k, k)
    kin = np.exp(-1j * (kx ** 2 + ky ** 2) * dt / (2 * m))
    pot = np.exp(-1j * V * dt / 2)
    y, x = np.mgrid[0:N, 0:N]
    sig = 6.0
    psi = np.exp(-(((x - x0) ** 2 + (y - C) ** 2) / (4 * sig ** 2))).astype(complex)
    psi /= np.sqrt((np.abs(psi) ** 2).sum())
    traj = []
    steps = int(t_total / dt)
    for s in range(steps):
        psi = pot * psi
        psi = np.fft.ifft2(kin * np.fft.fft2(psi))
        psi = pot * psi
        if s % 100 == 0:
            traj.append((np.abs(psi) ** 2 * x).sum())
    traj.append((np.abs(psi) ** 2 * x).sum())
    return np.array(traj)


def main():
    R = []
    rho1 = crowd_density(1.0)
    phi1, res1 = solve_field(rho1)
    scale = phi1.max()
    phi_n = phi1 / scale                       # base crowd -> peak 1.0 by definition
    g = 0.3                                     # rate r(x) = 1 - g*Phi ; slowest 0.7
    print("field residual %.2e, peak load %.1f (normalized to 1.0)" % (res1, scale))

    # G1: log far field + dilation in empty space
    ds = np.arange(10, 46)
    prof = np.array([phi_n[int(C), int(C + d)] for d in ds])
    lo = np.log(ds)
    A = np.vstack([lo, np.ones_like(lo)]).T
    coef, resid, _, _ = np.linalg.lstsq(A, prof, rcond=None)
    ss_tot = ((prof - prof.mean()) ** 2).sum()
    r2 = 1 - resid[0] / ss_tot
    rate_at = lambda d: 1 - g * phi_n[int(C), int(C + d)]
    R.append(check("G1", r2 > 0.98 and prof[20] > 0.05,
                   "far field ~ log d (R^2 = %.4f); EMPTY-space dilation: clock at d=30 runs "
                   "x%.3f of far clock (density there = 0)" % (r2, rate_at(30) / rate_at(45))))

    # G2: bending toward the crowd; flat in b; linear in crowd mass.
    # WEAK-FIELD regime (gw << g): the x2 mass-linearity is a weak-field prediction;
    # at strong coupling deflection goes superlinear (as it should - gravity is nonlinear).
    gw = 0.08
    n1 = 1.0 / (1 - gw * phi_n)
    angles = [trace_ray(n1, b) for b in (12, 16, 20, 24, 28)]
    toward = all(a < 0 for a in angles)        # ray passes above crowd -> bends down
    mags = np.abs(angles)
    flat = mags.std() / mags.mean()
    phi2, _ = solve_field(crowd_density(2.0))
    n2 = 1.0 / (1 - gw * phi2 / scale)         # same normalization: double mass = double field
    ratio = abs(trace_ray(n2, 20)) / abs(trace_ray(n1, 20))
    R.append(check("G2", toward and flat < 0.25 and abs(ratio - 2) < 0.3,
                   "all rays bend toward crowd; deflection %.4f+/-%.4f rad, flatness %.2f "
                   "(2D log signature); double mass -> x%.2f deflection (weak field)" %
                   (mags.mean(), mags.std(), flat, ratio)))

    # G3: free fall of a packet at rest (Compton clock: V = -m * g * Phi)
    m, x0, T = 1.0, C + 25, 40.0
    gyp, gxp = np.gradient(phi_n)
    a_pred = g * abs(bilinear(gxp, x0, C))
    traj1 = evolve_packet(-m * g * phi_n, m, x0, T)
    drift = x0 - traj1[-1]
    pred = 0.5 * a_pred * T * T
    R.append(check("G3", drift > 0 and 0.6 < drift / pred < 1.7,
                   "packet at rest falls TOWARD crowd: drift %.2f cells (naive (1/2)at^2 = %.2f; "
                   "field steepens on approach)" % (drift, pred)))

    # G4: equivalence principle - needs the Compton clock
    traj2 = evolve_packet(-2.0 * g * phi_n, 2.0, x0, T)      # mass 2, V scaled with mass
    dev = np.abs(traj1 - traj2).max()
    traj2c = evolve_packet(-1.0 * g * phi_n, 2.0, x0, T)     # CONTROL: V not scaled
    dev_c = abs(traj1[-1] - traj2c[-1])                       # theory: separates by drift/2
    R.append(check("G4", dev < 0.15 * drift and dev_c > 0.35 * drift,
                   "Compton-scaled: m=1 and m=2 trajectories agree to %.2f cells (equivalence); "
                   "control without scaling separates by %.2f cells (theory: %.2f)"
                   % (dev, dev_c, 0.5 * drift)))

    print()
    print("V2-2 SCOUTS: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
