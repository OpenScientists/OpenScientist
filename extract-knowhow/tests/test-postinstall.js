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
assert(content.includes("perform **exactly one** peer review using a different AI agent family"), "Command requires exactly one peer review");
assert(content.includes("If the current agent is **Codex CLI**, ask **Claude Code** or **Gemini** to review."), "Command defines Codex peer review routing");
assert(content.includes("\"peer_review\":"), "Command output schema includes peer review metadata");

console.log("\nTest: report template peer review rendering");
const template = fs.readFileSync(TEMPLATE, "utf-8");
assert(template.includes("Peer Review"), "Template includes peer review section");
assert(template.includes("review_status"), "Template includes peer review status handling");
const sampleHtml = template.replace(
  "const DATA = __REPORT_DATA__;",
  "const DATA = " + JSON.stringify({
    author: "Test User",
    email: "test@example.com",
    total_sessions: 1,
    date: "2026-04-03",
    projects: [{
      name: "Test Project",
      domain: "computer-science",
      subdomain: "machine-learning",
      session_count: 1,
      skills: [{
        title: "Test skill",
        category: "06-coding-and-execution",
        description: "Test description",
        domain_knowledge: "Test knowledge",
        reasoning_steps: ["Step 1"],
        tools: ["tool — role"],
        pitfalls: ["pitfall"],
        confidence: "high",
        peer_review: {
          reviewer_agent: "claude-code",
          review_status: "approved",
          notes: ["Looks reusable."]
        }
      }]
    }]
  }) + ";"
);
const scriptMatch = sampleHtml.match(/<script>([\s\S]*)<\/script>/);
assert(Boolean(scriptMatch), "Template contains a script block");
if (scriptMatch) {
  try {
    new Function(scriptMatch[1]);
    assert(true, "Template script parses after peer review data injection");
  } catch (err) {
    assert(false, "Template script parses after peer review data injection");
  }
}

console.log("\nTest: postuninstall.js");
execFileSync(process.execPath, [path.join(SCRIPT_DIR, "postuninstall.js")], { stdio: "pipe" });
assert(!fs.existsSync(TARGET), "Command file removed after uninstall");

console.log("\n" + passed + " passed, " + failed + " failed");
process.exit(failed > 0 ? 1 : 0);
