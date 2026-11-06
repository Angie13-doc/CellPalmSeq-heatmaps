# CellPalmSeq 2026 — release QA report

## Completed static checks
- 15 standalone heatmap explorers and Search by Gene are included.
- Updated the existing bottom hover **Expression** field in 8 TPM/nTPM/nCPM explorers, including both averaged datasets.
- The active colour-transform control determines the displayed hover value and correct transformed units.
- Search by Gene replaced with the user-approved clean-hover version.
- Source matrices, iframe files, and seven laboratory-line explorers are preserved. Their source units remain explicitly unverified where appropriate.
- All archive members tested for ZIP integrity.
- All embedded JavaScript scripts passed Node.js syntax checks.

## Not yet validated
- Interactive browser tests of hovering, filtering, ranking, and exporting.
- Independent source-data numerical verification and mean-group membership checks.
- End-to-end GitHub Pages and WordPress deployment.

Do not treat this archive as browser-validated until these tests pass.
