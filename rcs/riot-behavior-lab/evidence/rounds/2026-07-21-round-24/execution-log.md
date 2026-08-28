# Round 24 执行日志 — 移动 + 充电(act 78)

## 状态

部分完成：失败 HANG 已确认；成功订单未闭环（用户取消）；有线充电只读已采

## 建单要点

- 普通单：`move(站6) + act(78, param1=1, param2=0)`
- 站6 配置 `user_define_properties.enter_exit="8"` 后可通过；RIoT 自动展开为 `move(8)→move(6)→act(78)`
- 无进入退出点时 `10008`

## S1 失败路径

- act `resultCode=407802`
- **会重试**：失败后再次走 move，再进 act（本轮约 2～3 轮）
- 最终 `orderState=9 HANG`，`proc=INNER_FORCE_IDLE`
- 证据：`S1b-*` / `S1b-hang-detail.json`

## S2 成功路径（订单）

- 已到 act 后被用户取消 → `CANCELLED(2)`，未采到订单 SUCCESS

## S3 有线充电器只读（不下单）

- 首次（未解抱闸）：`batteryState=CHARGING`，但 `control=ERR` / `state=ERROR`；电量 22→23
- **解抱闸后复读**：`break=MOVABLE` / `breakSwState=1`，`control=OK`，聚合 `state=CHARGING`；电量约 24
- `proc=IDLE`，未强制移动
- 证据：`S3-wired-charge-*.json` / `S3b-wired-charge-after-brake-*.json`
