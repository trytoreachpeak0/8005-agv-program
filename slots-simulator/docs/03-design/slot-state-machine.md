# 仓位状态机设计模板

> 状态：Draft  
> 最后更新：YYYY-MM-DD  
> 主要依据：FR-002、FR-003、FR-004、FR-015、DR-010、DR-013、DR-014

## 1. 目的与边界

本文精确定义仓位动作的前置条件、副作用、错误和并发规则。  
注意：锁、门、实际遮挡、光幕 DI 是不同概念；占用状态由光幕 DI 即时推导，不独立存储。

## 2. 状态变量

| 变量 | 类型/候选值 | 来源 | 是否持久化 |
| --- | --- | --- | --- |
| `lockCommandDO` | `0/1` | Modbus | 否 |
| `lockStateDI` | `Locked/Unlocked` | 闩锁机构反馈或故障注入 | 否 |
| `doorState` | `Closed/Open` | 开锁成功自动弹门、API/WPF 关门 | 否 |
| `actualObstruction` | `Clear/Obstructed` | 放料、取出、测试构造 | 否 |
| `lightCurtainDI` | `Clear/Obstructed` | 正常镜像或故障注入 | 否 |
| `occupancy` | `Empty/Occupied` | 由 `lightCurtainDI` 计算 | 不存储 |
| `faults` | 故障集合 | API | 否 |

派生规则：

```text
occupancy = lightCurtainDI == Obstructed ? Occupied : Empty
```

## 3. 为什么不用单个枚举表示全部状态

仓位状态是锁、门、遮挡和故障的正交组合。若全部塞进一个枚举，会产生大量组合状态。建议：

- 使用多个明确变量保存事实。
- 使用动作 Guard 限制合法组合。
- 对外提供统一 `SlotSnapshot`。

## 4. 动作定义

### 4.1 Modbus 写开锁 DO

前置条件：地址和写入值合法。  
正常副作用：

1. 更新 DO。
2. Level 模式持续保持；Pulse 模式启动/重启计时器。
3. 有效开锁且未注入失败时，弹簧自动弹门：`doorState = Open`、`lockStateDI = Unlocked`。

### 4.2 关门 `closeDoor`

前置条件：门当前开启且开锁 DO 已复位。

副作用：`doorState = Closed`、`lockStateDI = Locked`。

注意：关门本身不改变遮挡和占用。

### 4.3 放料 `placeCargo`

前置条件：

- 门已开启。
- 实际遮挡当前为 Clear。

副作用：

- `actualObstruction = Obstructed`。
- 无光幕脱钩故障时 `lightCurtainDI = Obstructed`。
- 占用立即派生为 Occupied，无需等待关门。

### 4.4 取出 `removeCargo`

前置条件：

- 门已开启。
- 实际遮挡当前为 Obstructed。

副作用：

- `actualObstruction = Clear`。
- 无光幕脱钩故障时 `lightCurtainDI = Clear`。
- 占用立即派生为 Empty。

## 5. 迁移表

| 动作 | Guard | 成功后的变化 | 失败错误 |
| --- | --- | --- | --- |
| 开锁 DO | 地址合法且当前可触发 | 门→开启、锁 DI→未锁；DO 按模式保持/复位 | Modbus 异常 / 注入的开锁失败 |
| 关门 | 门开启且 DO 已复位 | 门→关闭、锁 DI→锁闭 | `DOOR_ALREADY_CLOSED` / `UNLOCK_OUTPUT_ACTIVE` |
| 放料 | 门开启且无遮挡 | 遮挡→有 | `DOOR_NOT_OPEN` / `CARGO_ALREADY_PRESENT` |
| 取出 | 门开启且有遮挡 | 遮挡→无 | `DOOR_NOT_OPEN` / `CARGO_NOT_PRESENT` |

> TODO：错误码名称需与 OpenAPI 文档统一。

## 6. 故障状态

| 故障 | 正常关系 | 故障行为 | 清除后 |
| --- | --- | --- | --- |
| 开锁/弹门失败 | 脉冲触发弹门且锁 DI 变未锁 | 门保持关闭、锁 DI 保持锁闭 | 按当前门和闩锁事实重建 |
| 闩锁失败 | 关门后锁 DI 变锁闭 | 关门后锁 DI 保持未锁 | 按当前门和闩锁事实重建 |
| 光幕 DI 不跟随 | DI 镜像实际遮挡 | 保持注入值或冻结值 | 按实际遮挡重建 |
| 模块断连 | TCP 正常服务 | 断开并拒绝连接 | 恢复监听 |
| 模块不响应 | 正常返回 PDU | 保持连接但不回复 | 恢复处理请求 |

故障必须能够显式清除；完整 reset 清除全部故障。

## 7. Pulse 模式

```text
写 ON
  ├─ 设置 DO=1
  ├─ 正常情况下门自动弹开、锁 DI=未锁
  └─ 启动 pulseWidthMs 计时

计时期间再次写 ON
  └─ 取消旧计时，从本次写入重新计时

计时到期
  ├─ 设置 DO=0
  └─ 门仍开、锁 DI 仍未锁，等待人工关门
```

必须使用可取消且带版本的计时器，防止 reset 后旧回调执行。

## 8. 并发与原子性

- 同一仓位的 Modbus、API 和计时器事件进入同一串行边界。
- 不同仓位可以并行。
- 涉及多个仓位的批量 API：
  1. 先验证全部目标；
  2. 按稳定顺序获取执行权；
  3. 全部成功或全部失败。
- Modbus 批量写同样不得部分提交。

## 9. 场景示例

### 9.1 正常装载

```text
主系统写开锁 DO
→ 弹簧自动弹门、锁状态 DI 未锁
→ API 放料
→ 光幕 DI 有遮挡，派生占用
→ API 关门
→ 锁状态 DI 锁闭
```

### 9.2 UC-001 E4.1

开门后未执行放料便关门，光幕 DI 仍无遮挡；模拟器只呈现硬件事实，由主系统识别异常。

### 9.3 空闲记录但实际有物

测试 API 预设实际遮挡，光幕 DI 显示有物；主系统开锁后由该硬件事实发现异常。

## 10. 待确认事项

- [ ] 锁状态 DI 的 0/1 与 Locked/Unlocked 对应关系
- [ ] 故障注入采用冻结当前值还是指定固定值
- [ ] 批量仓位操作的最大请求数量
- [ ] API 幂等键是否需要支持

## 11. 验证清单

- [ ] 每个动作至少有成功、Guard 失败、重复调用测试
- [ ] reset 后旧计时器不会回写
- [ ] 故障清除后反馈按当前事实重建
- [ ] 占用值始终等于光幕 DI 推导结果
