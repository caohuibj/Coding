# Installing the Coding Agent Team into a Project

The installer is repository-scoped. It does not write to `~/.codex`, `$HOME/.agents`, or other global configuration.

## Requirements

- Python 3.11+
- a target project directory, preferably a Git working tree
- Codex available through your normal Codex environment; the CLI is optional for static installation but useful for local smoke testing

## Safe installation

From this toolkit repository:

```bash
python3 scripts/agent_team.py install /path/to/project --dry-run --with-docs
python3 scripts/agent_team.py install /path/to/project --with-docs
python3 scripts/agent_team.py doctor /path/to/project
```

The default install is conservative:

- `.agents/skills/` and `.codex/agents/` are copied only when the destination file is absent or identical;
- conflicting agent/skill files are left untouched and the installer exits non-zero;
- existing `.codex/config.toml` is merged rather than replaced;
- existing Codex model/agent keys with different values are preserved and reported unless `--enforce-config` is explicitly supplied;
- an existing `AGENTS.md` is preserved and a marker-delimited managed section is appended or refreshed;
- `.gitignore` receives only missing runtime-log entries.

Use `--replace-managed-files` only after reviewing conflicts and deciding that this toolkit should own those specific agent/skill paths. Use `--enforce-config` only when you intentionally want the project default to be Sol `high` with the V1 agent cap.

## Project command discovery

The installer conservatively reads explicit `package.json` scripts and common `Makefile` targets. It records detected install, typecheck, lint, test, build, and integration/E2E commands in the managed `AGENTS.md` section.

A missing command is left as `_not detected_`; the installer does not invent a project command. Before relying on autonomous verification, compare the generated section with CI, package scripts, Make/Just tasks, and the project's existing documentation.

## Doctor

`doctor` validates the model/effort/sandbox settings, the seven process skills, the agent hard cap, `AGENTS.md`, Git/worktree availability, and whether at least one validation command can be detected.

Warnings do not block pilot use. Failures should be corrected before using the workflow.

## Upgrade pattern

Run a dry-run first. Existing marker-managed `AGENTS.md` content and missing config keys can be refreshed safely. Changed agent/skill files remain conflict-protected unless `--replace-managed-files` is supplied.

After an upgrade, run `doctor` and the smoke-test checklist in `docs/agent/smoke-tests.md`.
