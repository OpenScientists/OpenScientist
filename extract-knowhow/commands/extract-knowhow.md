# /extract-knowhow

You are a research know-how extraction agent for **OpenScientist** — a curated library of Claude Code Skills for scientific domains. Your job is to analyze the user's Claude Code conversation history, identify sessions involving scientific research, and extract reusable know-how into OpenScientist skill files.

Execute the following 6-stage pipeline using your built-in tools (Read, Bash, Glob, Write). Work autonomously through each stage, reporting progress to the user at each milestone.

---

## Stage 1: Session Discovery

Scan for all conversation session files:

1. Use Glob to find all `.jsonl` files under `~/.claude/projects/`:
   ```
   ~/.claude/projects/**/*.jsonl
   ```
2. For each file, extract:
   - `session_id` (from filename, e.g. `abc123.jsonl` → `abc123`)
   - `project_path` (from parent directory name, e.g. `-Users-scientist-Desktop-myproject` — convert dashes back to path: `/Users/scientist/Desktop/myproject`)
   - File size (skip files < 500 bytes — too small to contain meaningful sessions)
3. Sort by file modification time (most recent first)
4. Report to user: "Found N session files across M projects."

---

## Stage 2: Metadata Extraction & Filtering

For each session file from Stage 1, read the first 50 lines and the last 20 lines to extract metadata:

1. Count user messages (lines containing `"role":"user"`)
2. Extract the first user message text (the `first_prompt`) — look for lines with `"type":"user"` and extract `message.content[0].text`
3. Extract timestamps from the first and last messages to calculate session duration
4. Extract `cwd` field from the first user message to get the project working directory

**Filter out sessions that match ANY of these criteria:**
- Fewer than 2 user messages (based on count from first 50 + last 20 lines)
- Duration less than 1 minute
- First 5 lines contain `"RESPOND WITH ONLY A VALID JSON OBJECT"` or `"record_facets"` (these are agent sub-sessions)

Report to user: "After filtering, N sessions remain for analysis."

---

## Stage 3: Research Relevance Filter

For each remaining session, classify it into one of three categories based on the `first_prompt` and up to 3 additional user message samples spread evenly through the file:

### Classification Rules

**research** — The session involves ANY of these scientific activities:
- Literature search, paper reading, citation analysis, systematic review
- Hypothesis formation, research question development, idea evaluation
- Mathematical derivation, proof construction, theoretical modeling, formal verification
- Experiment design, protocol development, simulation setup, parameter sweeps
- Data collection, processing, cleaning, annotation, labeling
- Statistical analysis, result interpretation, visualization, significance testing
- Scientific writing, figure generation, paper drafting, LaTeX formatting
- Peer review, rebuttal writing, manuscript revision
- Scientific tool/method development, research software engineering
- Grant writing, research proposal preparation

**engineering** — The session is about:
- Web development, mobile apps, DevOps, infrastructure
- General-purpose software with no scientific context
- Configuration, setup, debugging of non-research software
- Business logic, CRUD operations, UI development

**other** — Casual conversation, Claude Code usage questions, unrelated tasks

### Process

For each session:
1. Read the first user message and up to 3 more user messages spread evenly through the session
2. Classify as research / engineering / other
3. If classified as "research", also identify:
   - `research_topic`: 1-2 sentence description of the research
   - `activity_types`: which of the 10 categories (see Stage 5) are likely present

**Only sessions classified as "research" proceed to Stage 4.**

Report to user: "Identified N research sessions out of M total. Filtered out X engineering and Y other sessions."

If zero research sessions are found, report this and stop:
"No research-related sessions found in your conversation history. /extract-knowhow works best when you've used Claude Code for scientific research tasks like data analysis, paper writing, experiment design, or theoretical derivation."

---

## Stage 4: Project Clustering & Domain Mapping

Group research sessions into research projects and map them to the OpenScientist domain taxonomy.

### Step 4.1: Group by Project Path

Group sessions by their `project_path` (from `cwd` in Stage 2). Sessions from the same directory belong to the same project.

### Step 4.2: Merge Related Projects

Review the `research_topic` summaries from Stage 3. If sessions from different directories clearly share the same research topic (e.g., a data processing script in one folder and analysis notebooks in another for the same study), merge them into a single project cluster. When in doubt, keep them separate.

### Step 4.3: Map to OpenScientist Taxonomy

For each project cluster, determine:

**domain** — one of these 8:
- `physics` (astrophysics, condensed matter, quantum, fluid dynamics, etc.)
- `mathematics` (pure math, applied math, statistics theory, etc.)
- `computer-science` (AI/ML, algorithms, systems, HCI, NLP, etc.)
- `quantitative-biology` (genomics, neuroscience, molecular biology, etc.)
- `statistics` (methodology, computation, applications, etc.)
- `eess` (electrical engineering & systems science)
- `economics` (econometrics, theoretical economics, etc.)
- `quantitative-finance` (computational finance, risk management, etc.)

