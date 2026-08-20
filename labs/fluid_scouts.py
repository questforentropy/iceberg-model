"""FLU scouts - the fluid dictionary (2026-08-17).

Tier 2 (V3 rows - the engine was secretly a fluid all along):
F1  vortex quantization: circulation comes in integer units of 2*pi because the
    stored field is single-valued - Wallstrom's missing axiom is free in a
    ledger; a fractional vortex reads as an integer and stays one
F2  continuity audit: d(rho)/dt + div j = 0 - probability is a locally
    conserved fluid; it flows, it never teleports
F3  Euler decomposition: the probability fluid's mean velocity comes from its
    own current, and its acceleration equals the congestion force (Ehrenfest
    in fluid variables) - "gravity accelerates the probability fluid"

Tier 3 (V4 "flowing fabric" founding scouts - load gets a FLUX):
F4  drag: waves in a DRIFTING medium travel at u +/- c - the Sagnac asymmetry,
    the off-diagonal metric term, frame dragging's 1D seed
F5  dumb hole: where the drift exceeds c, nothing gets back out - a one-way
    membrane with nothing frozen (Unruh's sonic horizon, in compute language)
"""

import math

import numpy as np


def check(label, ok, detail):
    print("%-6s %-4s %s" % ("PASS" if ok else "FAIL", label, detail))
    return ok


def winding(psi, cx, cy, rr, m=720):
    angs = np.linspace(0, 2 * math.pi, m, endpoint=False)
    xs = np.round(cx + rr * np.cos(angs)).astype(int)
    ys = np.round(cy + rr * np.sin(angs)).astype(int)
    ph = np.angle(psi[ys, xs])
    d = np.diff(np.concatenate([ph, ph[:1]]))
    d = (d + math.pi) % (2 * math.pi) - math.pi
    return float(d.sum() / (2 * math.pi))


def evolve_free(psi, steps, dt):
    n = psi.shape[0]
    k = 2 * math.pi * np.fft.fftfreq(n, 1.0)
    kx, ky = np.meshgrid(k, k)
    kin = np.exp(-1j * (kx ** 2 + ky ** 2) * dt / 2)
    for _ in range(steps):
        psi = np.fft.ifft2(kin * np.fft.fft2(psi))
    return psi


def spectral_grad(f):
    n = f.shape[0]
    k = 2 * math.pi * np.fft.fftfreq(n, 1.0)
    kx, ky = np.meshgrid(k, k)
    F = np.fft.fft2(f)
    gx = np.real(np.fft.ifft2(1j * kx * F)) if np.isrealobj(f) else np.fft.ifft2(1j * kx * F)
    gy = np.real(np.fft.ifft2(1j * ky * F)) if np.isrealobj(f) else np.fft.ifft2(1j * ky * F)
    return gx, gy


