"""Chain-fed randomness scout (user upgrade 2026-08-15).

v1 randomness: draw = hash(contract_seed, counter) - inside-sourced (the seed is chain
data) but a fixed per-contract stream.
v2 (this scout): THE LEDGER IS ITS OWN DICE - every write consumes the measuring
node's CURRENT tip hash once and produces a new block hash. The draw depends on the
whole history up to that write; the only outside input is the genesis string (the
initial condition). One hash per fold: draw consumption = block production = entropy.

Must re-verify: determinism, CHSH = 2sqrt2, no-signalling, order invariance,
no-conspiracy. PASS = statistics indistinguishable from v1.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke_test import ALICE_ANGLES, BOB_ANGLES, H, Node, World, u01


class ChainFedWorld(World):
    def measure(self, node, cid, angle):
        # GLOBAL UPDATE; the draw consumes the node's current head hash exactly once.
        c = self.contracts[cid]
        c.setdefault("version", 0)
        draw = u01(H(node.tip(), c["seed"], c["version"]))
        c["version"] += 1
        if not c["collapsed"]:
            c["collapsed"] = True
            c["axis"] = angle
            c["value"] = 1 if draw > 0.5 else -1
            out = c["value"]
        else:
            d = angle - c["axis"]
            p_plus = math.sin(d / 2) ** 2 if c["value"] == 1 else math.cos(d / 2) ** 2
            out = 1 if draw < p_plus else -1
        node.append("measure", "%s:%.6f:%+d" % (cid[:16], angle, out))
        return out


def run(genesis, n_trials, first="alternate"):
    w = ChainFedWorld(genesis)
    A, B = Node("A", w), Node("B", w)
    gen_a, gen_b = A.blocks[0]["hash"], B.blocks[0]["hash"]
    records = []
    for t in range(n_trials):
        cid = w.entangle(A, B)
        ia = int(H(gen_a, t, "setting"), 16) % 2
        ib = int(H(gen_b, t, "setting"), 16) % 2
        alice_first = (t % 2 == 0) if first == "alternate" else (first == "A")
        if alice_first:
            ra = w.measure(A, cid, ALICE_ANGLES[ia])
            rb = w.measure(B, cid, BOB_ANGLES[ib])
        else:
            rb = w.measure(B, cid, BOB_ANGLES[ib])
            ra = w.measure(A, cid, ALICE_ANGLES[ia])
        records.append((ia, ib, ra, rb, alice_first))
    bins = {}
    for ia, ib, ra, rb, _ in records:
        bins.setdefault((ia, ib), []).append(ra * rb)
    E = {k: sum(v) / len(v) for k, v in bins.items()}
    S = abs(E[(0, 0)] - E[(0, 1)] + E[(1, 0)] + E[(1, 1)])
    return S, records, w, min(len(v) for v in bins.values())


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def main():
    R = []
    N = 30000
    S, rec, w, nb = run("genesis-chainfed", N)
    sig = 2 / math.sqrt(nb)

    S2, _, w2, _ = run("genesis-chainfed", N)
    R.append(check("R1", w.transcript() == w2.transcript(),
                   "determinism survives: same genesis -> identical transcript (%d blocks)"
                   % len(w.log)))

    R.append(check("R2", abs(S - 2 * math.sqrt(2)) < 5 * sig,
                   "CHSH from head-fed draws: S = %.4f (2.8284 +/- %.3f)" % (S, 5 * sig)))

    b_by_ia = {0: [], 1: []}
    for ia, ib, ra, rb, alice_first in rec:
        if alice_first:
            b_by_ia[ia].append(rb)
    m0 = sum(b_by_ia[0]) / len(b_by_ia[0])
    m1 = sum(b_by_ia[1]) / len(b_by_ia[1])
    tol = 5 * math.sqrt(1 / len(b_by_ia[0]) + 1 / len(b_by_ia[1]))
    R.append(check("R3", abs(m0 - m1) < tol,
                   "no-signalling: Bob marginal shift %.4f (< %.4f)" % (abs(m0 - m1), tol)))

    S_a, _, _, nba = run("genesis-chainfed", 16000, first="A")
    S_b, _, _, nbb = run("genesis-chainfed", 16000, first="B")
    tol = 5 * math.sqrt((2 / math.sqrt(nba)) ** 2 + (2 / math.sqrt(nbb)) ** 2)
    R.append(check("R4", abs(S_a - S_b) < tol,
                   "order invariance: A-first S = %.4f vs B-first %.4f (|diff| < %.3f)"
                   % (S_a, S_b, tol)))

    seeds = [int(cid[0], 16) % 2 for cid in w.contracts]
    ias = [r[0] for r in rec]
    n = len(seeds)
    mx, my = sum(seeds) / n, sum(ias) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(seeds, ias)) / n
    vx = sum((a - mx) ** 2 for a in seeds) / n
    vy = sum((b - my) ** 2 for b in ias) / n
    corr = abs(cov / math.sqrt(vx * vy))
    R.append(check("R5", corr < 5 / math.sqrt(n),
                   "no-conspiracy: corr(pair seed, settings) = %.4f (< %.4f)"
                   % (corr, 5 / math.sqrt(n))))

    print()
    print("CHAIN-FED RANDOMNESS: %s (%d checks) - the ledger is its own dice; one hash "
          "consumed per fold, one block produced" % ("ALL PASS" if all(R) else "FAILURES", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
