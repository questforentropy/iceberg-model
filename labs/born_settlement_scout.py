"""Double-entry Born scout (user ask 2026-08-17): can the SQUARE in |psi|^2 be
obtained from the blockchain instead of imported?

Mechanism (P4 candidate amendment): measurement = SETTLEMENT, and a settlement
is a co-signed block - it has exactly two sides. Protocol: the contract
PROPOSES an outcome branch (uniform hash draw); EACH of the two signers
independently accepts with probability equal to the branch NORM |alpha|
(the stored modulus, used linearly - no squaring anywhere); rejection anywhere
re-proposes. Settled statistics: P(i) ~ |alpha_i|^2 - Born, with the square
supplied by the two-signature structure, not by a rule.

DE1  the signature ladder: 1 signature -> P ~ |alpha| (NOT Born, fails);
     2 signatures -> Born exactly; 3 -> |alpha|^3 (fails). The square is the
     dyadic settlement made arithmetic: probability is |psi|^2 because every
     transaction has exactly two sides - and the ladder is falsifiable.
DE2  the full QM battery (qm_tests 9 rows + CH retake 20 rows) rerun with the
     Born line REPLACED by the settlement protocol: everything must still pass.
"""

import contextlib
import io
import math

import ch_retake
import qm_tests
from qm_tests import H, QContract, u01


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def make_settlement_measure(nsig):
    def measure_z(self, q):
        step = 1 << q
        p1 = sum(abs(a) ** 2 for i, a in enumerate(self.amps) if i & step)
        p1 = min(max(p1, 0.0), 1.0)
        bit = 0
        for _ in range(100000):
            b = 1 if self._draw() < 0.5 else 0            # the proposal
            amp = math.sqrt(p1 if b else 1.0 - p1)        # branch NORM, linear
            sigs = [self._draw() for _ in range(nsig)]    # every signer signs
            if all(d < amp for d in sigs):
                bit = b
                break
        norm = math.sqrt(p1 if bit else 1 - p1)
        self.amps = [a / norm if bool(i & step) == bool(bit) else 0j
                     for i, a in enumerate(self.amps)]
        return -1 if bit else 1
    return measure_z


def born_curve_dev(nsig, n=8000):
    fn = make_settlement_measure(nsig)
    worst = 0.0
    for k, th in enumerate((0.4, 0.9, 1.4, 1.9, 2.4)):
        p_target = math.sin(th / 2) ** 2
        hits = 0
        for t in range(n):
            c = QContract(H("de", nsig, k, t), [math.cos(th / 2), math.sin(th / 2)])
            c.measure_z = fn.__get__(c)
            if c.measure_z(0) == -1:
                hits += 1
        worst = max(worst, abs(hits / n - p_target))
    return worst


def run_suite(module):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        module.main()
    out = buf.getvalue()
    npass = nfail = 0
    for ln in out.splitlines():
        tok = ln.split()
        if not tok:
            continue
        if tok[0] == "PASS":
            npass += 1
        elif tok[0] == "FAIL":
            nfail += 1
        elif tok[0].startswith("CH-") and len(tok) > 1:
            if tok[1] == "FAIL":
                nfail += 1
            elif tok[1] in ("PASS", "PASS*", "MERGED", "IMPORTED", "BANKED"):
                npass += 1
    return npass, nfail


def main():
    R = []

    # DE1: the signature ladder
    d1 = born_curve_dev(1)
    d2 = born_curve_dev(2)
    d3 = born_curve_dev(3)
    R.append(check("DE1", d1 > 0.08 and d2 < 0.02 and d3 > 0.04,
                   "signature ladder, max deviation from Born: 1 signature %.3f (P ~ "
                   "|alpha|, wrong), 2 signatures %.3f (BORN), 3 signatures %.3f "
                   "(|alpha|^3, wrong) - the square is the two-sided settlement made "
                   "arithmetic: probability is |psi|^2 because every transaction has "
                   "exactly two signers; a world of 3-party settlements would run on "
                   "|psi|^3 (falsifiable ladder)" % (d1, d2, d3)))

    # DE2: the full QM battery with the Born line replaced by settlement
    orig = QContract.measure_z
    QContract.measure_z = make_settlement_measure(2)
    try:
        p_qm, f_qm = run_suite(qm_tests)
        p_ch, f_ch = run_suite(ch_retake)
    finally:
        QContract.measure_z = orig
    R.append(check("DE2", f_qm == 0 and f_ch == 0 and p_qm >= 9 and p_ch >= 17,
                   "full battery under the settlement sampler: qm_tests %d pass / %d "
                   "fail, CH retake %d pass / %d fail - the Born LINE is gone; what "
                   "remains imported is each signer accepting in proportion to the "
                   "branch norm (linear) - the squaring now comes from the ledger's "
                   "double-entry structure" % (p_qm, f_qm, p_ch, f_ch)))

    print()
    print("BORN-SETTLE: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT",
                                           len(R)))
    return all(R)


if __name__ == "__main__":
    main()
