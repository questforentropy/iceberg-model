"""Leggett-Garg / temporal Bell scout (user ask 2026-08-18, article #11 cross-link).

The instrument: ONE system, three checkpoints, the same Z reading each time;
evolution between checkpoints = RY(theta), so the waiting time IS the angle.
Score K = C12 + C23 - C13. A diary world with free looks caps K at 1.

LG1  watchers cannot cross, two ways: (a) a passive deterministic rotor -
     every run scores +1 or -3, K sits exactly ON the ceiling for gaps up to
     90 deg and under it beyond; (b) the ledger settled at ALL THREE
     checkpoints per run - settling writes a diary of triples, and
     K = 2cos(t) - cos^2(t) <= 1 follows mechanically.
LG2  the fold crosses: two checkpoints per run, three separate batches
     (measurement = settlement re-prepares the contract, so with- and
     without-middle-reading batches are different worlds),
     K(t) = 2cos(t) - cos(2t), reaching 3/2 at 60 deg - and the same curve
     under the double-entry settlement sampler (QM-30/31), so v4's derived
     Born breaks the watcher ceiling exactly as the imported line does.
"""

import math

from born_settlement_scout import make_settlement_measure
from qm_tests import H, QContract, RY, u01

DEG = math.pi / 180


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def rotor_run(theta, n, tag):
    tot = 0
    zigzags = 0
    legal = True
    for t in range(n):
        x = 2 * math.pi * u01(H(tag, t))
        q = [1 if math.cos(x + k * theta) >= 0 else -1 for k in range(3)]
        s = q[0] * q[1] + q[1] * q[2] - q[0] * q[2]
        if s not in (1, -3):
            legal = False
        if s == -3:
            zigzags += 1
        tot += s
    return tot / n, zigzags, legal


def prepared(seed, tag, t):
    c = QContract(seed, [1, 0])
    c.apply1(RY(2 * math.pi * u01(H(tag, "prep", t))), 0)
    return c


def ledger_pair(theta, a, b, n, tag, sampler=None):
    # one batch: settle only checkpoints a and b (1-indexed), skip the third
    tot = 0
    for t in range(n):
        c = prepared(H(tag, a, b, t), tag, t)
        if sampler is not None:
            c.measure_z = sampler.__get__(c)
        q = {}
        for k in (1, 2, 3):
            c.apply1(RY(theta), 0)
            if k in (a, b):
                q[k] = c.measure_z(0)
        tot += q[a] * q[b]
    return tot / n


def ledger_K_batched(theta, n, tag, sampler=None):
    return (ledger_pair(theta, 1, 2, n, tag + "12", sampler)
            + ledger_pair(theta, 2, 3, n, tag + "23", sampler)
            - ledger_pair(theta, 1, 3, n, tag + "13", sampler))


def ledger_K_triples(theta, n, tag):
    # all three checkpoints settled in every run: the ledger writes the diary
    s12 = s23 = s13 = 0
    for t in range(n):
        c = prepared(H(tag, t), tag, t)
        q = []
        for _ in range(3):
            c.apply1(RY(theta), 0)
            q.append(c.measure_z(0))
        s12 += q[0] * q[1]
        s23 += q[1] * q[2]
        s13 += q[0] * q[2]
    return (s12 + s23 - s13) / n


def main():
    R = []
    n = 4000
    sig_k = 5 * math.sqrt(3.0 / n)   # 5 sigma on a sum of three +/-1 means

    # LG1a: passive rotor - per-run scores only +1/-3, mean never above 1
    flat = []
    ok_rotor = True
    for gd in (30, 60, 90, 120, 150):
        k, zz, legal = rotor_run(gd * DEG, n, "lgrot%d" % gd)
        ok_rotor &= legal and k <= 1.0 + 1e-12
        if gd <= 90:
            ok_rotor &= zz == 0 and abs(k - 1.0) < 1e-12
        flat.append("%d deg: %.4f (%d zigzags)" % (gd, k, zz))

    # LG1b: ledger settled at all three checkpoints - triples ARE a diary
    trip = []
    ok_trip = True
    for gd in (30, 60, 90):
        k = ledger_K_triples(gd * DEG, n, "lgtrip%d" % gd)
        pred = 2 * math.cos(gd * DEG) - math.cos(gd * DEG) ** 2
        ok_trip &= abs(k - pred) < sig_k and k <= 1.0 + sig_k
        trip.append("%d deg: %.3f (pred %.3f)" % (gd, k, pred))
    R.append(check("LG1", ok_rotor and ok_trip,
                   "watchers capped at 1: rotor flat ON the ceiling to 90 deg "
                   "[%s]; all-three-settled ledger writes its own diary, "
                   "K = 2cos t - cos^2 t stays under [%s]"
                   % ("; ".join(flat), "; ".join(trip))))

    # LG2: two-per-run batches, settlement re-preparation - the fold crosses
    curve = []
    ok_curve = True
    for gd in (30, 60, 90):
        k = ledger_K_batched(gd * DEG, n, "lgb%d" % gd)
        pred = 2 * math.cos(gd * DEG) - math.cos(2 * gd * DEG)
        ok_curve &= abs(k - pred) < sig_k
        curve.append("%d deg: %.3f (pred %.3f)" % (gd, k, pred))
    k60 = ledger_K_batched(60 * DEG, n, "lgb60x")
    kde = ledger_K_batched(60 * DEG, 3000, "lgde60",
                           sampler=make_settlement_measure(2))
    ok_de = abs(kde - 1.5) < 5 * math.sqrt(3.0 / 3000)
    R.append(check("LG2", ok_curve and k60 > 1.0 + sig_k and ok_de,
                   "the fold crosses the ceiling: K = 2cos t - cos 2t [%s]; "
                   "at 60 deg K = %.3f > 1 (temporal Tsirelson 3/2); "
                   "double-entry settlement sampler at 60 deg: K = %.3f - "
                   "the derived Born breaks the watcher ceiling too"
                   % ("; ".join(curve), k60, kde)))

    print()
    print("LG: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
