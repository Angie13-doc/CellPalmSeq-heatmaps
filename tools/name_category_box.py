"""Give the category box one consistent name per kind of grouping.

The category dropdown (#bps-broad-label) said "Cell-line categories" (or
"Cell-line groups", "Cancer type") on pages whose categories are diseases,
tissues, cell types or samples. Names now follow one scheme on both sites
(BrainPalmSeq and CellPalmSeq):
  cell types -> "Cell categories"   anatomical -> "Regions"
  cancer/disease -> "Primary disease"   tissues -> "Tissues"   samples -> "Samples"
Its heading, its "All ..." button and dropdown text, and its "All ...
selected" count change together. On HPA_NormalTissue and
HPA_SingleCell_CellTypes, Clear now shows "None selected" (it showed
"All ...", though no population is shown).

Run from the repository root:  python3 tools/name_category_box.py
"""
import re
import sys


def rename(path, heading, all_text, extra=()):
    t = open(path, encoding="utf-8").read()
    m = re.search(r'<label id="bps-broad-label">([^<]*)</label>', t)
    old_all = re.search(r'class="broad-all">([^<]*)<', t).group(1)
    n = t.count(old_all)
    if n not in (3, 4):
        sys.exit(f"{path}: expected 3-4 of {old_all!r}, found {n}")
    for old, new in extra:
        if t.count(old) != 1:
            sys.exit(f"{path}: expected exactly one of {old[:60]!r}")
        t = t.replace(old, new)
    t = t.replace(m.group(0), f'<label id="bps-broad-label">{heading}</label>')
    if old_all != all_text:
        t = t.replace(old_all, all_text)
    open(path, "w", encoding="utf-8").write(t)
    print(f"{path.split('/')[0]}: {m.group(1)!r} -> {heading!r}; {old_all!r} -> {all_text!r}")

PAGES = {
    "Broad_CCLE": ("Primary disease", "All primary diseases"),
    "Broad_CCLE_MeanByPrimaryDisease": ("Primary disease", "All primary diseases"),
    "Sanger_CMP": ("Primary disease", "All primary diseases"),
    "Sanger_CMP_MeanByCancerType": ("Primary disease", "All primary diseases"),
    "HPA_CellLines": ("Primary disease", "All primary diseases"),
    "HPA_NormalTissue": ("Tissues", "All tissues"),
    "HPA_SingleCell_Clusters": ("Tissues", "All tissues"),
    "HPA_SingleCell_CellTypes": ("Cell categories", "All cell categories"),
}
# With nothing ticked these two showed "All ..." although no population is shown.
NONE_SELECTED = {"HPA_NormalTissue": "All tissues", "HPA_SingleCell_CellTypes": "All cell categories"}
for lab in ["BHK21", "CHO", "Calu3", "MDCK", "NIH_3T3", "PC12", "VeroE6"]:
    PAGES["Lab_" + lab] = ("Samples", "All samples")


def main():
    for name, (heading, all_text) in PAGES.items():
        rename(f"CellPalmSeq2026_{name}/CellPalmSeq2026_{name}.html", heading, all_text)
    for name, all_text in NONE_SELECTED.items():
        path = f"CellPalmSeq2026_{name}/CellPalmSeq2026_{name}.html"
        t = open(path, encoding="utf-8").read()
        old = f"broadSelected.size===0?'{all_text}':"
        if t.count(old) != 1:
            sys.exit(f"{path}: expected one {old!r}")
        open(path, "w", encoding="utf-8").write(t.replace(old, "broadSelected.size===0?'None selected':"))
        print(f"{path.split('/')[0]}: Clear now shows 'None selected'")


if __name__ == "__main__":
    main()
