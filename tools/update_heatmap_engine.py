"""Bring pages already converted by apply_continuous_heatmap.py up to date.

Replaces each page's inline copy of the continuous-heatmap engine with
tools/continuous_heatmap_engine.js, and its summary-band markup and styles
with the current ones from apply_continuous_heatmap.py. Run from the
repository root:  python3 tools/update_heatmap_engine.py
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_continuous_heatmap import CSS, ENGINE, OVERVIEW_HTML  # noqa: E402

ENGINE_BLOCK = re.compile(r"// Continuous heatmap \(no paging\)\..*?\.observe\(scroll\)\}\n", re.S)
OVERVIEW_BLOCK = re.compile(r'<div class="bps-overview" hidden>.*?</canvas></div>', re.S)
CSS_BLOCK = re.compile(r"\n/\* Continuous heatmap with summary band \*/\n.*?(?=</style>)", re.S)


def update(path):
    t = open(path, encoding="utf-8").read()
    for pattern, new, what in ((ENGINE_BLOCK, ENGINE if ENGINE.endswith("\n") else ENGINE + "\n", "engine"),
                               (OVERVIEW_BLOCK, OVERVIEW_HTML, "summary band markup"),
                               (CSS_BLOCK, CSS, "summary band styles")):
        if len(pattern.findall(t)) != 1:
            sys.exit(f"{path}: expected exactly one {what}")
        t = pattern.sub(lambda _m: new, t)
    open(path, "w", encoding="utf-8").write(t)


def main():
    pages = sorted(p for pat in ("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html", "CellPalmSeq2026_*/CellPalmSeq2026_*.html")
                   for p in glob.glob(pat) if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for p in pages:
        update(p)
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
