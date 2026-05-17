#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const readline = require("readline");

const root = path.resolve(__dirname, "..");
const home = os.homedir();
const skills = ["ppp", "ppp-cloud"];
const personalTargets = [
  path.join(home, ".agents", "skills"),
  path.join(home, ".copilot", "skills"),
];
const repoLocalTargets = [path.join(process.cwd(), ".github", "skills")];

function parseArgs(argv) {
  const positional = [];
  const flags = new Set();

  for (const arg of argv) {
    if (arg.startsWith("-")) {
      flags.add(arg);
    } else {
      positional.push(arg);
    }
  }

  return {
    command: positional[0] || null,
    dryRun: flags.has("--dry-run"),
    force: flags.has("--force"),
    yes: flags.has("--yes") || flags.has("-y"),
    repoLocal: flags.has("--repo-local"),
    help: flags.has("--help") || flags.has("-h"),
  };
}

function usage() {
  console.log(`AI Engineering Starter Kit

Usage:
  ai-engineering-starter-kit install [--yes] [--dry-run] [--force] [--repo-local]
  ai-engineering-starter-kit uninstall [--yes] [--dry-run] [--repo-local]
  ai-engineering-starter-kit help

Examples:
  npx ai-engineering-starter-kit install --yes
  npx ai-engineering-starter-kit install --dry-run
  npx ai-engineering-starter-kit install --repo-local
`);
}

function log(message = "") {
  console.log(message);
}

function skillVersion(skillName) {
  const src = path.join(root, "skills", skillName, "SKILL.md");
  const content = fs.readFileSync(src, "utf8");
  const match = content.match(/^version:\s*(.+)$/m);
  return match ? match[1].trim() : "unknown";
}

function timestamp() {
  const now = new Date();
  const pad = (value) => String(value).padStart(2, "0");
  return [
    now.getFullYear(),
    pad(now.getMonth() + 1),
    pad(now.getDate()),
    pad(now.getHours()),
    pad(now.getMinutes()),
    pad(now.getSeconds()),
  ].join("");
}

function actionWord(dryRun, verb) {
  return dryRun ? `Would ${verb}` : verb[0].toUpperCase() + verb.slice(1);
}

function runMkdir(destDir, dryRun) {
  if (dryRun) {
    log(`[dry-run] mkdir -p ${destDir}`);
    return;
  }
  fs.mkdirSync(destDir, { recursive: true });
}

function runCopy(src, dest, dryRun) {
  if (dryRun) {
    log(`[dry-run] copy ${src} -> ${dest}`);
    return;
  }
  fs.copyFileSync(src, dest);
}

function runRemove(target, dryRun) {
  if (dryRun) {
    log(`[dry-run] remove ${target}`);
    return;
  }
  fs.rmSync(target, { recursive: true, force: true });
}

function backupFile(filePath, dryRun) {
  const backupPath = `${filePath}.bak.${timestamp()}`;
  runCopy(filePath, backupPath, dryRun);
  log(`${actionWord(dryRun, "back up existing file")} to ${backupPath}`);
}

async function confirmOverwrite(targetFile) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stderr,
  });

  const reply = await new Promise((resolve) => {
    rl.question(`Overwrite ${targetFile}? [y/N] `, resolve);
  });
  rl.close();

  return /^(y|yes)$/i.test(reply.trim());
}

async function shouldOverwrite(targetFile, options) {
  if (!fs.existsSync(targetFile)) {
    return true;
  }

  if (options.force) {
    return true;
  }

  if (options.yes || !process.stdin.isTTY) {
    log(`Exists at ${targetFile} - skipping (use --force to overwrite)`);
    return false;
  }

  const confirmed = await confirmOverwrite(targetFile);
  if (!confirmed) {
    log(`Skipping ${targetFile}`);
    return false;
  }
  return true;
}

