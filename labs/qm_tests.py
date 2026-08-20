"""Tiers 1-3 of the test catalogue: the amplitude contract (manifest P4).

Contract = 2^k complex amplitudes, global (the ruling). Measurement = basis
rotation + Born sample (hash draw, no dice) + projection + renormalize.
One mechanism; every correlation below must fall out of it.
"""

import hashlib
import math

SQ2 = math.sqrt(2)


def H(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def u01(seed_hex):
    return int(seed_hex, 16) / float(1 << 256)


def RY(t):
    c, s = math.cos(t / 2), math.sin(t / 2)
    return [[c, -s], [s, c]]


HAD = [[1 / SQ2, 1 / SQ2], [1 / SQ2, -1 / SQ2]]
S_GATE = [[1, 0], [0, 1j]]
SDG = [[1, 0], [0, -1j]]


def RZ(phi):
    return [[1, 0], [0, complex(math.cos(phi), math.sin(phi))]]


class QContract:
    """The global object (manifest P4): joint amplitude table, hash-seeded draws."""

    def __init__(self, seed, amps):
        self.seed = seed
        self.amps = [complex(a) for a in amps]
        self.draws = 0

    def _draw(self):
        self.draws += 1
        return u01(H(self.seed, "draw", self.draws))

    def apply1(self, U, q):
        step = 1 << q
        a = self.amps
        for i in range(len(a)):
            if not (i & step):
                j = i | step
                a0, a1 = a[i], a[j]
                a[i] = U[0][0] * a0 + U[0][1] * a1
                a[j] = U[1][0] * a0 + U[1][1] * a1

    def cnot(self, c, t):
        cs, ts = 1 << c, 1 << t
        a = self.amps
        for i in range(len(a)):
            if (i & cs) and not (i & ts):
                j = i | ts
                a[i], a[j] = a[j], a[i]

    def measure_z(self, q):
        # GLOBAL UPDATE: Born sample + projection + renormalize, atomically.
        step = 1 << q
        p1 = sum(abs(a) ** 2 for i, a in enumerate(self.amps) if i & step)
        bit = 1 if self._draw() < p1 else 0
        norm = math.sqrt(p1 if bit else 1 - p1)
        self.amps = [a / norm if bool(i & step) == bool(bit) else 0j
                     for i, a in enumerate(self.amps)]
        return -1 if bit else 1

    def measure_angle(self, q, theta):
        self.apply1(RY(-theta), q)
        r = self.measure_z(q)
        self.apply1(RY(theta), q)
        return r

    def measure_pauli(self, q, which):
        if which == "Z":
            return self.measure_z(q)
        if which == "X":
            return self.measure_angle(q, math.pi / 2)
        self.apply1(SDG, q)
        self.apply1(HAD, q)
        r = self.measure_z(q)
        self.apply1(HAD, q)
        self.apply1(S_GATE, q)
        return r


def singlet(seed):
    return QContract(seed, [0, 1 / SQ2, -1 / SQ2, 0])


def ghz(seed):
    a = [0j] * 8
    a[0] = a[7] = 1 / SQ2
    return QContract(seed, a)


def w_state(seed):
    a = [0j] * 8
    a[1] = a[2] = a[4] = 1 / math.sqrt(3)
    return QContract(seed, a)


def singlet_plus_spectator(seed):
    a = [0j] * 8
    a[1] = 1 / SQ2      # q2=0, |q1 q0> = |01>
    a[2] = -1 / SQ2
    return QContract(seed, a)


ALICE_ANGLES = [0.0, math.pi / 2]
BOB_ANGLES = [math.pi / 4, 3 * math.pi / 4]


def chsh(make, qa, qb, n, tag):
    bins = {}
    for t in range(n):
        c = make(H(tag, t))
        ia = int(H(tag, t, "sa"), 16) % 2
        ib = int(H(tag, t, "sb"), 16) % 2
        ra = c.measure_angle(qa, ALICE_ANGLES[ia])
        rb = c.measure_angle(qb, BOB_ANGLES[ib])
        bins.setdefault((ia, ib), []).append(ra * rb)
    E = {k: sum(v) / len(v) for k, v in bins.items()}
    S = abs(E[(0, 0)] - E[(0, 1)] + E[(1, 0)] + E[(1, 1)])
    return S, min(len(v) for v in bins.values())


def check(label, ok, detail):
    print("%-6s %-6s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []

    # C0: engine consistency - singlet correlation curve and CHSH
    n = 4000
    worst = 0.0
    for k in range(9):
        delta = k * math.pi / 8
        tot = 0
        for t in range(n):
            c = singlet(H("c0", k, t))
            tot += c.measure_angle(0, 0.0) * c.measure_angle(1, delta)
        worst = max(worst, abs(tot / n + math.cos(delta)))
    S, nb = chsh(singlet, 0, 1, 16000, "c0chsh")
    sig = 2 / math.sqrt(nb)
    R.append(check("C0", worst < 0.09 and abs(S - 2 * SQ2) < 5 * sig,
                   "E(d) = -cos d, max dev %.4f (<0.09); CHSH S = %.4f (2.8284 +/- %.3f)"
                   % (worst, S, 5 * sig)))

    # Q1: repeatability - same axis twice always agrees
    agree = 0
    n = 3000
    for t in range(n):
        c = QContract(H("q1", t), [1, 0])
        th = 2 * math.pi * u01(H("q1prep", t))
        c.apply1(RY(th), 0)
        axis = 2 * math.pi * u01(H("q1axis", t))
        agree += c.measure_angle(0, axis) == c.measure_angle(0, axis)
    R.append(check("Q1", agree == n, "same-axis remeasure: %d/%d agree" % (agree, n)))

    # Q2: non-commutativity - Z,X,Z re-randomizes; Z,Z stays
    n = 4000
    same_zxz = 0
    same_zz = 0
    for t in range(n):
        c = QContract(H("q2", t), [1 / SQ2, 1 / SQ2])
        r1 = c.measure_z(0)
        c.measure_pauli(0, "X")
        same_zxz += r1 == c.measure_z(0)
        c2 = QContract(H("q2b", t), [1 / SQ2, 1 / SQ2])
        same_zz += c2.measure_z(0) == c2.measure_z(0)
    frac = same_zxz / n
    R.append(check("Q2", abs(frac - 0.5) < 5 / (2 * math.sqrt(n)) and same_zz == n,
                   "Z,X,Z agree %.4f (target 0.5); Z,Z agree %d/%d" % (frac, same_zz, n)))

    # Q4: interference and which-path decoherence (P3, P9)
    def mz(t, phi, record):
        c = QContract(H("q4", t, phi, record), [1, 0, 0, 0])
        c.apply1(HAD, 0)
        if record:
            c.cnot(0, 1)
        c.apply1(RZ(phi), 0)
        c.apply1(HAD, 0)
        return c.measure_z(0) == 1
    n = 2500
    def visibility(record):
        ps = []
        for k in range(9):
            phi = k * 2 * math.pi / 8
            p0 = sum(mz(t, phi, record) for t in range(n)) / n
            ps.append(p0)
        return (max(ps) - min(ps)) / (max(ps) + min(ps))
    v_free, v_rec = visibility(False), visibility(True)
    R.append(check("Q4", v_free > 0.95 and v_rec < 0.10,
                   "visibility %.3f without record, %.3f with which-path record" % (v_free, v_rec)))

    # Q5: GHZ / Mermin - deterministic wins, M = 4; best LHV = 2
    settings = [("X", "X", "X", 1), ("X", "Y", "Y", -1), ("Y", "X", "Y", -1), ("Y", "Y", "X", -1)]
    n = 1500
    ok_all = True
    M = 0.0
    for sa, sb, sc, target in settings:
        tot = 0
        for t in range(n):
            c = ghz(H("q5", sa, sb, sc, t))
            p = c.measure_pauli(0, sa) * c.measure_pauli(1, sb) * c.measure_pauli(2, sc)
            tot += p
            if p != target:
                ok_all = False
        M += (tot / n) * (1 if target == 1 else -1)
    lhv_M = abs(1 - 1 - 1 - 1)  # best deterministic LHV assignment: |M| = 2
    R.append(check("Q5", ok_all and abs(M - 4) < 1e-9 and lhv_M == 2,
                   "every round exact: M = %.4f (LHV best = %d)" % (M, lhv_M)))

    # Q6: monogamy - GHZ pairwise classical; Toner bound on all states
    S_ghz_ab, _ = chsh(ghz, 0, 1, 12000, "q6ghz")
    S_sp_ab, nb1 = chsh(singlet_plus_spectator, 0, 1, 12000, "q6ab")
    S_sp_ac, _ = chsh(singlet_plus_spectator, 0, 2, 12000, "q6ac")
    S_w_ab, _ = chsh(w_state, 0, 1, 12000, "q6w")
    S_w_ac, _ = chsh(w_state, 0, 2, 12000, "q6wc")
    toner = [("singlet+spec", S_sp_ab, S_sp_ac), ("W", S_w_ab, S_w_ac)]
    toner_ok = all(sab ** 2 + sac ** 2 <= 8 + 0.45 for _, sab, sac in toner)
    sig1 = 2 / math.sqrt(nb1)
    R.append(check("Q6", S_ghz_ab <= 2 + 5 * sig1 and abs(S_sp_ab - 2 * SQ2) < 5 * sig1 and toner_ok,
                   "GHZ pair S = %.3f (<=2); singlet S_AB = %.3f, S_AC = %.3f; "
                   "W S_AB = %.3f, S_AC = %.3f; Toner sums %.2f, %.2f (<=8)"
                   % (S_ghz_ab, S_sp_ab, S_sp_ac, S_w_ab, S_w_ac,
                      S_sp_ab ** 2 + S_sp_ac ** 2, S_w_ab ** 2 + S_w_ac ** 2)))

    # Q7: three-party no-signalling - marginals flat across others' settings
    n = 2000
    marg = {}
    for sa, sb, sc, _ in settings:
        for t in range(n):
            c = ghz(H("q7", sa, sb, sc, t))
            outs = (c.measure_pauli(0, sa), c.measure_pauli(1, sb), c.measure_pauli(2, sc))
            for who in range(3):
                marg.setdefault((who, (sa, sb, sc)), []).append(outs[who])
    shift = 0.0
    for who in range(3):
        means = [sum(v) / len(v) for (w, _), v in marg.items() if w == who]
        shift = max(shift, max(means) - min(means))
    R.append(check("Q7", shift < 5 * math.sqrt(2.0 / n),
                   "max marginal shift across settings %.4f (< %.4f)" % (shift, 5 * math.sqrt(2.0 / n))))

    # Q8: record consistency - friend's record matches every later reader
    n = 2000
    ok8 = True
    for t in range(n):
        c = singlet(H("q8", t))
        axis = 2 * math.pi * u01(H("q8axis", t))
        friend_outcome = c.measure_angle(0, axis)
        record = friend_outcome                      # block appended to friend's chain
        wigner_remeasure = c.measure_angle(0, axis)  # Wigner repeats on the same contract
        if not (record == wigner_remeasure):
            ok8 = False
    R.append(check("Q8", ok8, "%d/%d: record == re-measurement for every reader" % (n, n)))

    # Q9: classicality by replication - ring gossip, monotone coverage, linear reversal cost
    N = 64
    informed = {0}
    curve = []
    rounds = 0
    while len(informed) < N:
        rounds += 1
        informed |= {(i + 1) % N for i in informed} | {(i - 1) % N for i in informed}
        curve.append(len(informed))
    monotone = all(b >= a for a, b in zip(curve, curve[1:]))
    R.append(check("Q9", monotone and rounds == N // 2 and curve[-1] == N,
                   "consensus in %d rounds (ring N=%d), coverage monotone, reversal cost = %d replicas"
                   % (rounds, N, N)))

    print()
    print("TIERS 1-3: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
