# 07 — `riot-sdk` 新增五个 `imap` 具名 Facade，发一版，服务端升 vendored 包

**做什么：** 让控制服务端能通过具名 Facade 取得路网边表与移除集，不使用 `.Raw`。分三步，
一张票走完：`riot-sdk` 新增五个方法 → 发一版 → `8005-agv-control-server` 升 vendored 包。

五个端点（`CP-0001` 修订项二批准的清单，`removedEdgeDetail` 不在内）：

- `GET /api/imap/v1/mapInfo/edges/{mapId}`
- `GET /api/imap/v1/mapInfo/stations/{mapId}`
- `GET /api/imap/v1/mapResource/removedEdge/{mapId}`
- `GET /api/imap/v1/mapResource/removedStation/{mapId}`
- `GET /api/imap/v1/mapEdgeGroup/all`

**自定义反序列化落在 SDK 内部**，不外溢到产品代码：snake_case、`s_node`／`e_node`、
站点侧键名字面带点。这是规格 5.6 的定案——产品代码看到的是干净的领域类型。

命令面的六个 Facade（`CancelOrder`／`OrderHold`／`OrderContinue`／`HangContinue`／
`TriggerEmergencyStop`／`CancelEmergencyStop`）**SDK 里已经有了并有测试**，本票不碰它们，
票 10 直接用。

**前置：** 票 04（`CP-0001` 批准）。未批准前不得据修订文开工。

**状态：** resolved（2026-09-07）—— 决议见 [07-answer.md](07-answer.md)。最后一条验收依赖票 03

- [ ] 五个方法在 Facade 层有具名实现，返回领域类型而非生成客户端的原始 DTO
- [ ] 反序列化的三处怪癖在 SDK 内部处理，每处有测试覆盖
- [ ] 五个方法各有 Facade 测试，与既有 Facade 测试同形态
- [ ] SDK 发一版，版本号可被 `Directory.Packages.props` 精确引用
- [ ] `8005-agv-control-server` 的 vendored 包升到新版，`RiotSdkPackageProvenanceTests` 仍绿
- [ ] 服务端 `src/` 下 `.Raw` 仍是零命中（这条由票 08 的架构测试守，本票不得引入首个命中）
- [ ] 假 RIoT 侧（票 03）的五个端点与真 SDK 的调用形状对得上，L2 可用
