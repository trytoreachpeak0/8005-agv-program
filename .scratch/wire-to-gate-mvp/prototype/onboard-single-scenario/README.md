# OnboardHmi 单场景操作原型（PROTOTYPE）

> THROWAWAY REVIEW ASSET — 仅用于“验证 OnboardHmi 单场景操作原型”票据的交互与责任边界评审，不是 ControlServer、OnboardHmi 或共享协议仓库的生产依赖，不得直接提升为生产代码。

三种 OnboardHmi 单场景布局，位于一个本地 HTML 路由，通过 `?variant=A|B|C` 与底部悬浮评审栏切换。原型覆盖连接与业务就绪分离、唯一 Demand、机台到站、Sublot 输入、多仓批量装货、发车安全等待、关卡自动批量卸货、本地完成、断联收敛、重启对账和最小异常处置。

## 运行

从仓库根目录执行一条命令：

```powershell
Start-Process '.\.scratch\wire-to-gate-mvp\prototype\onboard-single-scenario\onboard-single-scenario-prototype.html'
```

也可直接双击 HTML。查询参数可分享当前评审位置，例如：

```text
onboard-single-scenario-prototype.html?variant=A&stage=SUBLOT_ENTRY
```

左右方向键切换布局；焦点位于输入框、下拉框或可编辑内容时不会截获方向键。顶部“评审状态”可切换完整正常与异常状态。底部状态证据区始终显示当前组合状态，便于检查业务投影、车载物理事实和允许动作有没有被错误混成一个状态。

## 三个候选

- **A — 旅程导引台（推荐为领先候选）**：左侧固定旅程、中央只给当前一步和一个主动作、右侧固定八仓。适合单 Demand、低分支的现场作业。
- **B — 安全优先双栏**：安全与联锁占据最高视觉优先级，业务工作区和允许动作分栏。适合评审异常、断联和恢复是否足够醒目。
- **C — 站点作业板**：顶部四维车辆概览与横向路线，中部按当前站点呈现大尺寸触控工作区。适合评审车载屏幕上的触控密度与站点切换。

用户已选定 A 为后续生产 OnboardHmi 的 prototype-authoritative 交互与布局依据。B、C 只保留为设计证据；实施若吸收其局部元素，必须保持 A 的窗口层级、旅程层级、主工作区与固定八仓关系，并记录具体映射和理由。

## 评审必须回答

1. 车载端实际目标分辨率、缩放比例与触控/键鼠方式下，关键状态和按钮是否无需滚动或误触风险可接受？
2. “已连接”与 `VehicleBusinessReadiness`、本地任务完成与 `DepartureSafe` 是否清楚分离？
3. Sublot 扫描/键盘共用入口、ExpectedBasketCount 与完整仓位集只读，是否符合实际扫码设备接入方式？
4. 八仓图是否能让开发者实现业务绑定、占用三态、锁闭反馈、输出复位、本次目标和 ActiveUnlockSet，而不引入双主？
5. 断联时只允许 `SafelyFinishActiveUnlockSet`，重连/重启后五步对账且 READY 前禁用业务操作，是否可实现？
6. ExceptionRecoverySession 的四条批准路径、个人身份和固定范围能否映射到车载端能力；哪些现场动作需要额外但不属于系统审批的真实资质？
7. 关卡到站无需再扫 Sublot/工号，全部目标仓位自动批量卸货；8005 本地成功不等待 PDA/MES，是否会引发现场误解？

## 当前评审状态

- 获选方案：A — 旅程导引台。
- 用户侧选择依据：依据用户对本 Wayfinder 后续各票采用推荐值的明确授权。
- 车载端开发同事评审：**尚未发生；用户于 2026-08-25 明确豁免当前原型票的该门禁，不声称车载端开发同事已经批准**。
- 票据结论：A 已由用户作为 MVP 产品范围与最终发布的唯一批准人选定；真实车载分辨率、缩放、触控与扫码输入、现场可读性和可实现性转入实施与受控工厂试运行验收。本豁免不适用于共同协议 release 或其它需要真实第三方批准的后续门禁。

## 权威来源

- [验证 OnboardHmi 单场景操作原型](../../issues/08-validate-onboard-single-scenario-interaction-prototype.md)
- [决定机台取货、多仓装货、关卡卸货与成功边界](../../issues/04-decide-pickup-loading-gate-unloading-and-success-boundary.md)
- [决定 MVP 多仓容量、安全联锁与异常恢复最小集](../../issues/05-decide-minimum-multislot-safety-and-recovery-set.md)
- [决定 MVP RIoT 移动、建单对账与人工充电边界](../../issues/06-decide-riot-movement-order-reconciliation-and-manual-charging-boundary.md)
- [决定 ControlServer—OnboardHmi 职责边界与 MVP 消息面](../../issues/07-decide-controlserver-onboard-responsibilities-and-mvp-message-surface.md)
- [`CONTEXT.md`](../../../../CONTEXT.md) 与 [`docs/adr/cross/`](../../../../docs/adr/cross/)
