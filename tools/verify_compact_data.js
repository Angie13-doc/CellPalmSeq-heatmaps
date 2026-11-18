// Check that a compacted heatmap page rebuilds exactly the data of the original page.
// Usage: node tools/verify_compact_data.js ORIGINAL.html COMPACT.html [ORIGINAL.html COMPACT.html ...]
// Runs the page's own bpsData() decoder and compares JSON.stringify of the result with
// JSON.stringify(JSON.parse(original data)): same rows, field order, values and row order.
const fs = require('fs');
const DATA = /<script type="application\/json" class="bps-data">([\s\S]*?)<\/script>/;
function decoderFrom(html) {
  const start = html.indexOf('function bpsData(){');
  const end = html.indexOf('return bpsData.cache=out}', start);
  if (start < 0 || end < 0) throw new Error('decoder not found');
  return html.slice(start, end + 'return bpsData.cache=out}'.length);
}
let failed = 0;
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i += 2) {
  const orig = fs.readFileSync(args[i], 'utf8'), comp = fs.readFileSync(args[i + 1], 'utf8');
  const expected = JSON.stringify(JSON.parse(DATA.exec(orig)[1]));
  const text = DATA.exec(comp)[1];
  const fakeDocument = { getElementById: () => ({ querySelector: () => ({ textContent: text }) }) };
  const bpsData = new Function('document', decoderFrom(comp) + '\nreturn bpsData;')(fakeDocument);
  const actual = JSON.stringify(bpsData());
  const same = actual === expected;
  if (!same) failed++;
  console.log((same ? 'SAME ' : 'DIFF ') + args[i + 1] + '  (' + expected.length + ' chars of data)');
}
process.exit(failed ? 1 : 0);
