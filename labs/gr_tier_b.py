"""GR Tier B (V3 completion campaign, 2026-08-17).

SB1  SPRINKLED GRAVITY (the standing prerequisite): Poisson field on the random
     closed sphere graph from neighbor exchange only - fits the closed-sphere
     Green's function -ln sin(theta/2)
SB2  Shapiro delay on the sprinkled sphere: signals past the crowd arrive late
     (vs a same-separation control path away from the crowd)
SB3  gravitational redshift by frequency conservation: coordinate frequency of a
     wave is conserved crossing a static well, so the emitter's slowed pacing
     arrives intact (the pacing itself = the Compton-clock assertion, declared)
SB4  triangle-excess closure (Girard): locally measured angles vs globally
     measured sides agree about the curvature
SB5  apsidal precession in the congestion field: eccentric orbit precesses at
     the log-potential value 2*pi/sqrt(2) (DRAWBACK on record: 2D log != GR 1/r;
     the GR number needs 3D)
SB6  wave on the DISGUISED sphere: no antipodal refocus - the fake plane has no
     far side
"""

import heapq
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sphere_gr_scout import adjacency, dijkstra, knn_edges, sphere_points
from v2_gravity_scout import C, N, bilinear, crowd_density, solve_field


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def dijkstra_prev(adj, n, src):
    dist = np.full(n, np.inf)
    prev = np.full(n, -1, dtype=int)
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u] + 1e-12:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v] - 1e-12:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev


def node_at(pts, theta, az):
    v = np.array([math.sin(theta) * math.cos(az), math.sin(theta) * math.sin(az),
                  math.cos(theta)])
    return int(np.argmax(pts @ v))


