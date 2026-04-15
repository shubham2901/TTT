#!/usr/bin/env node
/**
 * TTT plugin installer — copies skills, commands, agents, and schemas into
 * Claude Code / Cursor / Windsurf–style locations (local project or global).
 *
 * Usage:
 *   npx to-the-t
 *   ttt --yes --project .
 *   node bin/install.js --claude --local
 *   node bin/install.js --cursor --global --yes
 *   node bin/install.js --all --local --project /path/to/project
 */

const fs = require("fs");
const path = require("path");
const os = require("os");
const readline = require("readline");

const PKG_ROOT = path.resolve(__dirname, "..");

function printHelp() {
  console.log(`
TTT install — copy skills and assets into your environment

Usage:
  ttt [options]
  node bin/install.js [options]

Options:
  --help, -h          Show this help
  --yes, -y           Non-interactive (use defaults where needed)
  --project <dir>     Target project root (default: cwd)
  --local             Install into the project (default)
  --global            Install into user home (Claude/Cursor/Windsurf skill dirs)
  --claude            Target Claude Code (.claude/skills, .claude/commands)
  --cursor            Target Cursor (.cursor/skills)
  --windsurf          Target Windsurf (~/.windsurf/skills)
  --all               All of the above runtimes
  --with-prompts      Also copy prompts/ and .cursor/rules/ttt.mdc (legacy compat)

Environment:
  TTT_PROJECT         Same as --project
`);
}

function parseArgs(argv) {
  const opts = {
    help: false,
    yes: false,
    project: process.env.TTT_PROJECT || process.cwd(),
    local: true,
    global: false,
    claude: false,
    cursor: false,
    windsurf: false,
    all: false,
    withPrompts: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") opts.help = true;
    else if (a === "--yes" || a === "-y") opts.yes = true;
    else if (a === "--local") {
      opts.local = true;
      opts.global = false;
    } else if (a === "--global") {
      opts.global = true;
      opts.local = false;
    } else if (a === "--claude") opts.claude = true;
    else if (a === "--cursor") opts.cursor = true;
    else if (a === "--windsurf") opts.windsurf = true;
    else if (a === "--all") {
      opts.all = true;
      opts.claude = true;
      opts.cursor = true;
      opts.windsurf = true;
    }
    else if (a === "--with-prompts") opts.withPrompts = true;
    else if (a === "--project") {
      opts.project = path.resolve(argv[++i] || "");
      if (!opts.project) {
        console.error("Missing value for --project");
        process.exit(1);
      }
    } else if (a.startsWith("-")) {
      console.error("Unknown flag:", a);
      process.exit(1);
    }
  }

  return opts;
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  ensureDir(dest);
  fs.cpSync(src, dest, { recursive: true, force: true });
}

function copyGlobSkills(srcRoot, destSkillsRoot) {
  if (!fs.existsSync(srcRoot)) return;
  for (const name of fs.readdirSync(srcRoot, { withFileTypes: true })) {
    if (!name.isDirectory()) continue;
    if (!name.name.startsWith("ttt-")) continue;
    copyDir(path.join(srcRoot, name.name), path.join(destSkillsRoot, name.name));
  }
}

function question(rl, q) {
  return new Promise((resolve) => rl.question(q, resolve));
}

async function interactiveDefaults(opts) {
  if (opts.all || opts.claude || opts.cursor || opts.windsurf) return opts;

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  try {
    console.log("\nTTT — select install target(s):\n  1) Claude Code\n  2) Cursor\n  3) Windsurf\n  4) All\n");
    const pick = (await question(rl, "Choice [1-4] (default 4): ")).trim() || "4";
    const n = pick;
    if (n === "1") opts.claude = true;
    else if (n === "2") opts.cursor = true;
    else if (n === "3") opts.windsurf = true;
    else opts.claude = opts.cursor = opts.windsurf = true;

    console.log("\nScope:\n  1) This project only (local)\n  2) User home (global)\n");
    const scope = (await question(rl, "Choice [1-2] (default 1): ")).trim() || "1";
    if (scope === "2") {
      opts.global = true;
      opts.local = false;
    }

    const proj = (await question(rl, `\nProject root for files & local skills [${opts.project}]: `)).trim();
    if (proj) opts.project = path.resolve(proj);
  } finally {
    rl.close();
  }

  return opts;
}

