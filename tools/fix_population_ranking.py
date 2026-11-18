"""Rank populations by the genes that are selected.

BrainPalmSeq2026_* pages: "Cell populations — highest global mean first"
ranked every population by its mean over all 40 genes, computed once when the
page loads, so with one gene ticked the order still followed the 40-gene
average. Populations are now ranked by their mean over the selected genes;
with a single gene, by that gene's value. Gene ranking is unchanged (each
gene's mean across all populations in the dataset). Label and help text say so.

CellPalmSeq2026_HPA_SingleCell_* pages: ticking either ranking option made
the page ignore the search and category filters, and ticking "Genes" also
brought back all 40 genes, so populations were ranked by all genes. They now
rank like the other CellPalmSeq pages: within the current search and filters,
by the selected genes.

Run from the repository root:  python3 tools/fix_population_ranking.py
"""
import glob
import sys

BRAIN = [
    (" // Global rankings: scores always use all populations and all genes, independent of filters.\n",
     " // Genes rank by their mean across all populations; populations rank by their mean over the selected genes.\n"),
    (" function meanForCell(c){return globalCellScores.get(c)??-Infinity}",
     " function meanForCell(c){let sum=0,n=0;for(const g of genes){const r=values.get(c+'\\u0000'+g);"
     "if(r&&Number.isFinite(r.Expression)){sum+=r.Expression;n++}}return n?sum/n:-Infinity}"),
    ("<label><input type=\"checkbox\" class=\"rank-genes\"> Genes — highest global mean first</label>"
     "<label><input type=\"checkbox\" class=\"rank-cells\"> Cell populations — highest global mean first (within each search group)</label>"
     "<div class=\"help\">Ranks use the entire dataset (all genes and cell populations), independent of current filters. "
     "Untick to restore the original order.</div>",
     "<label><input type=\"checkbox\" class=\"rank-genes\"> Genes — highest mean across all populations first</label>"
     "<label><input type=\"checkbox\" class=\"rank-cells\"> Cell populations — highest mean of the selected genes first (within each search group)</label>"
     "<div class=\"help\">Genes are ranked by their mean across every population in the dataset. Populations are ranked by "
     "their mean over the selected genes; with one gene selected, by that gene alone. Untick to restore the original order.</div>"),
]

CELL_HPA = [
    (" // Ranking deliberately ignores tissue, search, and population filters.\n"
     " // A gene ranking covers every population; a population ranking covers every gene.\n"
     " const globalRanking=rankGenes.checked||rankCells.checked;\n"
     " const groups=globalRanking?[{label:'',cells:[...cells.keys()]}]:selection().groups;\n"
     " let genes=rankGenes.checked?[...geneNames]:geneNames.filter(g=>chosen.has(g));\n"
     " const allPopulationNames=[...cells.keys()];\n"
     " function meanForGene(g){let sum=0,n=0;for(const c of allPopulationNames){",
     " // Ranking works within the current search and filters: genes by their mean across the\n"
     " // matching populations, populations by their mean over the selected genes.\n"
     " const groups=selection().groups;\n"
     " let genes=geneNames.filter(g=>chosen.has(g));\n"
     " function meanForGene(g){let sum=0,n=0;for(const group of groups)for(const c of group.cells){"),
]


def fix(path, edits):
    t = open(path, encoding="utf-8").read()
    for old, new in edits:
        if t.count(old) != 1:
            sys.exit(f"{path}: expected exactly one of {old[:70]!r}, found {t.count(old)}")
        t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)
    print("fixed", path)


def main():
    pages = [(p, BRAIN) for p in glob.glob("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html")] + \
            [(p, CELL_HPA) for p in glob.glob("CellPalmSeq2026_HPA_SingleCell_*/CellPalmSeq2026_HPA_SingleCell_*.html")]
    pages = sorted((p, e) for p, e in pages if not p.endswith("_iframe.html"))
    if not pages:
        sys.exit("No pages to fix; run from the repository root.")
    for p, edits in pages:
        fix(p, edits)


if __name__ == "__main__":
    main()
