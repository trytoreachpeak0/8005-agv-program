# Round 4（2026-07-20）

## 1. 研究目标

- 关联问题：`Q-018`
- 本轮要回答：现场有哪些有效地图，如何得到 `mapId`↔地图名。
- 明确不回答：站点清单（C2）、建单、路网；测试车当前绑定地图若无法从字段直接读出，只记录线索，不臆造。

## 2. 环境元数据

- 鉴权：`callApiKey`（BC-AUTH-002）
- 测试车：`新基测试300c协作1` / `BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 本机时区：`Asia/Shanghai`

## 3. 范围与授权

- 只读：`C1`（mapInfo/all + 轻量对照 + 测试车地图线索）
- 写操作：无
- 授权：2026-07-20，用户要求在已知派哪台车之后，继续弄清有哪些地图

## 4. 执行顺序

1. `GET /api/imap/v1/mapInfo/all`
2. `GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson`
3. 测试车只读状态中的地图相关字段探查
4. 更新 open-questions / knowledge / fixtures

## 5. 本轮状态表

| 编号 | 测试项 | 状态 |
|---|---|---|
| C1 | mapInfo/all 地图清单 | 通过 |
| C1 | getALLMapInfoExcludeMapJson 对照 | 通过 |
| C1 | 测试车当前 mapId 线索 | 通过（结论：对象上无直接 mapId） |

## 6. 收尾确认

- 无写操作、无遗留订单
- 凭据已脱敏
- 几何 `mapJson` 未写入证据
