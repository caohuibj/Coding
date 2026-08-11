#!/usr/bin/env python3
"""Install and validate the repository-scoped coding agent team."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    print("Python 3.11+ is required (tomllib is part of the standard library).", file=sys.stderr)
    raise SystemExit(2)

SOURCE_ROOT = Path(__file__).resolve().parents[1]
START_MARKER = "<!-- CODING-AGENT-TEAM:START -->"
END_MARKER = "<!-- CODING-AGENT-TEAM:END -->"

EXPECTED_AGENTS = {
    "luna-fast.toml": ("gpt-5.6-luna", "max", "workspace-write"),
    "luna-worker.toml": ("gpt-5.6-luna", "xhigh", "workspace-write"),
    "luna-explorer.toml": ("gpt-5.6-luna", "high", "read-only"),
    "critical-reviewer.toml": ("gpt-5.6", "xhigh", "read-only"),
}
EXPECTED_SKILLS = {
    "feature-design",
    "implementation-planning",
    "orchestrate-implementation",
    "bounded-implementation",
    "systematic-debugging",
    "verification-gate",
    "code-review",
}


def toml_literal(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value)
    raise TypeError(f"Unsupported TOML value: {value!r}")


def section_bounds(lines: list[str], section: str | None) -> tuple[int, int] | None:
    section_re = re.compile(r"^\s*\[([^\]]+)\]\s*(?:#.*)?$")
    if section is None:
        for index, line in enumerate(lines):
            if section_re.match(line):
                return 0, index
        return 0, len(lines)

    start = None
    for index, line in enumerate(lines):
        match = section_re.match(line)
        if not match:
            continue
        if start is not None:
            return start, index
        if match.group(1).strip() == section:
            start = index + 1
    return (start, len(lines)) if start is not None else None


def set_toml_key(lines: list[str], section: str | None, key: str, value: object) -> list[str]:
    bounds = section_bounds(lines, section)
    literal = toml_literal(value)
    key_re = re.compile(rf"^\s*{re.escape(key)}\s*=")

    if bounds is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([f"[{section}]", f"{key} = {literal}"])
        return lines

    start, end = bounds
    for index in range(start, end):
        if key_re.match(lines[index]):
            lines[index] = f"{key} = {literal}"
            return lines

    lines.insert(end, f"{key} = {literal}")
    return lines


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY-RUN write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def find_tree_conflicts(source: Path, target: Path) -> list[str]:
    conflicts: list[str] = []
    for src in sorted(source.rglob("*")):
        if not src.is_file():
            continue
        dst = target / src.relative_to(source)
        if dst.exists() and dst.read_bytes() != src.read_bytes():
            conflicts.append(str(dst))
    return conflicts


def copy_managed_tree(source: Path, target: Path, *, replace: bool, dry_run: bool) -> None:
    for src in sorted(source.rglob("*")):
        if not src.is_file():
            continue
        dst = target / src.relative_to(source)
        content = src.read_bytes()
        if dst.exists() and dst.read_bytes() == content:
            continue
        if dst.exists() and not replace:
            raise RuntimeError(f"Unexpected post-preflight conflict: {dst}")
        if dry_run:
            print(f"DRY-RUN copy {src} -> {dst}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(content)


def detect_package_manager(target: Path, package: dict) -> str:
    declared = str(package.get("packageManager", "")).split("@", 1)[0]
    if declared in {"pnpm", "yarn", "npm", "bun"}:
        return declared
    if (target / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (target / "bun.lock").exists() or (target / "bun.lockb").exists():
        return "bun"
    if (target / "yarn.lock").exists():
        return "yarn"
    return "npm"


def script_command(pm: str, script: str) -> str:
    if pm == "pnpm":
        return f"pnpm run {script}"
    if pm == "yarn":
        return f"yarn {script}"
    if pm == "bun":
        return f"bun run {script}"
    return f"npm run {script}"


def discover_commands(target: Path) -> dict[str, str]:
    commands: dict[str, str] = {}
    package_path = target / "package.json"
    if package_path.exists():
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            package = {}
        pm = detect_package_manager(target, package)
        if pm == "pnpm":
            commands["install"] = "pnpm install --frozen-lockfile" if (target / "pnpm-lock.yaml").exists() else "pnpm install"
        elif pm == "yarn":
            commands["install"] = "yarn install --immutable" if (target / "yarn.lock").exists() else "yarn install"
        elif pm == "bun":
            commands["install"] = "bun install --frozen-lockfile" if ((target / "bun.lock").exists() or (target / "bun.lockb").exists()) else "bun install"
        else:
            commands["install"] = "npm ci" if (target / "package-lock.json").exists() else "npm install"

        scripts = package.get("scripts", {}) if isinstance(package.get("scripts", {}), dict) else {}
        candidates = {
            "typecheck": ["typecheck", "type-check", "check:types", "check-types"],
            "lint": ["lint"],
            "test": ["test", "test:unit", "unit"],
            "build": ["build"],
            "e2e": ["test:e2e", "e2e", "test:integration", "integration"],
        }
        for category, names in candidates.items():
            for name in names:
                if name in scripts:
                    commands[category] = script_command(pm, name)
                    break

    makefile = target / "Makefile"
    if makefile.exists():
        targets = set(re.findall(r"^([A-Za-z0-9_.-]+)\s*:", makefile.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE))
        for category, names in {
            "typecheck": ["typecheck", "type-check"],
            "lint": ["lint"],
            "test": ["test"],
            "build": ["build"],
            "e2e": ["e2e", "integration"],
        }.items():
            if category in commands:
                continue
            for name in names:
                if name in targets:
                    commands[category] = f"make {name}"
                    break
    return commands


def render_project_commands(commands: dict[str, str]) -> str:
    labels = [
        ("Install", "install"),
        ("Typecheck", "typecheck"),
        ("Lint", "lint"),
        ("Unit / targeted tests", "test"),
        ("Build", "build"),
        ("Integration / E2E", "e2e"),
    ]
    lines = []
    for label, key in labels:
        if key in commands:
            lines.append(f"- **{label}:** `{commands[key]}`")
        else:
            lines.append(f"- **{label}:** _not detected; fill only if the repository defines a canonical command_")
    return "\n".join(lines)


def merge_agents_md(target: Path, commands: dict[str, str], dry_run: bool) -> None:
    template = (SOURCE_ROOT / "templates" / "agent-team-section.md").read_text(encoding="utf-8")
    section = template.replace("{{PROJECT_COMMANDS}}", render_project_commands(commands)).strip()
    path = target / "AGENTS.md"
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if START_MARKER in current and END_MARKER in current:
            pattern = re.compile(re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL)
            updated = pattern.sub(section, current, count=1)
        else:
            updated = current.rstrip() + "\n\n" + section + "\n"
    else:
        updated = "# Repository Agent Instructions\n\n" + section + "\n"
    write_text(path, updated, dry_run)


def merge_gitignore(target: Path, dry_run: bool) -> None:
    path = target / ".gitignore"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = current.splitlines()
    for entry in [".agent-team/runs/", ".codex-log/"]:
        if entry not in lines:
            lines.append(entry)
    write_text(path, "\n".join(lines).rstrip() + "\n", dry_run)


def merge_codex_config(target: Path, *, enforce: bool, dry_run: bool) -> list[str]:
    path = target / ".codex" / "config.toml"
    desired = [
        (None, "model", "gpt-5.6"),
        (None, "model_reasoning_effort", "high"),
        ("agents", "enabled", True),
        ("agents", "max_concurrent_threads_per_session", 4),
        ("agents", "interrupt_message", True),
    ]
    warnings: list[str] = []

    if not path.exists():
        write_text(path, (SOURCE_ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"), dry_run)
        return warnings

    data = load_toml(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    for section, key, wanted in desired:
        current_container = data if section is None else data.get(section, {})
        current = current_container.get(key) if isinstance(current_container, dict) else None
        if current is None:
            lines = set_toml_key(lines, section, key, wanted)
        elif current != wanted:
            if enforce:
                lines = set_toml_key(lines, section, key, wanted)
            else:
                warnings.append(f"Preserved existing {section + '.' if section else ''}{key}={current!r}; expected {wanted!r}")

    merged = "\n".join(lines).rstrip() + "\n"
    if not dry_run:
        temp = path.with_suffix(path.suffix + ".agent-team-tmp")
        temp.parent.mkdir(parents=True, exist_ok=True)
        temp.write_text(merged, encoding="utf-8")
        try:
            load_toml(temp)
        finally:
            temp.unlink(missing_ok=True)
    write_text(path, merged, dry_run)
    return warnings


def preflight_install(target: Path, *, replace: bool, with_docs: bool) -> list[str]:
    errors: list[str] = []

    if not replace:
        errors.extend(find_tree_conflicts(SOURCE_ROOT / ".agents" / "skills", target / ".agents" / "skills"))
        errors.extend(find_tree_conflicts(SOURCE_ROOT / ".codex" / "agents", target / ".codex" / "agents"))
        if with_docs:
            src = SOURCE_ROOT / "docs" / "agent" / "architecture.md"
            dst = target / "docs" / "agent" / "coding-agent-team.md"
            if dst.exists() and dst.read_bytes() != src.read_bytes():
                errors.append(str(dst))

    config = target / ".codex" / "config.toml"
    if config.exists():
        try:
            load_toml(config)
        except Exception as exc:
            errors.append(f"{config} is invalid TOML: {exc}")

    agents_md = target / "AGENTS.md"
    if agents_md.exists():
        text = agents_md.read_text(encoding="utf-8", errors="ignore")
        has_start = START_MARKER in text
        has_end = END_MARKER in text
        if has_start != has_end:
            errors.append(f"{agents_md} contains only one agent-team marker; repair the managed block before installing")

    return errors


def print_preflight_errors(errors: list[str]) -> None:
    print("Installation preflight failed; no files were written:", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    print("Resolve the conflicts, or use --replace-managed-files only for paths this toolkit should intentionally own.", file=sys.stderr)


def install(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if not target.exists() or not target.is_dir():
        print(f"Target directory does not exist: {target}", file=sys.stderr)
        return 2

    preflight_errors = preflight_install(target, replace=args.replace_managed_files, with_docs=args.with_docs)
    if preflight_errors:
        print_preflight_errors(preflight_errors)
        return 1

    copy_managed_tree(
        SOURCE_ROOT / ".agents" / "skills",
        target / ".agents" / "skills",
        replace=args.replace_managed_files,
        dry_run=args.dry_run,
    )
    copy_managed_tree(
        SOURCE_ROOT / ".codex" / "agents",
        target / ".codex" / "agents",
        replace=args.replace_managed_files,
        dry_run=args.dry_run,
    )

    warnings = merge_codex_config(target, enforce=args.enforce_config, dry_run=args.dry_run)
    commands = discover_commands(target)
    merge_agents_md(target, commands, args.dry_run)
    merge_gitignore(target, args.dry_run)

    if args.with_docs:
        source_doc = SOURCE_ROOT / "docs" / "agent" / "architecture.md"
        doc_target = target / "docs" / "agent" / "coding-agent-team.md"
        if args.dry_run:
            print(f"DRY-RUN copy {source_doc} -> {doc_target}")
        else:
            doc_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_doc, doc_target)

    for warning in warnings:
        print(f"WARN: {warning}")

    verb = "Would install" if args.dry_run else "Installed"
    print(f"{verb} coding agent team into {target}")
    if not args.dry_run:
        print(f"Next: {sys.executable} {Path(__file__).resolve()} doctor {target}")
    return 0


def parse_frontmatter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    match = re.search(r"^name:\s*([^\n]+)$", text[4:end], re.MULTILINE)
    return match.group(1).strip() if match else None


def run_git(target: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    git = shutil.which("git")
    if not git:
        return None
    return subprocess.run([git, "-C", str(target), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def doctor(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

    def check(condition: bool, message: str, *, warning: bool = False) -> None:
        if condition:
            passes.append(message)
        elif warning:
            warnings.append(message)
        else:
            failures.append(message)

    config_path = target / ".codex" / "config.toml"
    check(config_path.exists(), ".codex/config.toml exists")
    if config_path.exists():
        try:
            config = load_toml(config_path)
            check(config.get("model") == "gpt-5.6", "primary model is gpt-5.6 (Sol)")
            check(config.get("model_reasoning_effort") == "high", "primary reasoning effort is high")
            agents_cfg = config.get("agents", {})
            check(isinstance(agents_cfg, dict) and agents_cfg.get("enabled") is True, "multi-agent is enabled")
            cap = agents_cfg.get("max_concurrent_threads_per_session") if isinstance(agents_cfg, dict) else None
            check(isinstance(cap, int) and 1 <= cap <= 4, "spawned-agent hard cap is <= 4")
            if isinstance(cap, int) and 1 <= cap < 4:
                warnings.append(f"spawned-agent hard cap is {cap}; safe but lower than the V1 default of 4")
        except Exception as exc:
            failures.append(f".codex/config.toml parses correctly: {exc}")

    for filename, (model, effort, sandbox) in EXPECTED_AGENTS.items():
        path = target / ".codex" / "agents" / filename
        check(path.exists(), f"agent {filename} exists")
        if not path.exists():
            continue
        try:
            data = load_toml(path)
            check(data.get("model") == model, f"{filename}: model={model}")
            check(data.get("model_reasoning_effort") == effort, f"{filename}: effort={effort}")
            check(data.get("sandbox_mode") == sandbox, f"{filename}: sandbox={sandbox}")
        except Exception as exc:
            failures.append(f"{filename} parses correctly: {exc}")

    skill_root = target / ".agents" / "skills"
    for name in sorted(EXPECTED_SKILLS):
        skill = skill_root / name / "SKILL.md"
        check(skill.exists(), f"skill {name} exists")
        if skill.exists():
            check(parse_frontmatter_name(skill) == name, f"skill {name} frontmatter matches directory")

    agents_md = target / "AGENTS.md"
    check(agents_md.exists(), "AGENTS.md exists")
    if agents_md.exists():
        text = agents_md.read_text(encoding="utf-8", errors="ignore")
        check("luna_fast" in text and "READY_FOR_REVIEW" in text, "AGENTS.md contains routing/completion policy")
        check(START_MARKER in text and END_MARKER in text, "AGENTS.md has merge-safe managed markers", warning=True)

    git_status = run_git(target, "rev-parse", "--is-inside-work-tree")
    check(git_status is not None and git_status.returncode == 0, "target is a Git working tree")
    worktree_status = run_git(target, "worktree", "list", "--porcelain")
    check(worktree_status is not None and worktree_status.returncode == 0, "git worktree capability is available", warning=True)

    if shutil.which("codex"):
        passes.append("Codex CLI is available on PATH")
    else:
        warnings.append("Codex CLI not found on PATH; static configuration is ready, but CLI smoke tests cannot run here")

    discovered = discover_commands(target)
    validation_commands = {key: value for key, value in discovered.items() if key in {"typecheck", "lint", "test", "build", "e2e"}}
    check(bool(validation_commands), "at least one canonical validation command was auto-detected", warning=True)

    for message in passes:
        print(f"PASS: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    for message in failures:
        print(f"FAIL: {message}")

    print(f"\nSummary: {len(passes)} pass, {len(warnings)} warning, {len(failures)} fail")
    if failures:
        print("NOT READY: fix failures before relying on the workflow.")
        return 1
    print("READY FOR PILOT: run the manual Codex smoke tests in docs/agent/smoke-tests.md.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    install_parser = sub.add_parser("install", help="merge the workflow into a target repository")
    install_parser.add_argument("target")
    install_parser.add_argument("--dry-run", action="store_true", help="show intended file operations without writing")
    install_parser.add_argument("--replace-managed-files", action="store_true", help="replace conflicting agent-team skill/agent files")
    install_parser.add_argument("--enforce-config", action="store_true", help="set the managed Codex model/agent keys to the V1 defaults")
    install_parser.add_argument("--with-docs", action="store_true", help="copy the architecture guide into docs/agent/coding-agent-team.md")
    install_parser.set_defaults(func=install)

    doctor_parser = sub.add_parser("doctor", help="validate an installed target repository")
    doctor_parser.add_argument("target")
    doctor_parser.set_defaults(func=doctor)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
