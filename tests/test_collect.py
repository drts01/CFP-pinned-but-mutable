"""Test the root-level collection driver without network or corpus access."""

import os
import shutil
import subprocess
from pathlib import Path


def test_report_driver_resolves_repo_root_from_other_directory(tmp_path: Path) -> None:
    """Run from outside the checkout and find its own corpus and project environment."""
    root = tmp_path / "research"
    root.mkdir()
    shutil.copyfile(Path(__file__).resolve().parents[1] / "collect.sh", root / "collect.sh")
    corpus = root / "corpus"
    corpus.mkdir()
    (corpus / "corpus.csv").write_text("repo\n", encoding="utf-8")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("uv", "gh"):
        executable = bin_dir / name
        executable.write_text("#!/bin/sh\npwd\n" if name == "uv" else "#!/bin/sh\nexit 0\n", encoding="utf-8")
        executable.chmod(0o755)

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = subprocess.run(  # noqa: S603 -- run a trusted, locally copied script with fake external commands
        ["/bin/bash", str(root / "collect.sh"), "report"],
        cwd=elsewhere,
        env={**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )

    assert result.stdout == f"{root}\n"
