# ADR Index

Architecture Decision Records for the whole repo. Cite as `ADR-<category>-<NNNN>` (e.g. `ADR-sdk-0005`, `ADR-cross-0001`, `ADR-mes-0002`).

## cross — 跨子系统

| ID | Title |
|---|---|
| [ADR-cross-0001](cross/0001-v1-facade-shaped-for-mes-dispatch.md) | 第一版 Facade 按 MES 派车闭环定形，Lab 共用 |
| [ADR-cross-0002](cross/0002-hang-continue-named-facade.md) | HangContinue 与 OrderContinue 分开具名封装 |
| [ADR-cross-0003](cross/0003-onboard-disconnect-safe-finish-and-server-resume.md) | 车载上位机断线时只收尾当前开锁集合，重连后由服务端授权续行 |
| [ADR-cross-0004](cross/0004-onboard-hmi-exclusive-io-authority.md) | 车载上位机独占 IO 控制与硬件安全裁决 |
| [ADR-cross-0005](cross/0005-slot-physical-and-business-state-authority.md) | 仓位物理事实归车载上位机，业务事实归服务端 |
| [ADR-cross-0006](cross/0006-onboard-minimal-recovery-journal.md) | 车载上位机只持久化最小可恢复执行日志 |
| [ADR-cross-0007](cross/0007-stable-slot-identity-and-maintenance-io-config-change.md) | 仓位身份稳定，IO 配置只在整车配置维护态换版 |
| [ADR-cross-0008](cross/0008-onboard-departure-safety-server-movement-control.md) | 车载端给出离站安全许可，服务端控制车辆移动 |
| [ADR-cross-0009](cross/0009-fresh-safety-check-before-each-movement.md) | 每次请求车辆移动前必须取得实时安全核验 |
| [ADR-cross-0010](cross/0010-automatic-movement-intervention-on-safety-revocation.md) | 发车后安全许可失效必须自动介入车辆移动 |
| [ADR-cross-0011](cross/0011-tiered-riot-stop-on-departure-safety-revocation.md) | 离站安全许可失效采用暂停、取消、急停三级介入 |
| [ADR-cross-0012](cross/0012-persisted-movement-guard-during-station-operation.md) | 站点仓位操作期间服务端必须持续阻断车辆移动 |
| [ADR-cross-0013](cross/0013-progress-is-telemetry-result-commits-per-slot.md) | 实时进度只作遥测，可靠结果保留逐仓物理事实 |
| [ADR-cross-0014](cross/0014-durable-command-acceptance-and-same-operation-reconciliation.md) | 车载端持久化指令后才接受，超时沿用原仓位操作尝试编号对账 |
| [ADR-cross-0015](cross/0015-no-generic-cancel-load-recovers-unload-must-complete.md) | 不提供瞬时通用取消；装货清空后可取消，卸货必须完成 |
| [ADR-cross-0016](cross/0016-slot-command-is-irrevocable-commit-point.md) | 仓位操作指令一经发出即不可撤回 |
| [ADR-cross-0017](cross/0017-restart-resumes-only-from-proven-checkpoint.md) | 车载重启后只从可证明检查点恢复原操作 |
| [ADR-cross-0018](cross/0018-project-wide-operator-verification-enabled.md) | 装卸身份核验分别采用项目级策略，8005 装货启用、卸货关闭 |
| [ADR-cross-0019](cross/0019-onboard-technical-logs-server-business-audit.md) | 车载端保存硬件技术日志，服务端保存业务审计 |
| [ADR-cross-0020](cross/0020-io-config-drafts-and-maintenance-activation.md) | IO 配置草稿可离线编辑，只能在整车配置维护态激活 |
| [ADR-cross-0021](cross/0021-server-consumes-capabilities-not-io-configuration.md) | 服务端只消费仓位能力，不读取 IO 配置 |
| [ADR-cross-0022](cross/0022-capability-full-sync-on-connect-reliable-on-change.md) | 车载能力连接时全量同步，变化时可靠推送 |
| [ADR-cross-0023](cross/0023-one-fenced-connection-session-per-agv.md) | 每台 AGV 只承认一个带代次保护的车载连接会话 |
| [ADR-cross-0024](cross/0024-per-agv-connection-credential.md) | 每台 AGV 使用独立连接凭证 |
| [ADR-cross-0025](cross/0025-pinned-self-signed-tls-and-per-agv-secret.md) | 使用固定信任的自签名 TLS 证书与每车共享密钥 |
| [ADR-cross-0026](cross/0026-hold-system-movement-on-onboard-connection-loss.md) | 行驶中车载连接失联时暂停本系统移动任务 |
| [ADR-cross-0027](cross/0027-two-second-heartbeat-six-second-liveness-timeout.md) | 采用 2 秒心跳与 6 秒静默失联判定 |
| [ADR-cross-0028](cross/0028-connected-session-requires-explicit-business-readiness.md) | 车辆已连接不等于业务就绪 |
| [ADR-cross-0029](cross/0029-unified-five-step-recovery-handshake.md) | 首次连接与重连采用统一五步恢复握手 |
| [ADR-cross-0030](cross/0030-uniform-ndjson-protocol-envelope.md) | 所有车载通信消息使用统一 NDJSON 外壳 |
| [ADR-cross-0031](cross/0031-integer-protocol-version-with-exact-match.md) | 车载通信采用整数版本并要求精确匹配 |
| [ADR-cross-0032](cross/0032-explicit-message-delivery-classes.md) | 协议消息采用明确的交付类别 |
| [ADR-cross-0033](cross/0033-onboard-publishes-abstract-safety-state-changes.md) | 车载端可靠发布抽象安全状态变化 |
| [ADR-cross-0034](cross/0034-heartbeat-versions-detect-safety-state-gaps.md) | 心跳通过版本号发现能力与安全状态缺口 |
| [ADR-cross-0035](cross/0035-server-orders-slots-onboard-executes-array-order.md) | 服务端确定目标仓位集合，车载端批量开锁 |
| [ADR-cross-0036](cross/0036-load-batch-commit-and-hardware-fault-hold.md) | 装货整批成功才提交，硬件故障暂停等待人工处置 |
| [ADR-cross-0037](cross/0037-unload-batch-clears-business-state-only-after-all-empty.md) | 8005 卸货跨 Sublot 批量开锁，按仓位独立清空业务状态 |
| [ADR-cross-0038](cross/0038-new-slot-operation-attempt-id-after-compensated-load-retry.md) | 装货补偿后重试使用新的仓位操作尝试编号（已由 ADR-cross-0039 废止） |
| [ADR-cross-0039](cross/0039-operator-starts-server-authorized-load-compensation.md) | 操作员发起、服务端授权装货补偿 |
| [ADR-cross-0040](cross/0040-internal-light-curtain-is-slot-occupancy-evidence.md) | 仓内光幕作为仓位有货与空仓的物理证据 |
| [ADR-cross-0041](cross/0041-one-basket-per-physical-slot.md) | 每个物理仓位最多存放一个花篮 |
| [ADR-cross-0042](cross/0042-sublot-is-load-input-and-server-resolves-task.md) | 装货输入是 SUBLOT，服务端解析任务和花篮数 |
| [ADR-cross-0043](cross/0043-server-enforces-global-sublot-reservation.md) | 服务端保证 SUBLOT 的全局唯一占用 |
| [ADR-cross-0044](cross/0044-baskets-have-no-individual-identity.md) | 花篮没有独立身份，只追踪 SUBLOT 与仓位 |
| [ADR-cross-0045](cross/0045-load-final-confirmation-and-precommit-correction.md) | 装货正式提交前允许原操作内纠错 |
| [ADR-cross-0046](cross/0046-load-task-cancellable-until-departure-after-full-clearance.md) | 装货任务离站前可取消，但必须整批清空 |
| [ADR-cross-0047](cross/0047-demand-id-identifies-station-task-and-cancellation.md) | DemandId 标识站点任务，TransportDemandKey 负责取消抑制 |
| [ADR-cross-0048](cross/0048-versioned-current-stop-worklist-snapshot.md) | 当前停靠作业清单使用带版本的完整快照 |
| [ADR-cross-0049](cross/0049-station-task-type-many-to-many-admission.md) | 站点与任务类型采用多对多准入关系 |
| [ADR-cross-0050](cross/0050-admission-policy-frozen-at-operation-commit.md) | 任务类型准入规则在操作承诺点冻结 |
| [ADR-cross-0051](cross/0051-admission-policy-stored-in-server-db-no-v1-ui.md) | 任务准入关系存服务端数据库，第一版不做配置界面 |
| [ADR-cross-0052](cross/0052-onboard-clears-before-server-finalizes-load-cancellation.md) | 车载端清空全部目标仓位后服务端才完成取消 |
| [ADR-cross-0053](cross/0053-onboard-upcoming-stop-plan-and-vehicle-overview.md) | 车载端展示后续停靠计划与四维车辆概览 |
| [ADR-cross-0054](cross/0054-auto-load-commit-with-pre-departure-correction.md) | 装货物理闭环后自动提交，整站结束前仍可纠错 |
| [ADR-cross-0055](cross/0055-server-owned-station-departure-wait-timeout.md) | 服务端掌握装货站离站等待超时并原子结束本站 |