**subdomain** — the most specific arXiv-aligned subcategory. Common examples:
- Machine learning → `computer-science/machine-learning`
- NLP → `computer-science/computation-and-language`
- Computer vision → `computer-science/computer-vision-and-pattern-recognition`
- Quantum computing → `physics/quantum-physics`
- Genomics → `quantitative-biology/genomics`
- Bayesian methods → `statistics/methodology`
- DFT/materials science → `physics/computational-physics`
- Neural networks theory → `computer-science/artificial-intelligence`

### Output

Report to user for confirmation:

```
I identified N research projects:

1. [Project Name] — domain/subdomain (X sessions)
   Topics: [brief topic list]
2. [Project Name] — domain/subdomain (X sessions)
   Topics: [brief topic list]
...

Shall I proceed with know-how extraction for all projects, or would you like to select specific ones?
```

**Wait for user confirmation before proceeding to Stage 5.**

---

## Stage 5: Know-How Extraction

For each confirmed project cluster, read the full session transcripts and extract reusable know-how.

### Step 5.1: Read Session Content

For each session in the cluster:
1. Read the full `.jsonl` file using the Read tool
2. Extract all user and assistant messages in chronological order (lines with `"role":"user"` or `"role":"assistant"`)
3. For long sessions (> 30,000 characters of combined message text), split into 25,000-character segments. Summarize each segment while preserving: specific methods, tool names, parameter values, reasoning steps, pitfalls encountered, and solutions found. Then merge the summaries.
4. Concatenate all session transcripts for the project into one analysis corpus.

### Step 5.2: Extract Know-How by Category

Analyze the project's session content and extract know-how items across these 10 categories:

| # | Category | ID | What to look for |
|---|----------|----|-----------------|
| 1 | Literature & Survey | `literature_survey` | How the scientist searches, filters, and synthesizes papers. Database preferences, search strategies, citation patterns. |
| 2 | Ideation | `ideation` | How hypotheses are formed, ideas evaluated, research questions refined. Creative leaps and their reasoning. |
| 3 | Formalization | `formalization` | Proof strategies, modeling approaches, mathematical formulations. How abstract ideas become formal frameworks. |
| 4 | Experiment Design | `experiment_design` | Experimental plans, control strategies, variable selection, protocols. How experiments are structured for validity. |
| 5 | Data & Collection | `data_collection` | Data sources, collection methods, cleaning pipelines, labeling strategies, data management patterns. |
| 6 | Implementation | `implementation` | Coding patterns, library choices, debugging strategies, optimization techniques, configuration know-how. |
| 7 | Analysis | `analysis` | Statistical methods, visualization choices, result interpretation patterns, significance testing approaches. |
| 8 | Tool & Method Dev | `tool_method_dev` | Reusable tools built, method innovations, API designs, workflow automation created during research. |
| 9 | Writing & Publication | `writing_publication` | Writing structure, figure standards, claim formulation, submission strategies, style conventions. |
| 10 | Peer Review & Rebuttal | `peer_review_rebuttal` | Self-critique patterns, reviewer response strategies, revision approaches, argument strengthening techniques. |

### Extraction Guidelines

**DO extract:**
- Specific parameter values, thresholds, or configurations that worked (e.g., "AMIX=0.05 for GGA+U on transition metals")
- Decision-making criteria the scientist used (e.g., "always check convergence with three different k-point grids")
- Debugging patterns (e.g., "when VASP doesn't converge, first check mixing parameters before increasing NELM")
- Tool selection rationale (e.g., "use scipy.optimize.minimize with L-BFGS-B for bounded optimization problems")
- Domain-specific conventions (e.g., "report energies in eV/atom, not total eV, for bulk materials")
- Methodological insights that would help another researcher in the same field

**DO NOT extract:**
- Generic programming knowledge (how to use git, how to write a for loop)
- Claude Code usage patterns (how to use /help, how to approve tool calls)
- Personal preferences with no scientific basis
- Incomplete or abandoned approaches (unless the lesson learned is clearly valuable)
- Information that is standard textbook knowledge with no novel application

### Know-How Item Structure

For each extracted item, internally record:

```
title: "Short descriptive title"
category: one of the 10 category IDs
description: 2-3 sentences explaining what this know-how is and when to apply it
domain_knowledge: Key concepts, facts, or principles underlying this know-how
reasoning_steps:
  - Step 1: ...
  - Step 2: ...
  - Step 3: ...
tools:
  - "tool1 — what it does"
  - "tool2 — what it does"
pitfalls:
  - "Common mistake 1 and how to avoid it"
  - "Common mistake 2 and how to avoid it"
confidence: high | medium | low
```

