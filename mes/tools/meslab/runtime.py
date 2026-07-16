"""运行目录和可审计元数据。"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import time
import uuid
from typing import Any

from .bundle import utc_now, write_json


def create_run_directory(root: str | Path) -> tuple[str, Path]:
    output_root = Path(root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    for _ in range(10):
        run_id = f"run-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:10]}"
        run_dir = output_root / run_id
        try:
            run_dir.mkdir()
            (run_dir / "results").mkdir()
            return run_id, run_dir
        except FileExistsError:
            continue
    raise RuntimeError("无法生成唯一 run_id")


class ExecutionLog:
    """仅记录非敏感执行事实的 Markdown 日志。"""

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.started_at = utc_now()
        self._lines = [
            f"# MES 工厂执行日志：{run_id}",
            "",
            f"- 开始时间（UTC）：`{self.started_at}`",
            "- 连接意图：只读事务",
            "",
            "## 执行记录",
            "",
        ]

    def event(self, text: str) -> None:
        self._lines.append(f"- {text}")

    def write(self, path: str | Path, status: str) -> None:
        lines = self._lines + ["", f"- 最终状态：`{status}`", f"- 结束时间（UTC）：`{utc_now()}`"]
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


class Timer:
    def __enter__(self) -> "Timer":
        self.started_at = utc_now()
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: Any) -> None:
        self.ended_at = utc_now()
        self.duration_seconds = round(time.perf_counter() - self._start, 6)


def write_run_manifest(run_dir: str | Path, manifest: dict[str, Any]) -> None:
    write_json(Path(run_dir) / "run-manifest.json", manifest)
