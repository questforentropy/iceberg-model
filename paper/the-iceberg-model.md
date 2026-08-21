# The Iceberg Model: Quantum and Relativistic Mysteries as Properties of a Two-Layer Computational Architecture — a Mechanism Study with a Test Harness

**Marijus Masteika**
Independent researcher
masteris@gmail.com
Series: *Quest for Entropy* — questforentropy.substack.com

*Version 2.2 — 2026-08-21 — documents Iceberg manifest 1, reference instance **Solaris 1.0.0** — this repository is the paper's source of truth; changes arrive as visible commits*

---

## Abstract

We present the Iceberg Model: a two-layer computational architecture in which the classic mysteries of quantum mechanics and relativity stop being mysterious. The **visible layer** is a substrate of compute nodes with a *fixed total budget*: processing load slows the local rate, and from that one fact spacetime phenomenology emerges — the light-speed limit (records cannot cite records that don't exist yet), time dilation, gravity as congestion, cosmological expansion as the cost of a growing record, and black holes as regions where the rate approaches zero without ever reaching it. The **hidden layer** organizes the system's state and history as a decentralized, append-only ledger of co-signed records: entanglement is a shared contract, measurement is settlement, the universal wave function is the ledger stored factorized, and many-worlds is the settlement-free limit. The two layers meet at one point: every write costs budget.

**The claim of this paper is mechanism sufficiency, not empirical adequacy.** We argue — and demonstrate in a toy, against a versioned examination harness of 150 recorded rows across 11 test sets — that one simple construct suffices to make the strange behaviours ("God playing dice", the cat that is dead and alive, spooky action at a distance, time dilation, the expanding universe, warping spacetime, the universal wave function) *simply explainable*: each becomes what a distributed system looks like to a limited observer who emerges inside it. Demystifying the mechanisms is the achievement claimed. **We are not claiming to have built the universe on a laptop**: the model's parameters are deliberately unfitted, its named deviations and imports are cataloged in a dedicated Difficulties section (three examination rows are deliberately red), and where the model and established physics disagree, established physics is right. All numerical results — like every experiment behind them — were produced with AI assistance and remain under continuing verification and validation; the one-command reproduction (§8) exists precisely so that any reader can check any number independently.

---

## 1. Introduction

### 1.1 The kind of claim this paper makes

There is a recurring shape in the history of explanation: first comes a *mechanism* that dissolves a family of mysteries at once, with no fitted parameters; the quantitative synthesis — the numbers, the rates, the precision tests — comes later, often much later, and often from other hands. This paper is deliberately an artifact of the first stage, and says so.

Its claim is **mechanism sufficiency**: that a single simple construct — a fixed-compute substrate carrying an append-only ledger — *suffices* to reproduce, in a toy, the behavioural signatures that make quantum mechanics and relativity feel mysterious, and to do so in a way that makes each mystery legible as an ordinary property of distributed systems. What the paper does **not** claim: that nature is a blockchain; that the toy is empirically adequate; that any established theory or interpretation is refuted; that the universe has been built on a laptop. The model's parameters (its "configurations", §1.4) are deliberately unfitted to our world, and its deviations from established physics are named and quantified rather than hidden — where they disagree, established physics is right (§6).

Because a mechanism claim is cheap to make and expensive to check, the paper's method is the check: every behaviour cited below is a numbered row in a versioned examination harness (§4) that re-runs with one command, with pass criteria declared before each first run and never softened afterwards — including three rows that are deliberately red.

### 1.2 The architecture in one page

**The visible layer — fixed compute.** A finite set of processing nodes with a conserved total budget, connected as a random graph laid down once at genesis. Nothing geometric is installed: no metric, no clock field, no expansion parameter, no force law. Processing particles is *load*; load slows the local rate; and everything an internal observer can call spacetime is bookkeeping of that one fact.

**The hidden layer — the distributed ledger.** The substrate's state and history: hash-linked per-particle chains of interaction records, merged by co-signed joint blocks, with no global chain and no randomness primitive. The ledger is modelled on blockchain mechanics *as an approximation instrument* — the universe is obviously not a blockchain; the finding is that ledger mechanics approximate the hidden layer of quantum behaviour remarkably well, and the harness measures how far. The division of labour behind that choice is deliberate: the ledger implements *exactly* the part of the hidden layer this paper's claims live on — records, contracts, settlement, the bookkeeping of who knows what and when — while the wave content (complex amplitudes on pending branches) is carried as imported arithmetic rather than produced by a deeper mechanism (§6, difficulty 1). That is an implementation boundary, not a conceptual one: producing wave dynamics from a deeper substrate is beyond a laptop toy, demonstrating the principal mechanism is not, and the architecture is stated so that a future implementation can push the boundary — deriving, rather than importing, the amplitude layer is the declared extension target of the synthesis stage (§7).

**The coupling.** Every write costs budget. A settlement in the hidden layer is a load event in the visible one — which is why the quantum sector can drive the gravitational and cosmological sectors (§5.5), and why this is one model rather than two.

**The thesis.** Postulate that the universe can be a distributed compute system with a complex state. Then the "crazy" behaviour is not a property of the machinery at all: it is *what the machinery looks like to a limited observer inside it* — an observer made of the same records, who can read only their own ledger, can never see the whole state, and has no place to stand outside. The mysteries are perspective effects of being inside a large distributed system; the demystification (§5) is naming which effect each one is. An observer inside is standing in a house of warped mirrors: everything they see is real data, yet every image arrives shaped by the medium that delivers it — and the warping is lawful enough to be exactly calculable, and consistent enough to be perfectly convincing (§5.4's disguise result: a closed world that presents to its insiders as an infinite flat plane).

A working intuition used throughout: **a company with no head office.** Thousands of offices, no central database, no master dashboard; all that exists is one ledger book per office and one rule — *a fact is a transaction co-signed by two offices*. Every paradox in §5 is some question that quietly assumes the master screen showing "the real state right now." The model deletes the dashboard; with nothing left to be paradoxical against, each mystery becomes a bookkeeping question with a measured answer.

### 1.3 What is claimed, precisely

**Claimed:** that the mechanisms of §3 — spacetime as gossip structure on a fixed-compute sprinkle, gravity as congestion, expansion as the storage bill, black holes as asymptotic compute starvation, entanglement as a shared contract, measurement as two-signature settlement — *suffice to reproduce the behavioural battery of §4–§5, in a toy, at the stated tolerances, with the stated imports*. Every such claim cites its examination rows and reproduces from the companion archive.

**Not claimed:** empirical adequacy; a fitted cosmology; a replacement for any working theory. The residual physical content the model does *not* demystify is isolated rather than hidden — chiefly, that pending branches carry *amplitudes* and interfere until settled (§6, difficulty 1).

### 1.4 Status: an initial release, structured for evolution

The model is organized in three layers with semantic versioning `<instance> M.m.p`:

- **The architecture** (this paper's subject; the Iceberg manifest, major version **M**): the two principles and one coupling above, plus the postulates of §3. This is the layer that carries the demystification claim.
- **Implementations** (minor **m**): the mechanisms realizing each principle — which composition law load obeys, which exchange carries flux, which source feeds the deterministic draws. Several may coexist as branches, each sitting the same examinations.
- **Configurations** (patch **p**): tunable parameter values — couplings, grain density, topology, genesis seed — which must eventually be fitted to the world we live in. That fitting is future work, and deliberately so.

The reference instance is **Solaris 1.0.0**: manifest 1, first complete implementation, canonical configuration (a sprinkled 3-sphere; §3.3). **The model is not complete and work continues** — the harness is the contract between versions: refinements must re-sit every examination, and regressions are recorded, not silently repaired. What we commit to as the model's identity is the architecture; what we expect to change are implementations and configurations (§7 names the live candidates, including a measured implementation change that moves the model's sharpest gravitational deviation from +17% to +0.7%).

### 1.5 Method of production

The author is a software architect, not a physicist. The direction, the main concepts and ideas, the questions, the postulates' framing, and the accept/reject calls are his; the mathematics, the code, the numerical work, *and the texts themselves — this paper included —* were produced with AI assistance from the author's guidance, under an adversarial harness (Acknowledgements): pass marks declared before each run and never softened, results challenged in independent adversarial review passes, and errors recorded rather than erased. Every number in this paper is printed by code in the companion archive.

---

## 2. Related work

The idea that the universe computes is old and well-populated, and this model makes no priority claim on it: Zuse's *Rechnender Raum*, Fredkin's digital philosophy, Lloyd's universe-as-quantum-computer, Wolfram's hypergraph programme, Whitworth's virtual-reality framing. What we believe is distinctive is (a) the **fixed-compute-budget substrate** with spacetime phenomenology as emergent load bookkeeping rather than installed rules; (b) the **ledger dictionary** for the hidden layer — append-only, co-signed, forkable, no global chain — under which no-cloning is the double-spend problem (solved by the mechanism Nakamoto introduced for exactly that purpose), measurement is settlement, and entanglement is a shared contract; and (c) the **versioned examination harness** with named imports, named deviations, and pre-registered failures.

Individual sectors have close neighbours, cited in place: causal set theory (Bombelli–Lee–Meyer–Sorkin; Myrheim–Meyer dimension estimation) for the sprinkled substrate; Lamport's happens-before relation for the vector-clock reading of the DAG; analog gravity (Unruh; Barceló–Liberati–Visser; Steinhauer) for the flux sector and its horizons — including Unruh's kinematics/dynamics dichotomy, which the harness measures directly (§6); Jacobson's thermodynamic derivation of the Einstein equation, its recent quantum-information sharpening by Dorau and Much, and Verlinde's entropic gravity as the nearest members of the gravity-from-information family; Madelung and Wallstrom for the hydrodynamic sector; Yilmaz-type exponential metrics for the compounding composition law measured in §5.4; Zurek's quantum Darwinism for classicality-as-replication; and the Born-derivation lineage (Gleason; Zurek's envariance; Deutsch–Wallace) beside which the double-entry settlement mechanism of §5.2 is offered as a structurally different, internally falsifiable alternative. Barandes's indivisible-stochastic-process formulation is a particularly close neighbour: settlement events map naturally onto his division events, and we regard the ledger as a candidate concrete completion of the equivalence class his formulation deliberately leaves open. On storage, representing a global state by its entangled-cluster factorization is standard in quantum simulation; the observation here is the identification — the ledger's contract graph *is* that factorization, maintained by the model's own physical events. A useful contrast case: Pettini derives entanglement from a hidden *causal* channel and predicts small distance-dependent deviations from quantum mechanics; the Iceberg's shared contract is correlation-only by append-only construction and predicts exactly zero deviation — structural cousins, empirically opposed.

*A full literature pass precedes any journal submission; pointers to uncited prior art are welcome.*

---

## 3. The architecture in detail

### 3.1 The dictionary

| Ledger concept | Physics reading |
|---|---|
| Compute node + hash-linked chain of records | particle; the particle *is* its record |
| Joint co-signed block referencing two chains' tips | interaction (a merge commit) |
| The resulting DAG (no global chain, no total order) | causal structure; happens-before = hash pointer |
| Fork with per-branch amplitudes | superposition |
| Shared contract over k members (one joint table) | entanglement — **the model's one global object: the global hidden variable, named** |
| Contract merge (tensor product) | interaction of independent clusters |
| Settlement: propose, two signatures, project, re-factorize | measurement |
| Move-only handle, never copied | no-cloning as the double-spend problem |
| Head-hash consumption at every settlement | randomness (deterministic, chain-fed: the ledger is its own dice) |
| Gossip distance; one hop per event | space; light = record propagation itself |
| Self-records vs hop-records on a chain | aging vs motion |
| Replication of a record into many chains | classicality (consensus = objectivity) |
| Load slowing local block production | gravity (peaked load) and expansion (uniform load) |
| Budget flux dragging wave propagation | frame dragging |

### 3.2 The postulates (P1–P11, abbreviated)

**P1** substrate = DAG of per-particle chains, no global chain (a total order is a preferred frame, refused by construction). **P2** particle = its thread of records; the transferable handle is move-only. **P3** superposition = fork with amplitudes advanced by deterministic contract code. **P4** entanglement = one shared contract per cluster, non-factorizable by construction — the model's definition of quantumness and its named *global* hidden variable (the programme targets global, not local, hidden variables; Bell's theorem is an input, not an obstacle). **P5** measurement = settlement; the observer is a node; facts are relative until reconciled. **P6** every settlement consumes the writer's current head hash; the only outside input is the genesis string. **P7** settings derive from re-hashing each node's own history — superdeterminism in the letter, no conspiracy in the mechanism, and *checkable* (§5.2). **P8** space = gossip distance; the speed limit is structural. **P9** classicality = replication. **P10** load always slows, never speeds; peaked load = a transient well, uniform load = cumulative stretch; entropy increase is the conversion; the fabric is closed, so only contrast bends. **P11** the load also flows; density slows time, flux drags space; dragging requires exchange inertia; a hungry sink builds its own one-way horizon.

