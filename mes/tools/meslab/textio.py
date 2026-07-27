"""本地文本文件解码（工厂 Windows 常见 UTF-8 / GBK）。"""

from __future__ import annotations

from pathlib import Path


def read_local_text(path: str | Path) -> str:
    """按 utf-8-sig → utf-8 → gb18030 依次尝试解码。"""
    file_path = Path(path)
    raw = file_path.read_bytes()
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise ValueError(
        f"无法解码文件（已尝试 utf-8 / gb18030）: {file_path}"
    ) from last_error
