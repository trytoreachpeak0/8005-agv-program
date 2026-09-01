# 2026-08-26 阶段性 G3：真实双端、不动车

## 结论

`STAGED_G3_REAL_PEERS_NO_MOVEMENT` 运行通过，启动范围为 `W2G-IS-00` 与
`W2G-IS-06` 的会话、恢复和可靠重连基础。本结果不是任一完整切片的正式 G3
PASS；两片仍保持 `INCONCLUSIVE`，直到各自全部向量和真实业务边界完成。

本次没有创建 RIoT 订单，没有发送移动命令，也没有伪造停稳/驻车信号。真实
OnboardHmi 组合根继续使用 `UnavailableVehicleSafetySignalProvider`，所以三次
恢复都正确收敛到 `RECOVERY_REQUIRED / DEPARTURE_SAFETY_NOT_READY`，
ControlServer `/health/ready` 保持 HTTP 503。

## 冻结身份

- ControlServer：`cc6e2b97e4308fa14b519edf9a0089d0da7d6d14`
- OnboardHmi：`045514770da9858a8a49196dede276192e4f2a1b`
- slots-simulator：`fb5f7c593742bf98bc3957b8729a38aad5321f28`
- 协议：`protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279`
- manifest SHA-256：`a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f`
- 运行配置 SHA-256：`330794430137cbb203cd8fc50995543504267f92a8ae3b3aca92c02b8d2ac9bd`

## 运行观察

1. 全新 ControlServer SQLite 与全新 Onboard journal 首连，generation `1`；
2. 杀掉并重启真实 OnboardHmi，复用同一 journal，generation `2`；
3. 保持 OnboardHmi 运行，杀掉并重启真实 ControlServer，复用同一 SQLite，
   自动重连为 generation `3`；
4. 每一阶段在后续 12 秒稳定窗口内 generation 不变，stderr 均为空；
5. 服务端重启期间出现一次预期的“会话不可用”，2 秒后自动重连成功；清理时
   服务端记录的 transport warning 来自测试主动终止对端，不是协议失败。

前两次启动器尝试分别因“进程退出前读取锁定日志”和“稳定快照采集函数返回
null”而作废；它们是 runner 证据缺陷，不是产品 FAIL，未被提升为本次通过结果。
第三次使用全新数据库和 journal 重跑后才形成此证据。

## 证据

- [`run-result.json`](run-result.json)：机器可读运行结果，SHA-256
  `fb0f708efb8cce42d1d64b728312f8a91775d6469918d28816057c08c3297304`
- [`runner.ps1`](runner.ps1)：本次实际运行的启动器快照，SHA-256
  `7d789132d22c4db88064d0d114508f77d1d32fd41dd94188426a32aba64c20d8`
- 本目录内全部 13 个运行文件的排序 `name<TAB>sha256<TAB>length` 集合 SHA-256：
  `57619074b0a6963b3112f883f97e30476c3eab63856eb372250c195bfc21bfdd`

## 仍未通过

- IS-00 尚未覆盖正式 TLS/具名生产身份以及该切片的全部拒绝、冲突和恢复向量；
- IS-06 尚未覆盖完整业务消息的 drop/delay/duplicate、异内容冲突、首结果重放和
  恰好一次副作用；
- ControlServer 完整运行时旅程编排、MesIngest/RIoT 凭据与配置、车辆/Map/站点
  绑定、真实停稳/驻车 provider 仍缺失；
- W2G-IS-00～07 完整 G3、真实移动与现场验收均未开始宣称通过。