### 3.3 The substrate: a sprinkled 3-sphere, laid once

The node graph is generated once at genesis by iterated hashing — statistically Poisson (a "sprinkle"), not a lattice and not a quasicrystal. This is forced: regular structures carry preferred frames that measurably break boost invariance at every density, while random sprinkles hide the discreteness behind statistical isotropy (§5.1). Compute is fixed; expansion and curvature are loads *on* the substrate, never edits *to* it.

The fabric is closed (finite, edgeless). The canonical topology for the reference instance is the 3-sphere S³ — the dimensional-ladder continuation of the measured 2-sphere instruments, and isotropic, where a flat 3-torus would carry globally preferred wrap axes. No fourth spatial dimension enters: S³ is defined intrinsically; embedding coordinates are sprinkler scaffolding that never appears in the exchange graph. Topology is a *configuration* the examinations test, not an assumption: defined rows require the sprinkle to self-report its dimension from inside, require every local result to be topology-blind (identical on matched S³ and 3-torus patches), and localize all topology dependence at wrap scale. In particular, the gravitational deviation of §5.4 is *not* a dimension or topology artifact — it survives the honest three-dimensional port with a certified control.

### 3.4 The two grains

The **event grain** — the price of one write, the quantum of action ħ — is visible to internal observers because it *is* their interface. The **space grain** — node spacing — hides if and only if the sprinkle is random, fine, and undisguised (measured, §5.1). On this reading ħ is a construct of the interface, not a granularity of space.

