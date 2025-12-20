# AGENTS.md — Rules for automated changes (Codex)

This repo is an opinionated starter. `PROJECT_INTENT.md` is the source of truth.

## Ground rules
1) Do not add features that are not explicitly requested.
2) Do not expand documentation beyond quick-start + brief conceptual notes.
3) Prefer deleting confusing/unused behavior over adding “fallback magic.”
4) Keep changes minimal and scoped. Small PRs only.
5) Never change naming/layout conventions unless asked.
6) If anything is ambiguous, ask in the PR description instead of guessing.

## Dev/prod contract (do not violate)
- Dev uses docker compose and may use two containers (`api` + `assets`).
- Production is one image; Node is not included in the runtime image.
- Compiled frontend assets are not committed to git.
- `node_modules` must live inside a Docker named volume (not on host).

## Required evidence for PRs
For any PR that changes runtime behavior, include:
- What changed (bullet list)
- How to run it (exact commands)
- Proof it works (command output summary)

## Commands to run (when applicable)
- Python sanity:
  - `python -m compileall app`

- Container build/run sanity:
  - `docker compose build`
  - `docker compose up -d`
  - `docker compose ps`

- Asset sanity:
  - After the watcher starts, confirm compiled outputs exist under `app/static/`

If network access prevents Node installs in the sandbox environment, do NOT invent alternative pipelines.
Instead:
- Describe the limitation in the PR
- Keep the repo consistent with the dev/prod contract
- If CI exists, rely on CI for Node build verification
