# CellPalmSeq heatmaps

Interactive heatmaps of how the genes that control **protein S-palmitoylation** are expressed across human tissues, human cell types, cancer cell lines and commonly used laboratory cell lines, built from public RNA-seq data. Each dataset is a self-contained web page, served with GitHub Pages and embedded in the CellPalmSeq WordPress site.

## Goal

S-palmitoylation is a reversible lipid modification that controls where proteins go and how they behave. Its dysregulation is linked to brain and metabolic disorders, viral infection and cancer. It is added by the ZDHHC palmitoyl acyltransferases (with accessory proteins) and removed by depalmitoylating enzymes. CellPalmSeq shows where these genes are expressed in human cell types and tissues, and in the cell lines used in basic and preclinical research. It helps with choosing a cell line and interpreting palmitoylation experiments. The resource is described in Wild et al., *Frontiers in Physiology* 2023 ([Citation](#citation)); its companion for the nervous system is BrainPalmSeq.

This repository holds the 2026 heatmap release: one interactive heatmap per dataset, plus a Search by Gene page.

**Genes shown (up to 40):** the ZDHHC enzymes (*ZDHHC1*–*9*, *11*, *11B* and *12*–*24* in human data; *Zdhhc1*–*9* and *11*–*25* in rodent data), the depalmitoylating enzymes *LYPLA1*, *LYPLA2* and *PPT1*, ABHD-family hydrolases (*ABHD4*, *ABHD6*, *ABHD10*, *ABHD11*, *ABHD12*, *ABHD13*, *ABHD16A*, *ABHD17A*–*C*), and the accessory proteins *GOLGA7*, *GOLGA7B* and *SELENOK*. Gene symbols keep each source's spelling. Some laboratory matrices contain fewer genes (see the table).

## Live pages

The landing page [angie13-doc.github.io/CellPalmSeq-heatmaps](https://angie13-doc.github.io/CellPalmSeq-heatmaps/) (`index.html`) links to the datasets and Search by Gene. Each heatmap lives at
`https://angie13-doc.github.io/CellPalmSeq-heatmaps/<folder>/<folder>.html`, and each folder has a ready-to-paste WordPress embed as `<folder>_iframe.html`.

The iframes load the live page from GitHub Pages, so a change merged into `main` reaches the WordPress pages without editing them. GitHub Pages lets browsers keep a page for up to 10 minutes, so an update can take that long to appear; a hard refresh (Cmd/Ctrl+Shift+R) on the page itself shows it at once.

## Datasets

All folders start with `CellPalmSeq2026_`. Units are each source's own and are **not comparable across datasets**.

| Folder | Columns | Genes | Expression units | Category filter | Notes |
|---|---:|---:|---|---|---|
| `Broad_CCLE` | 1,406 human cancer cell lines | 40 | TPM | Primary disease (33) | Optional log₂(TPM + 1) colours |
| `Broad_CCLE_MeanByPrimaryDisease` | 33 disease groups | 40 | Mean TPM | Primary disease | Arithmetic means of original TPM; hover shows the number and names of contributing lines |
| `Sanger_CMP` | 442 human cancer cell lines | 40 | TPM | Cancer type (42) | Optional log₂(TPM + 1) colours |
| `Sanger_CMP_MeanByCancerType` | 42 cancer types | 40 | Mean TPM | Cancer type | Arithmetic means, as above |
| `HPA_NormalTissue` | 54 human tissues | 40 | nTPM | Organ | HPA/GTEx consensus bulk RNA-seq; the source file has no unit header, so the unit comes from the dataset's provenance. Optional log₂ colours |
| `HPA_SingleCell_CellTypes` | 154 human cell types | 40 | nCPM | Cell type class (e.g. blood and immune cells) | HPA single-cell RNA-seq. Optional log₂ colours |
| `HPA_SingleCell_Clusters` | 1,175 single-cell clusters | 40 | nCPM | Tissue | Optional log₂ colours |
| `HPA_CellLines` | 1,206 human cell lines | 40 | nTPM | Cell-line group | TPM and pTPM kept in hover; disease annotations matched by exact cell-line name. Optional log₂ colours |
| `Lab_BHK21` | 3 samples + mean | 36 | Source matrix values | Sample category | Syrian hamster kidney |
| `Lab_CHO` | 15 samples + mean | 37 | Source matrix values | Sample category | Chinese hamster ovary |
| `Lab_Calu3` | 12 samples + mean | 40 | Source matrix values | Sample category | Human lung adenocarcinoma |
| `Lab_MDCK` | 19 samples + mean | 34 | Source matrix values | Sample category | Dog kidney |
| `Lab_NIH_3T3` | 10 samples + mean | 40 | Source matrix values | Sample category | Mouse fibroblast |
| `Lab_PC12` | 9 samples + mean | 40 | Source matrix values | Sample category | Rat pheochromocytoma |
| `Lab_VeroE6` | 17 samples + mean | 34 | Source matrix values | Sample category | African green monkey kidney |

The laboratory matrices' units could not be established from the supplied files. They are shown as given, with no transformation; do not read them as TPM. The "mean" column in each is the mean provided by the source.

Each folder contains:

- `<folder>.html`: the heatmap page, with its data embedded.
- `<folder>_iframe.html`: the WordPress embed snippet.
- `README.md`: the dataset's source file, counts and units.
- The source data as CSV (or TSV): the source matrix, the 40-gene subset used, or the group means. HPA Cell Lines also has `HPA_cell_line_annotations.csv`.

## Using a heatmap

Genes are rows and columns are cell lines, tissues, cell types or samples, coloured on the reversed Hawaii scale (pale cyan = low, dark magenta = high).

- **Search** one or more cell lines, tissues or metadata values. Each extra search becomes a labelled comparison group. Suggestions come from the dataset's own annotations.
- **Filter** by the dataset's categories, and choose which genes to show (all, ZDHHC only, non-ZDHHC, or any set).
- **Colour scale:** *Fixed across all cells* uses the dataset maximum, which is best for comparing searches. *Fit current selection* uses the maximum across everything selected, on screen or not.
- **Expression scale** (CCLE, Sanger and HPA pages): original values, or log₂(value + 1) for colours. Hover and CSV keep the original values.
- **Rank** genes and/or columns by mean expression.
- **Browse:** every matching column sits in one strip that scrolls sideways. When the strip is wider than the view, a *Whole selection* band above it summarises everything selected, with a frame for the visible part. Click or drag the band, use its ◀ Left / Right ▶ buttons, or Tab to it and use the arrow keys, Page Up/Down and Home/End. *Heatmap size* zooms.

  **How the *Whole selection* band is drawn.** The band shows every selected column, squeezed to the width of the heatmap on your screen, with genes in the same order as the heatmap rows. When there are more columns than screen pixels across the band, several neighbouring columns share one screen pixel, and that pixel takes the **highest** of their values (for each gene). So a single strongly expressing column always shows up in the band, even next to low ones. A dark spot means at least one column there reaches that level, not that every column does; the heatmap below shows each column's own value. How much the band squeezes depends on the number of columns and on your screen: its width, and how many pixels it packs into that width. On a standard screen, Yao 2023 GABAergic (2,025 clusters) puts about 2 columns in each pixel and Glutamatergic (2,597) about 3; on a high-resolution (Retina) screen, about 1 and 1.4. When each column has its own screen pixel, the band shows exact values. Thin vertical lines in the band mark the starts of categories or comparison groups.

- **Hover** (or tap) a tile for the gene, the column's full source metadata, and the expression value.
- **Export** the whole selection as CSV, SVG or high-resolution PNG, optionally with a transparent background. Very wide selections may need SVG.

**Search by Gene** (`Search_by_Gene/`) shows one gene across HPA Normal Tissue (nTPM), HPA single-cell types (nCPM), Broad CCLE averaged by primary disease and Sanger CMP averaged by cancer type (TPM). Averages are computed within each study, never between studies.

## How it works

Each heatmap is a single static HTML file with no server, build step or external library, which makes it easy to host and embed. The pages use the same template as BrainPalmSeq. Each is a `<div id="bps-compare">` holding:

1. **Styles and controls** (sidebar and heatmap area).
2. **Embedded data** in `<script type="application/json" class="bps-data">`. It is stored compactly: each column's metadata once, plus one value per column and gene. A small decoder at the top of the page script, `bpsData()`, rebuilds the full rows (gene, column, metadata, expression) before anything reads them. CCLE went from 32 MB to 0.85 MB this way.
3. **The page script**, which builds the search, filters, gene picker, ranking, colour options, hover, CSV export and SVG/PNG figure export from those rows.
4. **The continuous-heatmap engine**, inlined from `tools/continuous_heatmap_engine.js`. It lays every selected column out in one strip and draws only the visible part on a canvas that stays fixed while the strip scrolls, so even 1,406 cell lines stay fast. It also draws the summary band and handles its mouse, keyboard and button navigation.

## How it is built

The dataset pages were first generated outside this repository from the source matrices in each folder and uploaded as release archives. That generator is not in this repository; the archives at the root are earlier releases. Since then, changes have been made directly to the pages with the scripts in `tools/`. Each script edits every page the same way and stops without writing anything if a page doesn't match what it expects:

| Script | What it did |
|---|---|
| `apply_hawaii_palette.py` | Set the reversed Hawaii colour map and removed the palette menu. |
| `italicize_gene_names.py` | Italicised gene names in labels, hover and exports. |
| `apply_continuous_heatmap.py` | Replaced pages of 150 columns with the continuous heatmap and summary band. Its markup and styles live here. |
| `continuous_heatmap_engine.js` | The engine itself (see above). |
| `update_heatmap_engine.py` | Copies the current engine, summary-band markup and styles into already-converted pages. |
| `compact_heatmap_data.py` | Stored the embedded data compactly and added the decoder. Before writing a page, it checks that the decoded data matches the original exactly. |
| `verify_compact_data.js` | Repeats that check with Node.js: `node tools/verify_compact_data.js ORIGINAL.html COMPACT.html`. |
| `fix_export_scale_bar.py` | Laid out the SVG/PNG scale bar so it is never clipped. |

The same scripts are used in BrainPalmSeq and handle both sites' pages.

**To change the heatmap engine:** edit `tools/continuous_heatmap_engine.js` (and the markup or styles in `apply_continuous_heatmap.py` if needed), then run from the repository root:

```bash
python3 tools/update_heatmap_engine.py
```

Most scripts are one-off migrations and refuse to run twice on the same page. Changes so far were tested in headless Chromium (Playwright), loading each page and exercising scrolling, hover, search, ranking, colour options and exports. Those tests are not stored in this repository.

**Publishing:** GitHub Pages serves the `main` branch root. Merging into `main` updates the live pages and the WordPress embeds.

## Data notes

- Expression values are the sources' own values; none were renormalised. Hover and CSV always show the original value; the log₂ option changes colours only.
- Units differ between datasets (see the table). Never compare unnormalised levels across studies.
- The release checks compared every embedded expression value against its embedded source value (0 mismatches).
- The two mean pages supplement the individual cell-line pages; they don't replace them.

## Other files

| File | Contents |
|---|---|
| `index.html` | Landing page listing the datasets. It does not yet link the two mean pages. |
| `Search_by_Gene/` | The Search by Gene page, its embed snippet and README. |
| `QA_REPORT.md` | Checks from the original release, including what was not validated at the time. |
| `CellPalmSeq2026_*.zip` | Earlier release archives, kept for reference. |
| `CellPalmSeq2026_Search_by_Gene_HOVER_CLEAN.html`, `_HOVER_FIXED.html`, `_UPDATED.html` | Earlier drafts of Search by Gene. Nothing links to them; the live page is in `Search_by_Gene/`. |

## Change history

- **2026-11-06:** expression units and hover/CSV labels audited per dataset; optional log₂(value + 1) colours added to the CCLE, Sanger and HPA pages; CCLE and Sanger disease-mean pages added.
- **2026-11-17:**
  - single reversed Hawaii colour map;
  - italic gene names;
  - Reset, empty-selection and Search by Gene gene-case fixes;
  - continuous heatmap with summary band ("Fit current selection" covers every selected column; exports cover the whole selection and follow the log₂ option);
  - CSV line-break fix;
  - compact embedded data (104 MB to 4 MB);
  - keyboard and button navigation;
  - unclipped SVG/PNG scale bar.

## Citation

Wild AR, Hogg PW, Flibotte S, Kochhar S, Hollman RB, Haas K, Bamji SX. CellPalmSeq: A curated RNAseq database of palmitoylating and de-palmitoylating enzyme expression in human cell types and laboratory cell lines. *Frontiers in Physiology* 2023;14:1110550. [doi:10.3389/fphys.2023.1110550](https://doi.org/10.3389/fphys.2023.1110550)

For the nervous system, see the companion resource BrainPalmSeq ([Angie13-doc/BrainPalmSeq-heatmaps](https://github.com/Angie13-doc/BrainPalmSeq-heatmaps)).

Please also cite the original source of each dataset you use (Broad DepMap CCLE, Sanger Cell Model Passports, the Human Protein Atlas, and the studies behind each laboratory cell line).
## Colour map and gene-name styling (2026-11-17)
- All 15 heatmaps use one colour map: reversed Hawaii (Crameri Scientific Colour Maps; pale cyan = low, dark magenta = high), 50 steps. Palette selector removed. Re-apply with `tools/apply_hawaii_palette.py`.
- Gene names are italic: heatmap row labels (screen, SVG, PNG), gene checklist, hover Gene value, and the Search by Gene hover heading. Letters unchanged. Re-apply with `tools/italicize_gene_names.py`.
- Heatmaps show every matching column in one continuous, sideways-scrolling strip (no pages of 150), with a whole-selection summary band above it (click or drag to jump; shown when the heatmap is wider than the view). "Fit current selection" scales to every selected column. CSV/SVG/PNG exports cover the whole selection, and SVG/PNG colours follow the log₂ option. Re-apply with `tools/apply_continuous_heatmap.py`.
- Embedded data is stored compactly (each column's details once, not once per gene): page data 104 MB -> 4 MB in total, e.g. Broad CCLE 32 MB -> 0.85 MB. A decoder in each page rebuilds the identical rows before anything reads them. Re-apply with `tools/compact_heatmap_data.py`; check with `tools/verify_compact_data.js`.
- Keyboard and button navigation: the summary band is a keyboard slider (Tab to it; arrow keys move a quarter of the view, Page Up/Down a full view, Home/End to the start or end) and ◀ Left / Right ▶ buttons sit beside the "Showing a–b of N" count. Update converted pages after engine changes with `tools/update_heatmap_engine.py`.
- SVG/PNG export scale bar: units line, colour bar, then "0" and the maximum on one line below the bar ("0" under the left end, maximum right-aligned under the right end). The legend has its own space and the image widens when the legend is wider than the heatmap, so nothing is clipped. Re-apply with `tools/fix_export_scale_bar.py`.
