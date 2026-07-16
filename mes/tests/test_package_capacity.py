from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from mes.analysis.analyze_package_coverage import (
    CoverageAnalysisError,
    analyze_mes_task_union,
)
from mes.analysis.package_capacity import (
    CapacityRule,
    RuleSet,
    RuleValidationError,
    calculate_expected_baskets,
    load_rules,
    resolve_package,
)


EXPECTED_EXACT = {
    "PDFN5×6-8L(12R)": 4,
    "PDFNWB3.3×3.34": 4,
    "PDFNWB5×6": 4,
    "TO-126": 8,
    "TO-220-2L-C": 8,
    "TO-220-3L": 8,
    "TO-220-3L-C(T0.5mm)": 8,
    "TO-220-5L": 8,
    "TO-220D-5L": 8,
    "TO-220F": 8,
    "TO-247": 6,
    "TO-247-2L-A": 6,
    "TO-247-4L": 6,
    "TO-247A-4L": 6,
    "TO-247B-3L": 6,
    "TO-247Plus-4L": 6,
    "TO-251": 10,
    "TO-252-2L(4R)": 5,
    "TO-252-2L(6R)": 4,
    "TO-252-2L(8R)": 4,
    "TO-252-5L": 10,
    "TO-263-2L": 8,
    "TO-263-5L": 8,
    "TO-263-7L(2R)": 6,
    "TO-263C-2L": 8,
    "TO-264-3L": 8,
    "TO-92": 12,
}


def make_rule(pattern: str, match_type: str, capacity: int) -> CapacityRule:
    return CapacityRule(
        pattern=pattern,
        match_type=match_type,
        max_boxes_per_basket=capacity,
        source="test",
        status="active",
        note="test",
    )


class RuleLoadingTests(unittest.TestCase):
    def test_standard_csv_contains_all_28_validated_rules(self) -> None:
        rules = load_rules()
        exact = {
            rule.pattern: rule.max_boxes_per_basket
            for rule in rules.rules
            if rule.match_type == "exact"
        }
        prefix = [
            (rule.pattern, rule.max_boxes_per_basket)
            for rule in rules.rules
            if rule.match_type == "prefix"
        ]
        self.assertEqual(exact, EXPECTED_EXACT)
        self.assertEqual(prefix, [("TOLL-", 3)])
        self.assertEqual(len(rules.rules), 28)

    def test_invalid_capacity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "rules.csv"
            path.write_text(
                "pattern,match_type,max_boxes_per_basket,source,status,note\n"
                "TO-X,exact,0,test,active,test\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                RuleValidationError, "max_boxes_per_basket"
            ):
                load_rules(path)

    def test_invalid_header_and_duplicate_rule_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            bad_header = temp / "bad-header.csv"
            bad_header.write_text(
                "pattern,match_type,max_boxes_per_basket\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuleValidationError, "字段必须严格"):
                load_rules(bad_header)

            duplicate = temp / "duplicate.csv"
            duplicate.write_text(
                "pattern,match_type,max_boxes_per_basket,source,status,note\n"
                "TO-X,exact,2,test,active,test\n"
                "TO-X,exact,2,test,active,test\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuleValidationError, "规则重复"):
                load_rules(duplicate)


class ResolutionTests(unittest.TestCase):
    def test_strip_and_exact_take_priority_over_prefix(self) -> None:
        rules = RuleSet(
            [
                make_rule("TO-", "prefix", 2),
                make_rule("TO-220", "exact", 8),
            ]
        )
        result = resolve_package("  TO-220  ", rules)
        self.assertIsNotNone(result)
        self.assertEqual(result.match_type, "exact")
        self.assertEqual(result.max_boxes_per_basket, 8)

    def test_longest_prefix_wins(self) -> None:
        rules = RuleSet(
            [
                make_rule("TO-", "prefix", 2),
                make_rule("TO-22", "prefix", 5),
            ]
        )
        result = resolve_package("TO-220X", rules)
        self.assertIsNotNone(result)
        self.assertEqual(result.matched_pattern, "TO-22")
        self.assertEqual(result.max_boxes_per_basket, 5)

    def test_toll_prefix_positive_and_negative_cases(self) -> None:
        rules = load_rules()
        result = resolve_package("TOLL-8L", rules)
        self.assertIsNotNone(result)
        self.assertEqual(result.match_type, "prefix")
        self.assertEqual(result.max_boxes_per_basket, 3)
        self.assertIsNone(resolve_package("TOLL", rules))
        self.assertIsNone(resolve_package("TOLLX", rules))

    def test_unknown_and_empty_values_do_not_match(self) -> None:
        rules = load_rules()
        self.assertIsNone(resolve_package("TO-999", rules))
        self.assertIsNone(resolve_package("", rules))
        self.assertIsNone(resolve_package("   ", rules))
        self.assertIsNone(resolve_package(None, rules))


class BasketCalculationTests(unittest.TestCase):
    def test_ceil_calculation(self) -> None:
        self.assertEqual(calculate_expected_baskets(1, 4), 1)
        self.assertEqual(calculate_expected_baskets(4, 4), 1)
        self.assertEqual(calculate_expected_baskets(5, 4), 2)
        self.assertEqual(calculate_expected_baskets("9", "4"), 3)

    def test_invalid_max_box_count_is_rejected(self) -> None:
        for value in (0, "0", -1, 1.5, "1.5", "abc", "", True, None):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "max_box_count"):
                    calculate_expected_baskets(value, 4)

    def test_invalid_capacity_is_rejected(self) -> None:
        for value in (0, -1, "0", 1.5, False):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "max_boxes_per_basket"):
                    calculate_expected_baskets(4, value)


