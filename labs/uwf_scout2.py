"""UWF scouts II - the snapshot isomorphism and the scale laws (SUB-19..21).

The demystification target (user, 2026-08-20): show the universe's global state
can be JUST BIG - a distributed system - with no black magic required.

SN1  Psi = a consistent cut (Chandy-Lamport): two different valid cuts through
     the same execution give DIFFERENT "instantaneous Psi" views but IDENTICAL
     settled records; two linear extensions of ONE cut give the same Psi (the
     cut is well-defined); and a freeze-everything-now wall-clock snapshot
     violates conservation (misses in-flight records) while the consistent
     snapshot conserves exactly - there is no global now, measured
SC1  the entanglement phase diagram: merges grow clusters, settlements cut
     them; control r = merge/settle. Two mean-field predictions were derived
     IN ADVANCE from count balance: (a) singleton fraction = 1 - r; (b) gel
     onset at r_c = 1. Measured: (a) CONFIRMED; (b) REFUTED - the giant
     cluster onsets EARLIER (r_c between 0.25 and 0.5), because merges pick
     random PARTICLES, so big clusters are hit in proportion to their mass:
     the multiplicative kernel (Erdos-Renyi giant-component physics), which
     gels before count balance breaks. The failed prediction is the finding.
SC2  the linear-storage law AND the storage transition: steady-state storage
     S(N) = c(r) * N (fit across N) holds in the CHEAP phase, whose boundary
     is SHARPER than percolation - Sum 2^k stays linear only while the
     cluster-size tail e^(-alpha k) beats 2^k, i.e. alpha > ln 2. Measured:
     the linear law with c(r) at deep-subcritical r; the tail slope crossing
     ln 2 between r = 0.1 and 0.2 (storage fluctuation-dominated there while
     still far below the gel point) - a second, earlier threshold; the
     labeled toy extrapolation to N = 1e80 against the two references (the
     flat table 2^(1e80); the Bekenstein ceiling ~1e122 bits)
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uwf_scout import DIM, N_Q, H, RY, Table, u01


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


# ---------------------------------------------------------------- SN1: cuts

def gen_circuit(seed, ops=40):
    evs = []
    for s in range(ops):
        rr = u01(H(seed, "op", s))
        if rr < 0.40:
            q = int(H(seed, "q", s), 16) % N_Q
            evs.append(("u", (q,), 2 * math.pi * u01(H(seed, "th", s))))
        elif rr < 0.65:
            c = int(H(seed, "c", s), 16) % N_Q
            t = int(H(seed, "t", s), 16) % (N_Q - 1)
            t = t + 1 if t >= c else t
            evs.append(("cx", (c, t), None))
        else:
            q = int(H(seed, "m", s), 16) % N_Q
            evs.append(("m", (q,), None))
    return evs


def build_deps(evs):
    last, deps = {}, []
    for i, (_, qs, _) in enumerate(evs):
        deps.append({last[q] for q in qs if q in last})
        for q in qs:
            last[q] = i
    return deps


def closure(idxs, deps):
    out, stack = set(), list(idxs)
    while stack:
        i = stack.pop()
        if i not in out:
            out.add(i)
            stack.extend(deps[i])
    return out


def execute(seed, evs, cut, order):
    tab = Table()
    outcomes = {}
    for i in order:
        kind, qs, par = evs[i]
        if kind == "u":
            tab.apply1(RY(par), qs[0])
        elif kind == "cx":
            tab.cnot(qs[0], qs[1])
        else:
            bit, _ = tab.measure(qs[0], u01(H(seed, "evt", i)))
            outcomes[i] = bit
    return tab.amps, outcomes


def alt_order(cut, deps):
    # a second linear extension: always take the HIGHEST-index available event
    remaining = set(cut)
    out = []
    while remaining:
        avail = [i for i in remaining if deps[i] <= (set(out))]
        pick = max(avail)
        out.append(pick)
        remaining.discard(pick)
    return out


def snapshot_cuts():
    trials = 0
    ok_records = ok_views = ok_welldef = 0
    min_view_gap = 1e9
    k = 0
    while trials < 20 and k < 200:
        seed = H("snap", k)
        k += 1
        evs = gen_circuit(seed)
        deps = build_deps(evs)
        settles = [i for i, e in enumerate(evs) if e[0] == "m" and i < len(evs) // 2]
        if not settles:
            continue
        c0 = closure(settles, deps)
        frontier = [i for i in range(len(evs))
                    if i not in c0 and evs[i][0] == "u" and deps[i] <= c0]
        if len(frontier) < 2:
            continue
        trials += 1
        cut_a = c0 | {frontier[0]}
        cut_b = c0 | {frontier[1]}
        psi_a, rec_a = execute(seed, evs, cut_a, sorted(cut_a))
        psi_b, rec_b = execute(seed, evs, cut_b, sorted(cut_b))
        psi_a2, rec_a2 = execute(seed, evs, cut_a, alt_order(cut_a, deps))
        gap = max(abs(x - y) for x, y in zip(psi_a, psi_b))
        wd = max(abs(x - y) for x, y in zip(psi_a, psi_a2))
        ok_records += (rec_a == rec_b and len(rec_a) > 0)
        ok_views += gap > 1e-6
        ok_welldef += (wd < 1e-9 and rec_a == rec_a2)
        min_view_gap = min(min_view_gap, gap)
    return trials, ok_records, ok_views, ok_welldef, min_view_gap


def token_sim(seed, steps=400, n=20, delay=5, total=100):
    rnd = random.Random(seed)
    hold = [total // n] * n
    flight = []
    snaps = naive_bad = cl_bad = 0
    for t in range(steps):
        hold_new = hold[:]
        keep = []
        for arr, dest, amt in flight:
            if arr == t:
                hold_new[dest] += amt
            else:
                keep.append((arr, dest, amt))
        hold, flight = hold_new, keep
        for i in range(n):
            if hold[i] > 0 and rnd.random() < 0.3:
                hold[i] -= 1
                flight.append((t + 1 + rnd.randrange(delay), (i + 1) % n, 1))
        if t % 20 == 10:                       # wall-clock snapshot attempts
            snaps += 1
            if sum(hold) != total:             # naive: node states only
                naive_bad += 1
            if sum(hold) + sum(a for _, _, a in flight) != total:
                cl_bad += 1                    # consistent: + channel contents
    return snaps, naive_bad, cl_bad


# ------------------------------------------------------- SC1/SC2: clusters

def cluster_run(N, r, seed, relax_mult=30, sample_mult=10):
    rnd = random.Random(seed)
    cluster_of = list(range(N))
    members = {i: {i} for i in range(N)}
    next_id = N
    p_merge = r / (1.0 + r) if r != float("inf") else 1.0
    relax, sample = relax_mult * N, sample_mult * N
    fracs, storages, singl, hist = [], [], [], {}
    for step in range(relax + sample):
        if rnd.random() < p_merge:
            a, b = rnd.randrange(N), rnd.randrange(N)
            ca, cb = cluster_of[a], cluster_of[b]
            if ca != cb:
                if len(members[ca]) < len(members[cb]):
                    ca, cb = cb, ca
                for x in members[cb]:
                    cluster_of[x] = ca
                members[ca] |= members[cb]
                del members[cb]
        else:
            a = rnd.randrange(N)
            ca = cluster_of[a]
            if len(members[ca]) > 1:
                members[ca].discard(a)
                cluster_of[a] = next_id
                members[next_id] = {a}
                next_id += 1
        if step >= relax and (step - relax) % max(1, sample // 200) == 0:
            sizes = [len(s) for s in members.values()]
            fracs.append(max(sizes) / N)
            singl.append(sum(1 for s in sizes if s == 1) / N)
            if max(sizes) < 60:                # storage only meaningful subcritical
                storages.append(sum(2.0 ** k for k in sizes))
            for s in sizes:
                hist[s] = hist.get(s, 0) + 1
    mean_st = sum(storages) / len(storages) if storages else float("inf")
    return (sum(fracs) / len(fracs), sum(singl) / len(singl), mean_st, hist)


def linfit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys) or 1e-30
    return a, b, 1.0 - ss_res / ss_tot


def main():
    R = []

    # SN1 - the snapshot isomorphism
    tr, okr, okv, okw, gap = snapshot_cuts()
    snaps, naive_bad, cl_bad = token_sim("tok1")
    R.append(check("SN1", tr == 20 and okr == 20 and okv == 20 and okw == 20
                   and cl_bad == 0 and naive_bad >= snaps // 2,
                   "%d executions: two valid cuts -> DIFFERENT instantaneous Psi "
                   "(min gap %.3f) yet IDENTICAL settled records %d/%d; two linear "
                   "extensions of one cut -> same Psi to 1e-9 (%d/%d) - the cut is "
                   "bookkeeping, the record is physics; freeze-now wall-clock "
                   "snapshot violates conservation in %d/%d attempts (in-flight "
                   "records missed), the consistent snapshot conserves %d/%d - "
                   "there is NO GLOBAL NOW, measured"
                   % (tr, gap, okr, tr, okw, tr, naive_bad, snaps,
                      snaps - cl_bad, snaps)))

    # SC1 - the phase diagram; two predictions made BEFORE the scan:
    # (a) singleton fraction = 1 - r; (b) gel onset at r_c = 1 (count balance)
    N = 2000
    ladder = [0.15, 0.25, 0.35, 0.5, 1.0, 2.0]
    fr = {}
    sg = {}
    for r in ladder:
        f, s, _, h = cluster_run(N, r, "sc1-%s" % r)
        fr[r], sg[r] = f, s
        if r == 0.15:
            hist_sub = h
    f_inf, _, _, _ = cluster_run(N, float("inf"), "sc1-inf", 5, 2)
    sub_ok = fr[0.15] < 0.03 and fr[0.25] < 0.05
    gel_ok = fr[1.0] > 0.4 and fr[2.0] > 0.6 and f_inf == 1.0
    onset_early = fr[0.5] > 0.15          # the REFUTATION: gel before r = 1
    mono = all(fr[a] <= fr[b] + 0.03 for a, b in zip(ladder, ladder[1:]))
    mf_ok = abs(sg[0.15] - 0.85) < 0.08 and abs(sg[0.25] - 0.75) < 0.08
    ks = sorted(k for k, c in hist_sub.items() if c >= 10 and k >= 1)
    _, slope, r2tail = linfit(ks, [math.log(hist_sub[k]) for k in ks])
    R.append(check("SC1", sub_ok and gel_ok and onset_early and mono and mf_ok
                   and slope < 0 and r2tail > 0.9,
                   "giant-cluster fraction vs r=merge/settle: %s; pure-merge limit "
                   "-> ONE cluster of N (the Everett corner as the r->inf endpoint). "
                   "Pre-registered predictions: singleton fraction = 1-r CONFIRMED "
                   "(%.2f at r=0.15 vs 0.85; %.2f at r=0.25 vs 0.75); r_c = 1 "
                   "REFUTED - gel onsets between r = 0.25 and 0.5, because merges "
                   "pick PARTICLES (mass-biased, multiplicative kernel: Erdos-Renyi "
                   "giant-component physics beats count balance) - the failed "
                   "prediction is the finding; subcritical tail exponential "
                   "(log-linear R^2 = %.3f) - many-worlds is the GEL PHASE; a "
                   "settling world stays sol"
                   % (", ".join("r=%.2g: %.2f" % (r, fr[r]) for r in ladder),
                      sg[0.15], sg[0.25], r2tail)))
    # tail fitted at r = 0.15, deep subcritical - near the (early) transition
    # the multiplicative kernel fattens the tail, which is expected physics

    # SC2 - the linear-storage law + the labeled extrapolation
    Ns = [250, 500, 1000, 2000, 4000]
    cs = {}
    r2s = {}
    for r in (0.05, 0.1):
        pts = [(n, cluster_run(n, r, "sc2-%s-%d" % (r, n))[2]) for n in Ns]
        _, b, r2 = linfit([p[0] for p in pts], [p[1] for p in pts])
        cvals = [p[1] / p[0] for p in pts]
        cs[r] = (b, min(cvals), max(cvals))
        r2s[r] = r2
    c_hi = cs[0.1][0]
    lin_ok = all(r2s[r] > 0.995 for r in cs) \
        and all(cs[r][2] / cs[r][1] < 1.35 for r in cs) \
        and cs[0.1][0] > cs[0.05][0]
    # the storage transition: tail slope alpha vs ln 2
    alphas = {}
    for r in (0.1, 0.2):
        _, _, _, h = cluster_run(2000, r, "sc2a-%s" % r)
        ks = sorted(k for k, c in h.items() if c >= 10 and k >= 1)
        _, sl, _ = linfit(ks, [math.log(h[k]) for k in ks])
        alphas[r] = -sl
    ln2 = math.log(2)
    # direct fluctuation evidence at r = 0.2: the linear fit degrades there
    pts2 = [(n, cluster_run(n, 0.2, "sc2-0.2-%d" % n)[2]) for n in Ns]
    fin2 = [p for p in pts2 if math.isfinite(p[1])]
    if len(fin2) >= 3:
        _, _, r2_edge = linfit([p[0] for p in fin2], [p[1] for p in fin2])
        cv2 = [p[1] / p[0] for p in fin2]
        spread2 = max(cv2) / min(cv2)
    else:
        r2_edge, spread2 = 0.0, float("inf")
    storage_edge = alphas[0.1] > 1.5 * ln2 and alphas[0.2] < 1.2 * ln2 \
        and (r2_edge < 0.9 or spread2 > 2.0)
    # the labeled toy extrapolation (one amplitude booked at 128 bits),
    # using the larger measured cheap-phase constant
    log10_ledger_bits = 80 + math.log10(c_hi * 128)
    log10_flat_exponent = 1e80 * math.log10(2)
    ceiling_ok = log10_ledger_bits < 122
    R.append(check("SC2", lin_ok and storage_edge and ceiling_ok,
                   "cheap-phase storage is LINEAR: S = c(r)*N with c(0.05) = %.2f, "
                   "c(0.1) = %.2f amplitudes/particle (fit R^2 %.4f/%.4f, c stable "
                   "across N = 250..4000 within %.0f%%); THE STORAGE TRANSITION: "
                   "linearity needs the size tail to beat 2^k (slope > ln 2 = "
                   "0.693) - measured slope %.2f at r=0.1 (deep in the cheap "
                   "phase) falling to %.2f at r=0.2 (AT the ln 2 edge), where "
                   "storage is directly measured fluctuation-dominated (c "
                   "estimates scatter x%.0f across N, fit R^2 %.2f) while still "
                   "far below the gel point - a second threshold BEFORE "
                   "percolation; TOY EXTRAPOLATION "
                   "(labeled, 128 bits/amplitude): N = 1e80 particles -> ledger "
                   "~ 10^%.1f bits - UNDER the Bekenstein ceiling 10^122 - while "
                   "the flat table needs 10^(%.1e) numbers; the gap between JUST "
                   "BIG and black magic is the exponent itself"
                   % (cs[0.05][0], cs[0.1][0], r2s[0.05], r2s[0.1],
                      100 * (max(cs[r][2] / cs[r][1] for r in cs) - 1),
                      alphas[0.1], alphas[0.2], min(spread2, 9999), r2_edge,
                      log10_ledger_bits, log10_flat_exponent)))

    print()
    print("UWF2: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
