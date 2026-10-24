const fs = require('fs');
const path = require('path');
const {execFileSync} = require('child_process');

const buildDir = path.join(__dirname, '..', 'build');
const src = path.join(buildDir, 'search-index.json');
const destDir = path.join(buildDir, 'assets');
const dest = path.join(destDir, 'search-index.js');

if (!fs.existsSync(src)) {
  console.error('[postbuild] 未找到 search-index.json，跳过');
  process.exit(0);
}

fs.mkdirSync(destDir, {recursive: true});
fs.copyFileSync(src, dest);
fs.rmSync(src, {force: true});

// 预压缩，服务器端 nginx 直接吐 .gz
try {
  execFileSync('gzip', ['-9', '-k', '-f', dest], {stdio: 'inherit'});
} catch {
  console.warn('[postbuild] 本地无 gzip，跳过预压缩（服务器上有 gzip_static 兜底）');
}

const kb = (fs.statSync(dest).size / 1024).toFixed(0);
console.log(`[postbuild] search-index -> ${dest} (${kb} KB)`);