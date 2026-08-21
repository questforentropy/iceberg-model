# Set GR — gravity

Labs, in numbering order: `v2_gravity_scout.py` (GR-1..4), `v2_gravity_scout2.py` (GR-5..6), `w1_why_fall.py` (GR-7..8), `cow_exam.py` (GR-9..12), `length_scouts.py` (GR-13..15), `sphere_gr_scout.py` (GR-16..22). Tier-B queue (Shapiro, redshift ticks, holonomy, precession, crowd-on-sphere, wave-on-disguised-sphere) will append as GR-23+ when built — defined in `../../sphere-gr-exam.md`.

| ID | Row | Verifies |
|---|---|---|
| GR-1 | G1 | Poisson far field (log d in 2D) from neighbor exchange only; dilation in EMPTY space (a field, not contact) |
| GR-2 | G2 | light bending toward the crowd; deflection ∝ mass (weak field) |
| GR-3 | G3 | free fall: packet at rest drifts toward the crowd (slow region = potential well) |
| GR-4 | G4 | equivalence principle holds iff internal frequency ∝ mass (Compton clock, isolated by control) |
| GR-5 | G5 | orbits: v_orb from the measured field holds its radius; rest falls, overspeed escapes |
| GR-6 | G6 | gravity at c: wave-type budget exchange arrives ballistically (t = d), statics still Poisson |
| GR-7 | W1a | at rest: point particle unmoved, wave packet falls — no steering rule exists or is needed |
| GR-8 | W1b | passing: point crosses dead straight, wave deflects — gravity is an interference effect |
| GR-9 | COW-1 | quantum interference reads the gravity field: fringe frequency = field-predicted clock-rate gap |
| GR-10 | COW-2 | COW fringe scales with arm separation |
| GR-11 | COW-3 | COW fringe scales with mass (Compton) |
| GR-12 | COW-4 | control: no crowd, no fringes |
| GR-13 | L1 | gravitational wavelength compression: pattern occupies fewer nodes where compute is busy |
| GR-14 | L2 | Lorentz contraction with no rule: sine-Gordon kink self-squeezes to w₀/γ (w·γ invariant) |
| GR-15 | Q1 | quasicrystal ruler verdict: Fibonacci = lattice = broken at e^(−η); only randomness cures counting |
| GR-16 | SG1 | sphere ruler: graph travel distance tracks great-circle distance (one zigzag factor) |
| GR-17 | SG2 | insider curvature: circle areas = 2π(1−cos r), not πr² |
| GR-18 | SG3 | closed topology: diameter = π, all geodesics reconverge at one antipode |
| GR-19 | SG4 | wave refocus: a pulse re-peaks at the antipode at the predicted time |
| GR-20 | SG5 | THE ILLUSION: c(θ) = 1+cos θ makes the sphere measure exactly Euclidean (stereographic; CM flatness at noise floor) |
| GR-21 | SG6 | the price: the antipode exiled to infinite travel time (horizon point = fake spatial infinity) |
| GR-22 | SG7 | the betrayal: grain density thins as (1+r²)⁻² — geometry can lie, the grain cannot |
| GR-23 | SB1 | SPRINKLED GRAVITY: Poisson field on the random closed sphere graph fits the sphere Green's function (statics need no lattice) |
| GR-24 | SB2 | Shapiro delay: signals grazing the crowd arrive late vs a control path |
| GR-25 | SB3 | gravitational redshift: coordinate frequency conserved crossing a static well (emitter pacing = the declared Compton assertion) |
| GR-26 | SB4 | Girard closure: locally measured angles and globally measured sides agree on the curvature |
| GR-27 | SB5 | apsidal precession at the log-potential value 2π/√2 (DRAWBACK on record: 2D log ≠ GR 1/r; the GR number needs 3D) |
| GR-28 | SB6 | wave on the disguised sphere: no antipodal refocus — the fake plane has no far side |
| GR-29 | RIP | budget ripples: an oscillating crowd radiates; wiggles ride the causal cone and decay outward (gravitational waves as load transients) |
| GR-30 | FF3 | 3D far field: the congestion potential falls as 1/r — Newton's shape; the 2D log was the toy's artifact |
| GR-31 | K3D | Kepler closure in 3D: eccentric orbits close (apsidal angle π) — the 2D precession drawback resolved as dimensional artifact |
| GR-32 | BEND | absolute bending: leading coefficient = 4GM/b, the full GR value (γ = 1 measured), 1/b law |
| GR-33 | PPN | the β = ½ audit: g₀₀ = −(1−GM/r)² gives perihelion advance 7/6 of GR (Schwarzschild control certifies the integrator) — a NAMED deviation: +17% on Mercury; deriving β = 1 is the sharpest open gravity dial |
| GR-34 | FL1 | (`gr_first_law.py`, Dorau-Much bridge, marks declared 2026-08-20 BEFORE first run) dumb-hole thermodynamics, mass-radius: horizon radius vs absorbed flux J fits a power law with exponent p in [0.7, 1.3] (Schwarzschild pattern r_h ~ M). PRE-REGISTERED ALTERNATIVE: analog-gravity lore (Unruh) says horizon KINEMATICS need not bring Einstein DYNAMICS - a FAIL here is the recorded kinematics-only verdict, itself a finding |
| GR-35 | FL2 | temperature-mass: measured surface gravity kappa vs J fits exponent q in [-1.35, -0.65] (Schwarzschild pattern T ~ 1/M) - same pre-registered alternative as FL1 |
| GR-36 | FL3 | the first-law closure: Clausius entropy S = INT 2pi dJ/kappa built from the MEASURED kappa(J) fits S ~ r_h^s with s in [1.5, 2.5] - the Bekenstein square (S ~ area in 3D reads S ~ r_h^2 here) assembled from two measured scalings, not installed |
| GR-37 | FE1 | (`gr_compounding.py`) the compounding rate law: slowdowns COMPOUND (each shell taxes the already-taxed rate; rates multiply - the ledger-native composition) -> c = e^(-Phi) instead of 1-Phi -> g00 = -e^(-2GM/r), grr = e^(+2GM/r). Perihelion through the SAME certified integrator as GR-33: precession ratio to GR within 0.03 of the Schwarzschild control - **beta = 1 measured; the GR-33 deviation closed by changing the composition law, not the dictionary** |
| GR-38 | FE2 | compounding bending: deflection still fits 4GM/b with leading coefficient in [0.95, 1.05] - gamma = 1 preserved (weak field identical; only second order moves) |
| GR-39 | FE3 | no coordinate horizon: the compounded redshift e^(-GM/r) is finite, positive, monotone at every r > 0 (Schwarzschild control hits zero at 2GM) - the metric-level echo of the BH-4 compute floor: rate approaches 0, never reaches it |
