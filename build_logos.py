"""
Build clean SVG versions of the three Aetas Partners logo lockups:
  1. aetas-mark.svg          — three interlocking rings only (Borromean)
  2. aetas-horizontal.svg    — mark + AETAS / PARTNERS stacked right
  3. aetas-stacked.svg       — mark above + AETAS PARTNERS on one line

The wordmark is rendered as PATHS extracted from Poppins-Medium so the
output renders identically anywhere, no font file required at view time.
"""
from __future__ import annotations
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

# ---------- brand ----------
NAVY = "#0d2c6c"
TURQ = "#00aabb"
TEAL = "#005357"

# ---------- ring geometry ----------
# Verified from pixel inspection of aetas_partners_png.png (300x300)
RINGS = {
    "navy": dict(cx=152, cy=102, r=92, color=NAVY),
    "turq": dict(cx=95,  cy=193, r=92, color=TURQ),
    "teal": dict(cx=198, cy=197, r=92, color=TEAL),
}
STROKE = 14

# ---------- font ----------
FONT_PATH = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
_font = TTFont(FONT_PATH)
_cmap = _font.getBestCmap()
_glyphs = _font.getGlyphSet()
UPEM = _font["head"].unitsPerEm           # 1000
CAP_HEIGHT = _font["OS/2"].sCapHeight     # 697


def glyph(ch):
    """Return (svg_d, advance_width) for one character (font units, y-up)."""
    if ch == " ":
        return None, _font["hmtx"].metrics[_cmap[ord(" ")]][0]
    gid = _cmap[ord(ch)]
    pen = SVGPathPen(_glyphs)
    _glyphs[gid].draw(pen)
    return pen.getCommands(), _font["hmtx"].metrics[gid][0]


def intersections(A, B):
    dx, dy = B["cx"] - A["cx"], B["cy"] - A["cy"]
    d = math.hypot(dx, dy)
    a = d / 2
    h = math.sqrt(A["r"] ** 2 - a * a)
    mx, my = A["cx"] + a * dx / d, A["cy"] + a * dy / d
    ox, oy = -dy / d * h, dx / d * h
    return [(mx + ox, my + oy), (mx - ox, my - oy)]


def mark_inner(*, navy_override: str | None = None) -> str:
    """Return the inner SVG markup for the Borromean rings (no <svg> wrapper).
    Pass navy_override='#ffffff' for use on dark navy backgrounds."""
    navy_colour = navy_override or NAVY
    # z-order: teal → navy → turq
    its = intersections(RINGS["turq"], RINGS["teal"])
    teal = RINGS["teal"]
    half_span = 10
    patch_arcs = []
    for (x, y) in its:
        ang = math.degrees(math.atan2(y - teal["cy"], x - teal["cx"]))
        a1, a2 = math.radians(ang - half_span), math.radians(ang + half_span)
        p1 = (teal["cx"] + teal["r"] * math.cos(a1), teal["cy"] + teal["r"] * math.sin(a1))
        p2 = (teal["cx"] + teal["r"] * math.cos(a2), teal["cy"] + teal["r"] * math.sin(a2))
        patch_arcs.append(f'M {p1[0]:.2f} {p1[1]:.2f} A {teal["r"]} {teal["r"]} 0 0 1 {p2[0]:.2f} {p2[1]:.2f}')

    lines = []
    lines.append(f'<g fill="none" stroke-width="{STROKE}" stroke-linecap="round">')
    for k in ("teal", "navy", "turq"):
        r = RINGS[k]
        c = navy_colour if k == "navy" else r["color"]
        lines.append(f'  <circle cx="{r["cx"]}" cy="{r["cy"]}" r="{r["r"]}" stroke="{c}"/>')
    for d in patch_arcs:
        lines.append(f'  <path d="{d}" stroke="{TEAL}"/>')
    lines.append("</g>")
    return "\n".join(lines)


def wordmark_path(text: str, *, tracking: int = 70) -> tuple[str, float]:
    """Return (combined-path-d, width-in-font-units) for `text`.
    Path is given in font units, y-DOWN (already flipped for SVG)."""
    parts = []
    x = 0.0
    for ch in text:
        d, adv = glyph(ch)
        if d:
            # Translate to (x, 0) then flip y so glyph sits on baseline at y=0
            # SVG can transform a path indirectly — easiest is to compose: use
            # a wrapping <g transform="translate(x 0) scale(1 -1)">. We'll emit
            # the path text and let caller wrap it.
            parts.append((x, d))
        x += adv + tracking
    total = x - tracking if text and text[-1] != " " else x
    return parts, total