class CoverageReportTests(unittest.TestCase):
    def test_coverage_reports_and_task_type_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "union.csv"
            output = temp / "report"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=("SUBLOT", "TASK_TYPE", "PACKAGE"),
                    lineterminator="\n",
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {
                            "SUBLOT": "S1",
                            "TASK_TYPE": "DIE_TO_OVEN",
                            "PACKAGE": "TO-126",
                        },
                        {
                            "SUBLOT": "S2",
                            "TASK_TYPE": "DIE_TO_OVEN",
                            "PACKAGE": "TOLL-8L",
                        },
                        {
                            "SUBLOT": "S3",
                            "TASK_TYPE": "WIRE_TO_GATE",
                            "PACKAGE": "UNKNOWN",
                        },
                        {
                            "SUBLOT": "S4",
                            "TASK_TYPE": "WIRE_TO_GATE",
                            "PACKAGE": "UNKNOWN",
                        },
                        {
                            "SUBLOT": "S5",
                            "TASK_TYPE": "WIRE_TO_GATE",
                            "PACKAGE": " ",
                        },
                    ]
                )

            result = analyze_mes_task_union(source, output)
            self.assertEqual(result.total_rows, 5)
            self.assertEqual(result.unique_packages, 3)
            self.assertEqual(result.empty_packages, 1)
            self.assertEqual(result.exact_rows, 1)
            self.assertEqual(result.prefix_rows, 1)
            self.assertEqual(result.unmatched_rows, 2)

            with (output / "unmatched_packages.csv").open(
                "r", encoding="utf-8-sig", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["PACKAGE"], "UNKNOWN")
            self.assertEqual(rows[0]["次数"], "2")
            self.assertEqual(rows[0]["TASK_TYPE分布"], "WIRE_TO_GATE:2")
            self.assertEqual(rows[0]["样例SUBLOT"], "S3 | S4")

            with (output / "prefix_matches.csv").open(
                "r", encoding="utf-8-sig", newline=""
            ) as handle:
                prefix_rows = list(csv.DictReader(handle))
            self.assertEqual(prefix_rows[0]["PACKAGE"], "TOLL-8L")
            self.assertEqual(prefix_rows[0]["matched_pattern"], "TOLL-")

            with (output / "matched_packages.csv").open(
                "r", encoding="utf-8-sig", newline=""
            ) as handle:
                matched_rows = list(csv.DictReader(handle))
            self.assertEqual(len(matched_rows), 2)

            summary = (output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("- 总行数：5", summary)
            self.assertIn("| DIE_TO_OVEN | 2 | 0 | 1 | 1 | 0 |", summary)
            self.assertIn("| WIRE_TO_GATE | 3 | 1 | 0 | 0 | 2 |", summary)

    def test_missing_package_column_rejects_old_six_column_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "old-union.csv"
            source.write_text(
                "SUBLOT,LOT_ID,TASK_TYPE,FROM_LOC,TO_LOC,PRIORITY\n"
                "S1,L1,DIE_TO_OVEN,A,B,1\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                CoverageAnalysisError, "缺少必需的 PACKAGE 列"
            ):
                analyze_mes_task_union(source, temp / "report")


if __name__ == "__main__":
    unittest.main()