def main():
    R = []

    # F1: vortex quantization - integer circulation, topologically protected
    n = 256
    yy, xx = np.mgrid[0:n, 0:n]
    cx = cy = n // 2
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    th = np.arctan2(yy - cy, xx - cx)
    env = np.exp(-((r / 90.0) ** 8))
    rows, ok1 = [], True
    for q in (1.0, 2.0, 0.4):
        psi = np.tanh(r / 3.0) ** max(1, int(round(abs(q)))) * np.exp(1j * q * th) * env
        w0 = winding(psi, cx, cy, 20)
        psi_t = evolve_free(psi.astype(complex), 400, 0.05)
        w1 = winding(psi_t, cx, cy, 20)
        ok1 = ok1 and abs(w0 - round(w0)) < 1e-6 and abs(w1 - round(w1)) < 1e-6
        if q in (1.0, 2.0):
            ok1 = ok1 and round(w0) == int(q) and round(w1) == int(q)
        rows.append("charge %.1f: winding %.0f -> %.0f after evolution" % (q, w0, w1))
    R.append(check("F1", ok1,
                   "circulation quantized in units of 2*pi and conserved: %s - the "
                   "attempted 0.4-vortex READS as an integer (single-valued storage "
                   "forces whole turns: Wallstrom's axiom is free in a ledger)" %
                   "; ".join(rows)))

    # F2 + F3: falling packet as a fluid - continuity + Euler
    n2 = 128
    yy2, xx2 = np.mgrid[0:n2, 0:n2]
    V = -0.4 * np.exp(-((xx2 - 48.0) ** 2 + (yy2 - 64.0) ** 2) / (2 * 10.0 ** 2))
    dVx, _ = spectral_grad(V)
    k2 = 2 * math.pi * np.fft.fftfreq(n2, 1.0)
    kx2, ky2 = np.meshgrid(k2, k2)
    dt = 0.02
    kin = np.exp(-1j * (kx2 ** 2 + ky2 ** 2) * dt / 2)
    pot = np.exp(-1j * V * dt / 2)
    psi = np.exp(-((xx2 - 80.0) ** 2 + (yy2 - 64.0) ** 2) / (4 * 5.0 ** 2)).astype(complex)
    psi /= np.sqrt((np.abs(psi) ** 2).sum())

    def step(p):
        p = pot * p
        p = np.fft.ifft2(kin * np.fft.fft2(p))
        return pot * p

    ts, xbar, vbar, fbar = [], [], [], []
    res_ratio = None
    for s in range(3000):
        if s == 1500:                                     # continuity snapshot mid-fall
            rho1 = np.abs(psi) ** 2
            psi2 = step(psi.copy())
            rho2 = np.abs(psi2) ** 2
            pm = 0.5 * (psi + psi2)
            gx, gy = spectral_grad(pm)
            jx = np.imag(np.conj(pm) * gx)
            jy = np.imag(np.conj(pm) * gy)
            divx, _ = spectral_grad(jx)
            _, divy = spectral_grad(jy)
            resid = (rho2 - rho1) / dt + divx + divy
            res_ratio = float(np.linalg.norm(resid) /
                              np.linalg.norm((rho2 - rho1) / dt))
        psi = step(psi)
        if s % 25 == 0:
            rho = np.abs(psi) ** 2
            gx, gy = spectral_grad(psi)
            jx = np.imag(np.conj(psi) * gx)
            ts.append(s * dt)
            xbar.append(float((rho * xx2).sum() / rho.sum()))
            vbar.append(float(jx.sum() / rho.sum()))
            fbar.append(float(-(rho * dVx).sum() / rho.sum()))
    R.append(check("F2", res_ratio is not None and res_ratio < 0.05,
                   "continuity d(rho)/dt + div j = 0 mid-fall: residual %.4f of the "
                   "flow term - probability is a locally conserved fluid; it flows "
                   "toward the crowd, it never teleports" % res_ratio))

    ts = np.array(ts)
    xbar, vbar, fbar = np.array(xbar), np.array(vbar), np.array(fbar)
    dxdt = np.gradient(xbar, ts)
    dvdt = np.gradient(vbar, ts)
    m_in = slice(2, -2)
    ratio_v = float(np.dot(dxdt[m_in], vbar[m_in]) / np.dot(vbar[m_in], vbar[m_in]))
    ratio_a = float(np.dot(dvdt[m_in], fbar[m_in]) / np.dot(fbar[m_in], fbar[m_in]))
    R.append(check("F3", abs(ratio_v - 1) < 0.02 and abs(ratio_a - 1) < 0.05,
                   "Euler in fluid variables: d<x>/dt = current/density (ratio %.3f) and "
                   "d<v>/dt = congestion force (ratio %.3f) - gravity ACCELERATES the "
                   "probability fluid; W1's phase tilt is the Madelung flow, measured" %
                   (ratio_v, ratio_a)))

    # F4: drift drags waves - u +/- c from the full moving-medium wave equation
    def drift_run(u0):
        Nx, dxg, dtg, c = 2048, 1.0, 0.1, 1.0
        x = np.arange(Nx) * dxg
        phi = np.exp(-((x - 1024.0) ** 2) / (2 * 10.0 ** 2))
        prev = phi.copy()
        u = np.full(Nx, u0)
        def Dx(f):
            return (np.roll(f, -1) - np.roll(f, 1)) / (2 * dxg)
        def Dxx(f):
            return (np.roll(f, -1) - 2 * f + np.roll(f, 1)) / dxg ** 2
        snaps = {}
        for s in range(3001):
            t = s * dtg
            if s in (1500, 3000):
                snaps[t] = phi.copy()
            nxt = (2 * phi - prev + dtg ** 2 * (c ** 2 - u ** 2) * Dxx(phi)
                   - 2 * u * dtg * (Dx(phi) - Dx(prev)))
            prev, phi = phi, nxt
        pk = {}
        for t, f in snaps.items():
            e = f ** 2
            pk[t] = (float(np.argmax(e[1124:1904]) + 1124), float(np.argmax(e[144:924]) + 144))
        vr = (pk[300.0][0] - pk[150.0][0]) / 150.0
        vl = (pk[300.0][1] - pk[150.0][1]) / 150.0
        return vr, vl

    vr, vl = drift_run(0.3)
    vr0, vl0 = drift_run(0.0)
    R.append(check("F4", abs(vr - 1.3) < 0.05 and abs(vl + 0.7) < 0.05
                   and abs(vr0 - 1.0) < 0.03 and abs(vl0 + 1.0) < 0.03,
                   "drifting medium u=0.3: wave speeds %.2f / %.2f (u+c and u-c; control "
                   "u=0: %.2f / %.2f) - the fabric's FLUX drags waves: the Sagnac "
                   "asymmetry = the off-diagonal metric term = frame dragging's seed" %
                   (vr, vl, vr0, vl0)))

    # F5: supersonic drift = a one-way membrane (the dumb hole).
    # Instrument note: the naive second-order discretization is unstable where
    # |u| > c, so this scout transports the out-going characteristic family at
    # its local speed u - c (conservative upwind). That u +/- c IS the medium's
    # wave speed was MEASURED from the full wave equation in F4 - the two
    # scouts carry the claim together.
    def hole_run(x_launch):
        Nx, dxg, dtg = 3000, 1.0, 0.2
        x = np.arange(Nx) * dxg
        u = 0.5 + 0.45 * (1 + np.tanh((x - 1500.0) / 15.0))     # 0.5 -> 1.4, horizon u=c
        a = u - 1.0                                             # out-going family speed
        a_f = 0.5 * (a + np.roll(a, -1))                        # interface speeds
        ap = np.maximum(a_f, 0.0)
        am = np.minimum(a_f, 0.0)
        l = np.exp(-((x - x_launch) ** 2) / (2 * 10.0 ** 2))
        min_x = x_launch
        probe_amp = 0.0
        for _ in range(8000):
            F = ap * l + am * np.roll(l, -1)                    # flux at i+1/2
            l = l - dtg / dxg * (F - np.roll(F, 1))
            l[:6] = 0.0
            l[-6:] = 0.0
            live = np.where(l > 0.02)[0]
            if len(live):
                min_x = min(min_x, float(live[0]))
            probe_amp = max(probe_amp, float(l[400]))
        return min_x, probe_amp

    minx_in, probe_in = hole_run(2000.0)
    minx_out, probe_out = hole_run(800.0)
    R.append(check("F5", minx_in > 1450 and minx_out < 500 and probe_in < 0.05 * probe_out,
                   "launch INSIDE the supersonic region: leftmost reach %.0f (horizon at "
                   "1500) and outside-probe amplitude %.1e vs the outside-launch control "
                   "(reach %.0f, probe %.1e) - where the drift beats c, nothing swims "
                   "back out: a one-way membrane with NOTHING frozen (the dumb hole)" %
                   (minx_in, probe_in, minx_out, probe_out)))

    print()
    print("FLU: %s (%d checks)" % ("ALL PASS" if all(R) else "FAILURES PRESENT", len(R)))
    return all(R)


if __name__ == "__main__":
    main()
