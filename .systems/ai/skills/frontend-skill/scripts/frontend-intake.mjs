#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const out = { json: false, strict: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--json") out.json = true;
    else if (arg === "--strict") out.strict = true;
    else if (arg === "--root") out.root = argv[++i];
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!out.root) throw new Error("Missing --root <path>");
  out.root = path.resolve(out.root);
  return out;
}

function readPackage(root) {
  const file = path.join(root, "package.json");
  if (!fs.existsSync(file)) return null;
  try { return JSON.parse(fs.readFileSync(file, "utf8")); }
  catch { return { invalid: true }; }
}

function has(root, relative) { return fs.existsSync(path.join(root, relative)); }

function detectFramework(pkg) {
  if (!pkg || pkg.invalid) return "unknown";
  const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
  if (deps.next) return "next";
  if (deps["react-router"] || deps["react-router-dom"]) return "react-router";
  if (deps.vue || deps["@vue/router"]) return "vue";
  if (deps.svelte || deps["@sveltejs/kit"]) return "svelte";
  if (deps.react) return "react";
  return "unknown";
}

function collect(root, relative, limit = 2000) {
  const target = path.join(root, relative);
  if (!fs.existsSync(target)) return [];
  const result = [];
  const walk = (dir) => {
    if (result.length >= limit) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.name === "node_modules" || entry.name === ".git") continue;
      if (entry.isDirectory()) walk(full);
      else result.push(path.relative(root, full));
    }
  };
  walk(target);
  return result;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!fs.existsSync(args.root) || !fs.statSync(args.root).isDirectory()) throw new Error("Root is not a directory");
  const pkg = readPackage(args.root);
  const framework = detectFramework(pkg);
  const files = [...collect(args.root, "app"), ...collect(args.root, "pages"), ...collect(args.root, "src")];
  const deps = pkg && !pkg.invalid ? Object.keys({ ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) }) : [];
  const result = {
    root: args.root,
    framework,
    package_json: pkg ? (pkg.invalid ? "invalid" : "present") : "missing",
    scripts: pkg && !pkg.invalid ? Object.keys(pkg.scripts || {}) : [],
    dependencies: deps.sort(),
    route_and_source_files: [...new Set(files)].sort(),
    signals: {
      design_system_files: ["components.json", "src/components", "src/ui", "app/globals.css", "src/app/globals.css"].filter((p) => has(args.root, p)),
      test_tooling: ["playwright.config.ts", "playwright.config.js", "vitest.config.ts", "jest.config.js", "cypress.config.ts", "axe.config.js"].filter((p) => has(args.root, p)),
      public_assets: ["public", "static", "assets"].filter((p) => has(args.root, p)),
      invalid_package: Boolean(pkg?.invalid)
    },
    findings: []
  };
  if (result.package_json === "missing") result.findings.push({ severity: "info", code: "package-json-missing", message: "No package.json found; framework detection is limited." });
  if (result.signals.invalid_package) result.findings.push({ severity: "high", code: "package-json-invalid", message: "package.json could not be parsed." });
  if (args.json) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`framework: ${result.framework}`);
    console.log(`package.json: ${result.package_json}`);
    console.log(`scripts: ${result.scripts.join(", ") || "none"}`);
    console.log(`design system signals: ${result.signals.design_system_files.join(", ") || "none"}`);
    console.log(`test tooling: ${result.signals.test_tooling.join(", ") || "none"}`);
    for (const finding of result.findings) console.log(`${finding.severity}: ${finding.code} - ${finding.message}`);
  }
  if (args.strict && result.findings.some((f) => ["high", "critical"].includes(f.severity))) process.exitCode = 1;
}

try { main(); }
catch (error) { console.error(`frontend-intake: ${error.message}`); process.exitCode = 2; }
