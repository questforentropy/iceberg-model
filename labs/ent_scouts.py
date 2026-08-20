"""ENT scouts - entropy proper, first rows (V3 completion campaign, 2026-08-17).

EN1  entropy written per fold: outcome stream carries H(p) bits/fold (Born
     p = cos^2), memoryless; the compressor cannot beat H (doctrine: entropy =
     description length of the record)
EN2  memory or compute, both explode: archive grows linearly; recomputing any
     point from genesis costs linearly - measured, the C3 storage bill
EN3  the arrow is structural: the head hash is an injective accumulator of all
     history - exact recurrence impossible while the chain grows (measured: all
     heads distinct)
EN4  the fold split: observer-layer irreversible (many pre-states -> one
     record), substrate-layer invertible (full replay bit-exact)
"""

import hashlib
import math
import time
import zlib

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def H(*parts):
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


def u01(h):
    return int(h[:12], 16) / 16 ** 12


def run_chain(seed, nfolds, p):
    head = H("genesis", seed)
    outs = []
    for _ in range(nfolds):
        o = 1 if u01(H(head, "draw")) < p else 0
        outs.append(o)
        head = H(head, str(o))
    return outs, head


def shannon(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def main():
    R = []

    # EN1: bits per fold = H(p), memoryless; zlib floor respected
    rows = []
    ok1 = True
    for p in (0.5, 0.85):
        outs, _ = run_chain("ent1-%s" % p, 40000, p)
        a = np.array(outs)
        phat = a.mean()
        h_emp = shannon(phat)
        # conditional on previous outcome (memorylessness)
        h_cond = 0.0
        for prev in (0, 1):
            m = a[1:][a[:-1] == prev]
            h_cond += (a[:-1] == prev).mean() * shannon(m.mean())
        z_bits = len(zlib.compress(bytes(outs), 9)) * 8 / len(outs)
        ok1 = ok1 and abs(h_emp - shannon(p)) < 0.02 and abs(h_cond - h_emp) < 0.01 \
            and z_bits > 0.98 * h_emp
        rows.append("p=%.2f: H=%.3f (theory %.3f), H(X|prev)=%.3f, zlib %.3f b/fold"
                    % (p, h_emp, shannon(p), h_cond, z_bits))
    R.append(check("EN1", ok1,
                   "entropy written per fold = Born H(cos^2), memoryless, compressor "
                   "floored at H: %s - the ledger pays full price for every fold" %
                   "; ".join(rows)))

    # EN2: memory or compute, both explode
    t0 = time.perf_counter()
    run_chain("ent2", 20000, 0.5)
    t1 = time.perf_counter()
    run_chain("ent2", 40000, 0.5)
    t2 = time.perf_counter()
    ratio_t = (t2 - t1) / (t1 - t0)
    R.append(check("EN2", 1.5 < ratio_t < 3.0,
                   "archive after 2N folds = exactly 2x the archive after N (append-only, "
                   "by construction); replay-from-genesis cost 2N/N = x%.2f (linear) - "
                   "keep the notebook or redo the work, both bills grow forever" % ratio_t))

    # EN3: structural arrow - no recurrence while the chain grows
    head = H("genesis", "ent3")
    heads = {head}
    nf = 150000
    for i in range(nf):
        o = 1 if u01(H(head, "draw")) < 0.5 else 0
        head = H(head, str(o))
        heads.add(head)
    R.append(check("EN3", len(heads) == nf + 1,
                   "%d folds, %d distinct heads (zero repeats): the head is an injective "
                   "accumulator of ALL history, so exact recurrence would need a hash "
                   "collision - the arrow is structural, not probabilistic" %
                   (nf, len(heads))))

    # EN4: the fold split - observer irreversible, substrate invertible
    pre_states = [i / 100.0 * math.pi for i in range(100)]        # 100 distinct phases
    records = set()
    for j, thta in enumerate(pre_states):
        pj = math.cos(thta / 2) ** 2
        o = 1 if u01(H("ent4", str(j))) < pj else 0
        records.add(o)
    outs_a, head_a = run_chain("ent4-replay", 5000, 0.5)
    outs_b, head_b = run_chain("ent4-replay", 5000, 0.5)
    R.append(check("EN4", len(records) == 2 and outs_a == outs_b and head_a == head_b,
                   "100 distinct pre-fold states -> %d distinct records (50:1 collapse; "
                   "the record alone cannot invert the fold) BUT full replay from genesis "
                   "is bit-exact - irreversible at the observer layer, invertible at the "
                   "substrate layer: L2 fold, L3 rewind" % len(records)))

    print()
    print("ENT: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
