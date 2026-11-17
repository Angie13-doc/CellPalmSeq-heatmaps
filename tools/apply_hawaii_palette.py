"""Set every CellPalmSeq2026 heatmap to the reversed Hawaii colour map only.

Hawaii is from Fabio Crameri's Scientific Colour Maps (v8, via the
`cmcrameri` package). It is reversed (hawaii_r) so low expression is pale
cyan and high expression is dark magenta, then sampled at 50 even steps,
the palette length the pages already use. The page's palette selector and
its switching code are removed.

Run from the repository root:  python3 tools/apply_hawaii_palette.py
"""
import glob
import json
import re
import sys

# cmcrameri.cm.hawaii_r sampled at numpy.linspace(0, 1, 50).
HAWAII_R_50 = [
    "#b3f2fd", "#a6f1f9", "#98f1f5", "#8af0ef", "#7deee8", "#6febde", "#67e9d5",
    "#61e6ca", "#5fe3c0", "#60dfb2", "#62dca7", "#66d89c", "#6ad591", "#6fd286",
    "#74ce79", "#79ca6e", "#7ec663", "#82c359", "#88be4c", "#8cb942", "#91b439",
    "#94ae30", "#97a828", "#9aa021", "#9b991d", "#9c921c", "#9d8c1c", "#9d841e",
    "#9c7e20", "#9c7823", "#9b7226", "#9b6c2a", "#9a662e", "#996131", "#985c34",
    "#985638", "#97513c", "#964c3f", "#964742", "#954246", "#943d4a", "#94374e",
    "#933252", "#922d56", "#91285a", "#902160", "#901c64", "#8f1569", "#8e0d6e",
    "#8c0273",
]

SELECTOR_HTML = (
    '<div><label for="bps-palette">Colour palette</label>'
    '<select id="bps-palette" class="palette-select">'
    '<option value="original">Spectral</option>'
    '<option value="viridis">Viridis</option>'
    '<option value="mako">Mako</option>'
    '<option value="rocket">Rocket</option></select></div>'
)
# Palette anchors, interpolation and the change handler, up to the listener.
SWITCHER_JS = re.compile(
    r"const paletteAnchors=\{.*?\$\('\.palette-select'\)\.addEventListener\('change',updatePalette\);\n",
    re.S,
)
RESET_JS = "$('.palette-select').value='original';palette=originalPalette;"
PALETTE_JSON = re.compile(r'"palette":\[[^\]]*\]')


def replace_once(text, old, new, path, what):
    count = text.count(old) if isinstance(old, str) else len(old.findall(text))
    if count != 1:
        sys.exit(f"{path}: expected exactly one {what}, found {count}")
    return text.replace(old, new) if isinstance(old, str) else old.sub(lambda _: new, text)


def main():
    pages = sorted(
        p for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html")
        if not p.endswith("_iframe.html")
    )
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    new_palette = '"palette":' + json.dumps(HAWAII_R_50, separators=(",", ":"))
    for path in pages:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        text = replace_once(text, PALETTE_JSON, new_palette, path, "embedded palette")
        text = replace_once(text, SELECTOR_HTML, "", path, "palette selector")
        text = replace_once(text, SWITCHER_JS, "", path, "palette switching code")
        text = replace_once(text, RESET_JS, "", path, "palette reset")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("updated", path)
    print(f"{len(pages)} pages updated")


if __name__ == "__main__":
    main()
