"""M3 - the closed fabric (user's ball universe, point 3) + massless bending (point 1).

The fabric is CLOSED (periodic torus here; the ball has no center and no edges).
On a closed fabric, Poisson's solvability condition FORCES the decomposition the
model wants: only the CONTRAST (rho - mean) can source the potential; the mean has
no solution and must act globally (the stretch). "Only contrast bends" stops being
a declared channel split and becomes topology.

And the source is TOTAL load - massless stuff (radiation) bends too, while it is
concentrated; once leveled it lives only in the mean (the global channel).

M3a  uniform bath: zero contrast -> zero field (forced; same mass as a clump, no well)
M3b  a radiation clump bends exactly like an equal-mass matter clump
M3c  as the radiation clump levels, its well fades into the mean; the matter well
     persists; total load on the closed fabric exactly conserved
"""

import numpy as np

N = 96


def lap_periodic(p):
    return (np.roll(p, 1, 0) + np.roll(p, -1, 0) + np.roll(p, 1, 1) + np.roll(p, -1, 1)
            - 4 * p)


def solve_periodic(rho, phi=None, iters=20000):
    src = rho - rho.mean()                 # forced: only zero-mean sources are solvable
    p = np.zeros_like(rho) if phi is None else phi.copy()
    for _ in range(iters):
        p = 0.25 * (np.roll(p, 1, 0) + np.roll(p, -1, 0) + np.roll(p, 1, 1)
                    + np.roll(p, -1, 1) + src)
        p -= p.mean()
    return p


def clump(cx, cy):
    y, x = np.mgrid[0:N, 0:N]
    return 40.0 * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * 4.0 ** 2))


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []
    m_clump = clump(24, 48)
    mass = m_clump.sum()

    # M3a: same mass, uniform -> no field at all (topologically forced)
    uniform = np.full((N, N), mass / N ** 2)
    phi_u = solve_periodic(uniform, iters=200)
    phi_m = solve_periodic(m_clump)
    R.append(check("M3a", abs(phi_u).max() < 1e-9 and phi_m.max() > 100,
                   "same mass: uniform bath -> field %.1e (nothing bends, forced by "
                   "solvability); clumped -> well contrast %.0f" % (abs(phi_u).max(),
                                                                    phi_m.max())))

    # M3b: a radiation clump bends like an equal-mass matter clump
    r_clump = clump(72, 48)
    phi_r = solve_periodic(r_clump)
    ratio = phi_r.max() / phi_m.max()
    R.append(check("M3b", abs(ratio - 1) < 0.02,
                   "radiation clump well / matter clump well = %.4f - massless stuff bends "
                   "too, while concentrated" % ratio))

    # M3c: the radiation well fades into the mean as it levels; the matter well persists
    rho_m = m_clump
    rho_r = r_clump.copy()
    total0 = (rho_m + rho_r).sum()
    phi = solve_periodic(rho_m + rho_r)
    c_m0, c_r0 = phi[48, 24], phi[48, 72]
    for step in range(400):
        for _ in range(5):
            rho_r += 0.2 * lap_periodic(rho_r)
    phi = solve_periodic(rho_m + rho_r, phi=phi, iters=20000)
    c_m1, c_r1 = phi[48, 24], phi[48, 72]
    drift = abs((rho_m + rho_r).sum() / total0 - 1)
    R.append(check("M3c", c_r1 < 0.15 * c_r0 and abs(c_m1 / c_m0 - 1) < 0.15
                   and drift < 1e-12,
                   "radiation well %.0f -> %.0f (leveled into the mean); matter well "
                   "%.0f -> %.0f (persists); closed-fabric conservation drift %.1e"
                   % (c_r0, c_r1, c_m0, c_m1, drift)))

    print()
    print("M3: %s (%d checks) - on a closed fabric, 'only contrast bends' is topology, "
          "not a choice" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
