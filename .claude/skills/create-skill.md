---
name: create-skill
description: Use when creating new Claude Code skills - guides SKILL.md structure, description writing, and file organization
---

# Creating Claude Code Skills

Skills are directories with a `SKILL.md` file that extend Claude's capabilities. Claude auto-discovers them based on the description field.

## Location

```bash
.claude/skills/skill-name/   # Project (shared via git)
~/.claude/skills/skill-name/ # Personal (local only)
```

## SKILL.md Structure

```yaml
---
name: kebab-case-name          # Lowercase, hyphens, numbers. Max 64 chars
description: [WHAT] + [WHEN]   # Max 1024 chars. THIS IS HOW CLAUDE FINDS IT
allowed-tools: Read, Grep      # Optional: restrict to specific tools
---

# Skill Title

## Instructions

Clear, actionable guidance for Claude. Include examples inline if short.
```

## The Description is Everything

Claude decides when to use a skill based ONLY on the description. Be specific about both WHAT and WHEN.

```yaml
# ✓ Good - clear trigger conditions
description: Use when creating pull requests - handles branch naming, commit messages, and PR descriptions

# ✓ Good - specific scope
description: Write SEO-optimized markdown articles with proper frontmatter and structure

# ✗ Bad - vague, no trigger
description: Helps with git stuff

# ✗ Bad - what but no when
description: Formats code according to standards
```

## Supporting Files (Optional)

Most skills only need `SKILL.md`. Add supporting files ONLY when the content is too large or complex for the main file.

```
my-skill/
├── SKILL.md           # Required - main instructions
├── templates.md       # Only if templates are extensive
└── scripts/
    └── helper.sh      # Only if automation is needed
```

**When to add templates.md:**
- Multiple reusable formats (PR templates, code snippets, config examples)
- Content too long to inline in SKILL.md

**When to add scripts/:**
- Automation Claude should execute (build, deploy, data transform)
- Complex multi-step shell commands

Reference them from SKILL.md when relevant:
```markdown
Use the PR template from [templates.md](templates.md).
Run `bash scripts/deploy.sh` to publish.
```

Claude reads supporting files on-demand - don't add them "just in case".

## Checklist

- [ ] `name`: kebab-case, ≤64 chars
- [ ] `description`: includes WHAT it does AND WHEN to use it
- [ ] Instructions are actionable, not vague
- [ ] Tested: ask Claude "what skills handle X?" to verify discovery
