# 进程崩溃重启 runner 归位并重绑

Type: task
Mode: AFK
Status: open
Blocked by: 19

## Question

「进程崩溃重启」向量由独立脚本 `run-staged-g3-no-movement.ps1` 负责，该脚本有两处问题：
绑定 `ControlServer cc6e2b9` + `OnboardHmi 0455147`，比当前双端落后两代；且位于规划仓
`.scratch/wire-to-gate-ai-implementation-kit/evidence/g3/`，而非归属仓。如何把它归位到
ControlServer 仓并重绑到 `3d8b00c` + `304e6ad`，取得当前 commit 下的重启向量证据？

### 与票据 18／19 的关系

本票只碰这一个独立脚本，不修改 `scripts/run-staged-g3.ps1`，与 18／19 无文件冲突。排在 19 之后
是为了保持单一前沿串行推进，不是技术依赖——若需调整顺序，直接改 `Blocked by` 即可。

### 位置决定（已定，2026-08-29 用户确认）

**搬到 ControlServer 仓 `scripts/` 下，保持独立脚本**，不并入主 runner：

- 主 runner 已 1452 行；重启向量需要反复起停服务端进程，与其单进程 TLS 探针模型冲突，并入会
  让两种生命周期纠缠。
- 独立带来的绑定漂移问题（本票的成因），改为让两个脚本引用同一处 commit 常量来解决，而不是靠
  合并脚本。

执行时不需要再就此征询。若实施中发现共享常量确实不可行，可改走合并路线，但必须在本票记录
推翻该决定的具体理由。

### 范围

- 脚本迁入 ControlServer 仓，从规划仓 `.scratch/` 移除。
- 重绑到 `3d8b00c` + `304e6ad` + `fb5f7c5` + `1531489e`，与主 runner 共享绑定来源。
- 重跑并断言：session generation 在「全新首连 → 车载重启复用 journal → 服务端重启复用数据库」
  三阶段稳定递增，每阶段后无意外 generation 变化，跨重启复用同一 Demand、车辆租约与消息身份。

### 完成判据

重启向量断言 PASS 且绑定 `3d8b00c` + `304e6ad`；脚本在 ControlServer 仓且规划仓不再保留副本；
证据归档于 ControlServer 仓 `evidence/g3/`，票据只留路由指针。

### 注意

不动车、不建单、不使用现场凭据。该脚本为 plaintext loopback，不需要临时根证书授权。
