import { cpSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, rmSync, symlinkSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

/** The checkout or installed package this CLI was launched from. */
export const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');

export const userTarget = () => join(homedir(), '.claude', 'skills');
export const projectTarget = (dir = process.cwd()) => join(resolve(dir), '.claude', 'skills');

/**
 * Read `description` out of the YAML front matter, including the indented
 * continuation lines that a long description wraps onto.
 */
function readDescription(skillFile) {
  const text = readFileSync(skillFile, 'utf8');
  const frontMatter = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontMatter) return '';

  const lines = frontMatter[1].split(/\r?\n/);
  const start = lines.findIndex((line) => /^description:/.test(line));
  if (start === -1) return '';

  const parts = [lines[start].replace(/^description:\s*/, '')];
  for (const line of lines.slice(start + 1)) {
    if (!/^\s/.test(line) || line.trim() === '') break;
    parts.push(line.trim());
  }
  return parts.join(' ').trim();
}

/** Every top-level directory holding a SKILL.md, so a new skill needs no code change. */
export function listSkills(root = packageRoot) {
  return readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(join(root, entry.name, 'SKILL.md')))
    .map((entry) => ({
      name: entry.name,
      dir: join(root, entry.name),
      description: readDescription(join(root, entry.name, 'SKILL.md')),
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
}

export function isInstalled(name, target) {
  try {
    lstatSync(join(target, name));
    return true;
  } catch {
    return false;
  }
}

/**
 * Put one skill in the target directory.
 * Returns 'copied', 'linked' or 'skipped'.
 */
export function installSkill(skill, target, { link = false, force = false } = {}) {
  const dest = join(target, skill.name);
  mkdirSync(target, { recursive: true });

  if (isInstalled(skill.name, target)) {
    if (!force) return 'skipped';
    rmSync(dest, { recursive: true, force: true });
  }

  if (link) {
    symlinkSync(skill.dir, dest, 'dir');
    return 'linked';
  }
  cpSync(skill.dir, dest, { recursive: true });
  return 'copied';
}

/** Returns 'removed' or 'missing'. */
export function uninstallSkill(name, target) {
  if (!isInstalled(name, target)) return 'missing';
  rmSync(join(target, name), { recursive: true, force: true });
  return 'removed';
}
