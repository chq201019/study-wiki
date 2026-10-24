const ts = require('typescript');
const fs = require('fs');
const src = fs.readFileSync('sidebars.ts', 'utf8');
const r = ts.transpileModule(src, { reportDiagnostics: true,
  compilerOptions: { module: ts.ModuleKind.CommonJS } });
const d = r.diagnostics || [];
if (d.length) { console.log('sidebars.ts FAIL'); d.forEach(x => console.log('  ' + x.messageText)); process.exit(1); }
console.log('sidebars.ts OK');
