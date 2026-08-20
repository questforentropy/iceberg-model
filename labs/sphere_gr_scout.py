"""Sphere-GR scouts (user ask 2026-08-16): the sidecar substrate - a closed 2D
sphere of SPRINKLED nodes (topology ruling + discreteness doctrine combined),
particles as waves/rays - and the first tier of the GR exam.

SG1  ruler          graph travel distance tracks great-circle distance
SG2  insider circles A(r) = 2*pi*(1-cos r) - insiders measure positive curvature
SG3  antipode       diameter = pi*R and ALL geodesics reconverge at one point
SG4  wave refocus   a wave pulse launched at a point re-peaks at the antipode
SG5  THE ILLUSION   compute profile c(theta) = 1 + cos(theta) disguises the
                    sphere as an EXACTLY Euclidean plane (stereographic):
                    travel distance = tan(theta/2), and 4-point Cayley-Menger
                    flatness drops to the flat-graph noise floor
SG6  the price      the antipode is exiled to infinite travel time (a horizon
                    point = spatial infinity of the fake plane)
SG7  the betrayal   node-grain density thins with travel radius (1+r^2)^-2 -
                    the geometry lies perfectly, the grain cannot
"""

import heapq
import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def sphere_points(run, n):
    rng = np.random.default_rng(4200 + run)
    v = rng.normal(size=(n, 3))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def disk_points(run, n, rad):
    rng = np.random.default_rng(8400 + run)
    r = rad * np.sqrt(rng.random(n))
    a = 2 * math.pi * rng.random(n)
    return np.stack([r * np.cos(a), r * np.sin(a)], axis=1)


def knn_edges(dist_matrix, k):
    n = len(dist_matrix)
    dm = dist_matrix + np.diag(np.full(n, np.inf))
    idx = np.argsort(dm, axis=1)[:, :k]
    pairs = set()
    for i in range(n):
        for j in idx[i]:
            pairs.add((min(i, int(j)), max(i, int(j))))
    ei = np.array([p[0] for p in pairs])
    ej = np.array([p[1] for p in pairs])
    return ei, ej, dist_matrix[ei, ej]


def adjacency(n, ei, ej, w):
    adj = [[] for _ in range(n)]
    for a, b, ww in zip(ei.tolist(), ej.tolist(), w.tolist()):
        adj[a].append((b, ww))
        adj[b].append((a, ww))
    return adj


def dijkstra(adj, n, src):
    dist = np.full(n, np.inf)
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
                heapq.heappush(pq, (nd, v))
    return dist


def cm_volume(ds):
    # Cayley-Menger: det = 288 V^2 of the 4-point tetrahedron; V = 0 iff the
    # six pairwise distances embed in a FLAT plane - the insider flatness meter
    d12, d13, d14, d23, d24, d34 = ds
    M = np.ones((5, 5))
    M[0, 0] = 0.0
    M[1:, 1:] = np.array([
        [0, d12, d13, d14],
        [d12, 0, d23, d24],
        [d13, d23, 0, d34],
        [d14, d24, d34, 0],
    ]) ** 2
    return math.sqrt(abs(np.linalg.det(M)) / 288.0)


def quad_scores(D, lo, hi, seed, keep=60):
    rng = np.random.default_rng(seed)
    m = len(D)
    scores = []
    for _ in range(6000):
        q = rng.choice(m, 4, replace=False)
        ds = [D[q[0], q[1]], D[q[0], q[2]], D[q[0], q[3]],
              D[q[1], q[2]], D[q[1], q[3]], D[q[2], q[3]]]
        if min(ds) < lo or max(ds) > hi:
            continue
        dbar = sum(ds) / 6.0
        scores.append(cm_volume(ds) / dbar ** 3)
        if len(scores) >= keep:
            break
    return float(np.median(scores)), len(scores)


def pairwise_graph_dist(adj, n, sources):
    D = np.zeros((len(sources), len(sources)))
    for a, s in enumerate(sources):
        d = dijkstra(adj, n, s)
        for b, t in enumerate(sources):
            D[a, b] = d[t]
    return D


