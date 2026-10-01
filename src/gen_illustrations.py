"""Generates the product illustrations as inline SVG strings.
Colours come from CSS classes defined in the page, so both themes work.
  .ln   front edges        .lf  back edges (faint)
  .at   atoms (front)      .pf  pentagon fill (green tint)
  .pc   carbon black particle fill   .po particle outline
"""
import math, itertools, random, json

def fmt(v):
    return f"{v:.1f}"

# ---------- C60: truncated icosahedron ----------
def c60_svg(size=240):
    phi = (1 + 5 ** 0.5) / 2
    base = [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]
    pts = set()
    for b in base:
        for signs in itertools.product([1, -1], repeat=3):
            v = tuple(b[i] * signs[i] for i in range(3))
            for k in range(3):  # cyclic permutations (even)
                p = (v[k % 3], v[(k + 1) % 3], v[(k + 2) % 3])
                pts.add(tuple(round(c, 6) for c in p))
    pts = list(pts)
    assert len(pts) == 60, len(pts)
    edges = [(i, j) for i in range(60) for j in range(i + 1, 60)
             if abs(math.dist(pts[i], pts[j]) - 2) < 1e-4]
    assert len(edges) == 90
    # rotation
    ax, ay = math.radians(18), math.radians(28)
    def rot(p):
        x, y, z = p
        y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
        x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
        return x, y, z
    R = [rot(p) for p in pts]
    r = max(math.sqrt(x * x + y * y + z * z) for x, y, z in R)
    sc = (size / 2 - 14) / r
    P = [(size / 2 + x * sc, size / 2 - y * sc, z) for x, y, z in R]
    # pentagons: find 5-cycles via adjacency
    adj = {i: set() for i in range(60)}
    for i, j in edges:
        adj[i].add(j); adj[j].add(i)
    pents = set()
    for a in range(60):
        for b in adj[a]:
            for c in adj[b] - {a}:
                for d in adj[c] - {a, b}:
                    for e in adj[d] - {a, b, c}:
                        if a in adj[e]:
                            cyc = (a, b, c, d, e)
                            # pentagon check: all edges length 2 & planar-ish: distance a-c ~ 2*phi
                            if abs(math.dist(pts[a], pts[c]) - 2 * 1.618034) < 1e-3:
                                pents.add(tuple(sorted(cyc)) + cyc)
    seen, pent_list = set(), []
    for p in pents:
        key = p[:5]
        if key not in seen:
            seen.add(key); pent_list.append(p[5:])
    assert len(pent_list) == 12, len(pent_list)
    out = []
    # faint back edges first
    for i, j in edges:
        if P[i][2] + P[j][2] < 0:
            out.append(f'<line class="lf" x1="{fmt(P[i][0])}" y1="{fmt(P[i][1])}" x2="{fmt(P[j][0])}" y2="{fmt(P[j][1])}"/>')
    for cyc in pent_list:
        zc = sum(P[k][2] for k in cyc) / 5
        if zc > r * 0.3:
            d = "M" + " L".join(f"{fmt(P[k][0])} {fmt(P[k][1])}" for k in cyc) + "Z"
            out.append(f'<path class="pf" d="{d}"/>')
    for i, j in edges:
        if P[i][2] + P[j][2] >= 0:
            out.append(f'<line class="ln" x1="{fmt(P[i][0])}" y1="{fmt(P[i][1])}" x2="{fmt(P[j][0])}" y2="{fmt(P[j][1])}"/>')
    for x, y, z in P:
        if z > 0:
            out.append(f'<circle class="at" cx="{fmt(x)}" cy="{fmt(y)}" r="2.6"/>')
    return f'<svg viewBox="0 0 {size} {size}" class="illo" role="img" aria-label="Drawing of a C60 fullerene molecule: 60 carbon atoms arranged in 12 pentagons and 20 hexagons">' + "".join(out) + "</svg>"

