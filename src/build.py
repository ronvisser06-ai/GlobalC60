"""Builds public/index.html from src/index.src.html, the illustrations and the logo paths.
Run from the repository root:  python3 src/build.py"""
import json, math, re, pathlib

here = pathlib.Path(__file__).parent
src = (here / "index.src.html").read_text()
ill = json.loads((here / "illustrations.json").read_text())
logo_inner = (here / "brand" / "logo_inner.txt").read_text()
li = (here / "li.txt").read_text().strip()

def logo(cls="logo", label="GlobalC60 Recovery"):
    return f'<svg class="{cls}" viewBox="0 0 1000 449" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{logo_inner}</svg>'

def lattice(pid):
    s = 22.0
    h = math.sqrt(3) * s
    d = (f"M0 {h/2:.2f} L{s/2:.2f} 0 L{1.5*s:.2f} 0 L{2*s:.2f} {h/2:.2f} L{1.5*s:.2f} {h:.2f} L{s/2:.2f} {h:.2f} Z "
         f"M{2*s:.2f} {h/2:.2f} L{3*s:.2f} {h/2:.2f}")
    return (f'<svg class="hero-lattice" aria-hidden="true" focusable="false"><defs>'
            f'<pattern id="{pid}" width="{3*s:.2f}" height="{h:.2f}" patternUnits="userSpaceOnUse"><path d="{d}"/></pattern>'
            f'</defs><rect width="100%" height="100%" fill="url(#{pid})"/></svg>')

def arrow(x, y, direction, cls):
    if direction == "r":
        pts = f"{x},{y} {x-9},{y-6} {x-9},{y+6}"
    elif direction == "u":
        pts = f"{x},{y} {x-6},{y+9} {x+6},{y+9}"
    else:
        pts = f"{x},{y} {x-6},{y-9} {x+6},{y-9}"
    return f'<polygon class="{cls}" points="{pts}"/>'

def diagram():
    parts = []
    # stack
    parts.append('<rect class="stackbody" x="34" y="120" width="54" height="206" rx="3"/>')
    parts.append('<rect class="stackbody" x="26" y="326" width="70" height="14" rx="2"/>')
    parts.append('<text x="61" y="104" text-anchor="middle" class="strong">YOUR STACK</text>')
    # flue gas to unit
    parts.append('<path class="gas" d="M88 236 H196"/>')
    parts.append(arrow(206, 236, "r", "gasfill"))
    parts.append('<text x="146" y="222" text-anchor="middle">CO₂ IN</text>')
    parts.append('<text x="146" y="260" text-anchor="middle">FLUE GAS</text>')
    # unit
    parts.append('<rect class="unit" x="208" y="164" width="150" height="144" rx="8"/>')
    # lattice inside unit (small hex row) clipped visually by drawing inside bounds
    hexes = []
    s = 11; h = math.sqrt(3) * s
    for row in range(3):
        for col in range(4):
            cx = 238 + col * 1.5 * s * 2 + (s * 1.5 if row % 2 else 0)
            cy = 262 + row * h / 2 * 1.0
            if cx + s > 350: continue
            pts = " ".join(f"{cx + s*math.cos(math.radians(a)):.1f},{cy + s*math.sin(math.radians(a)):.1f}" for a in range(0, 360, 60))
            hexes.append(f'<polygon class="unit-lattice" points="{pts}"/>')
    parts.extend(hexes)
    parts.append('<text x="283" y="196" text-anchor="middle" class="strong">GLOBAL C60</text>')
    parts.append('<text x="283" y="214" text-anchor="middle" class="strong">UNIT</text>')
    parts.append('<text x="283" y="232" text-anchor="middle">ON YOUR SITE</text>')
    parts.append('<circle class="act" cx="208" cy="236" r="6"/>')
    # treated gas up
    parts.append('<path class="gas-thin" d="M318 164 V78"/>')
    parts.append(arrow(318, 66, "u", "gasfill"))
    parts.append('<text x="332" y="92">TREATED GAS</text>')
    # product out
    parts.append('<path class="prod" d="M358 236 H428"/>')
    parts.append(arrow(438, 236, "r", "prodfill"))
    for (x, y, r) in [(462, 228, 11), (478, 240, 9), (464, 248, 8), (486, 224, 7), (451, 243, 6)]:
        parts.append(f'<circle class="particle" cx="{x}" cy="{y}" r="{r}"/>')
    parts.append('<text x="468" y="206" text-anchor="middle" class="strong">SOLID CARBON</text>')
    parts.append('<text x="468" y="276" text-anchor="middle">SOLD TO</text>')
    parts.append('<text x="468" y="292" text-anchor="middle">INDUSTRY</text>')
    # report
    parts.append('<path class="rep" d="M283 308 V346 H428"/>')
    parts.append(arrow(438, 346, "r", "repfill"))
    parts.append('<rect class="doc" x="446" y="322" width="38" height="48" rx="3"/>')
    for i, w in enumerate((24, 24, 16)):
        parts.append(f'<line class="docline" x1="453" y1="{336+i*10}" x2="{453+w}" y2="{336+i*10}"/>')
    parts.append('<text x="430" y="332" text-anchor="end">MONTHLY</text>')
    parts.append('<text x="430" y="370" text-anchor="end">CO₂ REPORT</text>')
    return ('<svg class="dg" viewBox="0 0 520 390" role="img" aria-label="CO2 in flue gas flows from your stack into a Global C60 unit on your site. '
            'Out come treated gas, solid carbon sold to industry, and a monthly CO2 report." xmlns="http://www.w3.org/2000/svg">'
            + "".join(parts) + "</svg>")

out = (src.replace("{{LOGO}}", logo())
          .replace("{{LOGO_FOOT}}", logo(label="GlobalC60 Recovery"))
          .replace("{{LATTICE}}", lattice("lat1"))
          .replace("{{LATTICE2}}", lattice("lat2"))
          .replace("{{DIAGRAM}}", diagram())
          .replace("{{CB}}", ill["cb"]).replace("{{SWCNT}}", ill["swcnt"])
          .replace("{{MWCNT}}", ill["mwcnt"]).replace("{{C60}}", ill["c60"])
          .replace("{{LI}}", li))
assert "{{" not in out, re.findall(r"\{\{\w+\}\}", out)
public = here.parent / "public"
public.mkdir(exist_ok=True)
(public / "index.html").write_text(out)

print("public/index.html", len(out), "bytes")