---

## 4. Method and evidence: the examination harness

Tests live in named sets with stable, append-only row identifiers (SET-N); model versions re-sit the sets; every full campaign is recorded as a per-version results table, regenerated by one command:

```
python run_exams.py all --record solaris-1.0.0
```

The current record (Solaris 1.0.0, 2026-08-21): **150 rows across 11 sets — 147 pass, 3 deliberately red** (§6, difficulty 4). Sets: substrate and ledger mechanics (SUB, 21), the quantum exam (QM, 30), advanced protocols (QX, 12), emergent spacetime (ST, 4), gravity (GR, 39), energy and Noether structure (EN, 6), expansion and cosmology (EX, 17), discreteness doctrine (DS, 3), entropy (ENT, 4), fluid structure and flux (FLU, 8), black holes (BH, 6).

Three design rules matter for reading §5. **Pre-registration**: some rows exist to record *predicted failures* (the naive dilation law fails the Lorentz form, as declared in advance — the failure is the finding), and failed predictions stay red rather than being tuned away. **Define-before-sit**: a new physics question enters as a defined row with declared pass marks before any version attempts it. **Status honesty**: PASS is earned; PASS\* passes *by construction* because an import guarantees it (and says so); IMPORTED is a disclosure, not a pass; of the 150 rows, 2 are PASS\*, 1 is IMPORTED, 4 are cross-references, 3 are red, and the remainder are earned.

