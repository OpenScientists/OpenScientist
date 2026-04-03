#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");
const { execFileSync } = require("child_process");

const COMMANDS_DIR = path.join(os.homedir(), ".claude", "commands");
const TARGET = path.join(COMMANDS_DIR, "extract-knowhow.md");
const SCRIPT_DIR = path.join(__dirname, "..", "scripts");
const TEMPLATE = path.join(__dirname, "..", "templates", "report.html");

let passed = 0;
let failed = 0;

function assert(condition, msg) {
  if (condition) {
    console.log("  ✓ " + msg);
    passed++;
  } else {
    console.error("  ✗ " + msg);
    failed++;
  }
}

// Clean up any existing file first
if (fs.existsSync(TARGET)) {
  fs.unlinkSync(TARGET);
}

console.log("Test: postinstall.js");
execFileSync(process.execPath, [path.join(SCRIPT_DIR, "postinstall.js")], { stdio: "pipe" });
assert(fs.existsSync(TARGET), "Command file exists after install");

const content = fs.readFileSync(TARGET, "utf-8");
assert(content.includes("extract-knowhow"), "Command file contains expected content");
assert(content.startsWith("#"), "Command file starts with markdown header");
assert(content.includes("Prefer fewer, stronger skills over many weak ones."), "Command includes the stronger skill-selection guidance");
assert(content.includes("Only keep an item if it passes **all** of these checks:"), "Command includes the reuse quality bar");
assert(content.includes("If you cannot write a concrete reasoning protocol or concrete pitfalls"), "Command enforces replicability requirements");

console.log("\nTest: report template invariants");
const template = fs.readFileSync(TEMPLATE, "utf-8");
assert(template.includes("const DATA = __REPORT_DATA__;"), "Template keeps a single DATA placeholder assignment");
assert(!template.includes("__REPORT_DATA__ is replaced by"), "Template does not repeat the placeholder in comments");
assert(template.includes("DATA.institution || ''"), "Template maps institution field from DATA.institution");

console.log("\nTest: postuninstall.js");
execFileSync(process.execPath, [path.join(SCRIPT_DIR, "postuninstall.js")], { stdio: "pipe" });
assert(!fs.existsSync(TARGET), "Command file removed after uninstall");

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed > 0 ? 1 : 0);
