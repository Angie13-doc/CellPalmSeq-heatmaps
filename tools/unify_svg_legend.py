"""Make CellPalmSeq's SVG/PNG figure export match BrainPalmSeq's.

- Scale bar: the existing smooth-gradient bar, without its grey outline.
- Caption: "Expression (unit)" as on BrainPalmSeq (was "Colour: original
  unit"); with the log scale on it stays "Colour: log2(unit + 1)", as on
  BrainPalmSeq. The on-page legend is unchanged.
- Title: "CellPalmSeq: <dataset>" from the page's file name, in a 44 px
  header as on BrainPalmSeq. The figure widens to fit it.

Run from the repository root:  python3 tools/unify_svg_legend.py
"""
import glob
import sys

EDITS = [
    ("function cpsFigureSVG(){",
     "// SVG caption: the legend's original \"Expression (unit)\" text, read before the page rewrites it.\n"
     "const cpsLegendBase=($('.legend span:first-child')?.textContent||'Expression').trim();\n"
     "function cpsFigureSVG(){"),
    (" const legendText=$('.legend span:first-child')?.textContent||'Expression';",
     " const legendText=$('#colour-transform-select')?.value==='log'?($('.legend span:first-child')?.textContent||cpsLegendBase):cpsLegendBase;\n"
     " const head=44,title='CellPalmSeq: '+(location.pathname.split('/').filter(Boolean).pop()||'').replace(/\\.html$/,'').replace(/^CellPalmSeq2026_/,'');"),
    (" const figW=Math.ceil(Math.max(width,lx+legendW+right)),ly=height+16,ry=ly+8,labelY=ry+12+12,fullHeight=Math.ceil(labelY+10);",
     " const figW=Math.ceil(Math.max(width,lx+legendW+right,48+measureText(title,'bold 16px Arial'))),ly=height+16,ry=ly+8,labelY=ry+12+12,fullHeight=Math.ceil(labelY+10)+head;"),
    (" if(!transparent)parts.push(`<rect width=\"100%\" height=\"100%\" fill=\"#ffffff\"/>`);\n",
     " if(!transparent)parts.push(`<rect width=\"100%\" height=\"100%\" fill=\"#ffffff\"/>`);\n"
     " parts.push(`<text x=\"24\" y=\"25\" font-family=\"Arial,sans-serif\" font-size=\"16\" font-weight=\"bold\" fill=\"#263649\">${esc(title.slice(0,125))}</text>`,`<g transform=\"translate(0 ${head})\">`);\n"),
    (' fill="url(#cps-legend-gradient)" stroke="#9aa9b6" stroke-width=".5"/>', ' fill="url(#cps-legend-gradient)"/>'),
    (" parts.push('</svg>');return {svg:parts.join(''),width:figW,height:fullHeight};",
     " parts.push('</g>','</svg>');return {svg:parts.join(''),width:figW,height:fullHeight};"),
]


def main():
    pages = sorted(p for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html") if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path in pages:
        t = open(path, encoding="utf-8").read()
        if "cpsLegendBase" in t:
            sys.exit(f"{path}: already updated")
        for old, new in EDITS:
            if t.count(old) != 1:
                sys.exit(f"{path}: expected exactly one of {old[:70]!r}, found {t.count(old)}")
            t = t.replace(old, new)
        open(path, "w", encoding="utf-8").write(t)
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