*Validation status.* Every number in this paper was produced with AI assistance under the discipline above and is under **continuing verification and validation**. The battery reruns from scratch with the one command, and a discrepancy found by a reader is exactly the contribution the repository invites.

---

## 5. The demystifications

This is the paper's core: mystery by mystery, what each becomes inside the architecture, with the rows that earned each sentence. (The claim fence of §1.3 applies to every entry: these are readings inside the model.)

### 5.1 The relativity block

**The speed of light.** Not a speed limit imposed on things but the pace of record propagation itself: a block cannot reference a block that does not exist yet, so "faster than light" would mean citing the future. Measured: causal reach after k gossip rounds is *exactly* graph distance k (ST-1).

**Time dilation, and where it honestly comes from.** A moving thread writes fewer self-records between the same causal milestones — its clock ticks slower, and no preferred frame exists because there is no global chain. The exact Lorentz factor is *not* a naive budget split: the split model predicts τ = T(1−v) and **measurably fails — we said so before running it** (ST-2, pre-registered, confirmed). The factor √(1−v²) is block-counting along the worldline in the randomly sprinkled causal graph, boost-invariant precisely because the sprinkle has no preferred directions (ST-3); regular lattices and even quasicrystals fail this at every density (DS-1, GR-15), and the last statistical trace of the random grain fades with fineness as a measured power law (DS-3). Photon chains carry essentially no self-records — light does not age (ST-4).

**Length contraction.** No contraction rule exists anywhere in the code: a moving kink launched at rest-width relaxes to w·γ = 1 *by itself* (GR-14) — the shape follows from the same record-writing the clock follows.

**"Now."** There is no global now — a distributed system cannot be photographed at an instant. "The state right now" is a *consistent cut* through the ledger: different valid cuts give different instantaneous descriptions and identical settled records, and the freeze-everything-simultaneously snapshot demonstrably does not exist (SUB-19). This entry is the hinge to the quantum block: most quantum "paradoxes" are questions that assume the photograph.

### 5.2 The quantum block

**Spooky action at a distance.** Nothing acts at a distance: entangled particles share one *contract* — a single record in the hidden layer. The correlation lives in that shared record, not in anything travelling; measuring is settling the contract, and the settlement provably leaves no in-layer trace — no signal, no order dependence, and *no causal path between the measurement events*, shown by graph traversal (SUB-7/8/10, with CHSH at the Tsirelson value 2√2 and the local-hidden-variable control capped at 2). What is shared is the contract — the named *global* hidden variable — never pre-stored local answers: the local-answer picture is the model's own control, and it stops at the classical bound (SUB-5). The freedom-of-choice loophole is handled structurally: settings are re-hashed from each node's own history, and a graph query certifies no path from the pair's seed to either setting (SUB-9).

