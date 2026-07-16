# MES 可复用样本治理

`samples/` 保存从已验证 evidence 派生的最小化、可复用样本。原始工厂输出属于 [`../evidence/`](../evidence/)，不得直接复制到这里冒充 latest。

## 晋升规则

1. 只有 `import-run` 可以创建版本化样本并晋升 `latest`；禁止手工覆盖。
2. 输入 evidence 必须具有唯一 run_id、有效 manifest、客户批准、查询哈希和输出 SHA-256。
3. `latest` 必须同时包含：
   - 数据文件；
   - `latest.meta.json`：QUERY_ID、schema_version、生成时间、行数、内容哈希和 `sourceEvidence`；
   - `latest.md`：由 CSV 自动生成的审阅视图。
4. 任一校验失败、缺批准、缺哈希、含凭据或含未批准敏感字段时，不得晋升。
5. latest 只是“最近一次通过治理的样本”，不代表生产现状、全集或最新查询版本。
6. 更新 latest 不删除历史版本；版本目录不可覆盖。

## 当前工具生成结构

    <query-id>/
      README.md
      latest.csv
      latest.md
      latest.meta.json

当前占位目录：

- [`mes-task-union/`](mes-task-union/)
- [`sublot-box-count/`](sublot-box-count/)
- [`operator-identity/`](operator-identity/)
- [`schema-introspection/`](schema-introspection/)

样本不得包含真实数据库 host、用户名、密码、完整连接字符串或无关个人信息。
