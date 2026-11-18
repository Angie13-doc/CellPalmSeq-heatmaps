"""Fix the colour scale bar in SVG/PNG figure exports.

Before: the scale bar's labels could fall outside the exported image (on
BrainPalmSeq the "0" sat below the bottom edge on every export; on narrow
selections the bar, the maximum and the units line ran past the right edge),
and the maximum sat beside the bar while "0" sat below it.

After: the legend (units line, bar, then "0" and the maximum on one line below
the bar, "0" under the bar's left end and the maximum right-aligned under its
right end) gets its own measured space, and the image widens when the legend
is wider than the heatmap. Works on BrainPalmSeq2026_* (bpsFigureExport) and
CellPalmSeq2026_* (cpsFigureSVG) pages. Run from the repository root:

    python3 tools/fix_export_scale_bar.py
"""
import glob
import sys

MEASURE = ("const measureText=(s,font)=>{const c=document.createElement('canvas').getContext('2d');"
           "c.font=font;return c.measureText(String(s)).width};")

BRAIN = [
    (" const pad=24,head=44,foot=64,W=L.width+pad*2,H=L.height+head+foot;\n",
     " const pad=24,head=44;\n"),
    (" let parts=[`<svg xmlns=",
     " // Legend below the heatmap: units line, colour bar, then \"0\" and the maximum on one line under the bar.\n"
     " " + MEASURE + "\n"
     " const maxLabel=max.toFixed(3),bar=Math.min(250,Math.max(160,L.width-left));\n"
     " const legendW=Math.max(measureText(unit,'12px Arial'),bar,measureText('0','11px Arial')+measureText(maxLabel,'11px Arial')+16);\n"
     " const W=Math.ceil(Math.max(L.width,legendW)+pad*2),unitY=head+L.height+16,by=unitY+8,barH=11,labelY=by+barH+13,H=Math.ceil(labelY+12);\n"
     " let parts=[`<svg xmlns="),
    (" parts.push(`<text x=\"${pad}\" y=\"${H-34}\" font-family=\"Arial\" font-size=\"12\" fill=\"#263649\">${esc(unit)}</text>`);\n"
     " const bar=Math.min(250,W-pad*2),by=H-23;\n"
     " for(let i=0;i<bar;i++)parts.push(`<rect x=\"${pad+i}\" y=\"${by}\" width=\"1\" height=\"11\" fill=",
     " parts.push(`<text x=\"${pad}\" y=\"${unitY}\" font-family=\"Arial\" font-size=\"12\" fill=\"#263649\">${esc(unit)}</text>`);\n"
     " for(let i=0;i<bar;i++)parts.push(`<rect x=\"${pad+i}\" y=\"${by}\" width=\"1\" height=\"${barH}\" fill="),
    (" parts.push(`<text x=\"${pad}\" y=\"${by+25}\" font-family=\"Arial\" font-size=\"11\">0</text>`,"
     "`<text x=\"${pad+bar+8}\" y=\"${by+10}\" font-family=\"Arial\" font-size=\"11\">${max.toFixed(3)}</text>`,'</svg>');",
     " parts.push(`<text x=\"${pad}\" y=\"${labelY}\" font-family=\"Arial\" font-size=\"11\" fill=\"#263649\">0</text>`,"
     "`<text x=\"${pad+bar}\" y=\"${labelY}\" text-anchor=\"end\" font-family=\"Arial\" font-size=\"11\" fill=\"#263649\">${maxLabel}</text>`,'</svg>');"),
]

CELL = [
    (" const extra=66, fullHeight=height+extra;\n", ""),
    (" const parts=[`<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"${width}\" height=\"${fullHeight}\" viewBox=\"0 0 ${width} ${fullHeight}\">`];",
     " // Legend below the heatmap: units line, colour bar, then \"0\" and the maximum on one line under the bar.\n"
     " " + MEASURE + "\n"
     " const highLabel=high.toFixed(3),lx=left,rampW=Math.min(220,Math.max(160,width-left-right));\n"
     " const legendW=Math.max(measureText(legendText,'11px Arial'),rampW,measureText('0','10px Arial')+measureText(highLabel,'10px Arial')+16);\n"
     " const figW=Math.ceil(Math.max(width,lx+legendW+right)),ly=height+16,ry=ly+8,labelY=ry+12+12,fullHeight=Math.ceil(labelY+10);\n"
     " const parts=[`<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"${figW}\" height=\"${fullHeight}\" viewBox=\"0 0 ${figW} ${fullHeight}\">`];"),
    (" const ly=height+16, lx=left, rampW=Math.min(220,Math.max(70,width-left-right-30));\n", ""),
    (" const ry=ly+12;\n", ""),
    ("<rect x=\"${lx+16}\" y=\"${ry}\" width=\"${rampW}\"", "<rect x=\"${lx}\" y=\"${ry}\" width=\"${rampW}\""),
    ("<text x=\"${lx}\" y=\"${ry+10}\" font-family=\"Arial,sans-serif\" font-size=\"10\" fill=\"#263649\">0</text>",
     "<text x=\"${lx}\" y=\"${labelY}\" font-family=\"Arial,sans-serif\" font-size=\"10\" fill=\"#263649\">0</text>"),
    ("<text x=\"${lx+22+rampW}\" y=\"${ry+10}\" font-family=\"Arial,sans-serif\" font-size=\"10\" fill=\"#263649\">${esc(high.toFixed(3))}</text>",
     "<text x=\"${lx+rampW}\" y=\"${labelY}\" text-anchor=\"end\" font-family=\"Arial,sans-serif\" font-size=\"10\" fill=\"#263649\">${esc(highLabel)}</text>"),
    ("return {svg:parts.join(''),width,height:fullHeight};", "return {svg:parts.join(''),width:figW,height:fullHeight};"),
]


def fix(path, edits):
    t = open(path, encoding="utf-8").read()
    for old, new in edits:
        if t.count(old) != 1:
            sys.exit(f"{path}: expected exactly one of {old[:70]!r}, found {t.count(old)}")
        t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)


def main():
    pages = [(p, BRAIN) for p in glob.glob("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html")] + \
            [(p, CELL) for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html")]
    pages = sorted((p, e) for p, e in pages if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for p, edits in pages:
        fix(p, edits)
    print(len(pages), "pages fixed")


if __name__ == "__main__":
    main()