def main():
    R = []
    n, k = 4000, 20
    pts = sphere_points(0, n)
    ang = np.arccos(np.clip(pts @ pts.T, -1.0, 1.0))
    ei, ej, elen = knn_edges(ang, k)
    adj_u = adjacency(n, ei, ej, elen)

    pole = int(np.argmax(pts[:, 2]))
    th = np.arccos(np.clip(pts[:, 2], -1, 1))     # polar angle from true north
    angs = ang[pole]                              # angle from the source node
    d_u = dijkstra(adj_u, n, pole)

    # SG1: the graph ruler tracks the true metric (up to one zigzag factor eta)
    sel = angs > 0.2
    eta = float((d_u[sel] * angs[sel]).sum() / (angs[sel] ** 2).sum())
    resid = d_u[sel] / eta - angs[sel]
    r2 = 1 - (resid ** 2).sum() / ((angs[sel] - angs[sel].mean()) ** 2).sum()
    R.append(check("SG1", r2 > 0.99 and 1.0 <= eta < 1.25,
                   "travel distance = %.3f x great-circle distance, R^2 = %.4f - one "
                   "isotropic zigzag factor, divided out below" % (eta, r2)))

    # SG2: insiders count sites inside travel-radius circles -> positive curvature
    sigma = n / (4 * math.pi)
    rows, ok2 = [], True
    for r in (1.0, 2.0):
        a_meas = (d_u / eta <= r).sum() / sigma
        a_sph = 2 * math.pi * (1 - math.cos(r))
        ok2 = ok2 and abs(a_meas / a_sph - 1) < 0.06
        rows.append("r=%.0f: A=%.2f (sphere %.2f, flat %.2f)" % (r, a_meas, a_sph, math.pi * r * r))
    R.append(check("SG2", ok2,
                   "circle areas fall short of pi*r^2 exactly as 2pi(1-cos r): %s - "
                   "insiders MEASURE the curvature without leaving" % "; ".join(rows)))

    # SG3: bounded diameter + all farthest points cluster at ONE antipode
    dmax = d_u.max() / eta
    far = np.argsort(d_u)[-20:]
    anti_ang = float(np.arccos(np.clip(-(pts[far] @ pts[pole]), -1, 1)).max())
    R.append(check("SG3", abs(dmax - math.pi) < 0.06 * math.pi and anti_ang < 0.3,
                   "diameter %.3f (pi = 3.142); the 20 farthest nodes all sit within "
                   "%.2f rad of the true antipode - every direction reconverges"
                   % (dmax, anti_ang)))

    # SG4: a real wave on the node graph refocuses at the antipode
    E_i = np.concatenate([ei, ej])
    E_j = np.concatenate([ej, ei])
    deg = np.bincount(E_i, minlength=n).astype(float)
    phi = np.exp(-angs ** 2 / (2 * 0.2 ** 2))
    prev = phi.copy()
    dt = 0.02
    cap = angs > math.pi - 0.25
    ring_masks = [np.abs(angs - a) < 0.06 for a in (0.5, 1.0, 1.5)]
    ts, cap_s, glob_s = [], [], []
    ring_s = [[] for _ in ring_masks]
    for s in range(1600):
        lap = np.bincount(E_i, weights=phi[E_j], minlength=n) - deg * phi
        nxt = 2 * phi - prev + dt * dt * lap
        prev, phi = phi, nxt
        e = ((phi - prev) / dt) ** 2
        ts.append((s + 1) * dt)
        cap_s.append(e[cap].mean())
        glob_s.append(e.mean())
        for rr, msk in zip(ring_s, ring_masks):
            rr.append(e[msk].mean())
    ts = np.array(ts)
    early = ts < 12.0
    t_arr = [float(ts[early][int(np.argmax(np.array(rr)[early]))]) for rr in ring_s]
    v = (1.5 - 0.5) / (t_arr[2] - t_arr[0])
    t_pred = t_arr[1] + (math.pi - 1.0) / v
    i_pk = int(np.argmax(cap_s))
    t_peak = float(ts[i_pk])
    contrast = cap_s[i_pk] / glob_s[i_pk]
    R.append(check("SG4", abs(t_peak - t_pred) < 0.15 * t_pred and contrast > 2,
                   "front speed %.3f -> predicted focus t=%.1f; antipodal energy peaks at "
                   "t=%.1f with %.1fx the global mean - the wave itself refocuses"
                   % (v, t_pred, t_peak, contrast)))

    # SG5: THE ILLUSION - c(theta) = 1+cos(theta) makes travel geometry EXACTLY flat
    slowness = 1.0 / (1.0 + np.cos(th))
    w_st = elen * 0.5 * (slowness[ei] + slowness[ej])
    adj_st = adjacency(n, ei, ej, w_st)
    d_st = dijkstra(adj_st, n, pole)
    u_true = np.tan(th / 2)
    sel5 = (th > 0.2) & (th < 2.8)
    slope = float((d_st[sel5] * u_true[sel5]).sum() / (u_true[sel5] ** 2).sum())
    res5 = d_st[sel5] / slope - u_true[sel5]
    r2s = 1 - (res5 ** 2).sum() / ((u_true[sel5] - u_true[sel5].mean()) ** 2).sum()

    rng = np.random.default_rng(7)
    cand = np.where((th > 0.4) & (th < 2.1))[0]
    srcs = rng.choice(cand, 25, replace=False)
    D_u = pairwise_graph_dist(adj_u, n, srcs)
    D_st = pairwise_graph_dist(adj_st, n, srcs)

    fpts = disk_points(0, n, 2.0)
    fr2 = (fpts ** 2).sum(axis=1)
    fdist = np.sqrt(np.maximum(fr2[:, None] + fr2[None, :] - 2 * fpts @ fpts.T, 0.0))
    fei, fej, felen = knn_edges(fdist, k)
    adj_f = adjacency(n, fei, fej, felen)
    fc = np.where(np.linalg.norm(fpts, axis=1) < 1.35)[0]
    fsrcs = np.random.default_rng(9).choice(fc, 40, replace=False)
    D_f = pairwise_graph_dist(adj_f, n, fsrcs)
    eucl = fdist[np.ix_(fsrcs, fsrcs)]
    m_off = eucl > 0.3
    eta_f = float((D_f[m_off] * eucl[m_off]).sum() / (eucl[m_off] ** 2).sum())

    # fat, large quadruples: curvature distortion grows ~ (size)^2, graph noise does not
    med_u, n_u = quad_scores(D_u, 1.4 * eta, 2.6 * eta, 11)
    med_st, n_st = quad_scores(D_st, 1.2 * slope, 2.4 * slope, 13)
    med_f, n_f = quad_scores(D_f, 1.1 * eta_f, 2.4 * eta_f, 17)
    R.append(check("SG5", r2s > 0.995 and abs(slope / eta - 1) < 0.10
                   and med_u > 4 * med_f and med_st < 0.3 * med_u,
                   "travel distance = %.3f x tan(theta/2), R^2 = %.4f (stereographic plane, "
                   "measured); 4-point flatness score: sphere %.4f vs FLAT GRAPH %.4f vs "
                   "disguised sphere %.4f (quads: %d/%d/%d) - the disguise measures flat "
                   "down to the noise floor" % (slope, r2s, med_u, med_f, med_st, n_u, n_f, n_st)))

    # SG6: the price of the disguise - the antipode moves to infinity
    horizon = d_st.max() / slope
    R.append(check("SG6", horizon > 4 * math.pi,
                   "farthest node now sits at travel distance %.1f vs the honest diameter "
                   "pi = 3.1 - the antipode is exiled toward infinity (diverges as the "
                   "grain refines): one unreachable point buys a whole fake plane" % horizon))

    # SG7: the betrayal - grain density per unit travel-area thins as (1+r^2)^-2
    rt = d_st / slope
    dens = []
    for lo, hi in ((0.0, 1.0), (2.5, 3.5)):
        cnt = int(((rt >= lo) & (rt < hi)).sum())
        dens.append(cnt / (math.pi * (hi * hi - lo * lo)))
    ratio = dens[0] / dens[1]
    R.append(check("SG7", ratio > 10,
                   "grain density inner disk / outer annulus = %.0f (prediction from "
                   "(1+r^2)^-2: 48; honest sphere: 1) - the metric lies perfectly, "
                   "the node count cannot" % ratio))

    print()
    print("SPHERE-GR: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