**Measurement and collapse.** No special role for observers: measurement is an ordinary co-signed settlement between two threads, and "collapse" is the ledger pruning unsettled branches — irreversible from inside (records don't un-write; 100 pre-settlement states collapse to 2 records for the observer), plain bookkeeping from outside (replay from genesis is bit-exact) (ENT-4).

**Schrödinger's cat.** The cat is never alive-and-dead because the cat is not a bystander — it is a huge *settling* system. Measurement is any co-signed interaction, no human required: the atom's fork settles at the first co-signature inside the box, and a *silent* detector settles just as well (QM-22 — the null outcome collapses too). A macroscopic body cannot hold a fork open: every co-signature replicates the record, visibility decays by a measured product law per leaked record, and undoing costs chasing every replica (QX-4, QM-4). In the engineer's one-liner: the sealed box is a `Future<Cat>` — an unresolved promise — and opening it is the `await`. Asking "but is it *really* alive right now?" is asking for a field of an unresolved future: a type error, not a mystery. The quantum refinement that keeps this honest: pending branches carry amplitudes and *interfere* until settled — a decided-but-unreported value could never interfere — and that measurable difference is the one piece of genuine quantum content the analogy does not dissolve (§6, difficulty 1). The analogy also makes no computational claim: a promise resolves to a Boolean, while a quantum branch carries an amplitude, and it is interference between amplitudes that gives quantum computation its extra power — a machine built of futures and Boolean values demonstrates the cat's "dead/alive" and cannot serve as a quantum computer.

**Wigner's friend.** Facts are relative until reconciled — bookkeeping, not paradox. The friend's ledger settled; Wigner, unmerged, correctly describes the lab as forked; both are right because they are different consistent cuts (SUB-19). Two measured theorems keep it honest: on merging, Wigner's re-measurement *always* agrees with the friend's record, for every reader (QM-8, 2000/2000 — agreement is a postcondition, because comparing IS reconciling), and a watcher who has not co-signed gains nothing (QM-29 — no joint block, no information, interference intact).

**"God playing dice."** There are no dice: every settlement consumes the measuring node's current head hash — the outcome depends deterministically on the entire history up to that fold, unpredictable from inside for the same reason hashes are. The full quantum battery is unchanged when every random draw is replaced by chain-fed hashes (SUB-11..15): the ledger is its own dice.

**The Born rule's square.** Probability is |ψ|² because every transaction has exactly two sides: settlement proposes a branch uniformly, and each of exactly *two* signers accepts with probability linear in the branch norm — the square emerges structurally. The mechanism is falsifiable inside the model: one signer yields P ∝ |ψ| (wrong, measured deviation 0.149), two yield Born (0.004), three yield |ψ|³ (wrong, 0.089); and the entire battery passes with the imported Born line deleted and the settlement sampler in its place (QM-30/31). The residual import is named: *norm-linear acceptance per signer* is still a rule — the question has moved from "why squared" to "why norm-linear." An external anchor says the dyadic choice is not arbitrary: the exponent 2 is heavily over-determined in quantum foundations — Gleason's theorem forces |ψ|² as the only consistent probability measure on Hilbert spaces of dimension ≥ 3, and the 2-norm is the only p-norm that nontrivial linear dynamics can conserve, so a world of one- or three-party settlements would be a world whose probabilities leak over time. The toy's two-sided settlement and nature's 2-norm point at the same number from opposite directions.

**The Tsirelson bound.** Why 2√2 and not the algebraic 4: one shared table, locally chosen settings, and two-sided settlement saturate at exactly 2√2 under a 10,000-point adversarial search, while the *same* settlement machinery serving a rewrite-contract (one that edits instead of appending) reaches 4 (QX-11/12). The quantum ceiling is single-table, append-only contract discipline; why nature keeps single-table contracts is the residual question, named.

**No-cloning.** Copying an unknown state is a double-spend, and the ledger refuses it by construction — the handle is move-only, used exactly once (QX-1): a deep quantum theorem as an accounting rule, and independently the linear-type discipline quantum programming languages arrived at.

**The rest of the zoo, in one line each, all measured:** which-path records kill interference and erasure restores it (QM-4, QM-23); complementarity V²+D²=1 (QM-24); delayed choice changes nothing (QM-21); GHZ wins deterministically at M=4 (QM-5); monogamy sits on the Toner boundary (QM-6); teleportation is exact with the two classical bits and garbage without (QX-2); entanglement swapping correlates parties that never met (QX-3); the Zeno effect (QX-5); the interaction-free bomb test at 50/25/25 (QX-10); and Leggett–Garg: passive watchers sit exactly *on* the macrorealist ceiling while settlement crosses it to the temporal Tsirelson value 3/2 — the model violates macrorealism for the structurally right reason, measurement is invasive by construction (QM-32/33).

### 5.3 The wave-function block

**The universal wave function.** Not a ghostly object containing all reality: it is the ledger's state, stored factorized — one contract per connected component of entanglement, merge = tensoring, settlement = re-factorizing. Re-tensor the contracts and Ψ comes back entry-by-entry to 10⁻¹⁵, with outcomes bit-identical between the two representations (SUB-16). Its fearsome size is a representation artifact — the flat table is the fully-replicated view of a sharded database: in the settling regime, storage is *linear* in particle number (about two amplitudes per particle, measured, SUB-21), so a universe of 10⁸⁰ particles books ~10⁸² bits — under the Bekenstein ceiling, where the flat view would need 10^(3×10⁷⁹) numbers. Just big; no magic.

**Many-worlds.** The ledger that never settles: with no settlements, contracts merge until one table of dimension 2ⁿ remains — literally Everett's Ψ, equal to the textbook object exactly (SUB-18). It even has a measured place on a phase diagram: merges grow entangled clusters, settlements cut them, and a giant cluster gels when merging wins (SUB-20). Many-worlds is the gel phase; a settling world stays sol. Not a rival theory — the architecture's settlement-free corner.

### 5.4 The gravity block

**Warping spacetime.** Nothing curves. A region dense with matter is dense with processing; compute there runs slower; and waves passing by refract toward the slow region — that refraction *is* falling. Only waves fall: a point particle sails straight through the same field (GR-7/8) — matter must be wavelike for gravity to act on it, and the packet's transport obeys the Madelung fluid equations exactly (FLU-2/3). The congestion field satisfies the Poisson law on the sprinkled closed substrate (GR-23, R² = 0.9997; 1/r in 3D, GR-30), light bends by the full general-relativistic coefficient 4GM/b (γ = 1, GR-32), orbits close (GR-31), and a two-arm interferometer reads the field exactly as in the Colella–Overhauser–Werner experiment (GR-9..12).

**The composition law — a live implementation result.** With *linear* composition of slowdowns (Solaris 1.0), the metric carries β = ½ and over-predicts Mercury's perihelion precession by 17% — a named deviation, kept on the books (GR-33). Measured this release: if slowdowns *compound* — rates multiply, each shell taxing the already-taxed rate, which is both how dilation factors actually stack and the minimal form of the self-coupling that horizon thermodynamics demands — the same certified instruments give **β = 0.979** (perihelion 1.0071×GR against a Schwarzschild control at 1.0065), γ = 1 preserved, and the compounded redshift e^(−GM/r) has no coordinate horizon at all (GR-37..39; the exponential metric of the Yilmaz type). The deviation closes by changing an implementation detail, not the architecture — the candidate Solaris 1.1 (§7).

**The Euclidean disguise (why we can't just look).** On the closed substrate, a conformal rate profile *exactly disguises* the sphere as an infinite flat plane — the travel-time metric becomes flat to noise floor, the antipode is exiled to infinite travel time — with one incorruptible tell: the grain density, which betrays the disguise at the predicted 48× contrast (GR-20..22). Geometry can lie; the grain cannot.

### 5.5 The cosmology block

*The entropy mechanism in one paragraph, first.* The state grows; the information that holds it is load; and load warps in exactly two shapes. **Peaked load** — matter being processed — slows its own neighbourhood: a gravitational well. **Uniform load** — records and radiation spread evenly across the fabric — slows everything equally: the global stretch. Entropy increase is the one-way conversion between them: structure radiates away, wells level into background, and what was local warping becomes global slowing — measured end to end (wells decay to 1.1% of their depth while the global stretch grows ×1.65, never shrinking, monotone with entropy and landing on the uniform prediction; EX-4..8). Gravity and expansion are the two shapes of one bill.

**The expanding universe.** The record grows; holding it costs budget; everything smoothly slows — and from inside, everything slowing uniformly is indistinguishable from everything moving apart. Expansion is the storage bill, and the loop is closed and measured: the ledger's real fold count feeds the slowdown — doubling the fold rate doubles the redshift rate (EX-16) at a constant price per bit across epochs (EX-17) — with the Hubble law z ∝ d and the supernova stretch factor exact in-toy (EX-2, EX-15). The energy "lost" to cosmological redshift is the bill being paid: in a static region energy is conserved to 10⁻⁸, under expansion it leaks at exactly the tax rate (EN-1/2), while E/ω rides through untouched — ħ is pinned (EN-3).

**Dark energy — a candidate mechanism, labelled as such.** What accelerating expansion names in standard cosmology is, in this architecture, a statement about *the shape of the entropy-production curve*: expansion is the storage bill (above), so the stretch accelerates exactly when record growth is super-linear — no substance, no energy component, no cosmological constant installed. The measured ingredients exist: the fold rate drives the stretch rate (EX-16), and exponential record growth produces a *permanent, observer-centered* horizon (EX-12/13) — precisely the de Sitter phenomenology that "dark energy" labels. In this reading, the cosmological constant corresponds to the asymptotic fold rate of a universe whose structure keeps writing. Not claimed: any ΛCDM number (the equation of state is not derived); the acceleration audit is a defined future examination row, and this entry is a candidate mechanism, not a result.

**The edge of the visible universe.** Space has no edge — the fabric is a closed sphere (§3.3). The edges we see are *emergent*: expansion is a slowdown, and where the accumulated slowing outruns the causality limit, records from beyond can never arrive — the "visible universe" is simply the region causality can still reach. Measured: with linear record growth the whole fabric remains eventually reachable, while exponential growth caps the reach at a *permanent* horizon, at exactly the predicted radius (EX-12/13); and the horizon is observer-centered — every observer finds an equal horizon centered on *themselves*, edges on an edgeless world (EX-14). Whether the universe has a permanent edge is a property of its entropy-production curve, not of its geometry.

**The arrow of time.** Append-only. The head hash accumulates all history injectively — recurrence would need a hash collision (150,000 folds, zero repeats, ENT-3). The past is fixed because records don't un-write; the future is open because it isn't written yet.

### 5.6 Black holes and temperature

**The singularity.** A black hole is a region packed so dense that its compute rate approaches zero — asymptotically, never arriving: the rate stays finite, positive, and monotone up to loads of 10³⁰⁰, redshift 1+z = 1+L exact, and the only diverging quantity is a continuum proxy the machine never inverts (BH-4). The "singularity" is continuum language dividing by zero; the ledger just runs slower. Deep wells are frozen but not sealed — a core signal escapes in finite time, with the measured log-law delays of the frozen-star image (BH-5, BH-3). A genuinely *one-way* horizon is a different, dynamical object, built by inflow rather than density (BH-1/2), and the two mechanisms are experimentally distinguishable inside the model (BH-6).

**The Unruh temperature.** Accelerate through the vacuum and it reads warm at exactly T = a/2π — not because heat exists, but because an accelerated sampling schedule reads the substrate's churn as thermal: measured to 0.4%, with temperature doubling when acceleration doubles and the inertial control exactly cold (EN-5/6). The temperature was never an input; only the worldline was. (The corresponding evaporation mechanism — a virtual pair as a fork-and-cancel transaction that a horizon forces to *commit*, the infalling partner posting the debit — is a defined, not-yet-run row, labelled as such.)

### 5.7 The constants

**Planck's constant.** Not the granularity of space — the price of one write, a property of the interface between the layers, visible to us precisely because it *is* our interface (§3.4; EN-3). The space grain is a different object, and it hides (DS-1..3).

**Circulation quantization.** A ledger cannot record 0.4 of a turn: single-valued storage forces whole windings, so vortex circulation comes in units of 2π for free (FLU-1) — the axiom Wallstrom showed hydrodynamics needs, as a structural property of ledgers.

---

## 6. Difficulties with the theory

Nothing here is hidden by a passing row; this section is the model's honesty device.

1. **The amplitude residue — the one thing not demystified.** Pending branches carry complex amplitudes and interfere until settled; a classical decided-but-unreported value could not. The architecture *isolates* this content (its arithmetic is the double-entry protocol, §5.2) rather than dissolving it. Norm-linear acceptance per signer remains a rule, and the complex-unitary structure remains imported (Barandes's representation theorem is a candidate route to restate it as derived bookkeeping; not yet executed). The computational corollary is stated plainly: real quantum systems are waves whose amplitudes interfere — strictly more computational power than any classical machine of promises and Boolean values. The futures analogy of §5.2 demystifies the paradox, not the processor.
2. **Single-table discipline.** The Tsirelson ceiling is internal (§5.2) *given* that contracts are single, persistent, append-only tables; why nature keeps single-table contracts is open.
3. **The gravitational composition law is measured, not derived.** Compounding closes the β deviation (§5.4) and is independently motivated, but the full derivation of the field equation from substrate mechanics — the Jacobson-style route — is open; until adopted and derived, Solaris 1.0's linear law and its named +17% Mercury deviation stay on the books as the recorded alternative.
4. **Three rows are deliberately red.** Declared marks asked whether the model's *dynamical* (flux-route) hole obeys Schwarzschild thermodynamics (r ∝ M, T ∝ 1/M, S ∝ area). It does not: absorbed flux saturates and bigger holes read hotter, not colder (GR-34..36, FAIL, kept). This is Unruh's analog-gravity dichotomy measured in-toy — horizon *kinematics* come free, horizon *thermodynamics* require the right dynamics — and the red rows are retained as the sharpest statement of what the model has not earned.
5. **Compton pacing asserted** (equivalence works because internal clock rate scales with mass — installed, not derived), and the coupling magnitudes (expansion price, flux–drag) are dials with derived shapes and installed values.
6. **The 2^k contract table** is the universal wave function's own dimensionality, localized (§5.3) and linear-in-N in the settling regime (SUB-21) — but a scaling wall for the toy regardless.
7. **The grain.** The discreteness blur fades with fineness as a measured power law but is nonzero at any fixed grain; the exact Euclidean disguise would need unbounded refinement.
8. **Untestable by construction:** "no global chain" cannot be refuted from inside; it is kept on parsimony grounds and labelled. Measured ablation also shows the *specific* hash function is not load-bearing (the draws need only determinism and decorrelation) — which licenses, but does not yet implement, sourcing randomness from substrate traffic itself.

---

## 7. The synthesis stage

If §5 is this programme's mechanism argument, the synthesis stage — fitting implementations and configurations until the toy's dials match the world — is deliberately left ahead, and the three-layer structure (§1.4) exists to receive it. Live candidates, all with defined examination rows: adopting the compounding composition law (Solaris 1.1: re-sit the gravity and cosmology sets; the strong-field regime, where the exponential metric has no true horizon, becomes the model's declared falsifiable frontier); the S³ self-report and topology-blindness rows; Hawking evaporation as forced settlement; the spinning (drain-vortex) hole with its ergoregion; traffic-sourced randomness; the entropy–thread-splitting route to expansion; the amplitude layer itself — deriving, rather than importing, the wave content of pending branches (§1.2, §6 difficulty 1; Barandes's representation theorem is the candidate route) — the extension that would move the model's deepest import inside the mechanism; and the ball ledger — surface as the compute screen, interior as archive — which changes the *architecture* (manifest 2) and whose native prediction, information scaling with horizon *area*, is the input that would connect the model to the Jacobson/Dorau–Much theorems at the level of bookkeeping rather than analogy.

The model will change. The examinations will not be weakened.

---

## 8. Reproduction

The companion archive contains the model, all examination definitions, and the runner; the full battery reproduces with one command (`python run_exams.py all --record solaris-1.0.0`), regenerating the 150-row table including the three red rows. Every number in §5–§6 appears in the printed output of its cited row. Archive: **github.com/questforentropy/iceberg-model** (the model's canonical home; this paper is its manifest) — *Zenodo DOI inserted at publication.*

---

## Acknowledgements and AI assistance disclosure

This work was produced by the author with substantial AI assistance: Anthropic's Claude models (Claude Fable, Claude Opus, Claude Sonnet) and DeepSeek. The division of labour: the author set the direction, originated the main concepts and ideas, posed the questions, supplied the framing postulates and rulings, and made every accept/reject call; the AI systems performed the mathematics, wrote and ran the code, executed the physics checks, and wrote the texts — this paper and the series' publications — from the author's guidance and under his editing. The work was conducted under an adversarial harness: examination pass marks declared before running and never softened afterwards; results challenged in independent adversarial review passes; instrument errors and overclaims recorded in a correction log rather than erased. All results remain under continuing verification and validation. The author regards full disclosure of AI involvement, together with one-command reproducibility of every number, as the appropriate response to the reasonable question of how one knows the AI did not fool the author.

## References

*(Initial list; a full literature pass precedes any journal submission.)*

- J. S. Bell, Physics 1, 195 (1964); J. F. Clauser, M. A. Horne, A. Shimony, R. A. Holt, Phys. Rev. Lett. 23, 880 (1969); B. S. Tsirelson, Lett. Math. Phys. 4, 93 (1980).
- S. Popescu, D. Rohrlich, Found. Phys. 24, 379 (1994); B. F. Toner, F. Verstraete (2006).
- A. J. Leggett, A. Garg, Phys. Rev. Lett. 54, 857 (1985).
- A. M. Gleason, J. Math. Mech. 6, 885 (1957); W. H. Zurek, Phys. Rev. A 71, 052105 (2005); D. Deutsch, Proc. R. Soc. A 455, 3129 (1999); D. Wallace, *The Emergent Multiverse* (2012).
- W. H. Zurek, "Quantum Darwinism," Nature Physics 5, 181 (2009).
- J. A. Barandes, the stochastic–quantum correspondence / indivisible stochastic processes (2023).
- L. Bombelli, J. Lee, D. Meyer, R. D. Sorkin, Phys. Rev. Lett. 59, 521 (1987); J. Myrheim (1978); D. A. Meyer, PhD thesis, MIT (1988).
- L. Lamport, CACM 21, 558 (1978).
- W. G. Unruh, Phys. Rev. Lett. 46, 1351 (1981); C. Barceló, S. Liberati, M. Visser, Living Rev. Relativity 8, 12 (2005); J. Steinhauer, Nature Physics 12, 959 (2016).
- T. Jacobson, Phys. Rev. Lett. 75, 1260 (1995); P. Dorau, A. Much, "From quantum relative entropy to the semiclassical Einstein equations," arXiv:2510.24491 (2026); E. Verlinde, JHEP 2011, 29 (2011).
- E. Madelung, Z. Phys. 40, 322 (1927); T. C. Wallstrom, Phys. Rev. A 49, 1613 (1994).
- H. Yilmaz, "New approach to general relativity," Phys. Rev. 111, 1417 (1958) *(the exponential-metric family; cited as prior art for §5.4's compounding measurement)*.
- R. Colella, A. W. Overhauser, S. A. Werner, Phys. Rev. Lett. 34, 1472 (1975).
- J. D. Bekenstein, Phys. Rev. D 7, 2333 (1973); S. W. Hawking, Commun. Math. Phys. 43, 199 (1975).
- K. Zuse, *Rechnender Raum* (1969); E. Fredkin (1990); S. Lloyd, *Programming the Universe* (2006); S. Wolfram (2020); B. Whitworth (2010).
- G. 't Hooft, *The Cellular Automaton Interpretation of Quantum Mechanics* (2016).
- S. Nakamoto, "Bitcoin: a peer-to-peer electronic cash system" (2008).
- A. C. Elitzur, L. Vaidman, Found. Phys. 23, 987 (1993).
- M. Pettini, Phys. Rev. Research (2025), arXiv:2311.17070.
- J. A. Wheeler, "Information, physics, quantum: the search for links" (1990).

---

*Attribution: this paper and the repository's documentation are CC BY 4.0; the code is MIT. If you present or build on the concepts of this work in any medium — a video, an article, a talk, a journal paper — please credit the author and cite this paper (`CITATION.cff` in the repository; DOI attached at release).*