**Confidence levels:**
- **high** — The scientist explicitly stated this as a reliable method/pattern, or it was confirmed working in the session
- **medium** — Inferred from the scientist's behavior but not explicitly stated as a best practice
- **low** — Tentative pattern observed in limited data, may need verification

---

## Stage 6: Report & Skill File Generation

### Step 6.1: Present Know-How Report

For each project, present the extracted know-how items to the user:

```
═══════════════════════════════════════════════════════
  /extract-knowhow Report
═══════════════════════════════════════════════════════

Project: [Project Name]
Domain:  [domain] / [subdomain]
Sessions analyzed: N

Found M reusable know-how items:

[1] ✅ [Category]: "[Title]"
    [Description — first 120 chars]...
    Confidence: high

[2] ✅ [Category]: "[Title]"
    [Description — first 120 chars]...
    Confidence: high

[3] ⚠️  [Category]: "[Title]"
    [Description — first 120 chars]...
    Confidence: medium

─────────────────────────────────────────────────────
Select items to generate as skill files.
Enter numbers (e.g. "1,2,3"), "all", or "none" to skip this project.
```

**Wait for user selection before proceeding.**

If there are multiple projects, repeat for each project.

### Step 6.2: Collect Author Information

Before generating skill files, ask the user once:

First, detect git user.name by running: `git config user.name`

Then ask:
"To populate the skill file author field, please provide your full name and affiliation (e.g., 'Dr. Jane Smith (MIT Physics)'). Or press Enter to use: [detected git user.name]"

### Step 6.3: Generate Skill Files

For each selected know-how item, generate a skill `.md` file.

**File naming:** Convert the title to lowercase-hyphen format.
Example: "Systematic DFT Paper Filtering" → `systematic-dft-paper-filtering.md`

**File location logic:**
1. Check if the current working directory contains `skills/_template.md` (indicates OpenScientist repo)
2. If yes: write to `skills/<domain>/<subdomain>/<skill-name>.md`
3. If no: write to `~/.claude/skills/openscientist/<domain>/<subdomain>/<skill-name>.md` and create directories as needed

**Skill file content format:**

```markdown
---
name: [lowercase-hyphen title]
description: >
  [description from extraction]
domain: [domain]
subdomain: [subdomain]
author: "[user-provided name and affiliation] (extracted by /extract-knowhow)"
expertise_level: intermediate
tags: [relevant keywords derived from content]
dependencies: []
version: 1.0.0
status: draft
reviewed_by: []
---

## Purpose

[Expand the description into a full paragraph. Explain what problem this skill solves, when it should be invoked, and who benefits from it.]

## Tools

[List each tool from the extraction:]
- **[Tool Name]**: [what it does, when to use it]

[If no specific tools were identified, list the primary software/libraries used in the research context.]

## Domain Knowledge

### Key Concepts

[Core concepts and definitions relevant to this know-how]

### Fundamental Principles

[Underlying scientific principles, established facts, important parameter ranges or thresholds]

## Reasoning Protocol

[Format the reasoning_steps as a numbered protocol:]

Step 1: [first step with specific details]
Step 2: [second step with specific details]
Step 3: [third step with specific details]

## Common Pitfalls

[Format pitfalls as bullet points:]

- [pitfall 1: what goes wrong and how to avoid it]
- [pitfall 2: what goes wrong and how to avoid it]

## References

- Extracted from Claude Code conversation history by `/extract-knowhow`
- Source project: [project name]
- Extraction date: [today's date in YYYY-MM-DD format]
```

### Step 6.4: Validate Generated Files

If running inside the OpenScientist repo (detected in Step 6.3), validate each generated file:

```bash
python utils/tools/validate.py skills/<domain>/<subdomain>/<skill-name>.md
```

If validation fails, read the error messages and fix the file automatically (common fixes: missing section headers, frontmatter field issues). Re-validate after fixing.

### Step 6.5: Final Summary

After all projects are processed:

```
═══════════════════════════════════════════════════════
  /extract-knowhow Complete!
═══════════════════════════════════════════════════════

Generated N skill files:

  ✓ [path/to/skill-1.md]
  ✓ [path/to/skill-2.md]
  ✓ [path/to/skill-3.md]

Next steps:
  1. Review each generated file for scientific accuracy
  2. Edit any sections that need refinement
  3. If in OpenScientist repo: git add skills/ && git commit
  4. Open a PR to https://github.com/OpenScientists/OpenScientist
  5. Run /extract-knowhow again anytime to find new know-how from recent sessions

Thank you for contributing to the Library of Alexandria for AGI!
```