def wordmark_svg(text: str, *, tracking: int = 70, fill=NAVY) -> tuple[str, float, float]:
    """Return (markup, width_in_font_units, cap_height_in_font_units)."""
    parts, w = wordmark_path(text, tracking=tracking)
    # Each glyph: wrap in transform that translates to its x and flips y so
    # baseline sits at y=0 and the letter extends upward to y=-CAP_HEIGHT.
    # We invert: place at y=CAP_HEIGHT then scale(1,-1) to put baseline at y=CAP_HEIGHT.
    inner = []
    for tx, d in parts:
        inner.append(f'  <path d="{d}" transform="translate({tx:.2f} {CAP_HEIGHT}) scale(1 -1)" fill="{fill}"/>')
    body = "\n".join(inner)
    return body, w, CAP_HEIGHT


# ============== 1. MARK ONLY ==============
def build_mark():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" role="img" aria-label="Aetas Partners">
  <title>Aetas Partners</title>
{mark_inner()}
</svg>
'''
    with open("aetas-mark.svg", "w") as f:
        f.write(svg)
    return svg


def build_mark_reverse():
    """Mark with white navy ring for use on navy/dark backgrounds."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" role="img" aria-label="Aetas Partners">
  <title>Aetas Partners</title>
{mark_inner(navy_override="#ffffff")}
</svg>
'''
    with open("aetas-mark-reverse.svg", "w") as f:
        f.write(svg)
    return svg


# ============== 2. HORIZONTAL LOCKUP ==============
def build_horizontal():
    """Mark on left, AETAS / PARTNERS stacked on right.
    The original PNG is 1247x317 with the mark filling roughly 0-300 horizontally
    and the text filling roughly 380-1247."""

    # Render the text in the font's native units, then we'll place it scaled.
    line1_body, line1_w, _ = wordmark_svg("AETAS",    tracking=70)
    line2_body, line2_w, _ = wordmark_svg("PARTNERS", tracking=70)

    # Both lines should be the same height (cap height). The text should appear
    # at the same scale on both lines. We want PARTNERS (the longer word) to fit
    # the available text width; AETAS will be shorter and left-aligned with it.

    # Target geometry inside viewBox 1240 x 320:
    #   mark: x = 10..310 (300 wide)
    #   gap : 60
    #   text: x = 370..1230 (860 wide, two lines)
    MARK_SIZE = 300
    GAP = 60
    TEXT_X = MARK_SIZE + GAP + 10  # 370
    TEXT_W = 860
    VIEW_W = TEXT_X + TEXT_W + 10  # 1240
    VIEW_H = 320

    # Scale so that PARTNERS fits TEXT_W exactly
    scale_p = TEXT_W / line2_w
    # In horizontal lockup we want same scale on both lines (consistent letter height)
    # PARTNERS sets the scale because it's the longer word
    SCALE = scale_p

    line_h = CAP_HEIGHT * SCALE        # height of each line of caps (~130)
    leading = line_h * 0.18            # small gap between lines
    total_text_h = 2 * line_h + leading
    text_top = (VIEW_H - total_text_h) / 2
    line1_y = text_top
    line2_y = text_top + line_h + leading

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W} {VIEW_H}" role="img" aria-label="Aetas Partners">
  <title>Aetas Partners</title>
  <!-- Mark -->
  <g transform="translate(10 {(VIEW_H - MARK_SIZE) / 2})">
{mark_inner()}
  </g>
  <!-- AETAS -->
  <g transform="translate({TEXT_X} {line1_y}) scale({SCALE:.6f})">
{line1_body}
  </g>
  <!-- PARTNERS -->
  <g transform="translate({TEXT_X} {line2_y}) scale({SCALE:.6f})">
{line2_body}
  </g>