# ---------- Single-wall nanotube, side view ----------
def swcnt_svg(w=320, h=200, n=12, rows=9):
    Rr = 52
    cx, cy = w / 2, h / 2
    a = 2 * math.pi * Rr / n  # hexagon width along circumference
    bond = a / math.sqrt(3)
    # zigzag-style lattice in (s, x) plane; x along tube axis
    nodes, edges = {}, []
    def node(key, s, x):
        nodes[key] = (s, x)
    # build graphene sheet points
    for col in range(n):
        for row in range(rows):
            s0 = col * a + (a / 2 if row % 2 else 0)
            x0 = row * 1.5 * bond
            node((col, row, 0), s0, x0)
            node((col, row, 1), s0, x0 + bond)
    for col in range(n):
        for row in range(rows):
            edges.append(((col, row, 0), (col, row, 1)))
            if row + 1 < rows:
                # upper node connects to two lower nodes of next row
                if row % 2 == 0:
                    edges.append(((col, row, 1), (col, row + 1, 0)))
                    edges.append(((col, row, 1), ((col - 1) % n, row + 1, 0)))
                else:
                    edges.append(((col, row, 1), (col, row + 1, 0)))
                    edges.append(((col, row, 1), ((col + 1) % n, row + 1, 0)))
    total = (rows - 1) * 1.5 * bond + bond
    tilt = math.radians(-10)
    def proj(s, x):
        th = s / Rr + 0.12
        y = Rr * math.cos(th)
        z = Rr * math.sin(th)
        xx = x - total / 2
        # tilt tube a little
        X = cx + xx * math.cos(tilt) - y * math.sin(tilt) * 0.35
        Y = cy + xx * math.sin(tilt) + y
        return X, Y, z
    P = {k: proj(*v) for k, v in nodes.items()}
    back, front, atoms = [], [], []
    for a_, b_ in edges:
        (x1, y1, z1), (x2, y2, z2) = P[a_], P[b_]
        if abs(x1 - x2) > 60 or abs(y1 - y2) > 60:
            continue
        seg = f'x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"'
        (front if z1 + z2 >= 0 else back).append(f'<line class="{"ln" if z1+z2>=0 else "lf"}" {seg}/>')
    for x, y, z in P.values():
        if z > 0:
            atoms.append(f'<circle class="at" cx="{fmt(x)}" cy="{fmt(y)}" r="2"/>')
    return f'<svg viewBox="0 0 {w} {h}" class="illo" role="img" aria-label="Drawing of a single-wall carbon nanotube: one layer of carbon atoms rolled into a tube">' + "".join(back + front + atoms) + "</svg>"

# ---------- Multi-wall nanotube, end view ----------
def mwcnt_svg(size=240, walls=(26, 44, 62, 80, 98)):
    c = size / 2
    out = []
    for i, r in enumerate(walls):
        out.append(f'<circle class="{"ln" if i==len(walls)-1 else "lr"}" cx="{c}" cy="{c}" r="{r}" fill="none"/>')
        n = max(8, int(2 * math.pi * r / 11))
        off = (i % 2) * math.pi / n
        for k in range(n):
            t = 2 * math.pi * k / n + off
            out.append(f'<circle class="at" cx="{fmt(c + r*math.cos(t))}" cy="{fmt(c + r*math.sin(t))}" r="2"/>')
    out.append(f'<circle class="pf" cx="{c}" cy="{c}" r="8"/>')
    return f'<svg viewBox="0 0 {size} {size}" class="illo" role="img" aria-label="End view of a multi-wall carbon nanotube: several tubes nested inside each other">' + "".join(out) + "</svg>"

# ---------- Carbon black aggregate ----------
def cb_svg(w=320, h=220, seed=7):
    rnd = random.Random(seed)
    parts = [(w / 2, h / 2, 24)]
    tries = 0
    while len(parts) < 17 and tries < 2000:
        tries += 1
        px, py, pr = rnd.choice(parts)
        r = rnd.uniform(15, 24)
        ang = rnd.uniform(0, 2 * math.pi)
        d = (pr + r) * 0.78
        x, y = px + d * math.cos(ang), py + d * math.sin(ang)
        if not (r + 8 < x < w - r - 8 and r + 8 < y < h - r - 8):
            continue
        if any(math.dist((x, y), (qx, qy)) < (r + qr) * 0.62 for qx, qy, qr in parts):
            continue
        parts.append((x, y, r))
    minx = min(x - r for x, y, r in parts); maxx = max(x + r for x, y, r in parts)
    miny = min(y - r for x, y, r in parts); maxy = max(y + r for x, y, r in parts)
    dx, dy = w / 2 - (minx + maxx) / 2, h / 2 - (miny + maxy) / 2
    parts = [(x + dx, y + dy, r) for x, y, r in parts]
    out = []
    for x, y, r in parts:
        out.append(f'<circle class="pc" cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}"/>')
    for x, y, r in parts:
        out.append(f'<circle class="po" cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}"/>')
        # graphitic layer hint: concentric arcs inside each particle
        for f in (0.55,):
            out.append(f'<circle class="lr" cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r*f)}" fill="none"/>')
    return f'<svg viewBox="0 0 {w} {h}" class="illo" role="img" aria-label="Drawing of a carbon black aggregate: small spherical carbon particles fused into a chain">' + "".join(out) + "</svg>"

if __name__ == "__main__":
    data = {"c60": c60_svg(), "swcnt": swcnt_svg(), "mwcnt": mwcnt_svg(), "cb": cb_svg()}
    json.dump(data, open("illustrations.json", "w"))
    for k, v in data.items():
        print(k, len(v))
