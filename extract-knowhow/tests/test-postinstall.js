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
const SKILL_TEMPLATE = path.join(__dirname, "..", "templates", "skill-template.md");

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

console.log("\nTest: disclaimer templates");
const template = fs.readFileSync(TEMPLATE, "utf-8");
const skillTemplate = fs.readFileSync(SKILL_TEMPLATE, "utf-8");
assert(template.includes("## AI Usage Disclaimer"), "Generated report skill markdown includes AI usage disclaimer");
assert(skillTemplate.includes("## AI Usage Disclaimer"), "Manual skill template includes AI usage disclaimer");
assert(skillTemplate.includes("significant token consumption"), "Manual skill template warns about token cost");

console.log("\nTest: postuninstall.js");
execFileSync(process.execPath, [path.join(SCRIPT_DIR, "postuninstall.js")], { stdio: "pipe" });
assert(!fs.existsSync(TARGET), "Command file removed after uninstall");

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed > 0 ? 1 : 0);
