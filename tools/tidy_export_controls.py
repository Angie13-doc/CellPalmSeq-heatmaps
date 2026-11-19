"""Tidy the CellPalmSeq export controls to match BrainPalmSeq.

- "Export PNG (high-res)" becomes "Export PNG" (the export is still
  high-resolution), so all three export buttons fit on one line at the same
  height.
- "Transparent background" gets its own line under the export buttons, in
  normal-weight text, so Reset spans the full width as on BrainPalmSeq.
- PNG and SVG files are named after the dataset page, like BrainPalmSeq
  (e.g. CellPalmSeq2026_Lab_CHO_heatmap.png). Before, they were named from the
  page title, which is empty, so every file was called "_heatmap.png" or
  "_heatmap.svg".

Run from the repository root:  python3 tools/tidy_export_controls.py
"""
import glob
import sys

EDITS = [
    ("cpsPngButton.textContent='Export PNG (high-res)'", "cpsPngButton.textContent='Export PNG'", 1),
    ("cpsTransparent.style.cssText='font-size:11px;display:inline-flex;align-items:center;gap:4px'",
     "cpsTransparent.style.cssText='font-size:11px;font-weight:400;display:flex;align-items:center;gap:4px;flex-basis:100%;margin:0'", 1),
    ("document.title.replace(/[^a-z0-9_-]+/gi,'_')+'_heatmap.",
     "(location.pathname.split('/').filter(Boolean).pop()||'CellPalmSeq').replace(/\\.html$/,'')+'_heatmap.", 2),
]


def main():
    pages = sorted(p for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html") if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No CellPalmSeq heatmap pages found; run from the repository root.")
    for path in pages:
        t = open(path, encoding="utf-8").read()
        for old, new, n in EDITS:
            if t.count(old) != n:
                sys.exit(f"{path}: expected {n} of {old[:60]!r}, found {t.count(old)}")
            t = t.replace(old, new)
        open(path, "w", encoding="utf-8").write(t)
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