## sdk — RIoT SDK

| ID | Title |
|---|---|
| [ADR-sdk-0001](sdk/0001-default-auth-callapikey.md) | 第一版默认鉴权使用 CallApiKey |
| [ADR-sdk-0002](sdk/0002-v1-seam-session-named-methods-raw-escape.md) | RiotSession 具名方法为主，Raw 为逃逸舱 |
| [ADR-sdk-0003](sdk/0003-v1-facade-method-scope.md) | 第一版必须封装的 Facade 能力范围 |
| [ADR-sdk-0004](sdk/0004-v1-csharp-python-parity.md) | 第一版 C# 与 Python 同步交付 |
| [ADR-sdk-0005](sdk/0005-facade-throws-on-business-failure.md) | 具名 Facade 统一将业务失败转为 RiotApiException |
| [ADR-sdk-0006](sdk/0006-imap-via-kiota.md) | Map/Station 经 imap OpenAPI 纳入 Kiota 生成 |
| [ADR-sdk-0007](sdk/0007-ready-helpers-no-blocking-wait.md) | 可再派判定辅助，不内置阻塞 Wait |
| [ADR-sdk-0008](sdk/0008-v1-explicit-non-goals.md) | 第一版明确排除的能力 |

## mes — MES / 调度策略

| ID | Title |
|---|---|
| [ADR-mes-0001](mes/0001-queueing-stall-handling.md) | QueueingStall：预防 + 下单前清积压；超时只报警 |
| [ADR-mes-0002](mes/0002-order-hang-handling.md) | OrderHang：充电与普通分支分开 |
| [ADR-mes-0003](mes/0003-charging-hang-auto-reassign.md) | 充电 OrderHang 由 MES 自动改派 |
| [ADR-mes-0004](mes/0004-charge-hang-station-selection.md) | 充电改派选桩：允许集合内 NearStationQuery |
| [ADR-mes-0005](mes/0005-charge-hang-retry-limit.md) | 充电自动改充重试上限 N=2 |
| [ADR-mes-0006](mes/0006-mes-ingest-vs-dispatch.md) | MES 任务接入与调度拆开；第一期只交付接入投影 |
| [ADR-mes-0007](mes/0007-mes-ingest-tech-stack.md) | MesIngest 第一期：Service + WPF + SQL Server |
| [ADR-mes-0008](mes/0008-full-source-snapshot-incremental-local-projection.md) | MES 完整源快照与本地增量投影/有界读取分离 |
| [ADR-mes-0009](mes/0009-demand-change-feed-and-authoritative-bootstrap.md) | Demand 变更账本采用有限保留与权威 Bootstrap |
| [ADR-mes-0010](mes/0010-watch-business-read-only-with-telemetry-ingest.md) | MesIngestWatch 保持业务只读，并允许受限遥测追加 |
| [ADR-mes-0011](mes/0011-series-error-catalog-owned-by-mesingest-contract.md) | Series 错误目录由 MesIngest 领域契约拥有 |
| [ADR-mes-0012](mes/0012-series-error-history-retained-with-demand-series-events.md) | Series 错误历史随 DemandSeriesEvent 永久保留 |
| [ADR-mes-0013](mes/0013-error-search-uses-as-of-event-history-snapshots.md) | 错误检索使用冻结时点的事件历史快照 |
| [ADR-mes-0014](mes/0014-series-error-history-separated-from-current-ingest-attention.md) | Series 错误历史与当前接入关注项分离 |
| [ADR-mes-0015](mes/0015-overview-uses-one-consistent-host-snapshot.md) | Watch 概览使用一个一致的 Host 业务快照 |
| [ADR-mes-0016](mes/0016-readability-audit-has-its-own-projection-snapshot.md) | 资格审计使用独立的投影快照身份 |
| [ADR-mes-0017](mes/0017-new-mesingest-replaces-the-database-and-contract.md) | 新 MesIngest 以空库和新契约整体替换旧版 |
