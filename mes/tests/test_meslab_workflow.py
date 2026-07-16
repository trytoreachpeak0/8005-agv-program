from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MES_ROOT = Path(__file__).resolve().parents[1]
TOOLS = MES_ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from meslab.bundle import BundleError, build_bundle, write_json
from meslab.hashing import sha256_file
from meslab.importer import ImportRunError, import_run
from meslab.manifest import load_query
from meslab.runner import run_factory
from meslab.samples import write_csv


def create_query(root: Path) -> Path:
    query_dir = root / "sample"
    query_dir.mkdir(parents=True)
    (query_dir / "query.sql").write_text("SELECT id, name FROM sample_view\n", encoding="utf-8")
    (query_dir / "query.toml").write_text(
        """id = "SAMPLE_QUERY"
title = "样例查询"
sql = "query.sql"
readonly = true
parameters = []
expected_columns = ["ID", "NAME"]
""",
        encoding="utf-8",
    )
    return query_dir


def create_union_query(root: Path) -> Path:
    query_dir = root / "mes-task-union"
    query_dir.mkdir(parents=True)
    (query_dir / "query.sql").write_text(
        "SELECT task_type, sublot, area, eqp, step, dates, package FROM task_view\n",
        encoding="utf-8",
    )
    (query_dir / "query.toml").write_text(
        """id = "MES_TASK_UNION"
title = "任务查询"
sql = "query.sql"
readonly = true
parameters = []
expected_columns = ["TASK_TYPE", "SUBLOT", "AREA", "EQP", "STEP", "DATES", "PACKAGE"]
""",
        encoding="utf-8",
    )
    return query_dir


