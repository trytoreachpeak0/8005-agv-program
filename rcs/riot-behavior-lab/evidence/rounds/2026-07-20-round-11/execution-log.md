# Round 11 执行日志（2026-07-20）

## 0. 状态

- 中途：S2 副作用导致 `enable=false` → 人工网页上线后 resume
- 收尾：站 1，`IDLE`，`enable=true`，`ON_LINE`

## 1. S1 无/假 appointVehicleKey 后派

| 用例 | 观察 | 结论 |
|---|---|---|
| **省略** `appointVehicleKey` | ~5s 内 `orderState=3`，`executeVehicleKey=测试车` | **会自动派车**；本轮派到空闲测试车，**未误派其它车** |
| **伪造** key | 90s 保持 `QUEUEING` / `execute=--` | 不会后派到真实车（至少短时） |

证据：`S1-nokey-*`，`S1-fakekey-*`  
消费：业务**禁止省略**指定车；空闲时省略可能派到任意可调度车。

## 2. S2 Q-020 调度上线 API

- `updateVehicleIntegrationLevel` 多种 body → `code=00002` 内部错误
- **危险副作用**：失败调用后 `enable→false`，`integrationLevel` 清空（对比 `S1-post-idle` 仍 ON_LINE）
- `vehicles/setting/update` → `00004` 参数类型不支持
- API 无法恢复；需网页上线

证据：`S2-online-attempts.json`，`S2-CRITICAL-offline.json`  
**硬性**：不要在生产脚本里调用该接口做“尝试上线”。

## 3. S3 多段 move→move

轨迹（离站出发 → 站1 → 站2）：

```text
order=1 idx=-1
→ order=3 idx=0 move RUNNING
→ order=3 idx=1 move RUNNING   （第二段）
→ order=5 idx=-1 IDLE st=2 SUCCESS
```

`executingIndex` 可区分当前段；全程绑测试车。完成后可再派。

证据：`S3-multimove-samples.json`

## 4. S4 REJECTED / HANG 命令族（执行中纯 move）

| 命令 | code | 消息 | 状态变化 |
|---|---|---|---|
| `CMD_ORDER_REJECTED` | **10015** | 订单无法推出队列 | 无，继续 EXECUTING |
| `CMD_ORDER_CONTINUE_FROM_REJECTED` | **10016** | 订单无法撤回队列 | 无 |
| `CMD_ORDER_CONTINUE_FROM_HANG` | **100021** | 基于车辆原因订单无法跳过或者继续 | 无 |
| `CMD_ORDER_JUMP_FROM_HANG` | **100021** | 同上 | 无 |

本现场执行中 move **不能**靠 REJECTED/HANG 族暂停；暂停仍用 HELD（Round10），取消用 CANCEL。

证据：`S4-*`

## 5. S5 act（等待 actionId=129）+ interrupt

- `move` + `act(129,15s)`：到达 act 段（`idx=1`，`missionType=act`，`MT_FINISHED`）后 interrupt → 仍 **`100036`**，订单继续，等待结束后 SUCCESS（经 cancel 路径前已采样）
- `act-only` 等待 5s：进入 EXECUTING 后 interrupt 仍 **`100036`**，随后自然 SUCCESS

结论：至少对模板「等待」类 act，`interrupt` **同样不可用**。

证据：`S5-*`，`S5b-*`

## 脚本

- `run-round11.ps1`（S1–S2，中断于人工）
- `run-round11-resume.ps1`（S3–S5）
