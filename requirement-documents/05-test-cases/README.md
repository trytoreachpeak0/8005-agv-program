# 05-test-cases 测试用例

本目录存放测试用例（Test Case）文档，编号格式为 `TC-001`、`TC-002` ...

- 新建测试用例时，套用 `_templates/template-test-case.md` 模板（已通过 Templater 插件按目录自动关联）。
- 每条测试用例的 frontmatter 中通过 `related_fr`、`related_uc` 字段登记它验证的功能需求/用例，配合 `06-traceability/traceability-matrix.md` 的 Dataview 查询自动汇总。
- 命名规范、ID 规则、跨文档引用方式见 `../README.md`。
- `Preconditions`/`Test Steps`/`Expected Result` 直接对应所验证 FR 的 Acceptance Criteria 中的 `Given`/`When`/`Then`，一条 AC 对应一条 TC；`Verifies` 字段写明具体 AC 编号（如 `FR-003 AC-1`）。
- 首批参考样例：[[tc-001-pending-slot-exists-pass|TC-001]] ~ [[tc-024-destination-residue-escalate-to-uc044|TC-024]]，对应 [[fr-003-confirm-completion-eligibility-check|FR-003]] ~ [[fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation|FR-009]]（UC-002/005/006/010 派生）。
- 第三批：[[tc-025-arrival-status-updated-to-arrived|TC-025]] ~ [[tc-041-reclose-residue-remains-require-reopen-again|TC-041]]，对应 [[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]] ~ [[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]]（UC-003/043/044 派生），至此 `01-site-operations` 域 8 个 UC 全部有对应 FR/TC 覆盖。
- 第四批（`02-slot-and-hardware` 域）：[[tc-042-dashboard-normal-display|TC-042]] ~ [[tc-063-mapping-required-point-missing-reject|TC-063]]，对应 [[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]] ~ [[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]]（UC-011/014/015/016/017/018/039 派生）。
- 第五批（`03-agv-fleet-management` 域）：[[tc-064-draft-validation-pass-and-publishable|TC-064]] ~ [[tc-097-fleet-dashboard-io-safety-status-fail-unknown|TC-097]]，对应 [[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] ~ [[fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning|FR-030]]（UC-013/019/020/021/022/038 派生）。
- 第六批补充（`01-site-operations` 域）：[[tc-098-cancel-occupancy-mismatch-auto-reopen|TC-098]] ~ [[tc-102-cancelled-slots-reused-for-new-sublot|TC-102]]，补齐已装货取消、提交后补偿、多 SUBLOT 隔离、物理操作串行与释放仓位复用。
- 第七批补充（`01-site-operations` 域）：[[tc-103-departure-wait-start-and-visual-warning|TC-103]] ~ [[tc-113-load-batch-auto-commit-and-wait-reset|TC-113]]，覆盖站点离站等待、超时原子取消、部分装货阻断、断联、竞态、后续路由、发车失败与 LoadBatch 自动提交。
- 第八批补充（`01-site-operations` 域）：[[tc-114-load-hardware-fault-holds-without-replacement-or-auto-clear|TC-114]]～[[tc-123-load-compensation-cancels-transport-demand|TC-123]]，覆盖装货批量开锁发生关键硬件反馈故障时不换仓、不新增开门、不自动清空，信号恢复后仍须授权维护人员人工确认和服务端授权，普通生产操作员越权确认被拒绝，R-09 整批清空决定和维护/生产管理兼任权限边界，普通取消不能绕过生产决策权限，整批清空决定缺少有效二次认证或原因码时拒绝提交，R-09 审批不替换 Sublot 生产操作员，以及三种补偿原因整批清空后统一以 `CANCELLED_BY_LOAD_COMPENSATION` 取消原搬运需求。
- 2026-07-14 起，本目录下按 `03-use-cases/` 同名的 11 个业务领域拆成子文件夹，TC 应与其验证的 FR 放在同一个领域子文件夹里，具体规则与映射表见 [[classification-rules|FR/NFR/TC 分类规则]]；本 `README.md` 仍保留在根目录。
