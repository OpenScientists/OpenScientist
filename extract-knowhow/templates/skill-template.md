---
# REQUIRED FIELDS — fill in all of these before opening a PR
name: your-skill-name                        # lowercase, hyphens only. This is the Claude Code invocation name.
description: >                               # 1-2 sentences: when should this skill be used?
  Describe what this skill does and when to invoke it.
domain: physics                              # physics | mathematics | computer-science | quantitative-biology | statistics | eess | economics | quantitative-finance
subdomain: ""                                # optional: more specific area
category: ""                                 # 01-literature-search | 02-hypothesis-and-ideation | 03-math-and-modeling | 04-experiment-planning | 05-data-acquisition | 06-coding-and-execution | 07-result-analysis | 08-reusable-tooling | 09-paper-writing | 10-review-and-rebuttal
author: "Full Name (Institution)"            # e.g. "Dr. Albert Einstein (ETH Zürich Physics)"
expertise_level: advanced                    # beginner | intermediate | advanced
tags: []                                     # optional: [keyword1, keyword2, ...]
dependencies: []                             # optional: names of other skills this builds on
version: 1.0.0
status: draft                                # leave as draft; reviewer will update after review
reviewed_by: []
---

<!--
  INSTRUCTIONS FOR CONTRIBUTORS
  ─────────────────────────────
  1. Delete these comment blocks before submitting.
  2. Fill in ALL required frontmatter fields above.
  3. Complete each section below. "Required" sections must be present.
  4. Run `python utils/tools/validate.py skills/<domain>/<subdomain>/<your-file>.md` before opening a PR.
  5. See utils/SKILL_SCHEMA.md for full field documentation.
-->

## Purpose
<!-- REQUIRED -->
<!-- One paragraph: what problem does this skill solve? When should it be invoked?
     Example: "Use this skill when analyzing experimental data involving quantum entanglement.
     It guides the AI through Bell inequality calculations and statistical interpretation." -->

## AI Usage Disclaimer
<!-- REQUIRED -->
<!-- Explain that applying this skill can trigger broad edits, long-running tool calls, or high token usage.
     Make clear that the skill is guidance, not a guarantee, and that users should review scope/cost before running it. -->

This skill may trigger substantial file modifications, long-running tool usage, and significant token consumption. Treat it as expert guidance rather than a guarantee of correctness, and review the proposed scope, cost, and downstream effects before letting an AI agent execute it at full depth.

## Tools
<!-- REQUIRED -->
<!-- List the key tools, software, libraries, databases, or instruments used in this domain.
     For each tool, briefly describe what it does and when to use it.
     Example: "BLAST (sequence alignment) — use when comparing DNA/protein sequences against a database." -->

- **[Tool Name]**: what it does, when to use it
- **[Tool Name]**: what it does, when to use it

## Domain Knowledge
<!-- REQUIRED -->
<!-- The core content: key concepts, definitions, equations, established facts.
     Be precise and comprehensive — this is what the AI will draw on. -->

### Key Concepts

### Fundamental Equations / Principles

### Important Results & Theorems

## Reasoning Protocol
<!-- REQUIRED -->
<!-- Numbered steps guiding AI reasoning for this domain. -->

Step 1: 
Step 2: 
Step 3: 

## Common Pitfalls
<!-- REQUIRED -->
<!-- Mistakes, misconceptions, edge cases, and counterintuitive results to watch for. -->

- 

## Examples
<!-- RECOMMENDED -->
<!-- One or more worked examples demonstrating correct application. -->

### Example 1: [Title]

**Problem:**

**Reasoning:**

**Answer:**

## References
<!-- RECOMMENDED -->
<!-- Key papers, textbooks, or resources. Use standard citation format. -->

- 
