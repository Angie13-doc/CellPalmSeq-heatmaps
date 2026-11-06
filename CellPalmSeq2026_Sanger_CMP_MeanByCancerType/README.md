# CellPalmSeq2026_Sanger_CMP_MeanByCancerType

Derived from the original Sanger_CMP source TPM matrix. Each value is the arithmetic mean of original TPM values across cell lines with the exact source `Cancer type` label. Groups are not merged or inferred. Cell-line count and contributing names are preserved per gene in hover and CSV. Optional log₂(mean TPM + 1) is for colour mapping only; it is not an average of transformed values.

Source expression is TPM. Each disease category is the arithmetic mean of original cell-line TPM values; number of contributing cell lines is included in hover. Heatmap colours default to mean TPM, with optional log₂(mean TPM + 1) colour scaling. Same CellPalmSeq/BrainPalmSeq heatmap layout as individual datasets.
