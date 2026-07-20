#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function args(argv) {
  const out = { json: false, strict: false, maxBytes: 1048576 };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--root") out.root = argv[++i];
    else if (argv[i] === "--max-bytes") out.maxBytes = Number(argv[++i]);
    else if (argv[i] === "--json") out.json = true;
    else if (argv[i] === "--strict") out.strict = true;
    else throw new Error(`Unknown argument: ${argv[i]}`);
  }
  if (!out.root) throw new Error("Missing --root <path>");
  if (!Number.isFinite(out.maxBytes) || out.maxBytes < 1) throw new Error("Invalid --max-bytes");
  out.root = path.resolve(out.root);
  return out;
}

function walk(dir, result) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, result);
    else result.push(full);
  }
}

function main() {
  const options = args(process.argv.slice(2));
  if (!fs.existsSync(options.root) || !fs.statSync(options.root).isDirectory()) throw new Error("Root is not a directory");
  const files = [];
  for (const folder of ["public", "static", "assets"]) walk(path.join(options.root, folder), files);
  const findings = [];
  const families = new Map();
  for (const file of files) {
    const stat = fs.statSync(file);
    const relative = path.relative(options.root, file);
    const ext = path.extname(file).toLowerCase();
    if (stat.size > options.maxBytes) findings.push({ severity: "medium", code: "large-public-asset", file: relative, bytes: stat.size });
    if (/\b(mock|placeholder|dummy|sample|test-image)\b/i.test(path.basename(file))) findings.push({ severity: "low", code: "mock-like-asset-name", file: relative });
    const family = path.basename(file).replace(/\.[^.]+$/, "").replace(/[-_](regular|medium|bold|semibold|light|italic|black|thin)$/i, "").toLowerCase();
    if (/\.(woff2?|ttf|otf|eot|svg|png|jpe?g|webp|gif)$/.test(ext)) {
      if (!families.has(family)) families.set(family, []);
      families.get(family).push(relative);
    }
  }
  for (const [family, entries] of families) if (entries.length > 3) findings.push({ severity: "low", code: "asset-family-review", family, files: entries });
  const result = { root: options.root, scanned_files: files.map((f) => path.relative(options.root, f)).sort(), findings };
  if (options.json) console.log(JSON.stringify(result, null, 2));
  else { console.log(`scanned files: ${result.scanned_files.length}`); for (const finding of findings) console.log(`${finding.severity}: ${finding.code} ${finding.file || finding.family || ""}`); }
  if (options.strict && findings.some((f) => ["high", "critical"].includes(f.severity))) process.exitCode = 1;
}

try { main(); }
catch (error) { console.error(`check-public-assets: ${error.message}`); process.exitCode = 2; }
