from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from mes.tools.migrate_legacy_sql_tree import migrate


class LegacySqlMigrationTests(unittest.TestCase):
    def test_preserves_all_files_and_classifies_sql(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "old"
            source.mkdir()
            (source / "read.sql").write_text(
                "SELECT id FROM sample_view\n", encoding="utf-8"
            )
            (source / "write.sql").write_text(
                "UPDATE sample SET value = 1\n", encoding="utf-8"
            )
            (source / "notes.md").write_text("# 说明\n", encoding="utf-8")
            target = root / "snapshot"

            migrate(source, target, remove_source=False)

            manifest = json.loads(
                (target / "source-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["source_file_count"], 3)
            self.assertEqual(manifest["sql_count"], 2)
            with (target / "catalog.csv").open(
                "r", encoding="utf-8-sig", newline=""
            ) as handle:
                rows = {row["path"]: row for row in csv.DictReader(handle)}
            self.assertEqual(
                rows["read.sql"]["classification"],
                "READ_ONLY_CANDIDATE_UNVERIFIED",
            )
            self.assertEqual(
                rows["write.sql"]["classification"],
                "WRITE_OR_PROCEDURAL_RESEARCH_ONLY",
            )
            self.assertTrue((target / "notes.md").is_file())


if __name__ == "__main__":
    unittest.main()
