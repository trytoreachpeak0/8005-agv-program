# Round 27（2026-07-21）— 执行中异常进入 HANG 与 CONTINUE 判别

## 问题（Q-035 / 修订 Q-006）

纯 move 执行中，下列异常是否进入 `orderState=9 HANG`？`CONTINUE_FROM_HANG` 能否区分可恢复 vs 需人工介入？

| 场景 | 触发 | 预期 HANG | CONTINUE |
|------|------|-----------|----------|
| A | 硬件急停 | 是 | 失败；车态可见急停 |
| B | 软件急停 `triggerEmergency` | 是 | 解急停后可成功 |
| E | 单机取消移动 | 是 | 可成功 |
| F | 旋钮进入解抱闸 | 是 | 失败；需人工拨回 |

暂缓：关机(C)、主动造故障(D)。

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：map29（api测试）；多段 move 往返拉长执行窗口
- `appointVehicleKey` 绑本车；不碰全局交管清理

## 步骤（每场景）

1. baseline：IDLE / 定位 / 无急停 / 抱闸可动
2. 建单 → 等到 EXECUTING
3. 人工或 API 触发异常
4. 密采样至 HANG
5. CONTINUE 探针（B：可先 cancelEmergency）
6. 清场后下一场景
