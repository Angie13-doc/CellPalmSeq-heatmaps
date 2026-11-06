# CellPalmSeq — GitHub Pages release

Upload the **contents of this ZIP** to the root of `angie13-doc/CellPalmSeq-heatmaps` (not the enclosing ZIP or an extra parent folder). Enable GitHub Pages from the main branch root. `index.html` links to all datasets.

Includes: Broad CCLE, Sanger CMP, HPA Normal Tissue, HPA Single Cell (154 types and 1,175 clusters), HPA Cell Lines with disease metadata, seven separate laboratory cell-line datasets, and Search by Gene.

**Expression units:** HPA Normal Tissue bulk RNA-seq: nTPM per original CellPalmSeq source description; HPA Single Cell: nCPM; HPA Cell Lines: nTPM; Broad CCLE/Sanger CMP: source TPM, with heatmap color transformation as documented in individual files; lab matrices: original source-provided values, normalization not specified. Never compare unnormalized levels across studies.

**Validation:** HPA cell-line annotations matched by exact names. JavaScript syntax checked; interactive browser regression testing not completed.


## Colour scaling and category selection (revision)

All standard CellPalmSeq heatmaps default to untransformed source expression values for colour mapping. For CCLE and CMP the default is original TPM; an optional `log₂(TPM + 1)` colour mapping can be selected. HPA heatmaps likewise provide an optional log₂(value + 1) colour mapping, with the source unit shown. Laboratory cell-line heatmaps preserve their supplied matrix values and do not apply an additional transformation. Hover and exported expression values remain the original source values. In the category dropdown, **All** selects all categories and **Clear** deselects all categories. The Search by Gene page is preserved from the previously approved version and is not part of this heatmap colour-control change.

## Expression units and metadata audit (2026-11-06)
- Broad CCLE: TPM (original expression in heatmap, hover, export); optional log₂(TPM + 1) affects colours only. Category dropdown: **Primary disease** (33 labels in the supplied matrix).
- Sanger CMP: TPM (original expression in heatmap, hover, export); optional log₂(TPM + 1) affects colours only. Category dropdown: **Cancer type** (42 labels in the supplied matrix).
- HPA Normal Tissue: nTPM (HPA/GTEx consensus bulk RNA-seq); original supplied matrix has no explicit unit header, so this unit is based on the dataset's provenance.
- HPA Single Cell (154 cell types and 1,175 clusters): nCPM (HPA source expression matrix).
- HPA Cell Lines: nTPM for colour and hover; original TPM and pTPM are also retained as separate metadata.
- Seven laboratory cell-line matrices: **units unverified** from the supplied CSVs; labels say source matrix values, and no additional transformation is applied. Do not interpret as TPM without source documentation.

For all 13 heatmaps, every embedded default expression value was numerically checked against its embedded original source value (0 mismatches). Generic hover and CSV labels were corrected to reflect the source units. The Search by Gene page retains its study-specific units and is unchanged in this update. JavaScript syntax checks passed, but full browser regression testing has not been performed.

## Additional disease-mean heatmaps
- `CellPalmSeq2026_Broad_CCLE_MeanByPrimaryDisease`: 33 primary disease groups; means of original TPM values.
- `CellPalmSeq2026_Sanger_CMP_MeanByCancerType`: 42 cancer type groups; means of original TPM values.
These are supplementary, not replacements for individual cell-line heatmaps.
