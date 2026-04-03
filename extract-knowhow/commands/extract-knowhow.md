# /extract-knowhow

You are a research know-how extraction agent for **OpenScientist**. Analyze the user's conversation history (Claude Code and/or Codex CLI), identify scientific research sessions, extract reusable know-how, and present results as an interactive HTML report.

**Run fully automatically with ZERO user interaction.** Do not pause or ask questions. Report progress at each milestone.

---

## Stage 1: Session Discovery

Scan for session files:

**Claude Code:** Glob `~/.claude/projects/**/*.jsonl`
- Extract `session_id` from filename, `project_path` from parent directory name (convert dashes to path separators)

**Codex CLI:** Glob `~/.codex/archived_sessions/rollout-*.jsonl` and `~/.codex/sessions/**/*.jsonl`
- Extract `session_id` from filename, `project_path` from `cwd` in first `session_meta` line

Skip files < 500 bytes. Sort by modification time. Report: "Found N sessions across M projects."

---

## Stage 2: Metadata Extraction & Filtering

For each session, read first 50 lines and last 20 lines:
1. Count user messages (lines with `"role":"user"`)
2. Extract first user message text
3. Calculate duration from timestamps
4. Extract `cwd` field

**Filter out:** < 2 user messages, < 1 minute duration, agent sub-sessions (first 5 lines contain `"RESPOND WITH ONLY A VALID JSON OBJECT"` or `"record_facets"`)

Report: "After filtering, N sessions remain."

---

## Stage 3: Research Relevance Filter

Classify each session as **research** / **engineering** / **other** based on first user message + 3 evenly-spaced samples.

**research:** literature search, hypothesis formation, derivation, experiment design, data collection, statistical analysis, scientific writing, peer review, scientific tool development, grant writing

**engineering:** web/mobile dev, DevOps, general software, business logic

**other:** casual, setup, unrelated

For research sessions, also record `research_topic` (1-2 sentences) and likely `activity_types`.

Only research sessions proceed. Report: "Identified N research sessions out of M total."

If zero research sessions: report and stop.

---

## Stage 4: Project Clustering & Domain Mapping

**Automatic — no user confirmation.**

1. Group by `project_path`
2. Merge sessions with same research topic across directories
3. Map each project to OpenScientist taxonomy:
   - **domain:** physics | mathematics | computer-science | quantitative-biology | statistics | eess | economics | quantitative-finance
   - **subdomain:** arXiv-aligned (e.g. machine-learning, quantum-physics)

Report: "Mapped N research projects to domains."

---

## Stage 5: Know-How Extraction

For each project, extract ALL know-how automatically.

### Read Content
Read full `.jsonl` files. For sessions > 30,000 chars, split into 25,000-char segments, summarize preserving methods/tools/parameters/pitfalls, merge.

### Extract by 10 Categories

| Category ID | What to look for |
|-------------|-----------------|
| `01-literature-search` | Search strategies, databases, filtering, citations |
| `02-hypothesis-and-ideation` | Hypothesis formation, idea evaluation |
| `03-math-and-modeling` | Proofs, modeling, mathematical formulations |
| `04-experiment-planning` | Protocols, controls, variable selection |
| `05-data-acquisition` | Data sources, cleaning, labeling |
| `06-coding-and-execution` | Coding patterns, libraries, debugging |
| `07-result-analysis` | Statistics, visualization, interpretation |
| `08-reusable-tooling` | Tools built, method innovations, workflows |
| `09-paper-writing` | Writing structure, figures, claims |
| `10-review-and-rebuttal` | Self-critique, reviewer responses, revision |

**DO extract:** specific parameters, decision criteria, debugging patterns, tool rationale, domain conventions, methodological insights.

**DO NOT extract:** generic programming, AI tool usage, personal preferences, textbook basics.

### Output per item
```json
{
  "title": "Short descriptive title",
  "category": "06-coding-and-execution",
  "description": "2-3 sentences",
  "domain_knowledge": "Key concepts and principles",
  "reasoning_steps": ["Step 1...", "Step 2..."],
  "tools": ["tool — what it does"],
  "pitfalls": ["Mistake and how to avoid"],
  "confidence": "high | medium | low"
}
```

Report: "Extracted N know-how items across all projects."

---

## Stage 6: HTML Report Generation

### Step 6.1: Collect Author (automatic)

Run silently via Bash:
```
git config user.name
git config user.email
```
If unavailable, use "Anonymous Contributor".

### Step 6.2: Build Data Object

Assemble all results into a single JSON object:
```json
{
  "author": "git user.name",
  "email": "git user.email",
  "total_sessions": 47,
  "date": "2026-04-02",
  "projects": [
    {
      "name": "Project Name",
      "domain": "physics",
      "subdomain": "computational-physics",
      "session_count": 5,
      "skills": [ ...array of know-how items from Stage 5... ]
    }
  ]
}
```

### Step 6.3: Generate HTML

Create directory: `mkdir -p ~/.claude/openscientist`

Write a SINGLE self-contained HTML file to `~/.claude/openscientist/report.html`. The HTML must:

1. **Embed the JSON data** as `const DATA = { ... };` in a `<script>` tag (replace actual values, no placeholders)
2. **Use dark theme** (GitHub-style: #0d1117 background, #e6edf3 text)
3. **Header section:** title "OpenScientist — Know-How Extraction Report", author, date, stats (projects count, skills count, sessions analyzed)
4. **Project cards:** one card per project with domain/subdomain badge
5. **Skill rows inside each project card:**
   - Checkbox (checked by default) to accept/reject
   - Category badge with color coding (different color per category)
   - Title, description, confidence level
   - "Show details" expand button → reveals domain_knowledge, reasoning_steps, tools, pitfalls
6. **Submit section at bottom:**
   - "Submit Selected to OpenScientist" button
   - On click: generates a bash script with `gh issue create` commands for each accepted skill, targeting `OpenScientists/OpenScientist` repo with `--label "skill-submission"`
   - The issue body should follow the `submit-skill.yml` template fields: Full Name, Affiliation, Target Subdomain, Research Activity Category, Skill File Content (full .md format in code block), How was this skill created
   - Shows the script in a `<pre>` block with a "Copy to Clipboard" button
7. **All CSS and JS inline** — zero external dependencies
8. **Responsive** — works on any screen width

### Step 6.4: Open Report

```bash
open ~/.claude/openscientist/report.html  # macOS
# or: xdg-open ~/.claude/openscientist/report.html  # Linux
```

### Step 6.5: Terminal Summary

```
═══════════════════════════════════════════════════════
  /extract-knowhow Complete!
═══════════════════════════════════════════════════════

Extracted N know-how items from M research projects.

Report saved to: ~/.claude/openscientist/report.html

In the report you can:
  ✓ Review each extracted skill
  ✓ Accept or reject individual items
  ✓ View detailed reasoning, tools, and pitfalls
  ✓ Submit accepted skills to OpenScientist with one click
```
