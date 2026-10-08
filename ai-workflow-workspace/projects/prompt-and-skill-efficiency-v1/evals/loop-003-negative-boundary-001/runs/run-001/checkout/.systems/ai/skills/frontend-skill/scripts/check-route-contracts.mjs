#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parse(argv) {
  const out = { json: false, strict: false };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--root") out.root = argv[++i];
    else if (argv[i] === "--json") out.json = true;
    else if (argv[i] === "--strict") out.strict = true;
    else throw new Error(`Unknown argument: ${argv[i]}`);
  }
  if (!out.root) throw new Error("Missing --root <path>");
  out.root = path.resolve(out.root);
  return out;
}

function exists(root, relative) { return fs.existsSync(path.join(root, relative)); }

function main() {
  const options = parse(process.argv.slice(2));
  if (!fs.existsSync(options.root) || !fs.statSync(options.root).isDirectory()) throw new Error("Root is not a directory");
  const packageFile = path.join(options.root, "package.json");
  let deps = {};
  if (fs.existsSync(packageFile)) {
    try { const pkg = JSON.parse(fs.readFileSync(packageFile, "utf8")); deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) }; }
    catch { deps = { __invalid_package_json: true }; }
  }
  const framework = deps.next ? "next" : deps["react-router-dom"] ? "react-router" : deps.vue ? "vue" : deps.svelte ? "svelte" : "unsupported";
  const result = { root: options.root, framework, checks: [], findings: [] };
  if (framework !== "next") {
    result.checks.push({ name: "route-boundary-contract", status: "not-applicable", reason: "The scanner has no framework-specific route contract for this project." });
  } else {
    const appRoot = exists(options.root, "app") ? "app" : exists(options.root, "src/app") ? "src/app" : null;
    const pagesRoot = exists(options.root, "pages") ? "pages" : exists(options.root, "src/pages") ? "src/pages" : null;
    const root = appRoot || pagesRoot;
    if (!root) result.findings.push({ severity: "high", code: "next-route-root-missing" });
    if (appRoot) {
      for (const file of ["loading.tsx", "error.tsx", "not-found.tsx"]) {
        const present = exists(options.root, `${appRoot}/${file}`);
        result.checks.push({ name: file, status: present ? "present" : "missing", path: `${appRoot}/${file}` });
        if (!present) result.findings.push({ severity: "medium", code: `next-${file}-missing`, path: `${appRoot}/${file}` });
      }
    }
    const metadataFiles = ["metadata.ts", "metadata.tsx", "layout.tsx", "generateMetadata.ts", "sitemap.ts", "robots.ts"].filter((file) => root && exists(options.root, `${root}/${file}`));
    result.checks.push({ name: "metadata-signals", status: metadataFiles.length ? "present" : "unknown", files: metadataFiles });
  }
  if (options.json) console.log(JSON.stringify(result, null, 2));
  else { console.log(`framework: ${result.framework}`); for (const check of result.checks) console.log(`${check.status}: ${check.name}`); for (const finding of result.findings) console.log(`${finding.severity}: ${finding.code}`); }
  if (options.strict && result.findings.some((f) => ["high", "critical"].includes(f.severity))) process.exitCode = 1;
}

try { main(); }
catch (error) { console.error(`check-route-contracts: ${error.message}`); process.exitCode = 2; }
