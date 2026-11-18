"""Add a "Colour map" menu: Hawaii (default), Turbo or Spectral.

Hawaii is the reversed Crameri Hawaii map already embedded in each page
(pale cyan = low, dark magenta = high). Turbo (matplotlib) is best for telling
small differences apart but is not colour-blind friendly. Spectral (matplotlib,
reversed) was the v1.0 default of BrainPalmSeq and of CellPalmSeq (each site's
label names its own); like Turbo, it is not colour-blind safe. Both run blue = low.
The chosen map colours the heatmap, summary band, legend and SVG/PNG exports;
Reset returns to Hawaii. Colours: matplotlib 3.11 colormaps sampled at 50
steps, the length of the embedded palette.

Run from the repository root:  python3 tools/add_colour_map_option.py
"""
import glob
import json
import sys

TURBO = ["#30123b", "#36215f", "#3b2f80", "#3f3e9c", "#424bb5", "#455ccf", "#4669e0", "#4776ee", "#4682f8", "#4391fe", "#3d9efe", "#35abf8", "#2cb7f0", "#23c3e4", "#1bd0d5", "#18d9c8", "#19e2bb", "#1fe9af", "#2cf09e", "#3cf58e", "#4ef97d", "#61fc6c", "#75fe5c", "#8bff4b", "#9cfe40", "#a9fb39", "#b7f735", "#c6f034", "#d2e935", "#dde037", "#e7d739", "#efcd3a", "#f7c13a", "#fbb637", "#fea933", "#fe9b2d", "#fd8a26", "#fa7b1f", "#f66c19", "#f15d13", "#eb500e", "#e2430a", "#da3907", "#d02f05", "#c52603", "#b71d02", "#a91601", "#9b0f01", "#8b0902", "#7a0403"]
SPECTRAL = ["#5e4fa2", "#555aa7", "#4d65ad", "#4471b2", "#3b7cb7", "#3389bd", "#3d95b8", "#47a0b3", "#52abae", "#5eb9a9", "#69c3a5", "#76c8a5", "#84cea5", "#91d3a4", "#a2d9a4", "#aedea3", "#bae3a1", "#c6e89f", "#d3ed9c", "#dff299", "#e8f69b", "#edf8a3", "#f2faaa", "#f8fcb4", "#fdfebb", "#fffcba", "#fff6b0", "#feefa3", "#fee999", "#fee28f", "#feda86", "#fed07e", "#fdc574", "#fdbb6c", "#fdb163", "#fca55d", "#fa9656", "#f88950", "#f67c4a", "#f47044", "#ef6645", "#e85b48", "#e2514a", "#dc484c", "#d63f4f", "#c9314c", "#be254a", "#b41947", "#a90d45", "#9e0142"]

MENU = ('<div class="wide"><label for="bps-cmap">Colour map</label><select id="bps-cmap">'
        '<option value="hawaii">Hawaii</option>'
        '<option value="turbo">Turbo (fine detail; not colour-blind safe)</option>'
        '<option value="spectral">Spectral ({SITE} v1.0; not colour-blind safe)</option>'
        '</select></div>')

JS = ("\n// Colour map: Hawaii (embedded palette, default), Turbo or Spectral (both blue = low).\n"
      "const bpsColourMaps={hawaii:originalPalette,turbo:" + json.dumps(TURBO, separators=(",", ":")) +
      ",spectral:" + json.dumps(SPECTRAL, separators=(",", ":")) + "};\n"
      "const bpsCmap=$('#bps-cmap');function bpsSetColourMap(k){bpsCmap.value=k;palette=bpsColourMaps[k]||originalPalette;"
      "$('.ramp').style.background='linear-gradient(to right,'+palette.join(',')+')'}\n"
      "bpsCmap.addEventListener('change',()=>{bpsSetColourMap(bpsCmap.value);render()});\n"
      "$('.reset').addEventListener('click',()=>bpsSetColourMap('hawaii'));\n")

ANCHOR_HTML = '<option value="dynamic">Fit current selection</option></select></div>'
ANCHOR_JS = "let palette=originalPalette;"


def main():
    pages = sorted(p for pat in ("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html", "CellPalmSeq2026_*/CellPalmSeq2026_*.html")
                   for p in glob.glob(pat) if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path in pages:
        t = open(path, encoding="utf-8").read()
        if 'id="bps-cmap"' in t:
            sys.exit(f"{path}: already has a colour map menu")
        for anchor in (ANCHOR_HTML, ANCHOR_JS):
            if t.count(anchor) != 1:
                sys.exit(f"{path}: expected exactly one of {anchor[:50]!r}")
        site = "BrainPalmSeq" if path.startswith("BrainPalmSeq") else "CellPalmSeq"
        t = t.replace(ANCHOR_HTML, ANCHOR_HTML + "\n" + MENU.replace("{SITE}", site)).replace(ANCHOR_JS, ANCHOR_JS + JS)
        open(path, "w", encoding="utf-8").write(t)
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
