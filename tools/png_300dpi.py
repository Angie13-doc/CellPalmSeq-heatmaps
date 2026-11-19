"""PNG figure export at 300 DPI, with the same rule on BrainPalmSeq and CellPalmSeq.

On screen a figure is laid out at 96 px per inch, so drawing it at 300/96 =
3.125x gives 300 DPI at the figure's natural size. Every PNG also records
300 DPI in the file (a pHYs chunk), so other programs open it at the right
print size. Before, BrainPalmSeq drew at 4x (capped at 16,000 px on the
longest side), CellPalmSeq at 4x (capped at 12,000 px per side and 55 million
pixels), and no PNG recorded a DPI.

A figure too wide for 300 DPI at natural size (over 16,000 px on a side or
60 million pixels in total, which browsers can't reliably draw) is saved
smaller, still at 300 DPI, so it prints proportionally smaller; a note under
the buttons suggests Export SVG for full detail. Figures too wide even for
that (under 1x) still ask for SVG, as before.

Run from the repository root:  python3 tools/png_300dpi.py
"""
import glob
import sys

HELPERS = r"""
// PNG export at 300 DPI: draw at 300/96 of the figure's on-screen size (96 px = 1 inch) and
// record 300 DPI in the file. Wider figures are scaled to fit browser limits and print smaller.
const BPS_PNG_DPI=300,BPS_PNG_MAX_SIDE=16000,BPS_PNG_MAX_PIXELS=60e6;
function bpsPngScale(w,h){return Math.min(BPS_PNG_DPI/96,BPS_PNG_MAX_SIDE/w,BPS_PNG_MAX_SIDE/h,Math.sqrt(BPS_PNG_MAX_PIXELS/(w*h)))}
function bpsCrc32(bytes){let crc=0xffffffff;for(let n=0;n<bytes.length;n++){let c=(crc^bytes[n])&0xff;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;crc=(crc>>>8)^c}return (crc^0xffffffff)>>>0}
async function bpsPngWithDpi(blob,dpi){
 const src=new Uint8Array(await blob.arrayBuffer()),ppm=Math.round(dpi/0.0254),phys=new Uint8Array(21),dv=new DataView(phys.buffer);
 dv.setUint32(0,9);phys.set([0x70,0x48,0x59,0x73],4);dv.setUint32(8,ppm);dv.setUint32(12,ppm);phys[16]=1;dv.setUint32(17,bpsCrc32(phys.subarray(4,17)));
 const parts=[src.subarray(0,8)];let i=8;const sv=new DataView(src.buffer,src.byteOffset,src.byteLength);
 while(i<src.length){const len=sv.getUint32(i),type=String.fromCharCode(...src.subarray(i+4,i+8)),end=i+12+len;
  if(type!=='pHYs')parts.push(src.subarray(i,end));if(type==='IHDR')parts.push(phys);i=end}
 return new Blob(parts,{type:'image/png'})}
function bpsPngNote(scale,cssWidth){let note=root.querySelector('.export-note');
 if(!note){note=document.createElement('div');note.className='help export-note';note.setAttribute('role','status');$('.actions').after(note)}
 note.textContent=scale<BPS_PNG_DPI/96-1e-6?'PNG saved at 300 DPI, '+(cssWidth*scale/BPS_PNG_DPI).toFixed(1)+' in wide: this selection is too wide for full size. Use Export SVG for full detail.':''}
"""

BRAIN = [
    ("function bpsFigureExport(format){", HELPERS.lstrip("\n") + "function bpsFigureExport(format){"),
    ("   const factor=Math.min(4,16000/Math.max(W,H));", "   const factor=bpsPngScale(W,H);"),
    ("   out.toBlob(blob=>{if(blob)save(blob,'png');else alert('PNG export failed. Try SVG instead.');},'image/png');",
     "   out.toBlob(async blob=>{if(blob){save(await bpsPngWithDpi(blob,BPS_PNG_DPI),'png');bpsPngNote(factor,W)}"
     "else alert('PNG export failed. Try SVG instead.');},'image/png');"),
]
CELL = [
    ("function cpsFigureSVG(){", HELPERS.lstrip("\n") + "function cpsFigureSVG(){"),
    (" const factor=Math.min(4,12000/fig.width,12000/fig.height,Math.sqrt(55000000/(fig.width*fig.height)));",
     " const factor=bpsPngScale(fig.width,fig.height);"),
    ("  const blob=await new Promise(resolve=>c.toBlob(resolve,'image/png'));",
     "  const raw=await new Promise(resolve=>c.toBlob(resolve,'image/png'));const blob=raw&&await bpsPngWithDpi(raw,BPS_PNG_DPI);"),
    ("+'_heatmap.png');", "+'_heatmap.png');bpsPngNote(factor,fig.width);"),
]


def main():
    pages = [(p, BRAIN) for p in glob.glob("BrainPalmSeq2026_*/BrainPalmSeq2026_*.html")] + \
            [(p, CELL) for p in glob.glob("CellPalmSeq2026_*/CellPalmSeq2026_*.html")]
    pages = sorted(x for x in pages if not x[0].endswith("_iframe.html"))
    if not pages:
        sys.exit("No heatmap pages found; run from the repository root.")
    for path, edits in pages:
        t = open(path, encoding="utf-8").read()
        if "BPS_PNG_DPI" in t:
            sys.exit(f"{path}: already exports PNGs at 300 DPI")
        for old, new in edits:
            if t.count(old) != 1:
                sys.exit(f"{path}: expected exactly one of {old[:60]!r}, found {t.count(old)}")
            t = t.replace(old, new)
        open(path, "w", encoding="utf-8").write(t)
    print(len(pages), "pages updated")


if __name__ == "__main__":
    main()