def main():
    R = []
    n, k = 4000, 14
    pts = sphere_points(0, n)
    ang = np.arccos(np.clip(pts @ pts.T, -1.0, 1.0))
    ei, ej, elen = knn_edges(ang, k)
    adj_plain = adjacency(n, ei, ej, elen)
    th = np.arccos(np.clip(pts[:, 2], -1, 1))
    E_i = np.concatenate([ei, ej])
    E_j = np.concatenate([ej, ei])
    deg = np.bincount(E_i, minlength=n).astype(float)

    # SB1: Poisson on the sprinkled closed sphere (crowd at the pole)
    rho = (th < 0.25).astype(float)
    src = rho - rho.mean()
    phi = np.zeros(n)
    for _ in range(20000):
        s = np.bincount(E_i, weights=phi[E_j], minlength=n)
        phi = (s + src) / deg
        phi -= phi.mean()
    sel = (th > 0.5) & (th < 2.6)
    x = -np.log(np.sin(th[sel] / 2))
    y = phi[sel]
    bins = np.linspace(x.min(), x.max(), 21)
    idx = np.digitize(x, bins)
    bx, by = [], []
    for b in range(1, 21):
        m = idx == b
        if m.sum() > 5:
            bx.append(x[m].mean())
            by.append(y[m].mean())
    bx, by = np.array(bx), np.array(by)
    a1, b1 = np.polyfit(bx, by, 1)
    r2 = 1 - ((by - (a1 * bx + b1)) ** 2).sum() / ((by - by.mean()) ** 2).sum()
    R.append(check("SB1", r2 > 0.97 and a1 > 0,
                   "SPRINKLED gravity: field on the random closed graph fits the sphere "
                   "Green's function -ln sin(theta/2) with R^2 = %.4f - Poisson statics "
                   "need no lattice, exchange on random neighbors suffices" % r2))

    # SB2: Shapiro delay past the crowd vs a control path
    phin = (phi - phi.min()) / (phi.max() - phi.min())
    slow = 1 + 0.8 * phin
    adj_slow = adjacency(n, ei, ej, elen * 0.5 * (slow[ei] + slow[ej]))
    a_n, b_n = node_at(pts, 1.047, 0.0), node_at(pts, 1.047, math.pi)
    a_f, b_f = node_at(pts, math.pi / 2, 0.0), node_at(pts, math.pi / 2, 2.094)
    t_slow_n = dijkstra(adj_slow, n, a_n)[b_n]
    t_plain_n = dijkstra(adj_plain, n, a_n)[b_n]
    t_slow_f = dijkstra(adj_slow, n, a_f)[b_f]
    t_plain_f = dijkstra(adj_plain, n, a_f)[b_f]
    exc_n = t_slow_n - t_plain_n
    exc_f = t_slow_f - t_plain_f
    d_all = dijkstra(adj_plain, n, a_n)
    m_eta = (ang[a_n] > 0.2) & (ang[a_n] < 2.6)
    eta = float((d_all[m_eta] * ang[a_n][m_eta]).sum() / (ang[a_n][m_eta] ** 2).sum())
    # straight-path prediction: line-integrate the ACTUAL node field along the meridian
    tgrid = np.linspace(0.02, 1.047, 120)
    prof = np.array([phin[node_at(pts, t, az)] for az in (0.0, math.pi) for t in tgrid])
    pred_n = 0.8 * eta * (np.trapezoid(prof[:120], tgrid) + np.trapezoid(prof[120:], tgrid))
    R.append(check("SB2", exc_n > 2.5 * exc_f and 0.35 * pred_n < exc_n < 1.15 * pred_n,
                   "Shapiro: excess delay past the crowd %.3f (straight-path prediction "
                   "%.3f; Fermat lets the path dodge, so <= is expected) vs control path "
                   "excess %.3f (x%.1f) - signals grazing mass arrive late" %
                   (exc_n, pred_n, exc_f, exc_n / max(exc_f, 1e-9))))

    # SB3: redshift = frequency conservation + slowed pacing (1D wave, well)
    Nx, dx, dt = 2400, 0.5, 0.2
    xg = np.arange(Nx) * dx
    cw = 1.0 - 0.3 * np.exp(-((xg - 200.0) ** 2) / (2 * 60.0 ** 2))
    r_e = float(cw[int(200 / dx)])
    f0 = 1.0 / 40.0
    f_drive = f0 * r_e                                    # emitter paced by its local rate
    w = np.zeros(Nx)
    wprev = np.zeros(Nx)
    rec = int(900 / dx)
    series = []
    for s2 in range(14000):
        t = s2 * dt
        lap = np.zeros(Nx)
        lap[1:-1] = w[2:] - 2 * w[1:-1] + w[:-2]
        nxt = 2 * w - wprev + (cw * dt / dx) ** 2 * lap
        nxt[int(200 / dx)] = math.sin(2 * math.pi * f_drive * t)
        nxt[-1] = 0.0
        nxt[xg > 1050] *= 0.98
        wprev, w = w, nxt
        if t > 1600:
            series.append(w[rec])
    series = np.array(series)
    zc = (np.diff(np.sign(series)) != 0).sum()
    f_rec = zc / (2 * len(series) * dt)
    conserve = f_rec / f_drive
    R.append(check("SB3", abs(conserve - 1.0) < 0.02,
                   "coordinate frequency conserved crossing the static well: received/"
                   "emitted = %.3f; so the receiver's faster clock reads the emitter "
                   "redshifted by r_e = %.2f exactly (pacing-by-local-rate = the Compton "
                   "assertion, declared; conservation = the measured part)" %
                   (conserve, r_e)))

    # SB4: triangle excess - local angles vs global sides
    A = node_at(pts, 0.9, 0.0)
    B = node_at(pts, 0.9, 2.443)
    Cv = node_at(pts, 1.92, 1.221)
    def sight_dir(vertex, target):
        # a geodesic sight-line to a beacon: its projection onto the local tangent
        # plane IS the initial tangent direction (great-circle geometry, exact)
        nh = pts[vertex]
        v = pts[target] - (pts[target] @ nh) * nh
        return v / np.linalg.norm(v)
    def vertex_angle(vx, t1, t2):
        d1 = sight_dir(vx, t1)
        d2 = sight_dir(vx, t2)
        return math.acos(max(-1, min(1, float(d1 @ d2))))
    angles = (vertex_angle(A, B, Cv) + vertex_angle(B, A, Cv) + vertex_angle(Cv, A, B))
    dA = dijkstra(adj_plain, n, A)
    dB = dijkstra(adj_plain, n, B)
    a_s = dB[Cv] / eta
    b_s = dA[Cv] / eta
    c_s = dA[B] / eta
    s = 0.5 * (a_s + b_s + c_s)
    lh = math.tan(s / 2) * math.tan((s - a_s) / 2) * math.tan((s - b_s) / 2) * math.tan((s - c_s) / 2)
    E_pred = 4 * math.atan(math.sqrt(max(lh, 0.0)))
    E_meas = angles - math.pi
    R.append(check("SB4", abs(E_meas - E_pred) < 0.25 and E_meas > 0.3,
                   "Girard closure: angle sum - pi = %.3f rad measured at the corners vs "
                   "%.3f predicted from the three side lengths (l'Huilier) - local "
                   "protractors and global rulers tell the same curvature" %
                   (E_meas, E_pred)))

    # SB5: apsidal precession in the congestion field (2D log potential)
    phi2, _ = solve_field(crowd_density(1.0))
    phin2 = phi2 / phi2.max()
    kap, h = 0.3, 0.5
    def acc(xx, yy):
        gx = (bilinear(phin2, xx + h, yy) - bilinear(phin2, xx - h, yy)) / (2 * h)
        gy = (bilinear(phin2, xx, yy + h) - bilinear(phin2, xx, yy - h)) / (2 * h)
        return kap * gx, kap * gy                      # a = -grad(-kap*phin) = +kap*grad
    r0 = 25.0
    ax0, _ = acc(C + r0, C)
    v_c = math.sqrt(abs(ax0) * r0)
    x0, y0, vx, vy = C + r0, float(C), 0.0, 0.75 * v_c
    dtp = 0.05
    rs, ps = [], []
    for _ in range(int(4000 / dtp)):
        axx, ayy = acc(x0, y0)
        vx += axx * dtp
        vy += ayy * dtp
        x0 += vx * dtp
        y0 += vy * dtp
        rs.append(math.hypot(x0 - C, y0 - C))
        ps.append(math.atan2(y0 - C, x0 - C))
        if len(ps) > 1000 and len([1 for i in range(1, len(rs) - 1)
                                   if rs[i] < rs[i - 1] and rs[i] < rs[i + 1]]) >= 4:
            break
    rs = np.array(rs)
    ps = np.unwrap(np.array(ps))
    mins = [i for i in range(1, len(rs) - 1) if rs[i] < rs[i - 1] and rs[i] < rs[i + 1]]
    dpsis = [abs(ps[mins[i + 1]] - ps[mins[i]]) for i in range(len(mins) - 1)]
    dpsi = float(np.mean(dpsis))
    pred = 2 * math.pi / math.sqrt(2)
    R.append(check("SB5", abs(dpsi - pred) < 0.30,
                   "eccentric orbit: perihelion-to-perihelion sweep %.2f rad vs log-"
                   "potential prediction 2pi/sqrt2 = %.2f (Kepler would be 6.28) - the "
                   "orbit precesses exactly as THIS field says. DRAWBACK on record: 2D "
                   "log field, not GR's 1/r - the GR precession number needs 3D" %
                   (dpsi, pred)))

    # SB6: wave on the DISGUISED sphere - no antipodal refocus
    pole = int(np.argmax(pts[:, 2]))
    angs = ang[pole]
    cnode = (1 + np.cos(th)) / 2.0
    wv = np.exp(-angs ** 2 / (2 * 0.2 ** 2))
    wprev2 = wv.copy()
    dtw = 0.02
    cap = angs > math.pi - 0.25
    contrast = 0.0
    for s3 in range(1600):
        lap = np.bincount(E_i, weights=wv[E_j], minlength=n) - deg * wv
        nxt = 2 * wv - wprev2 + dtw * dtw * cnode ** 2 * lap
        wprev2, wv = wv, nxt
        e = ((wv - wprev2) / dtw) ** 2
        gm = e.mean()
        if gm > 0:
            contrast = max(contrast, e[cap].mean() / gm)
    R.append(check("SB6", contrast < 3.0,
                   "disguised sphere c = (1+cos)/2: max antipodal energy contrast %.2f "
                   "over the whole run (honest sphere: ~20x refocus) - the fake plane "
                   "has no far side; the wave never comes home" % contrast))

    print()
    print("TIER B: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
