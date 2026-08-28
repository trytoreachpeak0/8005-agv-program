"""加载并解析 PACKAGE / 花篮容量规则。"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Union


RULE_FIELDS = (
    "pattern",
    "match_type",
    "max_boxes_per_basket",
    "source",
    "status",
    "note",
)
DEFAULT_RULES_PATH = (
    Path(__file__).resolve().parents[1]
    / "reference"
    / "package-basket-capacity.csv"
)
_NON_NEGATIVE_INTEGER = re.compile(r"^[0-9]+$")


class RuleValidationError(ValueError):
    """规则 CSV 不符合约定。"""


@dataclass(frozen=True)
class CapacityRule:
    pattern: str
    match_type: str
    max_boxes_per_basket: int
    source: str
    status: str
    note: str


@dataclass(frozen=True)
class PackageResolution:
    package: str
    rule: CapacityRule

    @property
    def match_type(self) -> str:
        return self.rule.match_type

    @property
    def matched_pattern(self) -> str:
        return self.rule.pattern

    @property
    def max_boxes_per_basket(self) -> int:
        return self.rule.max_boxes_per_basket


class RuleSet:
    """预索引规则，保证精确优先和最长前缀优先。"""

    def __init__(self, rules: Iterable[CapacityRule]):
        self.rules = tuple(rules)
        self._exact = {
            rule.pattern: rule
            for rule in self.rules
            if rule.match_type == "exact"
        }
        self._prefix = tuple(
            sorted(
                (rule for rule in self.rules if rule.match_type == "prefix"),
                key=lambda rule: len(rule.pattern),
                reverse=True,
            )
        )

    def resolve(self, package: object) -> Optional[PackageResolution]:
        normalized = _normalize_package(package)
        if normalized is None:
            return None

        exact_rule = self._exact.get(normalized)
        if exact_rule is not None:
            return PackageResolution(normalized, exact_rule)

        for rule in self._prefix:
            if normalized.startswith(rule.pattern):
                return PackageResolution(normalized, rule)
        return None


def _validate_unpadded(value: Optional[str], field: str, line_number: int) -> str:
    if value is None or value == "":
        raise RuleValidationError(
            f"第 {line_number} 行字段 {field!r} 不能为空"
        )
    if value != value.strip():
        raise RuleValidationError(
            f"第 {line_number} 行字段 {field!r} 含首尾空白"
        )
    return value


def load_rules(path: Union[str, Path, None] = None) -> RuleSet:
    """从 CSV 加载规则；任何结构或数据异常都会明确失败。"""

    rules_path = Path(path) if path is not None else DEFAULT_RULES_PATH
    try:
        handle = rules_path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise RuleValidationError(f"无法读取规则文件 {rules_path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        actual_fields = tuple(reader.fieldnames or ())
        if actual_fields != RULE_FIELDS:
            raise RuleValidationError(
                "规则 CSV 字段必须严格为 "
                f"{','.join(RULE_FIELDS)}；实际为 {','.join(actual_fields)}"
            )

        rules = []
        seen = set()
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise RuleValidationError(f"第 {line_number} 行存在多余字段")

            values = {
                field: _validate_unpadded(row.get(field), field, line_number)
                for field in RULE_FIELDS
            }
            match_type = values["match_type"]
            if match_type not in {"exact", "prefix"}:
                raise RuleValidationError(
                    f"第 {line_number} 行 match_type 必须是 exact 或 prefix"
                )
            if values["status"] != "active":
                raise RuleValidationError(
                    f"第 {line_number} 行 status 必须是 active"
                )

            capacity_text = values["max_boxes_per_basket"]
            if not _NON_NEGATIVE_INTEGER.fullmatch(capacity_text):
                raise RuleValidationError(
                    f"第 {line_number} 行 max_boxes_per_basket 必须是正整数"
                )
            capacity = int(capacity_text)
            if capacity <= 0:
                raise RuleValidationError(
                    f"第 {line_number} 行 max_boxes_per_basket 必须大于 0"
                )

            identity = (values["pattern"], match_type)
            if identity in seen:
                raise RuleValidationError(
                    f"第 {line_number} 行规则重复: {identity[0]!r}/{identity[1]}"
                )
            seen.add(identity)
            rules.append(
                CapacityRule(
                    pattern=values["pattern"],
                    match_type=match_type,
                    max_boxes_per_basket=capacity,
                    source=values["source"],
                    status=values["status"],
                    note=values["note"],
                )
            )

    if not rules:
        raise RuleValidationError("规则 CSV 至少需要一条规则")
    return RuleSet(rules)


def _normalize_package(package: object) -> Optional[str]:
    if package is None:
        return None
    if not isinstance(package, str):
        raise TypeError("PACKAGE 必须是字符串或 None")
    normalized = package.strip()
    return normalized or None


def resolve_package(
    package: object,
    rules: Optional[Union[RuleSet, Iterable[CapacityRule]]] = None,
) -> Optional[PackageResolution]:
    """解析 PACKAGE；空值或未知值返回 None，不进行模糊推断。"""

    rule_set = load_rules() if rules is None else _as_rule_set(rules)
    return rule_set.resolve(package)


def _as_rule_set(
    rules: Union[RuleSet, Iterable[CapacityRule]],
) -> RuleSet:
    return rules if isinstance(rules, RuleSet) else RuleSet(rules)


def _parse_non_negative_integer(value: object, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} 必须是非负整数")
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str) and _NON_NEGATIVE_INTEGER.fullmatch(value.strip()):
        parsed = int(value.strip())
    else:
        raise ValueError(f"{name} 必须是非负整数")
    if parsed < 0:
        raise ValueError(f"{name} 必须是非负整数")
    return parsed


def calculate_expected_baskets(
    max_box_count: object,
    max_boxes_per_basket: object,
) -> int:
    """按上取整计算所需花篮数；两个输入都必须是正整数。"""

    box_count = _parse_non_negative_integer(max_box_count, "max_box_count")
    if box_count <= 0:
        raise ValueError("max_box_count 必须是正整数")
    capacity = _parse_non_negative_integer(
        max_boxes_per_basket, "max_boxes_per_basket"
    )
    if capacity <= 0:
        raise ValueError("max_boxes_per_basket 必须是正整数")
    return (box_count + capacity - 1) // capacity
