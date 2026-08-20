"""Tsirelson scout (2026-08-17): does double-entry settlement explain the
2*sqrt(2) ceiling - and if not alone, WHICH ingredient does?

TS1  the model's own contract class - ONE persistent table, settings acting
     LOCALLY (each party rotates only their own factor), outcomes by
     double-entry settlement: optimize CHSH as hard as we can (thousands of
     restarts + refinement). Expectation: saturates at 2*sqrt(2) = 2.8284 and
     NEVER exceeds it.
TS2  the isolating control: a bespoke contract that REWRITES the second
     party's weights per (outcome, both settings) - still settled by the same
     two-signature protocol - reaches the PR-box value 4. So the square alone
     does not cap correlations; the cap = squares OF ONE LOCALLY-ROTATED
     TABLE. Within the model (P4 one contract + P5 local settings + dyadic
     settlement) the ceiling is INTERNAL; the residual question is why nature
     keeps single-table contracts.
"""

import hashlib
import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def apply_ry(v, q, theta):
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    v = v.copy()
    step = 1 << q
    for i in range(4):
        if not (i & step):
            j = i | step
            a0, a1 = v[i], v[j]
            v[i] = c * a0 - s * a1
            v[j] = s * a0 + c * a1
    return v


def corr(v, ta, tb):
    w = apply_ry(apply_ry(v, 0, -ta), 1, -tb)
    p = w ** 2
    return p[0] + p[3] - p[1] - p[2]


def chsh(params):
    v = params[:4]
    n = np.linalg.norm(v)
    if n < 1e-9:
        return -10.0
    v = v / n
    a0, a1, b0, b1 = params[4:]
    return (corr(v, a0, b0) + corr(v, a0, b1) + corr(v, a1, b0) - corr(v, a1, b1))


def main():
    R = []
    rng = np.random.default_rng(11)
    TSI = 2 * math.sqrt(2)

    # TS1: adversarial search of the one-table local-settings class
    best, best_p = -10.0, None
    global_max = -10.0
    for _ in range(4000):
        p = np.concatenate([rng.normal(size=4), rng.uniform(-math.pi, math.pi, 4)])
        s = chsh(p)
        global_max = max(global_max, s)
        if s > best:
            best, best_p = s, p
    # refine the champion with shrinking random perturbations
    step = 0.5
    p = best_p.copy()
    for it in range(6000):
        q = p + rng.normal(size=8) * step
        s = chsh(q)
        global_max = max(global_max, s)
        if s > best:
            best, p = s, q
        if it % 500 == 499:
            step *= 0.6
    R.append(check("TS1", best > 2.8283 and global_max <= TSI + 1e-6,
                   "one shared table + local settings + double-entry settlement: "
                   "10,000-point adversarial search reaches %.5f and NEVER exceeds "
                   "2*sqrt(2) = %.5f - the model's own contract class saturates exactly "
                   "at the Tsirelson ceiling" % (best, TSI)))

    # TS2: bespoke rewrite-contract under the SAME two-signature settlement -> PR
    def u01(h):
        return int(h[:12], 16) / 16 ** 12
    def H(*parts):
        return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    def settle(seed_parts, norms):
        # propose uniformly among branches; two signatures each vs the branch norm
        k = 0
        while True:
            k += 1
            b = int(u01(H(*seed_parts, "prop", k)) * len(norms))
            amp = norms[b]
            if (u01(H(*seed_parts, "sigA", k)) < amp
                    and u01(H(*seed_parts, "sigB", k)) < amp):
                return b
    N = 20000
    tot = {(x, y): 0.0 for x in (0, 1) for y in (0, 1)}
    counts = {k: 0 for k in tot}
    marg = 0
    for t in range(N):
        x = int(u01(H("set", t, "x")) * 2)
        y = int(u01(H("set", t, "y")) * 2)
        a = settle(("alice", t), [math.sqrt(0.5), math.sqrt(0.5)])
        want = a ^ (x & y)
        b = settle(("bob", t), [1.0 if bb == want else 0.0 for bb in (0, 1)])
        tot[(x, y)] += (1 if a == b else -1)
        counts[(x, y)] += 1
        marg += a
    E = {k: tot[k] / counts[k] for k in tot}
    S_pr = E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)]
    R.append(check("TS2", S_pr > 3.95 and abs(marg / N - 0.5) < 0.02,
                   "the SAME two-signature settlement serving a rewrite-contract: "
                   "S = %.3f (PR box; Alice marginal %.3f, flat) - the square alone "
                   "does not cap correlations; the ceiling = squares of ONE "
                   "locally-rotated persistent table. Within the model, Tsirelson is "
                   "now INTERNAL (P4 + P5 + dyadic settlement); the residue: why "
                   "nature keeps single-table contracts" % (S_pr, marg / N)))

    print()
    print("TSIRELSON: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT",
                                         len(R)))
    return all(R)


if __name__ == "__main__":
    main()
