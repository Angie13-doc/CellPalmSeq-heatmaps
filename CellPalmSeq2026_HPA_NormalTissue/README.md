# CellPalmSeq — HPA Normal Tissue

GitHub Pages path: `CellPalmSeq2026_HPA_NormalTissue/CellPalmSeq2026_HPA_NormalTissue.html`

Source: user-supplied `HPA_normal_tissue.csv` (not the newer HPA consensus file).

- 40 S-acylation-related genes in original order; 54 tissues, 15 original organ categories.
- Heatmap, hover, ranking, and CSV export use the original numeric matrix values.
- The source CSV does not explicitly specify expression units or HPA release version. These are **not** labelled TPM or nTPM without confirmation.
- Hover shows **Gene**, **Organ**, **Tissue**, **Expression (source matrix)** only. Organ and Tissue are the exact original matrix metadata rows.
- All 54 tissues remain searchable and rankable. No tissue categories are merged or inferred.
- Based on the existing BrainPalmSeq-style CellPalmSeq heatmap template.
- JavaScript syntax validated; live browser testing not completed.

Upload the `CellPalmSeq2026_HPA_NormalTissue` folder to the root of the `CellPalmSeq-heatmaps` GitHub repository.
