"""3D gravity port (2026-08-17) - the dimension drawback resolved, and the
model's PPN parameters measured.

The dictionary (declared, from measured V2 behavior): local rate r = 1 - GM/rad
slows BOTH clocks and hops -> g00 = -r^2, coordinate light speed = r^2
(index n = r^-2). Dynamics at the eikonal/point level (W1-certified concept:
waves derive it, points get it declared). The 3D far field is 1/r (GR-30/FF3).

K3D   Kepler closure: eccentric orbit in the 3D 1/r field closes (apsidal
      angle = pi) - the 2D log-potential precession was the DIMENSION's
      artifact, not the mechanism's
BEND  absolute bending: deflection = 4GM/b, the full GR value (gamma = 1
      measured), falling as 1/b
PPN   perihelion audit: the rate-squared clock gives beta = 1/2, predicting
      precession at (2+2*gamma-beta)/3 = 7/6 of GR - measured. A NAMED,
      falsifiable deviation: the model currently overshoots Mercury by 17%;
      deriving the beta = 1 nonlinearity is the sharpest open dial.
"""

import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def newton_apsidal(GM, r1, r2, npts=20000):
    L2 = 2 * GM * r1 * r2 / (r1 + r2)
    E = -GM / (r1 + r2)
    psi = (np.arange(npts) + 0.5) / npts * (math.pi / 2)
    r = r1 + (r2 - r1) * np.sin(psi) ** 2
    dr = (r2 - r1) * np.sin(2 * psi) * (math.pi / 2) / npts
    rdot2 = np.clip(2 * E + 2 * GM / r - L2 / r ** 2, 1e-30, None)
    return float((math.sqrt(L2) / (r ** 2 * np.sqrt(rdot2)) * dr).sum())


def metric_apsidal(A, B, r1, r2, npts=40000):
    # turning conditions: E^2/A_i - L^2/(B_i r_i^2) = 1, solved linearly
    M = np.array([[1 / A(r1), -1 / (B(r1) * r1 ** 2)],
                  [1 / A(r2), -1 / (B(r2) * r2 ** 2)]])
    E2, L2 = np.linalg.solve(M, np.array([1.0, 1.0]))
    psi = (np.arange(npts) + 0.5) / npts * (math.pi / 2)
    r = r1 + (r2 - r1) * np.sin(psi) ** 2
    dr = (r2 - r1) * np.sin(2 * psi) * (math.pi / 2) / npts
    rdot2 = np.clip((E2 / A(r) - 1 - L2 / (B(r) * r ** 2)) / B(r), 1e-30, None)
    dphi = math.sqrt(L2) / (B(r) * r ** 2 * np.sqrt(rdot2))
    return float((dphi * dr).sum())


def trace_ray(GM, b, ds=0.25, span=1600.0):
    pos = np.array([-span, b])
    t = np.array([1.0, 0.0])
    for _ in range(int(2 * span / ds) + 10):
        rad = math.hypot(pos[0], pos[1])
        rhat = pos / rad
        grad = -2 * (GM / rad ** 2) / (1 - GM / rad) * rhat      # grad ln n
        perp = grad - (grad @ t) * t
        t = t + perp * ds
        t /= math.hypot(t[0], t[1])
        pos = pos + t * ds
        if pos[0] > span:
            break
    return abs(math.atan2(t[1], t[0]))


def main():
    R = []
    GM = 1.0

    # K3D: the ellipse closes in 3D
    aps = newton_apsidal(GM, 40.0, 80.0)
    R.append(check("K3D", abs(aps - math.pi) < 0.01,
                   "eccentric orbit in the 3D 1/r field: apsidal angle %.4f (pi = "
                   "3.1416; the 2D log field gave 2.22) - closed ellipses: the old "
                   "precession drawback was the dimension's artifact, resolved" % aps))

    # BEND: leading coefficient of the deflection law via a two-term 1/b fit
    bs = np.array([40.0, 60.0, 90.0, 135.0, 200.0])
    als = np.array([trace_ray(GM, b) for b in bs])
    X = np.stack([1.0 / bs, 1.0 / bs ** 2], axis=1)
    c1, c2 = np.linalg.lstsq(X, als, rcond=None)[0]
    lead = c1 / (4 * GM)
    R.append(check("BEND", abs(lead - 1) < 0.03,
                   "deflection fits alpha = c1/b + c2/b^2 with c1 = %.3f x 4GM (the "
                   "FULL GR leading value: gamma = 1 measured; c2 = %.1f GM^2 = the "
                   "strong-field correction, reported) - the 1/b far-field law, "
                   "unreachable in 2D" % (lead, c2)))

    # PPN: the beta = 1/2 audit, weak field, with a Schwarzschild control through
    # the SAME integrator
    r1, r2 = 400.0, 800.0
    p = 2 * r1 * r2 / (r1 + r2)
    gr = 6 * math.pi * GM / p
    def A_ours(r):
        return (1 - GM / r) ** 2
    def B_ours(r):
        return (1 - GM / r) ** -2
    def A_schw(r):
        u = GM / (2 * r)
        return ((1 - u) / (1 + u)) ** 2
    def B_schw(r):
        return (1 + GM / (2 * r)) ** 4
    prec = 2 * metric_apsidal(A_ours, B_ours, r1, r2) - 2 * math.pi
    prec_s = 2 * metric_apsidal(A_schw, B_schw, r1, r2) - 2 * math.pi
    ours_pred = (2 + 2 * 1 - 0.5) / 3                          # 7/6, gamma=1 beta=1/2
    R.append(check("PPN", abs(prec_s / gr - 1) < 0.03
                   and abs((prec / gr) / ours_pred - 1) < 0.04,
                   "perihelion advance: Schwarzschild control through the same "
                   "integrator = %.4f x GR (instrument certified); the model's metric "
                   "g00 = -(1-GM/r)^2 gives %.4f x GR vs its own PPN prediction 7/6 = "
                   "1.1667 (gamma=1, beta=1/2) - a NAMED falsifiable deviation: +17%% "
                   "on Mercury; deriving the beta=1 nonlinearity is the sharpest open "
                   "dial in the gravity sector" % (prec_s / gr, prec / gr)))

    print()
    print("GR-3D: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
