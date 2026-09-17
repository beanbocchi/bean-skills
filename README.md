# bean-skills

Skills for [Claude Code](https://claude.com/claude-code). Each one is a directory
holding a `SKILL.md` and the scripts it calls.

## Skills

| Skill | What it does |
|---|---|
| [humanizing-writing](humanizing-writing/) | Rewrites prose so it does not read as machine-written. Ships `ai-tells.py`, a checker that flags the vocabulary and formatting habits, and `ai-tells.md`, the catalogue with examples. Works on English and Vietnamese. |
| [capturing-doc-screenshots](capturing-doc-screenshots/) | Produces documentation screenshots from a committed Playwright script, with regions outlined and numbered callouts painted from element locators. Ships `annotate.ts`. |

## Install

```bash
npx github:beanbocchi/bean-skills
```

That asks where to put the skills, which ones to take, and whether to copy or
symlink them. Nothing is installed globally. Claude Code runs on Node, so the
`npx` is already on the machine.

Restart Claude Code afterwards and run `/skills` to see them.

### Without the questions

```bash
npx github:beanbocchi/bean-skills install                    # all of them
npx github:beanbocchi/bean-skills install humanizing-writing # one
npx github:beanbocchi/bean-skills list
npx github:beanbocchi/bean-skills uninstall humanizing-writing
```

`install` and `uninstall` take:

| Flag | Effect |
|---|---|
| `--user` | Into `~/.claude/skills`, where Claude Code reads them in every project. The default. |
| `--project [dir]` | Into `<dir>/.claude/skills`, default the current directory. Overrides a skill of the same name in `~/.claude/skills`. |
| `--target <dir>` | Into a directory you name. |
| `--link` | Symlink instead of copy, so an edit in the clone applies without reinstalling. Needs a clone, not `npx`. |
| `--force` | Overwrite a skill that is already installed. |

### From a clone

```bash
git clone https://github.com/beanbocchi/bean-skills.git
cd bean-skills
npm install
node bin/cli.js
```

Use this to change a skill. `node bin/cli.js install --link` points
`~/.claude/skills` back at the clone.

## Requirements

Node 18 or newer for the installer. `humanizing-writing` runs its checker under
Python 3 with no packages. `capturing-doc-screenshots` needs Playwright in the
repository it runs against.

## Adding a skill

A skill is a directory at the top level of this repository with a `SKILL.md`
whose front matter carries `name` and `description`. The installer lists any
directory matching that shape, so a new skill needs no change to the CLI. Write
the description as the condition that should trigger the skill, because that line
is what Claude Code reads when deciding whether to load it.

## License

MIT.
