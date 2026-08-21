"""Exam runner - executes a test SET and tallies PASS/FAIL rows across its labs.

Tests are numbered SET-N in lab print order (stable as long as labs only
append). Set definitions live in tests/definitions/<set>.md; the generated
record (status + declared criterion + measured detail per row) is written to
tests/results/<version>.md.

Usage:
    python run_exams.py SUB EN
    python run_exams.py all
    python run_exams.py all --record solaris-1.0.0
        -> also writes tests/results/<version>.md (the record table)
    ... --expect-red GR-34,GR-35,GR-36
        -> exit 0 iff the failing rows are EXACTLY the declared pre-registered
           reds (the CI gate: green = all pass except the reds on the books)
"""

import os
import re
import subprocess
import sys
import time

SETS = {
    "SUB": ["smoke_test.py", "chain_randomness_scout.py", "uwf_scout.py",
            "uwf_scout2.py"],
    "QM": ["qm_tests.py", "ch_retake.py", "born_settlement_scout.py", "lg_scout.py"],
    "QX": ["x_exams.py", "tsirelson_scout.py"],
    "ST": ["spacetime_tests.py"],
    "GR": ["v2_gravity_scout.py", "v2_gravity_scout2.py", "w1_why_fall.py",
           "cow_exam.py", "length_scouts.py", "sphere_gr_scout.py",
           "gr_tier_b.py", "gr_ripples_3d.py", "gr_3d.py",
           "gr_first_law.py", "gr_compounding.py"],
    "EN": ["noether_scouts.py", "unruh_scout.py"],
    "EX": ["v3_expansion_scout.py", "m2_breathing_fabric.py",
           "m3_closed_fabric.py", "h1_ball_horizon.py", "ex_closed_loop.py"],
    "DS": ["discreteness_scout.py", "ds_fineness_blur.py"],
    "ENT": ["ent_scouts.py"],
    "FLU": ["fluid_scouts.py", "fluid_scouts2.py"],
    "BH": ["bh_scouts.py", "bh_scouts2.py"],
}
OK_STATUSES = {"PASS", "PASS*", "MERGED", "IMPORTED", "OK"}
PLANNED_SETS = []


def tests_dir(here):
    return os.path.normpath(os.path.join(here, "..", "tests"))


def load_criteria(here):
    """Map row ID -> declared criterion, from the definitions tables."""
    crit = {}
    d = os.path.join(tests_dir(here), "definitions")
    if not os.path.isdir(d):
        return crit
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        with open(os.path.join(d, f), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip("|"))]
                if len(cells) >= 3 and re.match(r"^[A-Z]+-\d+$", cells[0]):
                    crit[cells[0]] = cells[2]
    return crit


def parse_rows(text):
    """Yield (status, label, detail) for every scored row of a lab's stdout."""
    for line in text.splitlines():
        tok = line.split()
        if not tok:
            continue
        if tok[0] in ("PASS", "FAIL"):
            yield tok[0], (tok[1] if len(tok) > 1 else "?"), " ".join(tok[2:])
        elif tok[0].startswith("CH-") and len(tok) > 1:   # ch_retake status column
            yield tok[1], tok[0], " ".join(tok[2:])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    raw = sys.argv[1:]
    version = None
    expect_red = None
    if "--record" in raw:
        i = raw.index("--record")
        version = raw[i + 1]
        raw = raw[:i] + raw[i + 2:]
    if "--expect-red" in raw:
        i = raw.index("--expect-red")
        expect_red = {t.strip().upper() for t in raw[i + 1].split(",") if t.strip()}
        raw = raw[:i] + raw[i + 2:]
    args = [a.upper() for a in raw] or ["all"]
    wanted = list(SETS) if "ALL" in args else args
    unknown = [s for s in wanted if s not in SETS]
    if unknown:
        print("unknown set(s): %s   (known: %s)" % (", ".join(unknown), ", ".join(SETS)))
        return False
    grand_p = grand_f = 0
    failed_sets = []
    recorded = []                        # (test_id, label, status, detail)
    for s in wanted:
        print("== SET %s ==" % s)
        set_p = set_f = 0
        seq = 0
        for lab in SETS[s]:
            t0 = time.time()
            r = subprocess.run([sys.executable, os.path.join(here, lab)],
                               capture_output=True, text=True)
            npass = nfail = 0
            for status, label, detail in parse_rows(r.stdout):
                seq += 1
                tid = "%s-%d" % (s, seq)
                if status == "FAIL":
                    nfail += 1
                elif status in OK_STATUSES:
                    npass += 1
                recorded.append((tid, label, status, detail))
                if version:
                    print("  %-8s %-18s %-9s %s" % (tid, label, status, detail[:100]))
            crashed = r.returncode != 0
            if crashed:
                nfail = max(nfail, 1)
            set_p += npass
            set_f += nfail
            print("  %-28s %3d pass %3d fail  %5.1fs%s"
                  % (lab, npass, nfail, time.time() - t0,
                     "  [CRASH]" if crashed else ""))
            if crashed and r.stderr:
                print("    " + r.stderr.strip().splitlines()[-1])
        verdict = "PASS" if set_f == 0 else "FAIL"
        print("  -> %s: %s (%d/%d rows)" % (s, verdict, set_p, set_p + set_f))
        grand_p += set_p
        grand_f += set_f
        if set_f:
            failed_sets.append(s)
    print()
    print("TOTAL: %d pass, %d fail%s"
          % (grand_p, grand_f,
             "" if not failed_sets else "  (failing sets: %s)" % ", ".join(failed_sets)))
    if version:
        write_results(here, version, recorded, grand_p, grand_f)
    if expect_red is not None:
        failed_ids = {tid for tid, _, st, _ in recorded if st == "FAIL"}
        ok = failed_ids == expect_red
        print("EXPECTED-RED GATE: %s (red: %s; expected: %s)"
              % ("GREEN" if ok else "MISMATCH",
                 ",".join(sorted(failed_ids)) or "-", ",".join(sorted(expect_red))))
        return ok
    return grand_f == 0


def cell(text, cap):
    text = " ".join(text.split()).replace("|", "\\|")
    return text if len(text) <= cap else text[:cap - 1] + "…"


def write_results(here, version, recorded, grand_p, grand_f):
    out = os.path.join(tests_dir(here), "results", "%s.md" % version.lower())
    os.makedirs(os.path.dirname(out), exist_ok=True)
    criteria = load_criteria(here)
    day = time.strftime("%Y-%m-%d")
    lines = ["# Examination record - %s (run %s)" % (version.upper(), day), "",
             "Generated by `run_exams.py all --record %s`. Declared criteria: `../definitions/` "
             "(shown truncated); measured detail as printed by the lab." % version.lower(),
             "", "| Test | Row | Status | Declared criterion | Measured |",
             "|---|---|---|---|---|"]
    for tid, label, status, detail in recorded:
        lines.append("| %s | %s | %s | %s | %s |"
                     % (tid, label, status,
                        cell(criteria.get(tid, "?"), 200), cell(detail, 120)))
    for s in PLANNED_SETS:
        lines.append("| %s-* | (set not yet defined) | QUEUED | | |" % s)
    lines += ["", "**Total: %d pass, %d fail.**" % (grand_p, grand_f), ""]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("results written:", out)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
