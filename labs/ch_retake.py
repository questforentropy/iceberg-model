"""CH retake: the 20-question quantum exam (episode #3 suite) sat by the ledger model.

Framing (honest): The Machine took this exam WITHOUT the textbook - it tried to make
QM emerge and failed exactly two rows (CH-06 nulls, CH-16 CHSH). This model brought
the textbook: the Born line is imported (manifest confession 1). So the retake tests
whether the DISTRIBUTED LEDGER IMPLEMENTATION preserves every QM behaviour - and the
two rows The Machine could not do must pass here BECAUSE the answers were imported.

Statuses: PASS (measured) / PASS* (by construction - imported physics) /
BANKED (already measured in an earlier tier) / MERGED / IMPORTED (not a pass).
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qm_tests import QContract, H, u01, RY, HAD, RZ, SQ2, singlet


def cry(con, eta, cq, tq):
    cs, ts = 1 << cq, 1 << tq
    cc, ss = math.cos(eta / 2), math.sin(eta / 2)
    a = con.amps
    for i in range(len(a)):
        if (i & cs) and not (i & ts):
            j = i | ts
            a0, a1 = a[i], a[j]
            a[i] = cc * a0 - ss * a1
            a[j] = ss * a0 + cc * a1


def mz(seed, phi, eta=0.0, final_h=True):
    c = QContract(seed, [1, 0, 0, 0])
    c.apply1(HAD, 0)
    if eta:
        cry(c, eta, 0, 1)
    c.apply1(RZ(phi), 0)
    if final_h:
        c.apply1(HAD, 0)
    return c


PHIS = [k * 2 * math.pi / 8 for k in range(9)]


def visibility(tag, n, eta=0.0):
    ps = []
    for phi in PHIS:
        p0 = sum(mz(H(tag, phi, t), phi, eta).measure_z(0) == 1 for t in range(n)) / n
    # note: measure inside the sum above consumed the contract; recompute per phi
        ps.append(p0)
    return (max(ps) - min(ps)) / (max(ps) + min(ps)), ps


results = []


def row(ch, status, detail, ok=True):
    results.append((ch, status if ok else "FAIL", detail, ok))
    print("%-7s %-8s %s" % (ch, status if ok else "FAIL", detail))


def main():
    # CH-01 Born statistics
    n = 4000
    worst = 0.0
    for th in (0.3, 0.9, 1.7, 2.5):
        p = sum(1 for t in range(n)
                if (lambda c: (c.apply1(RY(th), 0), c.measure_z(0))[1])(QContract(H("ch01", th, t), [1, 0])) == 1) / n
        worst = max(worst, abs(p - math.cos(th / 2) ** 2))
    row("CH-01", "PASS", "Born: max |P - cos^2| = %.4f (< %.4f)" % (worst, 5 / (2 * math.sqrt(n))),
        worst < 5 / (2 * math.sqrt(n)))

    # CH-02 frame robustness: rotate preparation and measurement together
    n = 4000
    worst = 0.0
    for th, ph, d in ((0.9, 0.4, 0.7), (1.7, 2.1, 1.3), (2.5, 0.2, 2.9)):
        def p_of(theta, phi, tag):
            k = 0
            for t in range(n):
                c = QContract(H("ch02", tag, t), [1, 0])
                c.apply1(RY(theta), 0)
                k += c.measure_angle(0, phi) == 1
            return k / n
        worst = max(worst, abs(p_of(th, ph, "a%s" % th) - p_of(th + d, ph + d, "b%s" % th)))
    row("CH-02", "PASS", "frame shift leaves stats: max diff %.4f (< %.4f)" % (worst, 5 * math.sqrt(0.5 / n)),
        worst < 5 * math.sqrt(0.5 / n))

    # CH-03 no-disturbance (contextuality hinge, marginal form)
    n = 8000
    a_ang = 0.7
    ms = []
    for ctx in ("none", "Z", "X"):
        k = 0
        for t in range(n):
            c = singlet(H("ch03", ctx, t))
            if ctx == "Z":
                c.measure_z(1)
            elif ctx == "X":
                c.measure_angle(1, math.pi / 2)
            k += c.measure_angle(0, a_ang) == 1
        ms.append(k / n)
    spread = max(ms) - min(ms)
    row("CH-03", "PASS", "Alice marginal vs partner context (none/Z/X): spread %.4f (< %.4f)"
        % (spread, 5 * math.sqrt(0.5 / n)), spread < 5 * math.sqrt(0.5 / n))

    # CH-04 mixtures vs superpositions
    n = 2500
    v_sup, _ = visibility("ch04s", n)
    ps = []
    for phi in PHIS:
        k = 0
        for t in range(n):
            bit = int(H("ch04mprep", phi, t), 16) % 2
            c = QContract(H("ch04m", phi, t), [0, 1] if bit else [1, 0])
            c.apply1(RZ(phi), 0)
            c.apply1(HAD, 0)
            k += c.measure_z(0) == 1
        ps.append(k / n)
    v_mix = (max(ps) - min(ps)) / (max(ps) + min(ps))
    row("CH-04", "PASS", "superposition V = %.3f (>0.95); mixture V = %.3f (<0.10)" % (v_sup, v_mix),
        v_sup > 0.95 and v_mix < 0.10)

    # CH-05 cosine fringe purity (first harmonic only)
    n = 3000
    M = 16
    ps = []
    for k in range(M):
        phi = k * 2 * math.pi / M
        ps.append(sum(mz(H("ch05", k, t), phi).measure_z(0) == 1 for t in range(n)) / n)
    def four(kk):
        re = sum(p * math.cos(kk * 2 * math.pi * j / M) for j, p in enumerate(ps)) / M
        im = sum(p * math.sin(kk * 2 * math.pi * j / M) for j, p in enumerate(ps)) / M
        return math.hypot(re, im)
    ratio = max(four(2), four(3)) / four(1)
    row("CH-05", "PASS", "higher-harmonic / first-harmonic = %.4f (< 0.06)" % ratio, ratio < 0.06)

    # CH-06 arbitrarily deep nulls - THE MACHINE'S FAILED ROW; passes here by construction
    n = 50000
    dark = sum(mz(H("ch06", t), math.pi).measure_z(0) == 1 for t in range(n))
    row("CH-06", "PASS*", "null at phi=pi: %d/%d clicks (Machine's floor was ~1%%; ours is exact "
        "BECAUSE amplitudes are imported)" % (dark, n), dark == 0)

    # CH-07 decoherence law V(eta) = cos(eta/2)
    n = 2000
    worst = 0.0
    for eta in (0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi):
        v, _ = visibility("ch07-%s" % eta, n, eta)
        worst = max(worst, abs(v - abs(math.cos(eta / 2))))
    row("CH-07", "PASS", "V(eta) vs cos(eta/2): max dev %.4f (< 0.05)" % worst, worst < 0.05)

    # CH-08 which-path sum rule
    n = 3000
    worst = 0.0
    for phi in (0.0, math.pi / 3, 2 * math.pi / 3, math.pi):
        p_rec = sum(mz(H("ch08r", phi, t), phi, eta=math.pi).measure_z(0) == 1 for t in range(n)) / n
        singles = []
        for path in (0, 1):
            k = tot = 0
            for t in range(n):
                c = QContract(H("ch08s", path, phi, t), [1, 0])
                c.apply1(HAD, 0)
                if c.measure_z(0) != (1 if path == 0 else -1):
                    continue
                tot += 1
                c.apply1(RZ(phi), 0)
                c.apply1(HAD, 0)
                k += c.measure_z(0) == 1
            singles.append(k / tot)
        worst = max(worst, abs(p_rec - 0.5 * (singles[0] + singles[1])))
    row("CH-08", "PASS", "P_recorded = avg of single-path patterns: max dev %.4f (< %.4f)"
        % (worst, 5 * math.sqrt(0.5 / n)), worst < 5 * math.sqrt(0.5 / n))

    row("CH-09", "BANKED", "repeatability = Q1 (3000/3000 same-axis agree)")

    # CH-09b the collapse chain
    n = 8000
    th = (0.5, 1.9, 0.9)
    freq = {}
    for t in range(n):
        c = QContract(H("ch09b", t), [1, 0])
        rs = tuple(c.measure_angle(0, a) for a in th)
        freq[rs] = freq.get(rs, 0) + 1
    worst = 0.0
    for r1 in (1, -1):
        for r2 in (1, -1):
            for r3 in (1, -1):
                p1 = math.cos(th[0] / 2) ** 2 if r1 == 1 else math.sin(th[0] / 2) ** 2
                d12 = (th[1] - th[0]) / 2
                p2 = math.cos(d12) ** 2 if r2 == r1 else math.sin(d12) ** 2
                d23 = (th[2] - th[1]) / 2
                p3 = math.cos(d23) ** 2 if r3 == r2 else math.sin(d23) ** 2
                worst = max(worst, abs(freq.get((r1, r2, r3), 0) / n - p1 * p2 * p3))
    row("CH-09b", "PASS", "3-step chain vs product of conditionals: max dev %.4f (< 0.02)" % worst,
        worst < 0.02)

    row("CH-10", "BANKED", "post-measurement blurring = Q2 (Z,X,Z agree 0.4915)")

    # CH-11 delayed choice: the choice block's position leaves no trace
    n = 2000
    def curves(tag):
        out = {True: [], False: []}
        for phi in PHIS:
            k = {True: [0, 0], False: [0, 0]}
            for t in range(n):
                open_ = int(H(tag, "choice", phi, t), 16) % 2 == 0
                r = mz(H(tag, phi, t), phi, final_h=open_).measure_z(0) == 1
                k[open_][0] += r
                k[open_][1] += 1
            for o in (True, False):
                out[o].append(k[o][0] / max(k[o][1], 1))
        return out
    A, B = curves("ch11early"), curves("ch11late")
    worst = max(abs(a - b) for o in (True, False) for a, b in zip(A[o], B[o]))
    row("CH-11", "PASS", "early-drawn vs late-drawn choice: max curve diff %.4f (< %.4f)"
        % (worst, 5 * math.sqrt(1.0 / n)), worst < 5 * math.sqrt(1.0 / n))

    # CH-12 null-result collapse: the silent detector still collapses
    n = 2500
    ps = []
    for phi in PHIS:
        k = tot = 0
        for t in range(n):
            c = mz(H("ch12", phi, t), phi, eta=math.pi, final_h=False)
            if c.measure_z(1) != 1:      # detector fired (record flipped) - discard
                continue
            tot += 1
            c.apply1(HAD, 0)
            k += c.measure_z(0) == 1
        ps.append(k / tot)
    v_silent = (max(ps) - min(ps)) / (max(ps) + min(ps))
    row("CH-12", "PASS", "visibility conditioned on SILENT detector = %.3f (< 0.10; no click, "
        "still collapsed)" % v_silent, v_silent < 0.10)

    # CH-13 quantum eraser
    n = 4000
    sub = {1: {}, -1: {}}
    for phi in (0.0, math.pi / 2, math.pi):
        k = {1: [0, 0], -1: [0, 0]}
        for t in range(n):
            c = mz(H("ch13", phi, t), phi, eta=math.pi)
            r = c.measure_z(0)
            e = c.measure_pauli(1, "X")
            k[e][0] += r == 1
            k[e][1] += 1
        for e in (1, -1):
            sub[e][phi] = k[e][0] / k[e][1]
    ok13 = (sub[1][0.0] > 0.9 and sub[1][math.pi] < 0.1 and
            sub[-1][0.0] < 0.1 and sub[-1][math.pi] > 0.9 and
            abs(sub[1][math.pi / 2] - 0.5) < 0.05)
    row("CH-13", "PASS", "sorted by eraser: anti-phased fringes restored (P0 at phi=0: %.3f vs %.3f); "
        "unsorted flat" % (sub[1][0.0], sub[-1][0.0]), ok13)

    # CH-14 Englert visibility-distinguishability
    n = 2000
    worst = 0.0
    for eta in (math.pi / 6, math.pi / 3, math.pi / 2, 2 * math.pi / 3, 5 * math.pi / 6):
        v, _ = visibility("ch14v-%s" % eta, n, eta)
        succ = 0
        for t in range(n):
            c = QContract(H("ch14d", eta, t), [1, 0, 0, 0])
            c.apply1(HAD, 0)
            cry(c, eta, 0, 1)
            truth = c.measure_z(0)
            guess = c.measure_angle(1, eta / 2 + math.pi / 2)
            succ += (truth == 1) == (guess == 1)
        p = succ / n
        d = abs(2 * max(p, 1 - p) - 1)
        worst = max(worst, abs(v * v + d * d - 1))
    row("CH-14", "PASS", "V^2 + D^2 = 1: max dev %.4f (< 0.06)" % worst, worst < 0.06)

    row("CH-15", "BANKED", "no-signalling = S4 + Q7 (max marginal shift 0.007 / 0.061)")
    row("CH-16", "PASS*", "CHSH = 2.83 (C0/S3a) - THE MACHINE'S UNFINISHED ROW; passes here "
        "because the correlation rule is imported, and we say so")
    row("CH-17", "MERGED", "apparatus recoil merged into CH-14 here: the apparatus IS the record "
        "qubit; this model has no mass dial")
    row("CH-18", "IMPORTED", "complex-unitary observer view: true BY CONSTRUCTION (we imported "
        "complex amplitudes) - not a pass, a confession")

    # CH-19 passive observation cannot fake collapse
    n = 2500
    v_watched, _ = visibility("ch19", n)     # watcher reads gossip, never appends a joint block
    guess_ok = 0
    m = 4000
    for t in range(m):
        c = mz(H("ch19g", t), 0.0)
        watcher_guess = 1 if int(H("ch19w", t), 16) % 2 == 0 else -1
        guess_ok += c.measure_z(0) == watcher_guess
    p_guess = guess_ok / m
    row("CH-19", "PASS", "no joint block: visibility stays %.3f (>0.95); watcher's outcome guess "
        "%.3f (chance)" % (v_watched, p_guess),
        v_watched > 0.95 and abs(p_guess - 0.5) < 5 / (2 * math.sqrt(m)))

    print()
    bad = [r for r in results if not r[3]]
    counts = {}
    for _, st, _, _ in results:
        counts[st] = counts.get(st, 0) + 1
    print("RETAKE: %s | %s" % ("ALL ROWS OK" if not bad else "FAILURES PRESENT",
                               ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))))
    return not bad


if __name__ == "__main__":
    main()