async function installSkill(skillName, targetRoot, options) {
  const src = path.join(root, "skills", skillName, "SKILL.md");
  const destDir = path.join(targetRoot, skillName);
  const destFile = path.join(destDir, "SKILL.md");

  if (!fs.existsSync(src)) {
    throw new Error(`Missing skill source: ${src}`);
  }

  runMkdir(destDir, options.dryRun);

  if (!(await shouldOverwrite(destFile, options))) {
    return;
  }

  if (fs.existsSync(destFile)) {
    backupFile(destFile, options.dryRun);
  }

  runCopy(src, destFile, options.dryRun);
  log(`${actionWord(options.dryRun, "install")} ${skillName} ${skillVersion(skillName)} to ${destFile}`);
}

async function installCursorRule(options) {
  const src = path.join(root, "templates", "cursor-ppp-rule.mdc");
  const destDir = path.join(process.cwd(), ".cursor", "rules");
  const destFile = path.join(destDir, "ppp.mdc");

  if (!fs.existsSync(src)) {
    throw new Error(`Missing Cursor rule template: ${src}`);
  }

  if (!fs.existsSync(path.join(process.cwd(), ".cursor"))) {
    log("Cursor not detected in current directory - skipping Cursor rule install.");
    log("To install manually: copy templates/cursor-ppp-rule.mdc to .cursor/rules/ppp.mdc");
    return;
  }

  runMkdir(destDir, options.dryRun);

  if (!(await shouldOverwrite(destFile, options))) {
    return;
  }

  if (fs.existsSync(destFile)) {
    backupFile(destFile, options.dryRun);
  }

  runCopy(src, destFile, options.dryRun);
  log(`${actionWord(options.dryRun, "install")} Cursor rule to ${destFile}`);
}

async function install(options) {
  const targetRoots = options.repoLocal ? repoLocalTargets : personalTargets;

  log("PPP installer");
  log(`Version: ${skillVersion("ppp")}`);
  if (options.repoLocal) {
    log("Mode: repo-local");
  }
  if (options.dryRun) {
    log("Mode: dry-run");
  }
  if (options.force) {
    log("Overwrite mode: force");
  }
  log();

  for (const skill of skills) {
    for (const targetRoot of targetRoots) {
      await installSkill(skill, targetRoot, options);
    }
  }

  log();
  if (!options.repoLocal) {
    await installCursorRule(options);
  }

  log();
  log("Done.");
  log("Important: /ppp works only where your tool loads skills as slash commands.");
  log("Fallback: Use the Plan. Patch. Prove workflow on this prompt:");
  log("<paste prompt>");
}

function removeSkillDirs(targetRoots, options) {
  for (const skill of skills) {
    for (const targetRoot of targetRoots) {
      const targetDir = path.join(targetRoot, skill);
      if (fs.existsSync(targetDir)) {
        runRemove(targetDir, options.dryRun);
        log(`${actionWord(options.dryRun, "remove")} ${targetDir}`);
      } else {
        log(`Not found, skipping: ${targetDir}`);
      }
    }
  }
}

function removeCursorRule(options) {
  const cursorRule = path.join(process.cwd(), ".cursor", "rules", "ppp.mdc");
  if (fs.existsSync(cursorRule)) {
    runRemove(cursorRule, options.dryRun);
    log(`${actionWord(options.dryRun, "remove")} ${cursorRule}`);
  } else {
    log(`Not found, skipping: ${cursorRule}`);
  }
}

function uninstall(options) {
  const targetRoots = options.repoLocal ? repoLocalTargets : personalTargets;

  removeSkillDirs(targetRoots, options);
  if (!options.repoLocal) {
    removeCursorRule(options);
  }

  log("Done.");
}

async function main() {
  const options = parseArgs(process.argv.slice(2));

  if (!options.command || options.help || options.command === "help") {
    usage();
    process.exit(0);
  }

  if (options.command === "install") {
    await install(options);
    return;
  }

  if (options.command === "uninstall") {
    uninstall(options);
    return;
  }

  console.error(`Unknown command: ${options.command}`);
  usage();
  process.exit(1);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
