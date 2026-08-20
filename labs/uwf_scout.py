"""UWF scouts - the blockchain IS the universal wave function, stored factorized.

The claim (user, 2026-08-19): textbook QM writes one global Psi for the whole
universe; the ledger keeps the same object as a DAG of contracts - one factor
per connected component of entanglement. Merge = tensor product, settlement =
projection + re-factorization. Same state, sparse storage.

U1  equivalence: a random circuit universe run two ways - one global 2^n table
    vs the contract DAG - with draws keyed to the settlement EVENT (not the
    representation): outcomes bit-identical, settlement probabilities match,
    and the re-tensored DAG equals Psi entry by entry throughout the run
U2  sparsity: settlements re-factorize, so the DAG's live storage stays well
    under 2^n; merges grow it, folds shrink it back
U3  the Everett corner: never settle -> contracts merge until ONE factor of
    dimension 2^n remains, equal to the table exactly - the textbook universal
    wave function is the DAG's degenerate (settlement-free) limit
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qm_tests import H, u01, RY

N_Q = 8
DIM = 1 << N_Q


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def apply1_amps(amps, U, p):
    step = 1 << p
    for i in range(len(amps)):
        if not (i & step):
            j = i | step
            a0, a1 = amps[i], amps[j]
            amps[i] = U[0][0] * a0 + U[0][1] * a1
            amps[j] = U[1][0] * a0 + U[1][1] * a1


def cnot_amps(amps, pc, pt):
    cs, ts = 1 << pc, 1 << pt
    for i in range(len(amps)):
        if (i & cs) and not (i & ts):
            j = i | ts
            amps[i], amps[j] = amps[j], amps[i]


class Factor:
    """One contract: a connected component of entanglement.
    Local bit p of the amplitude index <-> global qubit qubits[p]."""

    def __init__(self, qubits, amps):
        self.qubits = list(qubits)
        self.amps = [complex(a) for a in amps]


class DAG:
    def __init__(self):
        self.factors = [Factor([q], [1, 0]) for q in range(N_Q)]
        self.merges = 0
        self.splits = 0

    def find(self, q):
        for f in self.factors:
            if q in f.qubits:
                return f
        raise KeyError(q)

    def merge(self, fa, fb):
        qubits = fa.qubits + fb.qubits
        amps = [0j] * (1 << len(qubits))
        ka = len(fa.qubits)
        for ib, b in enumerate(fb.amps):
            for ia, a in enumerate(fa.amps):
                amps[(ib << ka) | ia] = a * b
        self.factors.remove(fa)
        self.factors.remove(fb)
        nf = Factor(qubits, amps)
        self.factors.append(nf)
        self.merges += 1
        return nf

    def apply1(self, U, q):
        f = self.find(q)
        apply1_amps(f.amps, U, f.qubits.index(q))

    def cnot(self, c, t):
        fc, ft = self.find(c), self.find(t)
        if fc is not ft:
            fc = self.merge(fc, ft)
        cnot_amps(fc.amps, fc.qubits.index(c), fc.qubits.index(t))

    def measure(self, q, u):
        # settlement: project, renormalize, RE-FACTORIZE the settled qubit out
        f = self.find(q)
        p = f.qubits.index(q)
        step = 1 << p
        p1 = sum(abs(a) ** 2 for i, a in enumerate(f.amps) if i & step)
        bit = 1 if u < p1 else 0
        norm = math.sqrt(p1 if bit else 1 - p1)
        rest_qubits = [x for x in f.qubits if x != q]
        rest = [0j] * (1 << len(rest_qubits))
        for i, a in enumerate(f.amps):
            if bool(i & step) == bool(bit):
                lo = i & (step - 1)
                hi = (i >> (p + 1)) << p
                rest[hi | lo] = a / norm
        self.factors.remove(f)
        if rest_qubits:
            # the surviving branch's phase stays in the remainder factor
            self.factors.append(Factor([q], [0, 1] if bit else [1, 0]))
            self.factors.append(Factor(rest_qubits, rest))
        else:
            # fully dissolved contract: the settled thread keeps its own phase
            self.factors.append(Factor([q], [0, rest[0]] if bit else [rest[0], 0]))
        self.splits += 1
        return bit, p1

    def storage(self):
        return sum(len(f.amps) for f in self.factors)

    def psi(self):
        # re-tensor the DAG into the global vector
        out = []
        for g in range(DIM):
            a = 1 + 0j
            for f in self.factors:
                li = 0
                for p, qb in enumerate(f.qubits):
                    if (g >> qb) & 1:
                        li |= 1 << p
                a *= f.amps[li]
            out.append(a)
        return out


class Table:
    """The textbook object: one global 2^n amplitude vector."""

    def __init__(self):
        self.amps = [0j] * DIM
        self.amps[0] = 1 + 0j

    def apply1(self, U, q):
        apply1_amps(self.amps, U, q)

    def cnot(self, c, t):
        cnot_amps(self.amps, c, t)

    def measure(self, q, u):
        step = 1 << q
        p1 = sum(abs(a) ** 2 for i, a in enumerate(self.amps) if i & step)
        bit = 1 if u < p1 else 0
        norm = math.sqrt(p1 if bit else 1 - p1)
        self.amps = [a / norm if bool(i & step) == bool(bit) else 0j
                     for i, a in enumerate(self.amps)]
        return bit, p1


def run_universe(seed, ops=40, settle=True):
    dag, tab = DAG(), Table()
    out_d, out_t = [], []
    dev_p = dev_psi = 0.0
    max_store = dag.storage()
    for s in range(ops):
        r = u01(H(seed, "op", s))
        if r < 0.40:
            q = int(H(seed, "q", s), 16) % N_Q
            U = RY(2 * math.pi * u01(H(seed, "th", s)))
            dag.apply1(U, q)
            tab.apply1(U, q)
        elif r < 0.65:
            c = int(H(seed, "c", s), 16) % N_Q
            t = int(H(seed, "t", s), 16) % (N_Q - 1)
            t = t + 1 if t >= c else t
            dag.cnot(c, t)
            tab.cnot(c, t)
        elif settle:
            q = int(H(seed, "m", s), 16) % N_Q
            u = u01(H(seed, "evt", s))        # draw keyed to the EVENT, not the storage
            bd, pd = dag.measure(q, u)
            bt, pt = tab.measure(q, u)
            out_d.append(bd)
            out_t.append(bt)
            dev_p = max(dev_p, abs(pd - pt))
        max_store = max(max_store, dag.storage())
        if s % 5 == 0:
            psi = dag.psi()
            dev_psi = max(dev_psi, max(abs(a - b) for a, b in zip(psi, tab.amps)))
    return out_d, out_t, dev_p, dev_psi, max_store, dag


def main():
    R = []
    n_univ = 60
    all_match = True
    dev_p = dev_psi = 0.0
    stores, merges, splits = [], 0, 0
    for k in range(n_univ):
        od, ot, dp, dpsi, ms, dag = run_universe(H("uwf", k))
        all_match &= od == ot and len(od) > 0
        dev_p = max(dev_p, dp)
        dev_psi = max(dev_psi, dpsi)
        stores.append(ms)
        merges += dag.merges
        splits += dag.splits

    # U1: the two representations are the same object
    R.append(check("U1", all_match and dev_p < 1e-9 and dev_psi < 1e-9,
                   "%d random universes (n=%d, 40 ops each): outcomes bit-identical "
                   "global-table vs contract-DAG, settlement probabilities match to "
                   "%.1e, re-tensored DAG = Psi entry-by-entry to %.1e - the ledger "
                   "IS the universal wave function, stored factorized"
                   % (n_univ, N_Q, dev_p, dev_psi)))

    # U2: settlements keep the storage sparse
    mean_s = sum(stores) / len(stores)
    frac_sparse = sum(s < DIM for s in stores) / len(stores)
    R.append(check("U2", mean_s < 0.75 * DIM and frac_sparse > 0.5 and splits > 0,
                   "peak live storage mean %.0f amplitudes vs 2^n = %d global "
                   "(%d merges tensor factors together, %d settlements re-factorize "
                   "them apart; %.0f%% of universes never reach the global size) - "
                   "you pay 2^k only where entanglement lives"
                   % (mean_s, DIM, merges, splits, 100 * frac_sparse)))

    # U3: the Everett corner - never settle, one factor of dimension 2^n remains
    dag, tab = DAG(), Table()
    for q in range(N_Q):
        U = RY(2 * math.pi * u01(H("ev", q)))
        dag.apply1(U, q)
        tab.apply1(U, q)
    for q in range(N_Q - 1):
        dag.cnot(q, q + 1)
        tab.cnot(q, q + 1)
    for s in range(20):
        q = int(H("evq", s), 16) % N_Q
        U = RY(2 * math.pi * u01(H("evt2", s)))
        dag.apply1(U, q)
        tab.apply1(U, q)
    psi = dag.psi()
    dev = max(abs(a - b) for a, b in zip(psi, tab.amps))
    R.append(check("U3", len(dag.factors) == 1 and dag.storage() == DIM and dev < 1e-9,
                   "no settlements: contracts merge to ONE factor of dimension %d = 2^n, "
                   "equal to the textbook table to %.1e - Everett's universal Psi is the "
                   "DAG's settlement-free limit" % (dag.storage(), dev)))

    print()
    print("UWF: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
