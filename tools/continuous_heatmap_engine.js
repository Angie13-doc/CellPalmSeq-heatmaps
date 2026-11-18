// Continuous heatmap (no paging). Every selected column is laid out in one strip;
// a viewport-sized canvas, sticky inside .plot-scroll, draws only the visible part.
// The summary band (.bps-ov) shows the whole selection; click or drag it to jump.
// `layout` keeps its original shape ({n,genes,cols,positions,lookup,width,height},
// positions in full-strip coordinates), so hover and SVG/PNG/CSV export cover the
// whole selection.
const bpsOv=$('.bps-ov'),bpsOvBox=$('.bps-overview'),bpsOvRange=$('.bps-ov-range'),bpsSpacer=$('.bps-spacer');
let bpsState=null,bpsRaf=0,bpsOvBase=null,bpsColourOf=r=>Number(r.Expression);
function bpsColAt(x){if(!layout)return -1;const p=layout.positions;let lo=0,hi=p.length-1,ans=-1;while(lo<=hi){const m=(lo+hi)>>1;if(p[m]<=x){ans=m;lo=m+1}else hi=m-1}return ans>=0&&x<p[ans]+cw?ans:-1}
function bpsFirstAt(x){const p=layout.positions;let lo=0,hi=p.length-1,ans=0;while(lo<=hi){const m=(lo+hi)>>1;if(p[m]+cw<=x)lo=m+1;else{ans=m;hi=m-1}}return lo>=p.length?p.length:ans}
function bpsCategoryOf(c){const r=cells.get(c)||{};const v=broadField==='MatrixMetadata'?(r.MatrixMetadata||{})[typeof broadCategoryField!=='undefined'?broadCategoryField:'']:r[broadField];return String(v||'').split(',')[0].trim()}
function bpsPaletteIndex(v,high){return Math.max(0,Math.min(palette.length-1,Math.floor((high>0?v/high:0)*(palette.length-1))))}
function bpsUpdate(o){
 const n=o.cols.length,genes=o.genes;bpsColourOf=o.colour;
 const boundaries=[];let count=0;for(const g of o.visibleGroups.slice(0,-1)){count+=g.cells.length;if(count>0&&count<n)boundaries.push(count)}const groupGap=12;
 const width=left+n*cw+boundaries.length*groupGap+right,height=top+genes.length*rh+Math.max(bottom,Math.round(bottom*zoomFactor));
 const positions=new Array(n);let b=0;for(let i=0;i<n;i++){while(b<boundaries.length&&i>=boundaries[b])b++;positions[i]=left+i*cw+b*groupGap}
 const lookup=new Map();for(let x=0;x<n;x++)for(let y=0;y<genes.length;y++){const r=values.get(o.cols[x]+'\u0000'+genes[y]);if(r)lookup.set(y*n+x,r)}
 layout={n,genes,cols:o.cols,positions,lookup,width,height};
 // Category labels along the top: only for a single search in original order, and only where
 // categories form a few clean runs (not interleaved, and not one column per category).
 let runs=[];if(o.visibleGroups.length===1&&!rankCells.checked){let cur=null;for(let i=0;i<n;i++){const c=bpsCategoryOf(o.cols[i]);if(!runs.length||c!==cur){cur=c;runs.push({label:c,i0:i,i1:i})}else runs[runs.length-1].i1=i}const distinct=new Set(runs.map(x=>x.label)).size;if(runs.length<2||runs.length>2*distinct||n/runs.length<2)runs=[]}
 bpsState={...o,boundaries,runs};
 bpsSpacer.style.width=width+'px';
 bpsBuildOverview();bpsDraw();
}
function bpsDraw(){
 bpsRaf=0;if(!layout||canvas.hidden){bpsDrawOverviewFrame();return}
 const L=layout,s=bpsState,dpr=Math.min(window.devicePixelRatio||1,2),viewW=Math.max(1,Math.min(scroll.clientWidth||L.width,L.width)),H=L.height;
 const pw=Math.ceil(viewW*dpr),ph=Math.ceil(H*dpr);if(canvas.width!==pw||canvas.height!==ph){canvas.width=pw;canvas.height=ph}canvas.style.width=viewW+'px';canvas.style.height=H+'px';
 const ctx=canvas.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#fff';ctx.fillRect(0,0,viewW,H);
 const sx=scroll.scrollLeft,first=bpsFirstAt(sx+left),genes=L.genes;
 ctx.save();ctx.beginPath();ctx.rect(left-2,0,viewW-left+2,H);ctx.clip();
 if(s.runs.length){ctx.font='bold 11px Arial';ctx.textBaseline='middle';ctx.textAlign='left';for(let k=0;k<s.runs.length;k++){const run=s.runs[k],x0=L.positions[run.i0]-sx,x1=L.positions[run.i1]+cw-sx;if(x1<left||x0>viewW)continue;ctx.fillStyle=k%2?'#e4ebf2':'#eef3f8';ctx.fillRect(x0,4,x1-x0,top-10);const lx=Math.max(x0,left)+4,room=Math.min(x1,viewW)-lx-4;if(room>24&&run.label){ctx.fillStyle='#34648d';let t=run.label;while(t.length>1&&ctx.measureText(t+'…').width>room)t=t.slice(0,-1);ctx.fillText(t===run.label?t:t+'…',lx,top/2-1)}}}
 const maxChars=Math.max(12,Math.floor(32/zoomFactor));
 for(let x=first;x<L.n;x++){const px=L.positions[x]-sx;if(px>viewW)break;
  for(let y=0;y<genes.length;y++){const r=L.lookup.get(y*L.n+x);if(!r)continue;const v=s.colour(r);ctx.fillStyle=Number.isFinite(v)?palette[bpsPaletteIndex(v,s.high)]:'#333';ctx.fillRect(px,top+y*rh,cw-.5,rh-.5)}
  const c=L.cols[x],short=s.label(c),label=short.length>maxChars?short.slice(0,maxChars-1)+'…':short;
  ctx.save();ctx.font=Math.max(8,Math.round(8*zoomFactor))+'px Arial';ctx.fillStyle='#263649';ctx.textAlign='left';ctx.textBaseline='middle';ctx.translate(px+cw/2,top+genes.length*rh+7);ctx.rotate(Math.PI/2);ctx.fillText(label,0,0);ctx.restore()}
 for(let k=0;k<s.boundaries.length;k++){const i=s.boundaries[k],x=L.positions[i]-6-sx;if(x<left||x>viewW)continue;ctx.strokeStyle='#8b9db0';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(x,top-4);ctx.lineTo(x,top+genes.length*rh+2);ctx.stroke()}
 if(s.visibleGroups.length>1){ctx.font='bold 12px Arial';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillStyle='#34648d';let offset=0;for(const g of s.visibleGroups){const x0=L.positions[offset]-sx,x1=L.positions[offset+g.cells.length-1]+cw-sx;if(x1>=left&&x0<=viewW)ctx.fillText(g.label.slice(0,Math.max(5,Math.floor((x1-Math.max(x0,left))/7))),Math.max(x0,left),20);offset+=g.cells.length}}
 ctx.restore();
 ctx.fillStyle='#fff';ctx.fillRect(0,0,left-2,H);
 ctx.font='italic '+Math.max(10,Math.round(10*zoomFactor))+'px Arial';ctx.fillStyle='#263649';ctx.textAlign='right';ctx.textBaseline='middle';genes.forEach((g,i)=>ctx.fillText(g,left-8,top+(i+.5)*rh));
 bpsDrawOverviewFrame();
}
// Summary band: genes top to bottom, every selected column left to right; each pixel
// column shows the highest value among the columns it covers.
function bpsBuildOverview(){
 const s=bpsState,L=layout;if(!s||!L)return;const dpr=Math.min(window.devicePixelRatio||1,2),cssW=Math.max(1,bpsOv.clientWidth),cssH=Math.max(1,bpsOv.clientHeight);
 bpsOv.width=Math.round(cssW*dpr);bpsOv.height=Math.round(cssH*dpr);const w=bpsOv.width,h=bpsOv.height,N=L.n,G=L.genes.length;
 bpsOvBase=document.createElement('canvas');bpsOvBase.width=w;bpsOvBase.height=h;const c=bpsOvBase.getContext('2d');c.fillStyle='#fff';c.fillRect(0,0,w,h);if(!N||!G)return;
 const img=c.createImageData(w,h),buf=img.data,rgb=palette.map(hx=>[1,3,5].map(i=>parseInt(hx.slice(i,i+2),16))),blank=[238,242,246];
 const geneOf=new Array(h);for(let y=0;y<h;y++)geneOf[y]=Math.min(G-1,Math.floor(y*G/h));const mx=new Float64Array(G);
 for(let x=0;x<w;x++){const a=Math.floor(x*N/w),bnd=Math.max(a+1,Math.floor((x+1)*N/w));mx.fill(-Infinity);
  for(let k=a;k<bnd&&k<N;k++)for(let j=0;j<G;j++){const r=L.lookup.get(j*N+k);if(!r)continue;const v=s.colour(r);if(Number.isFinite(v)&&v>mx[j])mx[j]=v}
  for(let y=0;y<h;y++){const m=mx[geneOf[y]],cc=m===-Infinity?blank:rgb[bpsPaletteIndex(m,s.high)],o=(y*w+x)*4;buf[o]=cc[0];buf[o+1]=cc[1];buf[o+2]=cc[2];buf[o+3]=255}}
 c.putImageData(img,0,0);c.fillStyle='#263649';
 const marks=s.boundaries.length?s.boundaries:s.runs.slice(1).map(r=>r.i0);for(const i of marks)c.fillRect(Math.round(i/N*w),0,Math.max(1,Math.round(dpr)),h);
}
function bpsDrawOverviewFrame(){
 const c=bpsOv.getContext('2d');c.setTransform(1,0,0,1,0,0);c.clearRect(0,0,bpsOv.width,bpsOv.height);
 if(!layout||canvas.hidden){bpsOvBox.hidden=true;bpsSpacer.style.width='0px';return}
 // The band is only useful when the heatmap is wider than its view.
 const fits=layout.width<=scroll.clientWidth+1;if(bpsOvBox.hidden!==fits){bpsOvBox.hidden=fits;if(!fits)bpsBuildOverview()}if(fits)return;
 if(bpsOv.width!==Math.round(Math.max(1,bpsOv.clientWidth)*Math.min(window.devicePixelRatio||1,2)))bpsBuildOverview();
 if(bpsOvBase)bpsOv.getContext('2d').drawImage(bpsOvBase,0,0);const N=layout.n;if(!N)return;
 const dpr=Math.min(window.devicePixelRatio||1,2),w=bpsOv.width,viewW=Math.min(scroll.clientWidth||layout.width,layout.width),sx=scroll.scrollLeft;
 const a=Math.min(N-1,bpsFirstAt(sx+left)),bEnd=Math.max(a,bpsFirstAt(sx+viewW)-1);
 const x0=a/N*w,x1=Math.max(x0+3*dpr,(Math.min(N-1,bEnd)+1)/N*w);c.lineWidth=2*dpr;c.strokeStyle='#263649';c.strokeRect(x0+dpr,dpr,Math.max(1,x1-x0-2*dpr),bpsOv.height-2*dpr);
 bpsOvRange.textContent='Showing '+(a+1).toLocaleString()+'–'+(Math.min(N-1,bEnd)+1).toLocaleString()+' of '+N.toLocaleString();
}
function syncScrollControls(){if(!bpsRaf)bpsRaf=requestAnimationFrame(bpsDraw)}
function bpsJump(clientX){if(!layout||!layout.n)return;const rect=bpsOv.getBoundingClientRect(),f=Math.max(0,Math.min(1,(clientX-rect.left)/rect.width)),k=Math.min(layout.n-1,Math.floor(f*layout.n));const viewW=scroll.clientWidth;scroll.scrollLeft=Math.max(0,layout.positions[k]-left-(viewW-left)/2)}
let bpsDragging=false;
bpsOv.addEventListener('pointerdown',e=>{bpsDragging=true;try{bpsOv.setPointerCapture(e.pointerId)}catch(_){}bpsJump(e.clientX)});
bpsOv.addEventListener('pointermove',e=>{if(bpsDragging)bpsJump(e.clientX)});
bpsOv.addEventListener('pointerup',()=>{bpsDragging=false});bpsOv.addEventListener('pointercancel',()=>{bpsDragging=false});
if(window.ResizeObserver){let bpsLastW=0;new ResizeObserver(()=>{const w=scroll.clientWidth;if(w===bpsLastW)return;bpsLastW=w;if(bpsState){bpsBuildOverview();bpsDraw()}}).observe(scroll)}
