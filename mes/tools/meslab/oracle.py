"""Oracle 本地配置与延迟连接。"""

from __future__ import annotations

import configparser
from contextlib import contextmanager
from dataclasses import dataclass, field
import importlib
import os
from pathlib import Path
from typing import Any, Iterator


class OracleConfigError(ValueError):
    """Oracle 配置缺失或无效。"""


@dataclass(frozen=True)
class OracleConfig:
    user: str
    password: str = field(repr=False)
    dsn: str
    connect_timeout: int = 30
    call_timeout: int = 300_000
    mode: str = "thick"
    instant_client_dir: str = ""


def load_oracle_config(path: str | Path) -> OracleConfig:
    parser = configparser.ConfigParser(interpolation=None)
    config_path = Path(path)
    if not config_path.is_file():
        raise OracleConfigError(f"配置文件不存在: {config_path}")
    parser.read(config_path, encoding="utf-8")
    if not parser.has_section("oracle"):
        raise OracleConfigError("config.ini 缺少 [oracle] 段")
    required = ("user", "password", "dsn")
    missing = [key for key in required if not parser.get("oracle", key, fallback="").strip()]
    if missing:
        raise OracleConfigError(f"[oracle] 缺少配置: {', '.join(missing)}")
    mode = parser.get("oracle", "mode", fallback="thick").strip().lower()
    if mode not in {"thin", "thick", "auto"}:
        raise OracleConfigError("[oracle] mode 只能是 thin、thick 或 auto")
    return OracleConfig(
        user=parser.get("oracle", "user").strip(),
        password=parser.get("oracle", "password"),
        dsn=parser.get("oracle", "dsn").strip(),
        connect_timeout=parser.getint("oracle", "connect_timeout", fallback=30),
        call_timeout=parser.getint("oracle", "call_timeout", fallback=300_000),
        mode=mode,
        instant_client_dir=parser.get(
            "oracle", "instant_client_dir", fallback=""
        ).strip(),
    )


def connect(config: OracleConfig) -> Any:
    """仅在真正连接时导入 ``oracledb``。"""
    try:
        oracledb = importlib.import_module("oracledb")
    except ModuleNotFoundError as exc:
        raise RuntimeError("执行工厂查询需要安装 oracledb；构建和导入无需安装") from exc
    if config.mode in {"thick", "auto"} and oracledb.is_thin_mode():
        client_dir = (
            config.instant_client_dir
            or os.environ.get("ORACLE_CLIENT_LIB_DIR", "").strip()
        )
        try:
            if client_dir:
                oracledb.init_oracle_client(lib_dir=client_dir)
            else:
                oracledb.init_oracle_client()
        except Exception as exc:
            if config.mode == "thick":
                raise RuntimeError(
                    "Oracle Thick 模式初始化失败；请配置 instant_client_dir "
                    "或 ORACLE_CLIENT_LIB_DIR"
                ) from exc

    connection = oracledb.connect(
        user=config.user,
        password=config.password,
        dsn=config.dsn,
        tcp_connect_timeout=config.connect_timeout,
    )
    connection.call_timeout = config.call_timeout
    return connection


def runtime_info(config: OracleConfig) -> dict[str, str]:
    """返回不含地址、账号和密码的 Oracle 驱动环境信息。"""

    oracledb = importlib.import_module("oracledb")
    return {
        "driver": "python-oracledb",
        "driver_version": str(getattr(oracledb, "__version__", "UNKNOWN")),
        "requested_mode": config.mode,
        "actual_mode": "thin" if oracledb.is_thin_mode() else "thick",
    }


@contextmanager
def readonly_connection(config: OracleConfig) -> Iterator[Any]:
    """建立只读事务意图连接，退出时始终回滚。"""
    connection = connect(config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET TRANSACTION READ ONLY")
        yield connection
    finally:
        try:
            connection.rollback()
        finally:
            connection.close()