class BundleTests(unittest.TestCase):
    def test_bundle_manifest_contains_file_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            query = load_query(create_query(root / "queries"))
            bundle = root / "bundle"
            manifest = build_bundle([query], bundle)
            entry = manifest["queries"][0]
            self.assertEqual(entry["id"], "SAMPLE_QUERY")
            self.assertEqual(entry["sha256"]["sql"], sha256_file(bundle / entry["sql"]))
            self.assertEqual(
                entry["sha256"]["query_manifest"],
                sha256_file(bundle / entry["query_manifest"]),
            )
            self.assertTrue(manifest["runner_files"])
            bundled_help = subprocess.run(
                [
                    sys.executable,
                    str(bundle / "runner" / "mes_lab.py"),
                    "run-factory",
                    "--help",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(bundled_help.returncode, 0, bundled_help.stderr)
            on_disk = json.loads((bundle / "bundle-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(on_disk, manifest)

    def test_run_factory_help_does_not_require_oracle(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOLS / "mes_lab.py"), "run-factory", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--params-json", result.stdout)
        self.assertIn("--approval-json", result.stdout)

    def test_factory_run_rejects_missing_required_approval_before_connecting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            query_dir = create_query(root / "queries")
            manifest_path = query_dir / "query.toml"
            manifest_path.write_text(
                manifest_path.read_text(encoding="utf-8").replace(
                    "readonly = true\n",
                    "readonly = true\nrequires_approval = true\n",
                ),
                encoding="utf-8",
            )
            bundle = root / "bundle"
            build_bundle([load_query(query_dir)], bundle)
            with self.assertRaisesRegex(BundleError, "要求客户批准信息"):
                run_factory(
                    bundle,
                    root / "missing-config.ini",
                    root / "runs",
                )

    def test_experiment_can_bundle_customer_source_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_query(root / "queries")
            source = root / "sources"
            source.mkdir()
            (source / "customer.sql").write_text(
                "SELECT id, name FROM customer_view\n", encoding="utf-8"
            )
            (source / "customer.toml").write_text(
                """id = "CUSTOMER_BASELINE"
title = "客户基线"
sql = "customer.sql"
readonly = true
promote_sample = false
parameters = []
expected_columns = ["ID", "NAME"]
""",
                encoding="utf-8",
            )
            experiment = root / "experiment.toml"
            experiment.write_text(
                'query_ids = ["SAMPLE_QUERY"]\n'
                'source_manifests = ["sources/customer.toml"]\n',
                encoding="utf-8",
            )
            bundle = root / "bundle"
            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOLS / "mes_lab.py"),
                    "build-bundle",
                    "--queries-root",
                    str(root / "queries"),
                    "--experiment",
                    str(experiment),
                    "--output",
                    str(bundle),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(
                (bundle / "bundle-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                {entry["id"] for entry in manifest["queries"]},
                {"SAMPLE_QUERY", "CUSTOMER_BASELINE"},
            )
            source_entry = next(
                entry
                for entry in manifest["queries"]
                if entry["id"] == "CUSTOMER_BASELINE"
            )
            self.assertFalse(source_entry["promote_sample"])


class ImportRunTests(unittest.TestCase):
    def test_import_rejects_duplicate_and_generates_latest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            query = load_query(create_query(root / "queries"))
            bundle = root / "bundle"
            bundle_manifest = build_bundle([query], bundle)
            bundle_entry = bundle_manifest["queries"][0]

            run_id = "run-20260716T000000Z-test"
            run = root / "factory-runs" / run_id
            result = run / "results" / "SAMPLE_QUERY-round-001.csv"
            write_csv(result, ["ID", "NAME"], [(1, "甲"), (2, "乙")])
            (run / "execution-log.md").write_text("# test\n", encoding="utf-8")
            output_relative = result.relative_to(run).as_posix()
            write_json(
                run / "run-manifest.json",
                {
                    "schema_version": 1,
                    "run_id": run_id,
                    "status": "completed",
                    "bundle_id": bundle_manifest["bundle_id"],
                    "bundle_manifest_sha256": sha256_file(bundle / "bundle-manifest.json"),
                    "queries": [
                        {
                            "id": bundle_entry["id"],
                            "sql": bundle_entry["sql"],
                            "query_manifest": bundle_entry["query_manifest"],
                            "sha256": bundle_entry["sha256"],
                        }
                    ],
                    "executions": [
                        {
                            "query_id": "SAMPLE_QUERY",
                            "round": 1,
                            "row_count": 2,
                            "output": output_relative,
                            "output_sha256": sha256_file(result),
                        }
                    ],
                },
            )

            imported = import_run(run, bundle, root / "mes")
            sample = root / "mes" / "samples" / "sample"
            self.assertEqual(imported, root / "mes" / "evidence" / "runs" / run_id)
            self.assertEqual((sample / "latest.csv").read_bytes(), result.read_bytes())
            self.assertIn("| ID | NAME |", (sample / "latest.md").read_text(encoding="utf-8"))
            metadata = json.loads((sample / "latest.meta.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["run_id"], run_id)
            self.assertEqual(
                metadata["sourceEvidence"], f"evidence/runs/{run_id}"
            )
            self.assertEqual(metadata["output_sha256"], sha256_file(result))

            with self.assertRaises(ImportRunError):
                import_run(run, bundle, root / "mes")

    def test_union_import_generates_package_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            query = load_query(create_union_query(root / "queries"))
            bundle = root / "bundle"
            bundle_manifest = build_bundle([query], bundle)
            entry = bundle_manifest["queries"][0]

            run_id = "run-20260716T010000Z-coverage"
            run = root / "runs" / run_id
            result = run / "results" / "MES_TASK_UNION-round-001.csv"
            result.parent.mkdir(parents=True)
            result.write_text(
                "TASK_TYPE,SUBLOT,AREA,EQP,STEP,DATES,PACKAGE\n"
                "DIE_TO_OVEN,S1,A1,E1,装片烘烤,2026-07-16 12:00:00,TOLL-8L\n"
                "DIE_TO_OVEN,S2,A1,E1,装片烘烤,2026-07-16 12:01:00,UNKNOWN\n",
                encoding="utf-8",
            )
            (run / "execution-log.md").write_text("# test\n", encoding="utf-8")
            relative = result.relative_to(run).as_posix()
            write_json(
                run / "run-manifest.json",
                {
                    "schema_version": 1,
                    "run_id": run_id,
                    "status": "completed",
                    "bundle_id": bundle_manifest["bundle_id"],
                    "bundle_manifest_sha256": sha256_file(
                        bundle / "bundle-manifest.json"
                    ),
                    "queries": [
                        {
                            "id": entry["id"],
                            "sql": entry["sql"],
                            "query_manifest": entry["query_manifest"],
                            "sha256": entry["sha256"],
                        }
                    ],
                    "executions": [
                        {
                            "query_id": "MES_TASK_UNION",
                            "round": 1,
                            "row_count": 2,
                            "output": relative,
                            "output_sha256": sha256_file(result),
                        }
                    ],
                },
            )

            import_run(run, bundle, root / "mes")
            sample = root / "mes" / "samples" / "mes-task-union"
            self.assertTrue(
                (sample / "package-coverage" / "unmatched_packages.csv").is_file()
            )
            metadata = json.loads(
                (sample / "latest.meta.json").read_text(encoding="utf-8")
            )
            self.assertIn("package_coverage", metadata)


if __name__ == "__main__":
    unittest.main()