function installForClaude(projectRoot, global, pkgRoot) {
  const base = global ? path.join(os.homedir(), ".claude") : path.join(projectRoot, ".claude");
  const skillsDir = path.join(base, "skills");
  const commandsDir = path.join(base, "commands", "ttt");
  ensureDir(skillsDir);
  copyGlobSkills(path.join(pkgRoot, "skills"), skillsDir);
  copyDir(path.join(pkgRoot, "commands", "ttt"), commandsDir);

  const agentsDest = path.join(projectRoot, "ttt", "agents");
  ensureDir(agentsDest);
  copyDir(path.join(pkgRoot, "agents"), agentsDest);

  const schemasDest = path.join(projectRoot, "schemas");
  copyDir(path.join(pkgRoot, "schemas"), schemasDest);

  console.log(`[claude] skills → ${skillsDir}`);
  console.log(`[claude] commands → ${commandsDir}`);
  console.log(`[claude] agents → ${agentsDest}`);
  console.log(`[claude] schemas → ${schemasDest}`);
}

function installForCursor(projectRoot, global, pkgRoot) {
  const base = global ? path.join(os.homedir(), ".cursor") : path.join(projectRoot, ".cursor");
  const skillsDir = path.join(base, "skills");
  ensureDir(skillsDir);
  copyGlobSkills(path.join(pkgRoot, "skills"), skillsDir);

  const agentsDest = path.join(projectRoot, "ttt", "agents");
  ensureDir(agentsDest);
  copyDir(path.join(pkgRoot, "agents"), agentsDest);

  const schemasDest = path.join(projectRoot, "schemas");
  copyDir(path.join(pkgRoot, "schemas"), schemasDest);

  console.log(`[cursor] skills → ${skillsDir}`);
  console.log(`[cursor] agents → ${agentsDest}`);
  console.log(`[cursor] schemas → ${schemasDest}`);
}

function installForWindsurf(projectRoot, global, pkgRoot) {
  const base = global
    ? path.join(os.homedir(), ".windsurf")
    : path.join(projectRoot, ".windsurf");
  const skillsDir = path.join(base, "skills");
  ensureDir(skillsDir);
  copyGlobSkills(path.join(pkgRoot, "skills"), skillsDir);

  const agentsDest = path.join(projectRoot, "ttt", "agents");
  ensureDir(agentsDest);
  copyDir(path.join(pkgRoot, "agents"), agentsDest);

  const schemasDest = path.join(projectRoot, "schemas");
  copyDir(path.join(pkgRoot, "schemas"), schemasDest);

  console.log(`[windsurf] skills → ${skillsDir}`);
  console.log(`[windsurf] agents → ${agentsDest}`);
  console.log(`[windsurf] schemas → ${schemasDest}`);
}

function resolvePromptsDir(pkgRoot) {
  const primary = path.join(pkgRoot, "prompts");
  if (fs.existsSync(primary)) return primary;
  const archived = path.join(pkgRoot, "dev-archive", "prompts");
  if (fs.existsSync(archived)) return archived;
  return primary;
}

function installLegacyExtras(projectRoot, pkgRoot) {
  const promptsDest = path.join(projectRoot, "prompts");
  copyDir(resolvePromptsDir(pkgRoot), promptsDest);
  const rulesDir = path.join(projectRoot, ".cursor", "rules");
  ensureDir(rulesDir);
  const ruleSrc = path.join(pkgRoot, ".cursor", "rules", "ttt.mdc");
  if (fs.existsSync(ruleSrc)) {
    fs.copyFileSync(ruleSrc, path.join(rulesDir, "ttt.mdc"));
    console.log(`[legacy] .cursor/rules/ttt.mdc`);
  }
  console.log(`[legacy] prompts/ → ${promptsDest}`);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    printHelp();
    process.exit(0);
  }

  let o = { ...opts };
  if (o.yes && !o.claude && !o.cursor && !o.windsurf) {
    o.claude = true;
    o.cursor = true;
    o.windsurf = true;
  } else if (!o.yes && !o.all && !o.claude && !o.cursor && !o.windsurf) {
    o = await interactiveDefaults(o);
  } else if (o.all) {
    o.claude = o.cursor = o.windsurf = true;
  }

  ensureDir(o.project);

  console.log("\nTTT install");
  console.log("Project root:", o.project);
  console.log("Package root:", PKG_ROOT);
  console.log("");

  if (o.claude) installForClaude(o.project, o.global, PKG_ROOT);
  if (o.cursor) installForCursor(o.project, o.global, PKG_ROOT);
  if (o.windsurf) installForWindsurf(o.project, o.global, PKG_ROOT);

  if (!o.claude && !o.cursor && !o.windsurf) {
    console.error("No runtime selected. Use --claude, --cursor, --windsurf, or --all.");
    process.exit(1);
  }

  if (o.withPrompts) {
    installLegacyExtras(o.project, PKG_ROOT);
  }

  console.log("\nDone. See docs/USER-GUIDE.md for usage.\n");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
