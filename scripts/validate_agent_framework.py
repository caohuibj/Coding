#!/usr/bin/env python3
"""Validate stable repository-scoped agent framework contracts."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "docs/agent/architecture.md",
    "docs/agent/github-workflow.md",
    ".codex/config.toml",
    ".codex/agents/luna-fast.toml",
    ".codex/agents/luna-worker.toml",
    ".codex/agents/luna-explorer.toml",
    ".codex/agents/critical-reviewer.toml",
    ".agents/skills/feature-design/SKILL.md",
    ".agents/skills/implementation-planning/SKILL.md",
    ".agents/skills/orchestrate-implementation/SKILL.md",
    ".agents/skills/bounded-implementation/SKILL.md",
    ".agents/skills/systematic-debugging/SKILL.md",
    ".agents/skills/verification-gate/SKILL.md",
    ".agents/skills/code-review/SKILL.md",
    ".github/pull_request_template.md",
]

REQUIRED_AGENT_KEYS = {
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
    "developer_instructions",
}

FRONTMATTER_NAME = re.compile(r"^name:\s*(\S.*?)\s*$", re.MULTILINE)
FRONTMATTER_DESCRIPTION = re.compile(r"^description:\s*(\S.*?)\s*$", re.MULTILINE)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing required file: {relative}", errors)
        elif path.stat().st_size == 0:
            fail(f"required file is empty: {relative}", errors)


def load_toml(path: Path, errors: list[str]) -> dict | None:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        fail(f"invalid TOML {path.relative_to(ROOT)}: {exc}", errors)
        return None


def validate_codex_config(errors: list[str]) -> None:
    config = load_toml(ROOT / ".codex/config.toml", errors)
    if config is None:
        return
    if not config.get("model"):
        fail(".codex/config.toml must define model", errors)
    agents = config.get("agents")
    if not isinstance(agents, dict) or agents.get("enabled") is not True:
        fail(".codex/config.toml must enable [agents]", errors)


def validate_agent_configs(errors: list[str]) -> None:
    names: set[str] = set()
    for path in sorted((ROOT / ".codex/agents").glob("*.toml")):
        data = load_toml(path, errors)
        if data is None:
            continue
        missing = sorted(REQUIRED_AGENT_KEYS - data.keys())
        if missing:
            fail(f"{path.relative_to(ROOT)} missing keys: {', '.join(missing)}", errors)
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            fail(f"{path.relative_to(ROOT)} has invalid agent name", errors)
        elif name in names:
            fail(f"duplicate agent name: {name}", errors)
        else:
            names.add(name)

    expected = {"luna_fast", "luna_worker", "luna_explorer", "critical_reviewer"}
    missing_names = sorted(expected - names)
    if missing_names:
        fail(f"missing required agents: {', '.join(missing_names)}", errors)


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[str | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} must start with YAML frontmatter", errors)
        return None, None
    closing = text.find("\n---\n", 4)
    if closing == -1:
        fail(f"{path.relative_to(ROOT)} has unterminated YAML frontmatter", errors)
        return None, None
    frontmatter = text[4:closing]
    name_match = FRONTMATTER_NAME.search(frontmatter)
    description_match = FRONTMATTER_DESCRIPTION.search(frontmatter)
    if not name_match:
        fail(f"{path.relative_to(ROOT)} frontmatter is missing name", errors)
    if not description_match:
        fail(f"{path.relative_to(ROOT)} frontmatter is missing description", errors)
    return (
        name_match.group(1).strip() if name_match else None,
        description_match.group(1).strip() if description_match else None,
    )


def validate_skills(errors: list[str]) -> None:
    names: set[str] = set()
    skill_files = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
    if not skill_files:
        fail("no repository skills found under .agents/skills", errors)
        return

    for path in skill_files:
        name, description = parse_frontmatter(path, errors)
        if name:
            if name in names:
                fail(f"duplicate skill name: {name}", errors)
            names.add(name)
        if description is not None and len(description) < 12:
            fail(f"{path.relative_to(ROOT)} description is too short", errors)

    expected = {
        "feature-design",
        "implementation-planning",
        "orchestrate-implementation",
        "bounded-implementation",
        "systematic-debugging",
        "verification-gate",
        "code-review",
    }
    missing_names = sorted(expected - names)
    if missing_names:
        fail(f"missing required skills: {', '.join(missing_names)}", errors)


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_codex_config(errors)
    validate_agent_configs(errors)
    validate_skills(errors)

    if errors:
        print("Agent framework validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Agent framework validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
