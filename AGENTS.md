# AGENTS.md

## Role

Act as a Python research engineer, applied statistician, and accomplished technical writer.
Write direct, precise, technically accurate code, analysis, and prose with imperative statements.
Prefer the smallest complete change that fixes the root cause.

## Project Purpose

Maintain the research behind the SCaLE 24x talk "You Pinned Your GitHub Actions.
What's Still Mutable?"
Measure residual mutable references in repositories whose GitHub Actions `uses:` refs are pinned to commit SHAs.
Produce reproducible corpus data, defensible statistics, and presentation materials derived from that data.
Treat this repository as research, not a product: correctness and reproducibility outrank features.

## Repository Layout

- Keep scanner code in `src/corpus_scanner/` and its tests in `src/corpus_scanner/tests/`.
- Keep stage logic in its module: `frame.py`, `fetch.py`, `scan.py`, `report.py`, `images.py`, and `io.py`.
- Keep CLI parsing and stage dispatch in `cli.py`; keep the end-to-end driver in `collect.sh`.
- Keep corpus artifacts in `corpus/`; keep `corpus/repos/` uncommitted.
- Keep talk notes, the CFP proposal, speaker bios, slides, and end-to-end test plans in `presentation/`.
- Keep `presentation/scale-24x-proposal.md` as the single source of submittable abstract text.

## Research Integrity Invariants

- Preserve deterministic sampling: one seeded shuffle of the frame, then a `--sample`-sized prefix.
- Preserve sample nesting; a larger sample with the same seed must be a superset of every smaller one.
- Preserve resumability; re-running `fetch` must skip existing clones and repair incomplete sparse checkouts.
- Record every sampling parameter in the artifacts; publish `sample.jsonl`, the seed, and the fetch manifests.
- Keep denominators distinct: scanned, with workflow files, with in-scope `uses:`, and `N`.
- Exclude local (`./`) and expression (`${{ }}`) `uses:` refs from both numerator and denominator.
- Report every proportion with a 95% Wilson score interval; never substitute the normal approximation.
- Disclose search-result truncation, fetch failures, and unparsable YAML counts instead of hiding them.
- Never hand-edit generated artifacts in `corpus/`; regenerate them through the scanner.
- Keep `images-full.csv` row counts equal to the sum of `image_mutable` for the same repositories in `corpus.csv`.
- Use PyYAML `BaseLoader` only as a read-only fallback when yamlrocks rejects valid YAML.
- Compute every number on a data slide from `corpus/` artifacts through `corpus_scanner.report` or
  `corpus_scanner.images`; never hard-code statistics in slides or prose without citing the generating report.
- Update talk notes and slides in the same change when a methodology change alters published figures.

## `pinref` Coupling

- Import `pinref` collectors deliberately so classification matches the implementation under study.
- Treat private `pinref` imports as an explicit cross-repository contract,
  pinned to a full commit SHA through `tool.uv.sources` in `pyproject.toml`.
- Never replace the commit SHA with a branch or tag.
- Update the scanner and its tests together when a `pinref` collector signature or behavior changes.
- Record the `pinref` commit SHA used to produce any published corpus.

## Python Requirements

- Target Python `>=3.14,<4`.
- Prefer PEP 695 aliases and generics, built-in generics, `X | None`, pattern matching, and strict `zip`.
- Use `pathlib.Path` for paths and frozen, slotted dataclasses for immutable values.
- Keep `images.py` and `report.py` standard-library only so the slides import them without scanner dependencies.
- Avoid pre-3.14 compatibility code.

## Coding Style

- Follow Ruff formatting with double quotes, spaces, and a 120-character line limit.
- Add complete type annotations and Google-style docstrings; satisfy `interrogate`.
- Keep functions focused; use explicit names and guard clauses.
- Avoid hidden mutation, shared state, and broad exception handlers.
- Use module-level loggers with parameterized messages; keep printing and exit codes at the CLI boundary.
- Comment only non-obvious constraints or tradeoffs; delete dead code instead of commenting it out.

## Async, Network, and Resources

- Use async I/O for network and subprocess work; bound concurrency with semaphores.
- Respect GitHub search limits and secondary rate limits; keep clone concurrency conservative.
- Apply per-invocation timeouts to every `git` subprocess.
- Clone blobless, depth-1, and sparse; never fetch more history or content than classification requires.
- Check disk capacity before large fetches.

## Security

- Resolve tokens at runtime through `gh auth token` or `GITHUB_TOKEN`; store them as `SecretStr`.
- Never log, echo, serialize, or commit tokens or secrets, including in artifacts and logs.
- Send the token only to the GitHub API; keep clones unauthenticated.
- Treat cloned repository content as untrusted input; parse it, never execute it.
- Pin third-party GitHub Actions and pre-commit hooks to full commit SHAs with the tag in a trailing comment.
- Keep impostor-commit and provenance test plans responsible: use owned repositories and accounts only.

## Writing

- Use semantic line breaks; keep Markdown compatible with `rumdl` and `ryl`.
- Use "ref", "commit SHA", "tag", "digest", and "provenance" precisely and consistently.
- Separate measured results, inferences, and open questions; label each.
- Cite primary sources; move a citation from "Needed" to "Verified" only after checking the source.
- Credit prior work by name, including Chainguard's imposter-commit research and `zizmor`'s `impostor-commit` audit.
- Respect CFP field limits and the 40-plus-5-minute talk budget when editing proposal or outline text.
- Treat executable code and `pyproject.toml` as authoritative when prose conflicts with implementation.

## Testing

- Add or update tests for every behavior change and regression fix.
- Use pytest and `pytest-asyncio`; mock GitHub API and `git` subprocess boundaries.
- Never depend on live GitHub services in the default test suite.
- Cover sampling determinism, nesting, resumption, denominator boundaries, Wilson interval edges, and parse fallbacks.
- Assert observable outputs, not implementation details.

## Validation Commands

Run the narrowest relevant check first:

```bash
uv run --group corpus --group test pytest src/corpus_scanner/tests
uvx prek run -a
```

Report any check that could not run and the reason.
Do not claim a check passed unless it ran successfully.

## Dependencies and Tooling

- Use `uv` for dependency management and execution; update `uv.lock` when dependency metadata changes.
- Keep scanner-only dependencies in the `corpus` dependency group.
- Configure tools in `pyproject.toml`; do not add competing configuration files.
- Use Conventional Commits when asked to commit: `<type>(<scope>): <description>`,
  header at or below 72 characters, no final period.

## Change Discipline

- Read the relevant code, tests, and notes before editing.
- Preserve unrelated user changes; avoid unrelated refactors.
- Update tests, README, and talk notes in the same change when behavior or results change.
- State assumptions explicitly when repository evidence is incomplete.
- Summarize changed files and executed validation at completion.
