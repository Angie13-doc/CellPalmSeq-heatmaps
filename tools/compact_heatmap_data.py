"""Shrink the data embedded in each heatmap page without changing what it holds.

Each page embeds {"rows": [...], ...}: one row per population and gene, which
repeats every population's details for every gene. This stores those details
once per population, the per-gene fields as plain value lists, and the gene
names once. A small decoder added to the page rebuilds the identical rows
(same fields, same field order, same values, same row order) before any page
code reads them, so nothing else on the page changes.

Before writing a page, the script decodes the result in Python and checks it
matches the original exactly; tools/verify_compact_data.js repeats that check
with the browser's own JSON parser.

Run from the repository root:  python3 tools/compact_heatmap_data.py
"""
import glob
import json
import re
import sys

DATA = re.compile(r'(<script type="application/json" class="bps-data">)(.*?)(</script>)', re.S)
PARSE_CALL = "JSON.parse($('.bps-data').textContent)"
IIFE_START = "(function(){'use strict';"

DECODER = r"""
// Embedded data is stored compactly (each population's details once); rebuild the
// original rows exactly before anything reads them. See tools/compact_heatmap_data.py.
function bpsData(){if(bpsData.cache)return bpsData.cache;const D=JSON.parse(document.getElementById('bps-compare').querySelector('.bps-data').textContent);const C=D.compact;if(!C)return bpsData.cache=D;
 const G=C.genes.length,N=C.cells.length,n=G*N,col=k=>C.alias[k]?C.r[C.alias[k]]:C.r[k],rows=new Array(n);
 const plan=C.keys.map(k=>{if(k===C.geneKey)return{k,t:'g'};const ci=C.ck.indexOf(k);if(ci>=0)return{k,t:'c',i:ci};if(C.nest[k]){const S=C.nest[k];return{k,t:'n',cs:S.cs,shapes:S.shapes.map(sh=>sh.map(s=>{const j=S.ck.indexOf(s);return j>=0?{s,c:true,j}:{s,c:false,v:S.alias[s]?S.r[S.alias[s]]:S.r[s]}})),cells:S.cells}}return{k,t:'r',v:col(k)}});
 for(let i=0;i<n;i++){const c=C.order==='gene'?i%N:Math.floor(i/G),g=C.order==='gene'?Math.floor(i/N):i%G,o={};
  for(const p of plan){if(p.t==='g')o[p.k]=C.genes[g];else if(p.t==='c')o[p.k]=C.cells[c][p.i];else if(p.t==='r')o[p.k]=p.v[i];else{const m={};for(const q of p.shapes[p.cs[c]])m[q.s]=q.c?p.cells[c][q.j]:q.v[i];o[p.k]=m}}
  rows[i]=o}
 const out={};for(const k of C.top)out[k]=k==='rows'?rows:D[k];return bpsData.cache=out}
"""


def split(dicts, groups):
    """Split per-row dicts into keys constant within each group and keys that vary."""
    keys = list(dicts[0].keys())
    for d in dicts:
        if list(d.keys()) != keys:
            raise ValueError("rows do not share one key order")
    const = []
    for k in keys:
        if all(len({json.dumps(dicts[i][k], sort_keys=True) for i in idx}) == 1 for idx in groups):
            const.append(k)
    return keys, const


def encode_nested(vals, groups):
    """Dict-valued field: each population has one field list (it may differ between populations)."""
    shapes, cs = [], []
    for idx in groups:
        shape = list(vals[idx[0]].keys())
        if any(list(vals[i].keys()) != shape for i in idx):
            raise ValueError("nested field order varies within a population")
        if shape not in shapes:
            shapes.append(shape)
        cs.append(shapes.index(shape))
    union = []
    for s in shapes:
        union += [k for k in s if k not in union]
    const = [k for k in union
             if all(len({json.dumps(vals[i][k], sort_keys=True) for i in idx}) == 1 for idx in groups if k in vals[idx[0]])]
    cols = {k: [v.get(k) for v in vals] for k in union if k not in const}
    al = aliases(cols)
    return {"shapes": shapes, "cs": cs, "ck": const,
            "cells": [[vals[idx[0]].get(k) for k in const] for idx in groups],
            "r": {k: v for k, v in cols.items() if k not in al}, "alias": al}


def aliases(cols):
    out, seen = {}, {}
    for k, v in cols.items():
        sig = json.dumps(v)
        if sig in seen:
            out[k] = seen[sig]
        else:
            seen[sig] = k
    return out


