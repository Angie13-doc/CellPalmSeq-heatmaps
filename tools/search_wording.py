"""One wording for the population search on every page (BrainPalmSeq and CellPalmSeq).

The search heading, its "+ Add another ..." button and each search box's
screen-reader label had wording copied between datasets ("tissue search" on
cell-line and sample pages, "Cell type or brain region search" on Broad and
Sanger). They now read "Populations to compare", "+ Add another search" and
"Population search 1", "Population search 2", ...

Run from the repository root:  python3 tools/search_wording.py
"""
import glob
import re
import sys

EDITS = [
    (re.compile(r'<div class="wide"><label>[^<]*</label><div class="region-groups">'),
     '<div class="wide"><label>Populations to compare</label><div class="region-groups">'),
    (re.compile(r'class="add-region">[^<]*<'), 'class="add-region">+ Add another search<'),
    (re.compile(r"input\.setAttribute\('aria-label','[^']*'\+\(i\+1\)\)"), "input.setAttribute('aria-label','Population search '+(i+1))"),
]


def main():
    pages = sorted(p for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html") if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path in pages:
        t = open(path, encoding="utf-8").read()
        for pattern, new in EDITS:
            t, n = pattern.subn(new, t)
            if n != 1:
                sys.exit(f"{path}: expected exactly one match of {pattern.pattern[:50]!r}, found {n}")
        open(path, "w", encoding="utf-8").write(t)
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
