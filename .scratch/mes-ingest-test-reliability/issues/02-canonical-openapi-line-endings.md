# 02 — 统一运行时与离线 OpenAPI 描述的换行格式

**What to build:** 让 MesIngest 运行时生成的 OpenAPI 与安装包离线 OpenAPI 在 Windows、Linux 和不同 Git 换行设置下保持同一契约，使操作员和工具读取到稳定一致的描述文本。

**Blocked by:** None — can start immediately

**Status:** done

- [x] 运行时 OpenAPI 的所有多行描述使用平台无关的规范换行，不受源文件检出为 CRLF 或 LF 影响。
- [x] 离线 OpenAPI 与运行时 OpenAPI 的路径、参数、错误响应、排序 allow-list 和描述文本继续精确一致。
- [x] 不通过放宽字段或契约断言掩盖真实漂移；仅消除无业务意义的平台换行差异。
- [x] OpenAPI 契约测试在 Windows 与 LF 环境均稳定通过。
- [x] MesIngest Release 完整测试套件通过，且不改变正式只读 GET API 的行为。

## Comments

- Runtime info and operation descriptions now canonicalize source-controlled line endings to LF before Swashbuckle serializes the document.
- The live/static contract test rejects carriage returns in every OpenAPI description and compares the complete `paths` trees, covering parameters, responses, allow-lists, and operation descriptions without weakening assertions.
- Release verification: 427 tests passed, 0 failed, 0 skipped.
