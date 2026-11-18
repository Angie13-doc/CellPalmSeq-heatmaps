"""Replace the paged heatmap (150 columns at a time) with one continuous heatmap.

Each page keeps its own controls, text, search, ranking, colour options and
exports. Only the drawing code changes: all selected columns sit in one strip
that scrolls sideways, a summary band above it shows the whole selection
(click or drag to jump), and "Fit current selection" scales to every selected
column. Exports now cover the whole selection rather than one page.

Works for BrainPalmSeq2026_* and CellPalmSeq2026_* pages (same original
template). Run from the repository root:

    python3 tools/apply_continuous_heatmap.py
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = open(os.path.join(HERE, "continuous_heatmap_engine.js"), encoding="utf-8").read()

CSS = """
/* Continuous heatmap with summary band */
#bps-compare .plot-scroll canvas.canvas{position:sticky;left:0}
#bps-compare .bps-spacer{height:1px;margin-top:-1px;pointer-events:none}
#bps-compare .bps-overview{margin:2px 0 8px}
#bps-compare .bps-overview[hidden]{display:none}
#bps-compare .bps-ov-head{display:flex;justify-content:space-between;gap:4px 10px;flex-wrap:wrap;font-size:11px;color:#5e6d7b;margin-bottom:3px}
#bps-compare .bps-ov-head strong{color:#263649}
#bps-compare .bps-ov-range{font-variant-numeric:tabular-nums}
#bps-compare .bps-ov{display:block;width:100%;height:72px;border:1px solid #dfe5ed;cursor:pointer;touch-action:none}
#bps-compare .bps-ov:focus-visible{outline:2px solid #336b9c;outline-offset:2px}
#bps-compare .bps-ov-nav{display:inline-flex;align-items:center;gap:6px}
#bps-compare .bps-ov-nav button{font-size:11px;padding:2px 7px;min-height:0;cursor:pointer;background:#f2f6fa}
#bps-compare .bps-ov-nav button:disabled{opacity:.4;cursor:default}
"""

OVERVIEW_HTML = (
    '<div class="bps-overview" hidden><div class="bps-ov-head"><span><strong>Whole selection</strong>'
    ' · click, drag or use the arrow keys to jump; each line shows the highest value among the columns it covers</span>'
    '<span class="bps-ov-nav"><button type="button" class="bps-ov-left" aria-label="Scroll heatmap left">◀ Left</button>'
    '<span class="bps-ov-range"></span>'
    '<button type="button" class="bps-ov-right" aria-label="Scroll heatmap right">Right ▶</button></span></div>'
    '<canvas class="bps-ov" role="slider" tabindex="0" aria-label="Heatmap position. Arrow keys, Page Up, Page Down, '
    'Home and End move through the columns; click or drag to jump"></canvas></div>'
)
PAGE_NAV_HTML = ('<div class="heatmap-navigation"><button type="button" class="page-prev">◀ Previous 150</button>'
                 '<span class="page-status"></span><button type="button" class="page-next">Next 150 ▶</button></div>')
SCROLL_NAV_HTML = ('<div class="heatmap-navigation" aria-label="Horizontal heatmap navigation"><button type="button" '
                   'class="scroll-left" aria-label="Scroll heatmap left">◀ Left</button><input type="range" '
                   'class="scroll-position" min="0" max="1000" value="0" step="1" aria-label="Heatmap horizontal position">'
                   '<button type="button" class="scroll-right" aria-label="Scroll heatmap right">Right ▶</button></div>\n')
PAGE_JS = ("$('.page-prev').addEventListener('click',()=>{page=Math.max(0,page-1);render()});\n"
           "$('.page-next').addEventListener('click',()=>{page++;render()});\n")
SCROLL_JS = re.compile(r"const scrollLeftBtn=\$\('\.scroll-left'\).*?window\.addEventListener\('resize',syncScrollControls\);\n", re.S)
PAGING = re.compile(r"[ \t]*const pageCount=Math\.max\(1,Math\.ceil\(allCols\.length/pageSize\)\);\n.*?"
                    r"[ \t]*\$\('\.page-prev'\)\.disabled=page===0;\$\('\.page-next'\)\.disabled=page>=pageCount-1;\n", re.S)
DRAWING = re.compile(r"[ \t]*const boundaries=\[\];let count=0;.*?layout=\{n,genes,cols,positions,lookup,width,height\};syncScrollControls\(\);\}\n", re.S)
HOVER_OLD = re.compile(r"[ \t]*const x=\(clientX-rect\.left\)\*layout\.width/rect\.width,y=\(clientY-rect\.top\)\*layout\.height/rect\.height,row=Math\.floor\(\(y-top\)/rh\);\n"
                       r"[ \t]*const col=layout\.positions\.findIndex\(px=>x>=px&&x<px\+cw\);")
HOVER_NEW = (" const vx=clientX-rect.left,x=vx<left?-1:vx+scroll.scrollLeft,y=clientY-rect.top,row=Math.floor((y-top)/rh);\n"
             " const col=x<0?-1:bpsColAt(x);")
CANVAS_CLOSE = re.compile(r'(<div class="plot-scroll"><canvas class="canvas"[^>]*></canvas>)')

# Wording that described paging or the removed slider/buttons.
TEXT_EDITS = [
    (" All lines remain available, with horizontal paging.", " All matches appear in one continuous heatmap."),
    ("Use the horizontal slider or Left/Right buttons to navigate wide heatmaps without browser back gestures. ",
     "Scroll sideways through wide heatmaps, or click or drag the summary band above the heatmap to jump. "),
    (" before paging, not statistical enrichment.", ", not statistical enrichment."),
    (" across all matching populations, including other pages.", " across all matching populations."),
]
# Cell pages: the SVG/PNG export coloured tiles from original values even in log mode.
SVG_COLOUR_EDITS = [
    ("const fraction=high>0?r.Expression/high:0;", "const cval=bpsColourOf(r),fraction=high>0?cval/high:0;"),
    ("const color=Number.isFinite(r.Expression)?palette[index]:'#333333';", "const color=Number.isFinite(cval)?palette[index]:'#333333';"),
]


def once(text, old, new, path, what):
    n = len(old.findall(text)) if hasattr(old, "findall") else text.count(old)
    if n != 1:
        sys.exit(f"{path}: expected exactly one {what}, found {n}")
    return old.sub(lambda _m: new, text) if hasattr(old, "sub") else text.replace(old, new)


def convert(path):
    t = open(path, encoding="utf-8").read()
    if "bps-overview" in t:
        sys.exit(f"{path}: already converted")
    t = once(t, "</style>", CSS + "</style>", path, "</style>")
    t = once(t, PAGE_NAV_HTML, OVERVIEW_HTML, path, "page navigation")
    t = once(t, SCROLL_NAV_HTML, "", path, "scroll navigation")
    if len(CANVAS_CLOSE.findall(t)) != 1:
        sys.exit(f"{path}: expected exactly one heatmap canvas")
    t = CANVAS_CLOSE.sub(lambda m: m.group(1) + '<div class="bps-spacer"></div>', t)
    t = once(t, PAGE_JS, "", path, "page buttons")
    t = once(t, PAGING, " const cols=allCols;const visibleGroups=rankedGroups.filter(g=>g.cells.length);\n", path, "paging")

    m = DRAWING.search(t)
    if not m:
        sys.exit(f"{path}: drawing block not found")
    block = m.group(0)
    colour = "colourValue(r)" if "colourValue(r)/high" in block else "Number(r.Expression)"
    label = "shortPopulationLabel(c)" if "shortPopulationLabel(c)" in block else "c"
    t = once(t, DRAWING,
             " bpsUpdate({cols,visibleGroups,genes,high,colour:r=>%s,label:c=>%s});}\n" % (colour, label),
             path, "drawing block")
    t, k = re.subn(r" \('\+n\+' displayed\)  · '", " · '", t)
    if k != 1:
        sys.exit(f"{path}: expected one '(n displayed)' summary, found {k}")
    t = once(t, HOVER_OLD, HOVER_NEW, path, "hover mapping")
    t = once(t, SCROLL_JS, ENGINE + "\n", path, "scroll controls")
    if "function cpsFigureSVG" in t:
        for old, new in SVG_COLOUR_EDITS:
            t = once(t, old, new, path, "SVG colour")
    for old, new in TEXT_EDITS:
        t = t.replace(old, new)
    for leftover in ("page-prev", "page-next", "scroll-left", "pageSize)", "Previous 150"):
        if leftover in t:
            sys.exit(f"{path}: leftover {leftover!r}")
    open(path, "w", encoding="utf-8").write(t)


def main():
    pages = sorted(p for pat in ("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html", "CellPalmSeq2026_*/CellPalmSeq2026_*.html")
                   for p in glob.glob(pat) if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for p in pages:
        convert(p)
        print("converted", p)
    print(len(pages), "pages converted")


if __name__ == "__main__":
    main()
