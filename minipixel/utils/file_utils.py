"""Filesystem naming helpers used by the command-line interface."""

from pathlib import Path


def make_output_path(source: str | Path, operation: str, output_dir: str | Path = "output") -> Path:
    """Build ``output_dir/<source-stem>_<operation><suffix>``."""
    source_path = Path(source)
    if not operation or any(character in operation for character in ("/", "\\", "\0")):
        raise ValueError("operation must be a non-empty filename-safe label")
    suffix = source_path.suffix or ".png"
    return Path(output_dir) / f"{source_path.stem}_{operation}{suffix}"
