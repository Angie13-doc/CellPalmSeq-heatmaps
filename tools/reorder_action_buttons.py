"""Reorder the action buttons: Export PNG · Export SVG · Export CSV, then Reset.

BrainPalmSeq pages: Reset · Export CSV · Export PNG · Export SVG
becomes Export PNG · Export SVG · Export CSV · Reset.
CellPalmSeq pages (Export SVG, Export PNG and the transparent-background option
are added by script after Reset and Export CSV): Reset · Export CSV · Export
SVG · Export PNG (high-res) · Transparent background becomes Export PNG
(high-res) · Export SVG · Export CSV · Transparent background · Reset.

Run from the repository root:  python3 tools/reorder_action_buttons.py
"""
import glob
import sys

BRAIN_OLD = ('<div class="actions wide"><button type="button" class="reset">Reset</button>'
             '<button type="button" class="export">Export CSV</button>'
             '<button type="button" class="export-png">Export PNG</button>'
             '<button type="button" class="export-svg">Export SVG</button></div>')
BRAIN_NEW = ('<div class="actions wide"><button type="button" class="export-png">Export PNG</button>'
             '<button type="button" class="export-svg">Export SVG</button>'
             '<button type="button" class="export">Export CSV</button>'
             '<button type="button" class="reset">Reset</button></div>')
CELL_OLD = "cpsActions.append(cpsSvgButton,cpsPngButton,cpsTransparent);"
CELL_NEW = ("cpsActions.append(cpsSvgButton,cpsPngButton,cpsTransparent);\n"
            "// Button order: Export PNG, Export SVG, Export CSV, transparent-background option, Reset.\n"
            "cpsActions.append(cpsPngButton,cpsSvgButton,$('.export'),cpsTransparent,$('.reset'));")


def main():
    pages = [(p, BRAIN_OLD, BRAIN_NEW) for p in glob.glob("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html")] + \
            [(p, CELL_OLD, CELL_NEW) for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html")]
    pages = sorted(x for x in pages if not x[0].endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path, old, new in pages:
        t = open(path, encoding="utf-8").read()
        if t.count(old) != 1:
            sys.exit(f"{path}: button row not found as expected")
        open(path, "w", encoding="utf-8").write(t.replace(old, new))
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
