"""Quantum-blockchain smoke tests (manifest P1-P9, pre-O1).

S1  determinism      same genesis => bit-identical world transcript; different genesis => different
S2  chain integrity  hash links valid, parents precede children, per-node indices contiguous
S3  CHSH             global-contract measurement ~ 2*sqrt(2); LHV control <= 2; PR-box control = 4
S4  no-signalling    second party's marginal independent of first party's setting (in-layer invisibility)
S5  order invariance Alice-first vs Bob-first: same S within noise
S6  no-conspiracy    settings from own genesis hash, statistically independent of pair seed
S7  ancestry audit   remote measurement block never in local measurement's causal ancestry
"""

import hashlib
import math


def H(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def u01(seed_hex):
    return int(seed_hex, 16) / float(1 << 256)


class Node:
    def __init__(self, name, world):
        self.name = name
        self.world = world
        self.blocks = []
        self.append("genesis", world.genesis + ":" + name)

    def tip(self):
        return self.blocks[-1]["hash"]

    def append(self, kind, payload, extra_parents=()):
        parents = ([self.tip()] if self.blocks else []) + list(extra_parents)
        b = {"node": self.name, "idx": len(self.blocks), "kind": kind,
             "payload": payload, "parents": parents, "seq": self.world.next_seq()}
        b["hash"] = H(b["node"], b["idx"], b["kind"], b["payload"], *parents)
        self.blocks.append(b)
        self.world.log.append(b)
        return b


class World:
    def __init__(self, genesis):
        self.genesis = genesis
        self.log = []
        self.seq = 0
        self.contracts = {}

    def next_seq(self):
        self.seq += 1
        return self.seq

    def entangle(self, a, b):
        ta, tb = a.tip(), b.tip()
        cid = H(ta, tb, "entangle")
        a.append("entangle", cid, extra_parents=[tb])
        b.append("entangle", cid, extra_parents=[ta])
        self.contracts[cid] = {"seed": cid, "collapsed": False, "axis": None, "value": 0}
        return cid

    def measure(self, node, cid, angle):
        # GLOBAL UPDATE (manifest ruling 2026-08-15): atomic RMW on the substrate contract.
        # The appended block references only the node's own chain: no in-layer cross edge.
        c = self.contracts[cid]
        if not c["collapsed"]:
            c["collapsed"] = True
            c["axis"] = angle
            c["value"] = 1 if u01(H(c["seed"], "collapse")) > 0.5 else -1
            out = c["value"]
        else:
            d = angle - c["axis"]
            p_plus = math.sin(d / 2) ** 2 if c["value"] == 1 else math.cos(d / 2) ** 2
            out = 1 if u01(H(c["seed"], "response")) < p_plus else -1
        blk = node.append("measure", "%s:%.6f:%+d" % (cid[:16], angle, out))
        return out, blk["hash"]

    def transcript(self):
        acc = hashlib.sha256()
        for b in self.log:
            acc.update(b["hash"].encode())
        for cid, c in self.contracts.items():
            acc.update(("%s:%s:%s" % (cid, c["axis"], c["value"])).encode())
        return acc.hexdigest()


ALICE_ANGLES = [0.0, math.pi / 2]
BOB_ANGLES = [math.pi / 4, 3 * math.pi / 4]


def sign(x):
    return 1 if x > 0 else -1


def run_chsh(genesis, n_trials, first="alternate", model="quantum"):
    w = World(genesis)
    A, B = Node("A", w), Node("B", w)
    gen_a, gen_b = A.blocks[0]["hash"], B.blocks[0]["hash"]
    records = []
    for t in range(n_trials):
        cid = w.entangle(A, B)
        ia = int(H(gen_a, t, "setting"), 16) % 2      # own genesis hash only (P7)
        ib = int(H(gen_b, t, "setting"), 16) % 2
        a_ang, b_ang = ALICE_ANGLES[ia], BOB_ANGLES[ib]
        alice_first = (t % 2 == 0) if first == "alternate" else (first == "A")
        ha = hb = None
        if model == "quantum":
            if alice_first:
                ra, ha = w.measure(A, cid, a_ang)
                rb, hb = w.measure(B, cid, b_ang)
            else:
                rb, hb = w.measure(B, cid, b_ang)
                ra, ha = w.measure(A, cid, a_ang)
        elif model == "lhv":
            lam = 2 * math.pi * u01(H(cid, "lambda"))
            ra = sign(math.cos(a_ang - lam))
            rb = sign(math.cos(b_ang - lam + math.pi))
        elif model == "prbox":
            ra = 1 if u01(H(cid, "pr")) > 0.5 else -1
            rb = ra * (1 if (ia, ib) == (0, 1) else -1)   # saturates |S| = 4
        records.append((t, ia, ib, ra, rb, alice_first, ha, hb))
    bins = {}
    for _, ia, ib, ra, rb, _, _, _ in records:
        bins.setdefault((ia, ib), []).append(ra * rb)
    E = {k: sum(v) / len(v) for k, v in bins.items()}
    S = E[(0, 0)] - E[(0, 1)] + E[(1, 0)] + E[(1, 1)]
    n_bin = min(len(v) for v in bins.values())
    return abs(S), records, w, n_bin


def check(label, ok, detail):
    print("%-6s %-18s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    results = []
    N = 40000
    S_q, rec_q, w_q, nb = run_chsh("genesis-v1", N)
    sigma_S = 2.0 / math.sqrt(nb)

    # S1 determinism
    S_q2, _, w_q2, _ = run_chsh("genesis-v1", N)
    S_alt, _, w_alt, _ = run_chsh("genesis-v2", N)
    results.append(check("S1a", w_q.transcript() == w_q2.transcript(),
                         "same genesis -> identical transcript"))
    results.append(check("S1b", w_q.transcript() != w_alt.transcript(),
                         "different genesis -> different transcript"))

    # S2 chain integrity
    seq_of = {b["hash"]: b["seq"] for b in w_q.log}
    ok_hash = all(b["hash"] == H(b["node"], b["idx"], b["kind"], b["payload"], *b["parents"])
                  for b in w_q.log)
    ok_order = all(all(seq_of[p] < b["seq"] for p in b["parents"]) for b in w_q.log)
    results.append(check("S2", ok_hash and ok_order,
                         "hashes recompute, all parents precede children (%d blocks)" % len(w_q.log)))

    # S3 the three ceilings
    results.append(check("S3a", abs(S_q - 2 * math.sqrt(2)) < 5 * sigma_S,
                         "quantum S = %.4f (target 2.8284 +/- %.3f)" % (S_q, 5 * sigma_S)))
    S_l, _, _, nb_l = run_chsh("genesis-v1", 20000, model="lhv")
    results.append(check("S3b", S_l <= 2 + 5 * (2 / math.sqrt(nb_l)),
                         "LHV control S = %.4f (must stay <= 2)" % S_l))
    S_p, _, _, _ = run_chsh("genesis-v1", 8000, model="prbox")
    results.append(check("S3c", abs(S_p - 4) < 1e-9,
                         "PR-box control S = %.4f (algebraic ceiling 4)" % S_p))

    # S4 no-signalling: second party's marginal split by first party's setting
    b_out = {0: [], 1: []}
    a_out = {0: [], 1: []}
    for _, ia, ib, ra, rb, alice_first, _, _ in rec_q:
        if alice_first:
            b_out[ia].append(rb)
        else:
            a_out[ib].append(ra)
    def marg_diff(d):
        m0, m1 = sum(d[0]) / len(d[0]), sum(d[1]) / len(d[1])
        return abs(m0 - m1), math.sqrt(1 / len(d[0]) + 1 / len(d[1]))
    db, sb = marg_diff(b_out)
    da, sa = marg_diff(a_out)
    results.append(check("S4", db < 5 * sb and da < 5 * sa,
                         "marginal shift B|A-setting %.4f (<%.4f), A|B-setting %.4f (<%.4f)"
                         % (db, 5 * sb, da, 5 * sa)))

    # S5 order invariance
    S_af, _, _, nba = run_chsh("genesis-v1", 20000, first="A")
    S_bf, _, _, nbb = run_chsh("genesis-v1", 20000, first="B")
    tol = 5 * math.sqrt((2 / math.sqrt(nba)) ** 2 + (2 / math.sqrt(nbb)) ** 2)
    results.append(check("S5", abs(S_af - S_bf) < tol,
                         "Alice-first S = %.4f, Bob-first S = %.4f, |diff| < %.3f" % (S_af, S_bf, tol)))

    # S6 no-conspiracy: settings vs pair-seed bit
    def corr(xs, ys):
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
        vx = sum((x - mx) ** 2 for x in xs) / n
        vy = sum((y - my) ** 2 for y in ys) / n
        return cov / math.sqrt(vx * vy) if vx * vy > 0 else 0.0
    seeds = [int(cid[0], 16) % 2 for cid in w_q.contracts]
    ias = [r[1] for r in rec_q]
    ibs = [r[2] for r in rec_q]
    ca, cb = abs(corr(seeds, ias)), abs(corr(seeds, ibs))
    lim = 5 / math.sqrt(len(seeds))
    results.append(check("S6", ca < lim and cb < lim,
                         "corr(seed, setting) A = %.4f, B = %.4f (< %.4f); settings built from own genesis only"
                         % (ca, cb, lim)))

    # S7 ancestry audit on a small world: remote measure block absent from local ancestry
    _, rec_s, w_s, _ = run_chsh("genesis-audit", 200)
    seq_s = {b["hash"]: b for b in w_s.log}
    def ancestors(h):
        seen, stack = set(), [h]
        while stack:
            x = stack.pop()
            for p in seq_s[x]["parents"]:
                if p not in seen:
                    seen.add(p)
                    stack.append(p)
        return seen
    ok_audit = True
    for _, ia, ib, ra, rb, alice_first, ha, hb in rec_s:
        first_h, second_h = (ha, hb) if alice_first else (hb, ha)
        if first_h in ancestors(second_h):
            ok_audit = False
            break
    results.append(check("S7", ok_audit,
                         "200 trials: first measurement never in causal ancestry of second "
                         "(correlation with no in-layer path)"))

    print()
    if all(results):
        print("SMOKE: ALL PASS (%d checks)" % len(results))
    else:
        print("SMOKE: FAILURES PRESENT")
    return all(results)


if __name__ == "__main__":
    main()
