# 2026-10-17 agv03 充电单：建单后约 30 分钟未派，充电中派出（现场观测，非实验轮）

这不是本实验室的实验轮，没有 round-plan，也没有任何为本实验室做的写操作。来源是 v2 生产切换现场（`8005-agv-control-server#564` 方案 A，2026-10-17 14:11:53 开闸，factory01 上的 v2 实例，生产 RIoT `172.19.206.222:8888`，map 26 `老厂前线new_wk`）。现场会话对 RIoT 只做只读 GET；订单由 v2 实例在开闸后自动建。

知识条目：[`BC-ORDER-023`](../../../knowledge/behavioral-contracts.md)；开放问题：[`Q-044`](../../../hypotheses/open-questions.md)。

| 文件 | 内容 | 原始出处 |
| --- | --- | --- |
| `01-order-before-dispatch-1421.txt` | 14:21 只读 `GET /api/order/v1/orderRecord/detailByOrderId/order-2111339400939044864` 原始响应 | 现场证据 `production-20261014/d5/51-agv03-charge-order.txt`，原样复制 |
| `02-order-after-dispatch-1443.txt` | 14:43:18 同一接口原始响应 | 同上 `d5/54-agv03-charge-order-after.txt`，原样复制 |
| `03-trip-watch-1408-1445.txt` | 约 30 秒一次的三车读数摘录 | 同上 `d2/34-trip-watch.txt`，只删列，见文件头 |

没有落盘、只在现场会话对话里读过的读数（`ro-riot-battery.ps1` 输出），在知识条目里单独标出，不当作这里的文件证据。

车：agv03 = `BROKERX-7daca4ee91da498d8026c68b7b941127`，RIoT 车名「老厂前线新多仓位3」，见 `remote-ops/fleet.md`。
