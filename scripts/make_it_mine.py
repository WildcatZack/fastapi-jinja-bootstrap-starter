#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Customize the starter and generate a local .env file."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing .env if present.",
    )
    return parser.parse_args()


def prompt_text(label: str, default: str | None = None) -> str:
    prompt = f"{label}"
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if default is not None:
            return default
        print("Value is required.")


def load_env_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def render_env(example_text: str, updates: dict[str, str]) -> str:
    lines: list[str] = []
    seen_keys: set[str] = set()
    for line in example_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            lines.append(line)
            continue
        key, _ = line.split("=", 1)
        key = key.strip()
        if key in updates:
            lines.append(f"{key}={updates[key]}")
            seen_keys.add(key)
        else:
            lines.append(line)
    missing_keys = [key for key in updates if key not in seen_keys]
    if missing_keys:
        if lines and lines[-1].strip() != "":
            lines.append("")
        for key in missing_keys:
            lines.append(f"{key}={updates[key]}")
    return "\n".join(lines) + "\n"


def update_file(path: Path, content: str, dry_run: bool, summary: list[str]) -> None:
    if path.exists() and path.read_text() == content:
        return
    summary.append(str(path))
    if not dry_run:
        path.write_text(content)


def update_package_json(path: Path, slug: str, dry_run: bool, summary: list[str]) -> None:
    data = json.loads(path.read_text())
    data["name"] = f"{slug}-frontend"
    content = json.dumps(data, indent=2) + "\n"
    update_file(path, content, dry_run, summary)


def update_package_lock(path: Path, slug: str, dry_run: bool, summary: list[str]) -> None:
    data = json.loads(path.read_text())
    updated = False
    new_name = f"{slug}-frontend"
    if "name" in data:
        data["name"] = new_name
        updated = True
    packages = data.get("packages")
    if isinstance(packages, dict):
        root_package = packages.get("")
        if isinstance(root_package, dict) and "name" in root_package:
            root_package["name"] = new_name
            updated = True
    if not updated:
        print(f"Warning: {path} missing name fields; skipping updates.")
        return
    content = json.dumps(data, indent=2) + "\n"
    update_file(path, content, dry_run, summary)


def update_templates(paths: list[Path], old_name: str, new_name: str, dry_run: bool, summary: list[str]) -> None:
    for path in paths:
        content = path.read_text()
        updated = content.replace(old_name, new_name)
        update_file(path, updated, dry_run, summary)


def update_readme(path: Path, display_name: str, host_port: str, dry_run: bool, summary: list[str]) -> None:
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines[index] = f"# {display_name}"
            break
    content = "\n".join(lines) + "\n"
    content = re.sub(r"http://127\.0\.0\.1:\d+/", f"http://127.0.0.1:{host_port}/", content)
    update_file(path, content, dry_run, summary)


def main() -> int:
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    env_example_path = repo_root / ".env.example"
    env_path = repo_root / ".env"

    existing_env = load_env_values(env_path)
    example_env = load_env_values(env_example_path)
    current_display = existing_env.get("PROJECT_DISPLAY_NAME") or example_env.get(
        "PROJECT_DISPLAY_NAME", "FastAPI Starter"
    )

    slug = prompt_text("Project slug")
    display_name = prompt_text("Project display name", current_display)
    host_port = prompt_text("Host port", "8000")

    updates = {
        "PROJECT_SLUG": slug,
        "PROJECT_DISPLAY_NAME": display_name,
        "HOST_PORT": host_port,
        "CONTAINER_PORT": "8000",
        "IMAGE_NAME": slug,
    }

    if env_path.exists() and not args.force and not args.dry_run:
        print(f"{env_path} already exists. Use --force to overwrite.")
        return 1

    summary: list[str] = []

    env_content = render_env(env_example_path.read_text(), updates)
    update_file(env_path, env_content, args.dry_run, summary)

    update_package_json(repo_root / "frontend/package.json", slug, args.dry_run, summary)
    update_package_lock(
        repo_root / "frontend/package-lock.json", slug, args.dry_run, summary
    )

    template_paths = [
        repo_root / "app/templates/base.html",
        repo_root / "app/templates/partials/_navbar.html",
        repo_root / "app/templates/index.html",
        repo_root / "app/templates/about.html",
        repo_root / "app/templates/docs.html",
    ]
    update_templates(template_paths, current_display, display_name, args.dry_run, summary)

    update_readme(repo_root / "README.md", display_name, host_port, args.dry_run, summary)

    if not args.dry_run:
        package_json_path = repo_root / "frontend/package.json"
        package_lock_path = repo_root / "frontend/package-lock.json"
        expected_name = f"{slug}-frontend"
        package_json_name = json.loads(package_json_path.read_text()).get("name")
        package_lock = json.loads(package_lock_path.read_text())
        package_lock_name = package_lock.get("name")
        packages = package_lock.get("packages", {})
        root_package = packages.get("") if isinstance(packages, dict) else None
        root_package_name = (
            root_package.get("name") if isinstance(root_package, dict) else None
        )

        if package_json_name != expected_name:
            print("Warning: frontend/package.json name did not update as expected.")
        if package_lock_name is None and root_package_name is None:
            print("Warning: frontend/package-lock.json missing name fields to verify.")
        else:
            if package_lock_name is not None and package_lock_name != expected_name:
                print("Warning: frontend/package-lock.json top-level name mismatch.")
            if root_package_name is not None and root_package_name != expected_name:
                print(
                    "Warning: frontend/package-lock.json packages[\"\"] name mismatch."
                )

    print("\nSummary")
    print("=======")
    print(f"PROJECT_SLUG={slug}")
    print(f"PROJECT_DISPLAY_NAME={display_name}")
    print(f"HOST_PORT={host_port}")
    print("CONTAINER_PORT=8000")
    print(f"IMAGE_NAME={slug}")
    if summary:
        print("\nFiles updated:")
        for item in summary:
            print(f"- {item}")
    else:
        print("\nNo changes needed.")

    if args.dry_run:
        print("\nDry run complete. No files were modified.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
