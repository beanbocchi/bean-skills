# bean-skills

Skills for [Claude Code](https://claude.com/claude-code). Each one is a directory
holding a `SKILL.md` and the scripts it calls.

## Skills

| Skill | What it does |
|---|---|
| [humanizing-writing](humanizing-writing/) | Rewrites prose so it does not read as machine-written. Ships `ai-tells.py`, a checker that flags the vocabulary and formatting habits, and `ai-tells.md`, the catalogue with examples. Works on English and Vietnamese. |
| [capturing-doc-screenshots](capturing-doc-screenshots/) | Produces documentation screenshots from a committed Playwright script, with regions outlined and numbered callouts painted from element locators. Ships `annotate.ts`. |

## Install

Clone the repository and run the installer:

```bash
git clone https://github.com/beanbocchi/bean-skills.git
cd bean-skills
./install.sh
```

That copies every skill into `~/.claude/skills`, where Claude Code finds them in
any project. Restart Claude Code and run `/skills` to see them.

Without a clone:

```bash
curl -fsSL https://raw.githubusercontent.com/beanbocchi/bean-skills/main/install.sh | bash
```

The piped form clones the repository into a temporary directory and deletes it
when it finishes.

### Options

```
./install.sh                          every skill into ~/.claude/skills
./install.sh humanizing-writing       one skill
./install.sh --list                   the skills in this repository
./install.sh --project                into ./.claude/skills, for this project only
./install.sh --project ../other-repo  into another project
./install.sh --link                   symlink instead of copy
./install.sh --force                  overwrite what is installed
./install.sh --uninstall              remove them all
./install.sh --uninstall humanizing-writing
```

`--link` symlinks each skill back to the clone, so an edit in the clone takes
effect on the next Claude Code session without reinstalling. Use it when you are
changing a skill.

A skill installed under `--project` overrides one of the same name in
`~/.claude/skills`.

## Requirements

The installer needs bash and, for the piped form, git. `humanizing-writing` runs
its checker under Python 3 with no packages. `capturing-doc-screenshots` needs
Playwright in the repository it runs against.

## Adding a skill

A skill is a directory at the top level of this repository with a `SKILL.md`
whose front matter carries `name` and `description`. The installer picks up any
directory matching that shape, so a new skill needs no change to `install.sh`.
Write the description as the condition that should trigger the skill, because
that line is what Claude Code reads when deciding whether to load it.

## License

MIT.
