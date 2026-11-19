"""Order heatmap genes by function instead of alphabetically.

Gene rows (and gene ticks, CSV) now run:
  de-S-acylating enzymes:  ABHD4 ... ABHD17C, LYPLA1, LYPLA2, PPT1
  accessory proteins:      SELENOK, GOLGA7, GOLGA7B
  S-acylating enzymes:     ZDHHC1 ... ZDHHC25
with numbers in numeric order inside each group, as on BrainPalmSeq.
Rodent symbols (Zdhhc1, ...) sort the same way. Genes missing from a
lab cell line's data are skipped.

Run from the repository root:  python3 tools/gene_order.py
"""
import glob
import sys

OLD_SORT = "geneNames=[...new Set(rows.map(r=>r.Gene))].sort(collator.compare)"
NEW_SORT = "geneNames=[...new Set(rows.map(r=>r.Gene))].sort((a,b)=>bpsGeneGroup(a)-bpsGeneGroup(b)||collator.compare(a,b))"
GROUP_FN = ("// Gene order: de-S-acylating enzymes, then accessory proteins, then ZDHHC S-acylating enzymes.\n"
            "const bpsGeneGroup=g=>{const s=String(g).toLowerCase();return /^abhd/.test(s)?0:/^lypla\\d/.test(s)?1:/^ppt/.test(s)?2:"
            "/^(selenok|selk)$/.test(s)?3:/^golga/.test(s)?4:/^zdhhc/.test(s)?5:6};\n")


def main():
    pages = sorted(p for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html") if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path in pages:
        t = open(path, encoding="utf-8").read()
        if "bpsGeneGroup" in t:
            sys.exit(f"{path}: already updated")
        if t.count(OLD_SORT) != 1:
            sys.exit(f"{path}: expected exactly one gene sort, found {t.count(OLD_SORT)}")
        t = t.replace(OLD_SORT, NEW_SORT)
        line = t.rfind("\n", 0, t.index(NEW_SORT)) + 1
        t = t[:line] + GROUP_FN + t[line:]
        open(path, "w", encoding="utf-8").write(t)
    print(len(pages), "pages reordered")


if __name__ == "__main__":
    main()
