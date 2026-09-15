# 每个物理仓位最多存放一个花篮

同事初稿 §4 确定车辆有 8 个固定物理仓位，§5.1 规定服务端根据操作员提交的 Sublot 解析任务后下发完整仓位列表。业务上一个 Sublot 包含 1～N 个花篮；每个物理仓位最多存放一个花篮，每个花篮必须各自分配一个目标仓位，即 OneBasketPerSlot。

服务端在 OperationCommitPoint 前必须满足：

`ExpectedBasketCount == SlotOperationCommand.slots.Count`

并且目标仓位数量不得超过当前可操作且满足业务条件的仓位数量。装货前，每个目标仓位的 SlotBusinessState 必须可预留，车载 SlotOccupancyState 必须为 EMPTY；卸货前，每个目标仓位必须属于该子批号，车载 SlotOccupancyState 必须为 OCCUPIED。任一仓位不满足时拒绝整个操作，不打开任何仓门。

仓内光幕只负责判断一个仓位 OCCUPIED、EMPTY 或 UNKNOWN，不负责识别产品、统计同仓数量或判断子批号归属；这些业务约束由服务端的任务、子批号和仓位分配保证。花篮没有独立身份，按 ADR-cross-0044 作为 AnonymousBasket 处理。

**Status**: accepted（部分由 [ADR-cross-0059](0059-front-rear-slot-groups-judged-server-side.md) 修订：可用仓位数与物理仓位数改按所需仓位分组计，2026-09-15 随 `CP-0002` 批准）

**Considered Options**:
- 允许一个仓位放多个花篮（拒绝：单个光幕占用状态无法证明花篮数量）
- 不校验花篮数与目标仓位数，由操作员自行分配（拒绝：会破坏 LoadBatch 整批原子性）
- 一仓一篮，服务端保证数量映射，车载端验证物理占用前置条件（采纳）

**Consequences**:
- 一个 LoadBatch 最多容纳的花篮数受车辆固定物理仓位数和当前 SlotOperability 共同限制。
- 子批号花篮数大于可用仓位数时，服务端直接拒绝本次装货，不允许部分装入。
- 服务端负责 Sublot 与仓位的业务映射；车载端只在活动装货的最小恢复记录中保留提交的 Sublot 引用，不拥有其任务详情、产品标识或业务生命周期。
- 逐仓 OperationResult 仍按物理仓位号报告，服务端据占用仓位数量核对花篮数，不关联单篮身份。
- 初稿 §4、§5.1 和 §14 应增加花篮数、仓位数及初始占用状态的整批校验。
