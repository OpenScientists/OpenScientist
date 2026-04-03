# @openscientist/extract-knowhow

> Automatically extract reusable research know-how from your Claude Code / Codex CLI conversation history and generate [OpenScientist](https://github.com/OpenScientists/OpenScientist) skill files.

## What It Does

When you use Claude Code for scientific research — data analysis, paper writing, experiment design, theoretical derivation — your conversations contain valuable tacit knowledge: judgment calls, debugging strategies, tool preferences, and reasoning patterns.

`/extract-knowhow` analyzes your conversation history and extracts this knowledge into structured, reusable skill files that follow the OpenScientist format.

Generated skills should be treated as high-value but potentially resource-intensive guidance: applying one may trigger large edits, long tool runs, or significant token usage depending on the task.

## Install

```bash
npm install -g @openscientist/extract-knowhow
```

This installs the command into both environments automatically:
- **Claude Code** → `~/.claude/commands/extract-knowhow.md`
- **Codex CLI** → `~/.codex/skills/extract-knowhow/SKILL.md`

## Usage

**Claude Code:**
```
/model opus[1m]
/effort max
/extract-knowhow
```

**Codex CLI:**
```
$extract-knowhow
```

The command will:

1. **Discover** all your Claude Code sessions
2. **Filter** to only research-related sessions (ignoring pure engineering/casual conversations)
3. **Cluster** sessions by research project and map to scientific domains
4. **Extract** reusable know-how across 10 categories:
   - Literature & Survey
   - Ideation
   - Formalization
   - Experiment Design
   - Data & Collection
   - Implementation
   - Analysis
   - Tool & Method Development
   - Writing & Publication
   - Peer Review & Rebuttal
5. **Present** a report for your review and confirmation
6. **Generate** OpenScientist-format skill files ready for contribution

## Output

Generated skill files follow the [OpenScientist skill format](https://github.com/OpenScientists/OpenScientist/blob/main/utils/SKILL_SCHEMA.md) with all required sections:

- YAML frontmatter (name, domain, subdomain, author, etc.)
- Purpose, Domain Knowledge, Reasoning Protocol, Common Pitfalls
- Tools, Examples, References

## Contributing Back

After reviewing the generated skills:

- [**Submit via GitHub Issue →**](https://github.com/OpenScientists/OpenScientist/issues/new?template=submit-skill.yml) (just paste the file content — no git required!)
- Or open a PR if you prefer git

## Uninstall

```bash
npm uninstall -g @openscientist/extract-knowhow
```

## Privacy

- All analysis happens locally via your Claude Code session
- Session data is read from `~/.claude/projects/` on your machine
- No data is sent to external servers beyond your normal Claude Code API usage
- You choose which extracted items to keep or discard

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Part of [OpenScientist](https://github.com/OpenScientists/OpenScientist)

> Building the Library of Alexandria for AGI — Accelerating Automated Scientific Discovery.
