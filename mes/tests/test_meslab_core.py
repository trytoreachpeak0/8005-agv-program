from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile
import unittest


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from meslab.hashing import sha256_file
from meslab.manifest import QueryCatalog, load_query
from meslab.sqlguard import SqlValidationError, validate_readonly_sql


def create_query(root: Path, query_id: str = "TEST_QUERY") -> Path:
    query_dir = root / query_id.lower()
    query_dir.mkdir(parents=True)
    (query_dir / "query.sql").write_text(
        "SELECT id, name FROM test_view WHERE factory_code = :FACTORY_CODE;\n",
        encoding="utf-8",
    )
    (query_dir / "query.toml").write_text(
        f"""id = "{query_id}"
title = "测试查询"
sql = "query.sql"
readonly = true
parameters = ["FACTORY_CODE"]
expected_columns = ["ID", "NAME"]
""",
        encoding="utf-8",
    )
    return query_dir


class ManifestTests(unittest.TestCase):
    def test_load_toml_and_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            query_dir = create_query(root)
            query = load_query(query_dir)
            self.assertEqual(query.id, "TEST_QUERY")
            self.assertEqual(query.parameters, ("FACTORY_CODE",))
            self.assertEqual(query.expected_columns, ("ID", "NAME"))
            self.assertEqual(QueryCatalog(root).get("TEST_QUERY"), query)


class SqlGuardTests(unittest.TestCase):
    def test_accepts_select_with_comments_literals_and_trailing_semicolon(self) -> None:
        sql = """-- DELETE is documentation
SELECT 'UPDATE x', q'[DROP TABLE x]' AS note
FROM safe_view /* INSERT is documentation */;
-- trailing comment
"""
        validated = validate_readonly_sql(sql)
        self.assertTrue(validated.lstrip().startswith("-- DELETE"))
        self.assertNotIn(";", validated[-3:])
        validate_readonly_sql("WITH q AS (SELECT 1 id FROM dual) SELECT id FROM q")

    def test_rejects_writes_multiple_statements_and_plsql(self) -> None:
        rejected = (
            "INSERT INTO t VALUES (1)",
            "UPDATE t SET value = 1",
            "DELETE FROM t",
            "MERGE INTO t USING s ON (t.id=s.id) WHEN MATCHED THEN UPDATE SET t.x=s.x",
            "CREATE TABLE t (id NUMBER)",
            "BEGIN NULL; END;",
            "SELECT 1 FROM dual; DELETE FROM t",
            "SELECT dbms_random.value FROM dual",
            "SELECT * FROM t FOR UPDATE",
        )
        for sql in rejected:
            with self.subTest(sql=sql):
                with self.assertRaises(SqlValidationError):
                    validate_readonly_sql(sql)


class HashTests(unittest.TestCase):
    def test_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "data.bin"
            path.write_bytes(b"abc")
            self.assertEqual(sha256_file(path), hashlib.sha256(b"abc").hexdigest())


if __name__ == "__main__":
    unittest.main()
