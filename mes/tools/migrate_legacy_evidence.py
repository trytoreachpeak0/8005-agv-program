"""一次性把重构前产物迁入不可变 legacy evidence。

该命令拒绝覆盖目标目录，并为迁入文件生成 SHA-256 清单。它不负责把 legacy
产物晋升为 samples。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def migrate(source: Path, target: Path, includes: list[str]) -> None:
    if target.exists():
        raise FileExistsError(f"目标已存在，拒绝覆盖：{target}")
    if not source.is_dir():
        raise FileNotFoundError(f"源目录不存在：{source}")
    selected = includes or [
        path.name for path in source.iterdir() if path.is_file()
    ]
    files = []
    for name in selected:
        if Path(name).name != name:
            raise ValueError(f"--include 只允许源目录内文件名：{name}")
        path = source / name
        if not path.is_file():
            raise FileNotFoundError(f"源文件不存在：{path}")
        files.append(path)

    target.mkdir(parents=True)
    manifest_files = []
    for path in files:
        destination = target / path.name
        shutil.copyfile(path, destination)
        manifest_files.append(
            {
                "name": destination.name,
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    manifest = {
        "schema_version": 1,
        "kind": "legacy-evidence-migration",
        "migrated_at": datetime.now(timezone.utc).isoformat(),
        "source_note": "重构前本地目录；路径仅作迁移说明，不是运行时依赖",
        "promotable_to_samples": False,
        "files": manifest_files,
    }
    (target / "legacy-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (target / "README.md").write_text(
        "# Legacy evidence\n\n"
        "本目录由迁移工具从重构前产物生成，只用于历史追溯。其查询版本、"
        "输出契约或批准信息不完整，不得由 `import-run` 晋升为 latest 样本。\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="迁移重构前 MES 证据")
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--include", action="append", default=[])
    args = parser.parse_args()
    migrate(args.source.resolve(), args.target.resolve(), args.include)
    print(f"已迁移 legacy evidence：{args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
