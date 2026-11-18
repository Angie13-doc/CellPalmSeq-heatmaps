"""Hover on pages with the log2 Expression scale: show the original value and,
with log2 on, the log value too, e.g. "12.3 TPM (log₂(TPM + 1) = 3.733)".

Before, the log2 setting replaced the original value in the hover with the
log value, contradicting the control's note that hover keeps original
values. Matches BrainPalmSeq's Zhang 2014, HippoSeq and Sjostedt 2020 pages.
Run from the repository root:  python3 tools/hover_original_and_log.py
"""
import glob
import re
import sys

OLD = re.compile(r"\(colourTransform\.value==='log'\?Math\.log2\(Math\.max\(0,r\.(TPM|SourceValue)\)\+1\)\.toFixed\(3\)"
                 r"\+' log₂\(([^)]+) \+ 1\)':r\.\1\+' \2'\)")


def new(m):
    field, unit = m.group(1), m.group(2)
    return (f"(r.{field}+' {unit}'+(colourTransform.value==='log'?' (log₂({unit} + 1) = '"
            f"+Math.log2(Math.max(0,r.{field})+1).toFixed(3)+')':''))")


def main():
    n = 0
    for path in sorted(glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html")):
        if path.endswith("_iframe.html"):
            continue
        t = open(path, encoding="utf-8").read()
        k = len(OLD.findall(t))
        if k == 0:
            continue
        if k != 1:
            sys.exit(f"{path}: expected one hover expression, found {k}")
        open(path, "w", encoding="utf-8").write(OLD.sub(new, t))
        n += 1
        print("updated", path)
    print(n, "pages updated")


if __name__ == "__main__":
    main()
