"""Italicize gene names on the CellPalmSeq2026 heatmap and Search-by-Gene pages.

Heatmap pages: gene row labels (on screen, SVG and PNG export), the
"Genes to display" checklist, the hover box's Gene value and marker-gene
fields, and search suggestions of kind "Marker gene".

Search-by-Gene page: the gene in the hover heading. The <select> gene
dropdown is left plain, because browsers ignore styling on native options.

Only styling changes: the letters of every gene name are left as they are.
Gene names inside cell-population names and descriptions stay plain.

Run from the repository root:  python3 tools/italicize_gene_names.py
"""
import glob
import json
import sys

# Hover-box fields whose whole value is a list of gene symbols.
GENE_FIELDS = ["Gene", "Marker genes", "MarkerGenes", "Marker Genes",
               "Type marker", "Top Enriched Genes", "Class marker"]
FIELD_EXCLUSIONS = {}

HEATMAP_EDITS = [
    ("checklist",
     "label.append(input,document.createTextNode(gene))",
     "label.append(input,Object.assign(document.createElement('i'),{textContent:gene}))"),
    ("canvas row labels",
     "ctx.font=Math.max(10,Math.round(10*zoomFactor))+'px Arial';ctx.fillStyle='#263649';ctx.textAlign='right'",
     "ctx.font='italic '+Math.max(10,Math.round(10*zoomFactor))+'px Arial';ctx.fillStyle='#263649';ctx.textAlign='right'"),
    ("SVG row labels",
     'font-size="${geneFont}" fill="#263649">${esc(g)}',
     'font-size="${geneFont}" font-style="italic" fill="#263649">${esc(g)}'),
    ("hover values",
     "tip.appendChild(strong);tip.appendChild(document.createTextNode(String(v)));",
     "tip.appendChild(strong);tip.appendChild(geneFields.has(k)?Object.assign(document.createElement('i'),{textContent:String(v)}):document.createTextNode(String(v)));"),
    ("marker-gene suggestions",
     "title.textContent=item.label;",
     "title.textContent=item.label;if(item.kind==='Marker gene')title.style.fontStyle='italic';"),
]
HOVER_FIELDS_ANCHOR = " const fields=[['Gene',r.Gene],"

SEARCH_EDITS = [
    ("hover heading",
     "head.textContent=gene+' · '+name;",
     "head.append(Object.assign(document.createElement('i'),{textContent:gene}),' · '+name);"),
]


def apply(text, path, edits):
    for what, old, new in edits:
        count = text.count(old)
        if count != 1:
            sys.exit(f"{path}: expected exactly one {what}, found {count}")
        text = text.replace(old, new)
    return text


def main():
    heatmaps = sorted(
        p for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html")
        if not p.endswith("_iframe.html")
    )
    searches = ["Search_by_Gene/CellPalmSeq2026_Search_by_Gene.html"]
    if not heatmaps:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path in heatmaps:
        dataset = path.split("/")[0]
        fields = [f for f in GENE_FIELDS if f not in FIELD_EXCLUSIONS.get(dataset, set())]
        anchor_new = " const geneFields=new Set(" + json.dumps(fields) + ")," + HOVER_FIELDS_ANCHOR[len(" const "):]
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        text = apply(text, path, HEATMAP_EDITS + [("hover field list", HOVER_FIELDS_ANCHOR, anchor_new)])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("updated", path)
    for path in searches:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        text = apply(text, path, SEARCH_EDITS)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("updated", path)
    print(f"{len(heatmaps)} heatmap pages and {len(searches)} search pages updated")


if __name__ == "__main__":
    main()
