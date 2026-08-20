"""M2 - the breathing fabric (user's corrected picture, 2026-08-16).

One rule: stuff always slows compute. The SHAPE of the load is the geometry:
  peaked load (matter, node channel: clocks + potential)  -> bubble = gravity, transient
  uniform load (radiation, link channel: hop tax)         -> stretch = expansion, cumulative
Entropy increase = the conversion: clumps radiate, wells level, the fabric stretches.

Declared (not derived): the node/link channel assignment - required for observability,
since a fully uniform all-channel slowdown is invisible (E3). Measured here = the
DYNAMICS: wells transient, stretch monotone, both riding one conserved total,
coexistence in between ("bubbles on a stretching fabric").

M2a  well depth decays as matter radiates (gravity is the transient part)
M2b  GLOBAL stretch grows monotonically, riding total radiated mass
M2c  spatial entropy rises monotonically; global stretch rises with it (rank corr 1)
M2d  mid-run coexistence: deep wells AND substantial stretch at once
M2e  the bubble-to-fabric flow: a row through the clumps overshoots (local radiation
     bubble) then relaxes toward the uniform value; a far row only ever stretches;
     the two converge - "bubbles form locally, then extend to the global fabric"
"""

import math

import numpy as np

N = 96
LAM = 0.008          # matter -> radiation conversion per step (entropy production)
G_R = 0.5            # link (hop) tax per unit radiation density
STEPS = 600
SAMPLE = 30
D_SUB = 5            # diffusion substeps, dt = 0.2


def laplace_neumann(p):
    # flux-free boundaries: the fabric keeps its stuff (conservative diffusion)
    pe = np.pad(p, 1, mode="edge")
    return (pe[2:, 1:-1] + pe[:-2, 1:-1] + pe[1:-1, 2:] + pe[1:-1, :-2] - 4 * p)


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []
    y, x = np.mgrid[0:N, 0:N]
    rho_m = np.zeros((N, N))
    for cx, cy in ((30, 48), (66, 40), (50, 70)):
        rho_m += 40.0 * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * 4.0 ** 2))
    rho_r = np.zeros((N, N))
    total0 = rho_m.sum()

    phi = np.zeros((N, N))
    samples = []
    for step in range(STEPS + 1):
        if step % SAMPLE == 0:
            for _ in range(20000 if step == 0 else 1200):   # cold-start converged, then warm
                phi[1:-1, 1:-1] = 0.25 * (phi[2:, 1:-1] + phi[:-2, 1:-1]
                                          + phi[1:-1, 2:] + phi[1:-1, :-2]
                                          + rho_m[1:-1, 1:-1])
            well = phi.max()
            cr_near = N + G_R * rho_r[N // 2, :].sum()   # row through the clumps
            cr_far = N + G_R * rho_r[8, :].sum()         # row far from any clump
            cr_glob = N + G_R * rho_r.sum() / N          # all-row average (global stretch)
            tot = rho_m + rho_r
            p = (tot / tot.sum()).ravel()
            p = p[p > 0]
            S = float(-(p * np.log(p)).sum())
            samples.append((step, well, cr_near, cr_far, cr_glob, S, total0 - rho_m.sum()))
        dm = LAM * rho_m
        rho_m -= dm
        rho_r += dm
        for _ in range(D_SUB):
            rho_r += 0.2 * laplace_neumann(rho_r)

    steps_, wells, near, far, glob, ents, radiated = map(np.array, zip(*samples))
    conserved = abs((rho_m.sum() + rho_r.sum()) / total0 - 1)
    uniform_pred = N + G_R * total0 / N
    print("conservation drift %.2e; matter remaining %.1f%%; uniform prediction %.1f ticks"
          % (conserved, 100 * rho_m.sum() / total0, uniform_pred))
    print("  step   well  near-row  far-row  global  entropy  radiated")
    for s, w, cn, cf, cg, e, rr in samples:
        print("  %4d  %6.1f  %8.1f  %7.1f  %6.1f  %7.4f  %8.0f" % (s, w, cn, cf, cg, e, rr))

    # M2a: wells are the transient part
    mono_dn = all(b <= a * 1.001 for a, b in zip(wells, wells[1:]))
    R.append(check("M2a", mono_dn and wells[-1] < 0.05 * wells[0],
                   "well depth decays monotonically to %.1f%% of initial - gravity fades as "
                   "its stuff radiates" % (100 * wells[-1] / wells[0])))

    # M2b: the GLOBAL stretch is monotone and rides total radiated mass
    # (linearity is conservation-level bookkeeping, declared; the physics content is
    # that radiated mass - entropy's arrow - only ever grows)
    mono_up = all(b >= a - 1e-9 for a, b in zip(glob, glob[1:]))
    R.append(check("M2b", mono_up and glob[-1] / glob[0] > 1.3,
                   "global stretch %.0f -> %.0f ticks (x%.2f), never shrinks, riding radiated "
                   "mass; uniform prediction %.1f" % (glob[0], glob[-1], glob[-1] / glob[0],
                                                      uniform_pred)))

    # M2c: entropy and stretch rise together
    ent_mono = (all(b >= a - 1e-5 * abs(a) for a, b in zip(ents, ents[1:]))
                and ents[-1] > ents[0] + 0.5)
    R.append(check("M2c", ent_mono and mono_up,
                   "spatial entropy %.2f -> %.2f, monotone; global stretch monotone with it "
                   "(rank correlation 1.0) - the fabric stretches BECAUSE entropy rises"
                   % (ents[0], ents[-1])))

    # M2d: the in-between - bubbles on a stretching fabric
    gain = glob - glob[0]
    co = [(w >= 0.35 * wells[0]) and (g >= 0.3 * gain[-1]) for w, g in zip(wells, gain)]
    R.append(check("M2d", any(co),
                   "mid-run coexistence at t=%s: wells still >= 35%% deep while >= 30%% of the "
                   "final stretch is already in - bubbles forming on a stretching fabric"
                   % ([int(s) for s, c in zip(steps_, co) if c][:3])))

    # M2e: the bubble-to-fabric flow (the user's sentence, measured)
    peak = near.max()
    far_mono = all(b >= a - 1e-9 for a, b in zip(far, far[1:]))
    relax = abs(near[-1] - uniform_pred) < 0.5 * abs(peak - uniform_pred)
    gap = near - far
    gap_shrinks = gap[-1] < 0.4 * gap.max()
    R.append(check("M2e", peak > uniform_pred + 5 and near[-1] < peak and relax
                   and far_mono and gap_shrinks,
                   "clump row overshoots to %.0f (bubble), relaxes to %.0f toward uniform %.1f; "
                   "far row only ever stretches (%.0f -> %.0f); near-far gap %.0f -> %.0f - "
                   "bubbles level into the global fabric"
                   % (peak, near[-1], uniform_pred, far[0], far[-1], gap.max(), gap[-1])))

    print()
    print("M2: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