</svg>
'''
    with open("aetas-horizontal.svg", "w") as f:
        f.write(svg)
    return svg


# ============== 3. STACKED LOCKUP ==============
def build_stacked():
    """Mark on top, AETAS PARTNERS on a single line beneath."""
    body, total_w, _ = wordmark_svg("AETAS PARTNERS", tracking=70)
    # Original stacked PNG is 918x408 — roughly square-ish with text below
    # Target viewBox: width determined by text, height = mark_size + gap + text_h
    MARK_SIZE = 300
    GAP = 40
    # We'd like the text to be roughly the same width as the mark sits centred above.
    # Pick a scale that gives the wordmark a width close to ~880.
    TEXT_TARGET_W = 880
    SCALE = TEXT_TARGET_W / total_w
    actual_text_w = total_w * SCALE
    text_h = CAP_HEIGHT * SCALE
    VIEW_W = max(MARK_SIZE, actual_text_w) + 20
    VIEW_H = MARK_SIZE + GAP + text_h + 20

    mark_x = (VIEW_W - MARK_SIZE) / 2
    text_x = (VIEW_W - actual_text_w) / 2
    text_y = MARK_SIZE + GAP

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W:.2f} {VIEW_H:.2f}" role="img" aria-label="Aetas Partners">
  <title>Aetas Partners</title>
  <!-- Mark -->
  <g transform="translate({mark_x:.2f} 10)">
{mark_inner()}
  </g>
  <!-- AETAS PARTNERS -->
  <g transform="translate({text_x:.2f} {text_y:.2f}) scale({SCALE:.6f})">
{body}
  </g>
</svg>
'''
    with open("aetas-stacked.svg", "w") as f:
        f.write(svg)
    return svg


def build_horizontal_reverse():
    """White wordmark for use on dark backgrounds (header on navy, footer, etc.)."""
    line1_body, line1_w, _ = wordmark_svg("AETAS",    tracking=70, fill="#ffffff")
    line2_body, line2_w, _ = wordmark_svg("PARTNERS", tracking=70, fill="#ffffff")
    MARK_SIZE = 300; GAP = 60; TEXT_X = MARK_SIZE + GAP + 10; TEXT_W = 860
    VIEW_W = TEXT_X + TEXT_W + 10; VIEW_H = 320
    SCALE = TEXT_W / line2_w
    line_h = CAP_HEIGHT * SCALE
    leading = line_h * 0.18
    total_text_h = 2 * line_h + leading
    text_top = (VIEW_H - total_text_h) / 2
    line1_y = text_top
    line2_y = text_top + line_h + leading

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W} {VIEW_H}" role="img" aria-label="Aetas Partners">
  <title>Aetas Partners</title>
  <g transform="translate(10 {(VIEW_H - MARK_SIZE) / 2})">
{mark_inner(navy_override="#ffffff")}
  </g>
  <g transform="translate({TEXT_X} {line1_y}) scale({SCALE:.6f})">
{line1_body}
  </g>
  <g transform="translate({TEXT_X} {line2_y}) scale({SCALE:.6f})">
{line2_body}
  </g>
</svg>
'''
    with open("aetas-horizontal-reverse.svg", "w") as f:
        f.write(svg)


def build_stacked_reverse():
    body, total_w, _ = wordmark_svg("AETAS PARTNERS", tracking=70, fill="#ffffff")
    MARK_SIZE = 300; GAP = 40; TEXT_TARGET_W = 880
    SCALE = TEXT_TARGET_W / total_w
    actual_text_w = total_w * SCALE
    text_h = CAP_HEIGHT * SCALE
    VIEW_W = max(MARK_SIZE, actual_text_w) + 20
    VIEW_H = MARK_SIZE + GAP + text_h + 20
    mark_x = (VIEW_W - MARK_SIZE) / 2
    text_x = (VIEW_W - actual_text_w) / 2
    text_y = MARK_SIZE + GAP

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W:.2f} {VIEW_H:.2f}" role="img" aria-label="Aetas Partners">
  <title>Aetas Partners</title>
  <g transform="translate({mark_x:.2f} 10)">
{mark_inner(navy_override="#ffffff")}
  </g>
  <g transform="translate({text_x:.2f} {text_y:.2f}) scale({SCALE:.6f})">
{body}
  </g>
</svg>
'''
    with open("aetas-stacked-reverse.svg", "w") as f:
        f.write(svg)


if __name__ == "__main__":
    build_mark()
    build_mark_reverse()
    build_horizontal()
    build_stacked()
    build_horizontal_reverse()
    build_stacked_reverse()
    print("Built six SVG variants: mark, mark-reverse, horizontal, stacked, "
          "horizontal-reverse, stacked-reverse")