def encode(d):
    rows = d["rows"]
    cells, genes = [], []
    for r in rows:
        if r["ClusterName"] not in cells:
            cells.append(r["ClusterName"])
        if r["Gene"] not in genes:
            genes.append(r["Gene"])
    G, N = len(genes), len(cells)
    if len(rows) != G * N:
        raise ValueError("not one row per population and gene")
    if all(rows[i]["ClusterName"] == cells[i // G] and rows[i]["Gene"] == genes[i % G] for i in range(len(rows))):
        order, cell_of = "cell", (lambda i: i // G)
    else:
        genes = []
        for r in rows:
            if r["Gene"] not in genes:
                genes.append(r["Gene"])
        if all(rows[i]["ClusterName"] == cells[i % N] and rows[i]["Gene"] == genes[i // N] for i in range(len(rows))):
            order, cell_of = "gene", (lambda i: i % N)
        else:
            raise ValueError("rows are neither population-major nor gene-major")
    groups = [[] for _ in cells]
    for i in range(len(rows)):
        groups[cell_of(i)].append(i)
    keys, const = split(rows, groups)
    ck = [k for k in const if k != "Gene"]
    first = [rows[idx[0]] for idx in groups]
    nest, r = {}, {}
    for k in keys:
        if k == "Gene" or k in ck:
            continue
        vals = [row[k] for row in rows]
        if all(isinstance(v, dict) for v in vals):
            nest[k] = encode_nested(vals, groups)
        else:
            r[k] = vals
    al = aliases(r)
    compact = {"keys": keys, "geneKey": "Gene", "ck": ck, "order": order, "genes": genes,
               "cells": [[f[k] for k in ck] for f in first],
               "r": {k: v for k, v in r.items() if k not in al}, "alias": al, "nest": nest,
               "top": list(d.keys())}
    out = {"compact": compact}
    for k, v in d.items():
        if k != "rows":
            out[k] = v
    return out


def decode(e):
    """Python mirror of the page's bpsData(), used to check every page before writing it."""
    C = e["compact"]
    G, N = len(C["genes"]), len(C["cells"])
    col = lambda k: C["r"][C["alias"].get(k, k)]
    rows = []
    for i in range(G * N):
        c, g = (i % N, i // N) if C["order"] == "gene" else (i // G, i % G)
        o = {}
        for k in C["keys"]:
            if k == C["geneKey"]:
                o[k] = C["genes"][g]
            elif k in C["ck"]:
                o[k] = C["cells"][c][C["ck"].index(k)]
            elif k in C["nest"]:
                S = C["nest"][k]
                o[k] = {s: (S["cells"][c][S["ck"].index(s)] if s in S["ck"] else S["r"][S["alias"].get(s, s)][i])
                        for s in S["shapes"][S["cs"][c]]}
            else:
                o[k] = col(k)[i]
        rows.append(o)
    return {k: (rows if k == "rows" else e[k]) for k in C["top"]}


def compact_page(path):
    t = open(path, encoding="utf-8").read()
    m = DATA.search(t)
    if not m or len(DATA.findall(t)) != 1:
        sys.exit(f"{path}: expected one bps-data block")
    raw = m.group(2)
    d = json.loads(raw)
    if "compact" in d:
        sys.exit(f"{path}: already compact")
    e = encode(d)
    if json.dumps(decode(e)) != json.dumps(d):
        sys.exit(f"{path}: decoded data differs from the original")
    new = json.dumps(e, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    calls = t.count(PARSE_CALL)
    if calls < 1 or t.count(IIFE_START) != 1:
        sys.exit(f"{path}: unexpected script layout")
    t = t[:m.start(2)] + new + t[m.end(2):]
    t = t.replace(PARSE_CALL, "bpsData()")
    t = t.replace(IIFE_START, IIFE_START + DECODER, 1)
    open(path, "w", encoding="utf-8").write(t)
    return len(raw), len(new)


def main():
    pages = sorted(p for pat in ("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html", "CellPalmSeq2026_*/CellPalmSeq2026_*.html")
                   for p in glob.glob(pat) if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    before = after = 0
    for p in pages:
        a, b = compact_page(p)
        before += a
        after += b
        print(f"{p.split('/')[-1]:60} {a/1e6:7.2f} MB -> {b/1e6:6.2f} MB")
    print(f"{len(pages)} pages: embedded data {before/1e6:.1f} MB -> {after/1e6:.1f} MB")


if __name__ == "__main__":
    main()
