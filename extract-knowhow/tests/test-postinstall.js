#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");
const { execFileSync } = require("child_process");

const COMMANDS_DIR = path.join(os.homedir(), ".claude", "commands");
const TARGET = path.join(COMMANDS_DIR, "extract-knowhow.md");
const SCRIPT_DIR = path.join(__dirname, "..", "scripts");
const REPORT_TEMPLATE = path.join(__dirname, "..", "templates", "report.html");
const ISSUE_TEMPLATE = path.join(__dirname, "..", "..", ".github", "ISSUE_TEMPLATE", "01-submit-skill.yml");

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

console.log("\nTest: submission form alignment");
const reportTemplate = fs.readFileSync(REPORT_TEMPLATE, "utf-8");
const issueTemplate = fs.readFileSync(ISSUE_TEMPLATE, "utf-8");
assert(reportTemplate.includes('value="PhD Candidate"'), "Report template keeps full role labels for issue prefill");
assert(reportTemplate.includes('value="Principal Investigator (PI)"'), "Report template keeps full PI label for issue prefill");
assert(issueTemplate.includes("- type: input\n    id: role"), "Issue template uses text input for role prefill compatibility");
assert(issueTemplate.includes("Recommended in Claude Code for highest-quality extraction"), "Issue template documents the recommended Claude model setup");

console.log("\nTest: postuninstall.js");
execFileSync(process.execPath, [path.join(SCRIPT_DIR, "postuninstall.js")], { stdio: "pipe" });
assert(!fs.existsSync(TARGET), "Command file removed after uninstall");

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed > 0 ? 1 : 0);
