"""GR ripples + 3D far field (V3 completion campaign, 2026-08-17).

RIP  a moving crowd radiates budget ripples: an oscillating source's field
     wiggle arrives at distant probes with the causal lag and decays with
     distance - gravitational waves as load transients (G6's promised sequel)
FF3  the 3D far field: budget diffusion around a ball of load falls as 1/r
     (2D gave log r; 3D gives Newton's actual potential shape)
"""

import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []

    # RIP: oscillating crowd radiates; probes at two distances
    Ng, dt, c = 192, 0.1, 1.0
    yy, xx = np.mgrid[0:Ng, 0:Ng]
    Cc = Ng // 2
    psi = np.zeros((Ng, Ng))
    prev = psi.copy()
    Om, A = 0.35, 3.0
    d1, d2 = 35, 60
    p1, p2, s_src = [], [], []
    sponge = np.ones((Ng, Ng))
    edge = np.minimum(np.minimum(xx, Ng - 1 - xx), np.minimum(yy, Ng - 1 - yy))
    sponge[edge < 12] = 0.985
    for s in range(2600):
        t = s * dt
        xc = Cc + A * math.sin(Om * t)
        rho = np.exp(-((xx - xc) ** 2 + (yy - Cc) ** 2) / (2 * 2.0 ** 2))
        lap = (np.roll(psi, 1, 0) + np.roll(psi, -1, 0) + np.roll(psi, 1, 1)
               + np.roll(psi, -1, 1) - 4 * psi)
        nxt = (2 * psi - prev + (c * dt) ** 2 * lap + dt * dt * rho) * sponge
        prev, psi = psi, nxt
        p1.append(psi[Cc + d1, Cc])
        p2.append(psi[Cc + d2, Cc])
        s_src.append(xc - Cc)
    p1 = np.array(p1)
    p2 = np.array(p2)
    a1 = float(np.std(p1[1200:] - p1[1200:].mean()))
    a2 = float(np.std(p2[1200:] - p2[1200:].mean()))
    # causal lag by ONSET (a monochromatic tail makes correlation lag mod-period)
    t_on1 = float(np.argmax(np.abs(p1) > 0.15 * a1)) * dt
    t_on2 = float(np.argmax(np.abs(p2) > 0.15 * a2)) * dt
    lag = t_on2 - t_on1
    pred_lag = (d2 - d1) / c
    R.append(check("RIP", abs(lag - pred_lag) < 0.3 * pred_lag and a2 < a1,
                   "oscillating crowd radiates: probe-to-probe lag %.1f vs causal %.1f "
                   "(field wiggles ride the cone); amplitude %.2e at d=35 -> %.2e at "
                   "d=60 (decays outward) - gravitational waves as load transients" %
                   (lag, pred_lag, a1, a2)))

    # FF3: 3D far field ~ 1/r
    n3 = 48
    z3, y3, x3 = np.mgrid[0:n3, 0:n3, 0:n3]
    C3 = n3 // 2
    r3 = np.sqrt((x3 - C3) ** 2 + (y3 - C3) ** 2 + (z3 - C3) ** 2)
    src = (r3 < 4).astype(float)
    phi = np.zeros((n3, n3, n3))
    for _ in range(6000):
        s6 = (np.roll(phi, 1, 0) + np.roll(phi, -1, 0) + np.roll(phi, 1, 1)
              + np.roll(phi, -1, 1) + np.roll(phi, 1, 2) + np.roll(phi, -1, 2))
        phi = (s6 + src) / 6.0
        phi[0, :, :] = phi[-1, :, :] = 0.0
        phi[:, 0, :] = phi[:, -1, :] = 0.0
        phi[:, :, 0] = phi[:, :, -1] = 0.0
    m = (r3 > 8) & (r3 < 18)
    inv_r = 1.0 / r3[m]
    vals = phi[m]
    aa, bb = np.polyfit(inv_r, vals, 1)
    r2_inv = 1 - ((vals - (aa * inv_r + bb)) ** 2).sum() / ((vals - vals.mean()) ** 2).sum()
    lg = np.log(r3[m])
    a2_, b2_ = np.polyfit(lg, vals, 1)
    r2_log = 1 - ((vals - (a2_ * lg + b2_)) ** 2).sum() / ((vals - vals.mean()) ** 2).sum()
    R.append(check("FF3", r2_inv > 0.99 and r2_inv > r2_log and aa > 0,
                   "3D budget field: fits 1/r with R^2 = %.4f (log fit: %.4f) - in three "
                   "dimensions the congestion far field IS Newton's potential shape; the "
                   "2D log was the toy's artifact, not the mechanism's" % (r2_inv, r2_log)))

    print()
    print("RIP/FF3: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
