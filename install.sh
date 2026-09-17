#!/usr/bin/env bash
# Install the skills in this repository into a Claude Code skills directory.
# Run ./install.sh --help for options.

set -euo pipefail

REPO_URL="https://github.com/beanbocchi/bean-skills.git"

TARGET="${HOME}/.claude/skills"
MODE="copy"
FORCE=0
ACTION="install"
SOURCE=""
CLONE_DIR=""

say() { printf '%s\n' "$*"; }
err() { printf 'error: %s\n' "$*" >&2; }

usage() {
  cat <<'EOF'
Usage: install.sh [options] [skill ...]

Installs every skill in this repository, or only the skills named as arguments.

Options:
  --user            Install into ~/.claude/skills (default).
  --project [DIR]   Install into DIR/.claude/skills, default the current directory.
  --target DIR      Install into DIR.
  --link            Symlink each skill instead of copying it. Edits in the
                    repository take effect without reinstalling.
  --force           Overwrite a skill that is already installed.
  --list            Print the skills in this repository and exit.
  --uninstall       Remove the named skills from the target, or all of them.
  -h, --help        Print this message.

Examples:
  ./install.sh                          every skill into ~/.claude/skills
  ./install.sh humanizing-writing       one skill
  ./install.sh --project --link         symlink all skills into ./.claude/skills
  ./install.sh --uninstall humanizing-writing
EOF
}

cleanup() {
  if [ -n "$CLONE_DIR" ] && [ -d "$CLONE_DIR" ]; then
    rm -rf "$CLONE_DIR"
  fi
}
trap cleanup EXIT

# Locate the skills. When the script runs from a clone, they sit beside it. When
# it runs from a pipe (curl ... | bash), it clones the repository into a temp
# directory and removes it on exit.
resolve_source() {
  local script_dir
  if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -n "$(find_skills "$script_dir")" ]; then
      SOURCE="$script_dir"
      return
    fi
  fi

  command -v git >/dev/null 2>&1 || {
    err "no skills found beside this script and git is not installed"
    exit 1
  }
  CLONE_DIR="$(mktemp -d)"
  say "Cloning ${REPO_URL}"
  git clone --depth 1 --quiet "$REPO_URL" "$CLONE_DIR"
  SOURCE="$CLONE_DIR"
}

# A skill is any top-level directory holding a SKILL.md.
find_skills() {
  local root="$1" dir
  for dir in "$root"/*/; do
    [ -f "${dir}SKILL.md" ] || continue
    basename "$dir"
  done
}

skill_description() {
  sed -n 's/^description:[[:space:]]*//p' "$1/SKILL.md" | head -1 | cut -c1-90
}

install_one() {
  local name="$1" src="$SOURCE/$1" dest="$TARGET/$1"

  if [ ! -f "$src/SKILL.md" ]; then
    err "no skill named '$name' in $SOURCE"
    return 1
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ "$FORCE" -eq 0 ]; then
      say "skip    $name (already installed, use --force to overwrite)"
      return 0
    fi
    rm -rf "$dest"
  fi

  if [ "$MODE" = "link" ]; then
    ln -s "$src" "$dest"
    say "linked  $name -> $src"
  else
    cp -R "$src" "$dest"
    say "copied  $name"
  fi
}

uninstall_one() {
  local name="$1" dest="$TARGET/$1"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    rm -rf "$dest"
    say "removed $name"
  else
    say "skip    $name (not installed)"
  fi
}

NAMES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --user)      TARGET="${HOME}/.claude/skills" ;;
    --project)
      if [ $# -gt 1 ] && [ -d "$2" ]; then
        TARGET="$(cd "$2" && pwd)/.claude/skills"
        shift
      else
        TARGET="$(pwd)/.claude/skills"
      fi
      ;;
    --target)
      [ $# -ge 2 ] || { err "--target needs a directory"; exit 1; }
      TARGET="$2"; shift ;;
    --link)      MODE="link" ;;
    --force)     FORCE=1 ;;
    --list)      ACTION="list" ;;
    --uninstall) ACTION="uninstall" ;;
    -h|--help)   usage; exit 0 ;;
    -*)          err "unknown option: $1"; usage >&2; exit 1 ;;
    *)           NAMES+=("$1") ;;
  esac
  shift
done

resolve_source

AVAILABLE=()
while IFS= read -r line; do
  [ -n "$line" ] && AVAILABLE+=("$line")
done <<< "$(find_skills "$SOURCE")"

if [ "${#AVAILABLE[@]}" -eq 0 ]; then
  err "no skills found in $SOURCE"
  exit 1
fi

if [ "$ACTION" = "list" ]; then
  for name in "${AVAILABLE[@]}"; do
    printf '%-28s %s\n' "$name" "$(skill_description "$SOURCE/$name")"
  done
  exit 0
fi

if [ "${#NAMES[@]}" -eq 0 ]; then
  NAMES=("${AVAILABLE[@]}")
fi

if [ "$ACTION" = "uninstall" ]; then
  for name in "${NAMES[@]}"; do
    uninstall_one "$name"
  done
  say ""
  say "Target: $TARGET"
  exit 0
fi

mkdir -p "$TARGET"

# A symlink into the temp clone breaks as soon as the clone is removed.
if [ "$MODE" = "link" ] && [ -n "$CLONE_DIR" ]; then
  err "--link needs a clone on disk; run install.sh from a checkout"
  exit 1
fi

status=0
for name in "${NAMES[@]}"; do
  install_one "$name" || status=1
done

say ""
say "Target: $TARGET"
if [ "$status" -eq 0 ]; then
  say "Restart Claude Code, then run /skills to see them."
fi
exit $status
