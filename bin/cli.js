#!/usr/bin/env node
import * as p from '@clack/prompts';
import { Command } from 'commander';
import pc from 'picocolors';

import {
  installSkill,
  isInstalled,
  listSkills,
  projectTarget,
  uninstallSkill,
  userTarget,
} from '../src/skills.js';

const skills = listSkills();

function stop(message) {
  p.cancel(message);
  process.exit(1);
}

function bail(value) {
  if (p.isCancel(value)) {
    p.cancel('Cancelled.');
    process.exit(0);
  }
  return value;
}

/** Turn --user / --project / --target into one directory. */
function targetFrom(options) {
  if (options.target) return options.target;
  if (options.project !== undefined) {
    return projectTarget(typeof options.project === 'string' ? options.project : process.cwd());
  }
  return userTarget();
}

function resolveNames(names) {
  if (names.length === 0) return skills;
  const known = new Map(skills.map((skill) => [skill.name, skill]));
  const missing = names.filter((name) => !known.has(name));
  if (missing.length > 0) {
    stop(`No skill named ${missing.map((name) => pc.bold(name)).join(', ')}. Run ${pc.bold('bean-skills list')}.`);
  }
  return names.map((name) => known.get(name));
}

function report(results, target) {
  for (const { name, outcome } of results) {
    if (outcome === 'skipped') {
      p.log.warn(`${name} ${pc.dim('already installed, pass --force to overwrite')}`);
    } else {
      p.log.success(`${name} ${pc.dim(outcome)}`);
    }
  }
  p.log.message(`Target ${pc.dim(target)}`);
}

function runInstall(chosen, target, { link, force }) {
  if (link && !existsAsCheckout()) {
    stop('--link needs a clone on disk. Clone the repository and run ./bin/cli.js from it.');
  }
  return chosen.map((skill) => ({
    name: skill.name,
    outcome: installSkill(skill, target, { link, force }),
  }));
}

/** npx unpacks into a cache directory that it may clear, so a symlink there would dangle. */
function existsAsCheckout() {
  return !process.env.npm_config_cache || !import.meta.url.includes('_npx');
}

async function interactive() {
  p.intro(pc.inverse(pc.cyan(' bean-skills ')));

  if (skills.length === 0) stop('No skills found next to this CLI.');

  const where = bail(
    await p.select({
      message: 'Where should they go?',
      options: [
        { value: 'user', label: userTarget(), hint: 'every project' },
        { value: 'project', label: projectTarget(), hint: 'this project only' },
      ],
    }),
  );
  const target = where === 'user' ? userTarget() : projectTarget();

  const names = bail(
    await p.multiselect({
      message: 'Which skills?',
      options: skills.map((skill) => ({
        value: skill.name,
        label: isInstalled(skill.name, target) ? `${skill.name} ${pc.yellow('(installed)')}` : skill.name,
        hint: skill.description.slice(0, 70),
      })),
      initialValues: skills.map((skill) => skill.name),
      required: true,
    }),
  );
  const chosen = skills.filter((skill) => names.includes(skill.name));

  // Symlinking only makes sense from a clone. Under npx the package sits in a
  // cache directory that npm may clear, which would leave the link dangling.
  const link = !existsAsCheckout()
    ? false
    : bail(
        await p.select({
          message: 'Copy or symlink?',
          options: [
            { value: false, label: 'Copy', hint: 'a snapshot of the files' },
            { value: true, label: 'Symlink', hint: 'edits in this clone apply without reinstalling' },
          ],
        }),
      );

  let force = false;
  const clashes = chosen.filter((skill) => isInstalled(skill.name, target));
  if (clashes.length > 0) {
    force = bail(
      await p.confirm({
        message: `${clashes.length} of these are already installed. Overwrite?`,
        initialValue: false,
      }),
    );
  }

  const spin = p.spinner();
  spin.start(link ? 'Linking' : 'Copying');
  const results = runInstall(chosen, target, { link, force });
  spin.stop(`${results.filter((r) => r.outcome !== 'skipped').length} of ${results.length} installed`);

  report(results, target);
  p.outro(`Restart Claude Code, then run ${pc.bold('/skills')} to see them.`);
}

const program = new Command();

program
  .name('bean-skills')
  .description('Install Claude Code skills from this repository.')
  .version('0.1.0')
  .action(interactive);

const withTargetOptions = (command) =>
  command
    .option('--user', 'install into ~/.claude/skills (default)')
    .option('--project [dir]', 'install into <dir>/.claude/skills, default the current directory')
    .option('--target <dir>', 'install into <dir>');

withTargetOptions(
  program
    .command('install')
    .description('install the named skills, or all of them')
    .argument('[skills...]', 'skill names, default all'),
)
  .option('--link', 'symlink each skill instead of copying it')
  .option('--force', 'overwrite a skill that is already installed')
  .action((names, options) => {
    const target = targetFrom(options);
    const chosen = resolveNames(names);
    p.intro(pc.inverse(pc.cyan(' bean-skills ')));
    const results = runInstall(chosen, target, { link: !!options.link, force: !!options.force });
    report(results, target);
    p.outro(`Restart Claude Code, then run ${pc.bold('/skills')} to see them.`);
  });

withTargetOptions(
  program
    .command('uninstall')
    .description('remove the named skills, or all of them')
    .argument('[skills...]', 'skill names, default all'),
).action((names, options) => {
  const target = targetFrom(options);
  const chosen = resolveNames(names);
  p.intro(pc.inverse(pc.cyan(' bean-skills ')));
  for (const skill of chosen) {
    const outcome = uninstallSkill(skill.name, target);
    if (outcome === 'removed') p.log.success(`${skill.name} removed`);
    else p.log.warn(`${skill.name} ${pc.dim('not installed')}`);
  }
  p.outro(`Target ${target}`);
});

withTargetOptions(program.command('list').description('print the skills in this repository')).action(
  (options) => {
    const target = targetFrom(options);
    const width = Math.max(...skills.map((skill) => skill.name.length));
    for (const skill of skills) {
      const mark = isInstalled(skill.name, target) ? pc.green('*') : ' ';
      const room = Math.max((process.stdout.columns || 80) - width - 6, 20);
      console.log(`${mark} ${pc.bold(skill.name.padEnd(width))}  ${pc.dim(skill.description.slice(0, room))}`);
    }
    console.log(pc.dim(`\n* installed in ${target}`));
  },
);

program.parseAsync(process.argv).catch((error) => stop(error.message));
