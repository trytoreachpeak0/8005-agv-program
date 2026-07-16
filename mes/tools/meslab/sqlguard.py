"""保守的只读 SQL 校验。"""

from __future__ import annotations

import re


class SqlValidationError(ValueError):
    """SQL 不满足离线工具的只读约束。"""


_DANGEROUS_KEYWORDS = {
    "ALTER",
    "ANALYZE",
    "AUDIT",
    "BEGIN",
    "CALL",
    "COMMIT",
    "CREATE",
    "DECLARE",
    "DELETE",
    "DROP",
    "EXEC",
    "EXECUTE",
    "GRANT",
    "INSERT",
    "LOCK",
    "MERGE",
    "NOAUDIT",
    "RENAME",
    "REVOKE",
    "ROLLBACK",
    "SAVEPOINT",
    "TRUNCATE",
    "UPDATE",
}


def _strip_comments_and_literals(sql: str) -> str:
    """用空白替换注释、字符串和双引号标识符，保留语句结构。"""
    output: list[str] = []
    index = 0
    length = len(sql)
    while index < length:
        char = sql[index]
        next_char = sql[index + 1] if index + 1 < length else ""

        if char == "-" and next_char == "-":
            output.extend("  ")
            index += 2
            while index < length and sql[index] not in "\r\n":
                output.append(" ")
                index += 1
            continue

        if char == "/" and next_char == "*":
            output.extend("  ")
            index += 2
            closed = False
            while index < length:
                if sql[index] == "*" and index + 1 < length and sql[index + 1] == "/":
                    output.extend("  ")
                    index += 2
                    closed = True
                    break
                output.append("\n" if sql[index] == "\n" else " ")
                index += 1
            if not closed:
                raise SqlValidationError("SQL 含未闭合的块注释")
            continue

        if char in {"'", '"'}:
            quote = char
            output.append(" ")
            index += 1
            closed = False
            while index < length:
                if sql[index] == quote:
                    if index + 1 < length and sql[index + 1] == quote:
                        output.extend("  ")
                        index += 2
                        continue
                    output.append(" ")
                    index += 1
                    closed = True
                    break
                output.append("\n" if sql[index] == "\n" else " ")
                index += 1
            if not closed:
                raise SqlValidationError("SQL 含未闭合的引号")
            continue

        # Oracle q'[text]'、q'{text}' 等替代引号。
        if char.lower() == "q" and next_char == "'" and index + 2 < length:
            opener = sql[index + 2]
            closer = {"[": "]", "{": "}", "(": ")", "<": ">"}.get(opener, opener)
            output.extend("   ")
            index += 3
            closed = False
            while index < length:
                if sql[index] == closer and index + 1 < length and sql[index + 1] == "'":
                    output.extend("  ")
                    index += 2
                    closed = True
                    break
                output.append("\n" if sql[index] == "\n" else " ")
                index += 1
            if not closed:
                raise SqlValidationError("SQL 含未闭合的 Oracle q 引号")
            continue

        output.append(char)
        index += 1
    return "".join(output)


def validate_readonly_sql(sql: str) -> str:
    """验证并返回去掉末尾分号的单条 SELECT/WITH SQL。"""
    if not isinstance(sql, str) or not sql.strip():
        raise SqlValidationError("SQL 不能为空")

    cleaned = _strip_comments_and_literals(sql)
    stripped = cleaned.strip()
    semicolons = [match.start() for match in re.finditer(";", cleaned)]
    statement_end: int | None = None
    if semicolons:
        statement_end = semicolons[0]
        if len(semicolons) != 1 or cleaned[statement_end + 1 :].strip():
            raise SqlValidationError("只允许单条 SQL")
        stripped = cleaned[:statement_end].strip()

    first_word = re.match(r"[A-Za-z_][A-Za-z0-9_$#]*", stripped)
    if not first_word or first_word.group(0).upper() not in {"SELECT", "WITH"}:
        raise SqlValidationError("只允许 SELECT 或 WITH 查询")

    words = {word.upper() for word in re.findall(r"[A-Za-z_][A-Za-z0-9_$#]*", stripped)}
    found = sorted(words & _DANGEROUS_KEYWORDS)
    if found:
        raise SqlValidationError(f"SQL 含禁止关键字: {', '.join(found)}")
    if re.search(r"\bDBMS_[A-Za-z0-9_$#]*\b", stripped, flags=re.IGNORECASE):
        raise SqlValidationError("SQL 不允许调用 DBMS_* 包")

    # cleaned 与原文等长，因此可安全移除真正的语句终止分号及其后注释。
    return (sql[:statement_end] if statement_end is not None else sql).strip()
