// minimal build script for static site
const fs = require('fs');
const path = require('path');
const { minify } = require('html-minifier-terser');
const esbuild = require('esbuild');

const srcDir = path.join(__dirname, 'src');
const outDir = path.join(__dirname, 'dist');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function build() {
  ensureDir(outDir);

  // handle HTML
  const htmlPath = path.join(srcDir, 'index.html');
  let html = fs.readFileSync(htmlPath, 'utf-8');
  html = await minify(html, {
    collapseWhitespace: true,
    removeComments: true,
    removeRedundantAttributes: true,
    useShortDoctype: true,
    minifyCSS: true,
    minifyJS: true,
  });
  fs.writeFileSync(path.join(outDir, 'index.html'), html);

  // minify and copy CSS
  const cssSrc = path.join(srcDir, 'styles.css');
  if (fs.existsSync(cssSrc)) {
    const cssContent = fs.readFileSync(cssSrc, 'utf-8');
    const cssMin = esbuild.transformSync(cssContent, { loader: 'css', minify: true }).code;
    fs.writeFileSync(path.join(outDir, 'styles.css'), cssMin);
  }

  // minify and copy JS
  const jsSrc = path.join(srcDir, 'script.js');
  if (fs.existsSync(jsSrc)) {
    const jsResult = esbuild.buildSync({
      entryPoints: [jsSrc],
      outfile: path.join(outDir, 'script.js'),
      bundle: false,
      minify: true,
      platform: 'browser'
    });
  }

  // copy remaining files (images, favicon, etc.)
  const items = fs.readdirSync(srcDir);
  for (const item of items) {
    if (item === 'index.html' || item === 'styles.css' || item === 'script.js') continue;
    const srcPath = path.join(srcDir, item);
    const destPath = path.join(outDir, item);
    const stat = fs.statSync(srcPath);
    if (stat.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
  console.log('Build complete: dist/');
}

function copyRecursive(src, dest) {
  ensureDir(dest);
  for (const name of fs.readdirSync(src)) {
    const srcPath = path.join(src, name);
    const destPath = path.join(dest, name);
    const stat = fs.statSync(srcPath);
    if (stat.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

build().catch(err => {
  console.error(err);
  process.exit(1);
});
