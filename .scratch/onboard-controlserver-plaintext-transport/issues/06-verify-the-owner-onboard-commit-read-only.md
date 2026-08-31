# 只读回读核验 owner 的车载端改动

Type: task
Mode: AFK
Status: open
Blocked by: 05

## Question

王昆改完并推送后，在**只读**前提下核验车载端改动确实落地且与服务端形态对齐，然后把该 commit 固定
为本轮候选的车载端身份。对 `8005-agv-onboard-hmi` 零写入：只 fetch 与 `git show`，不建分支、不提交、
不推送、不建 tag。

核验内容：

- **四处**校验在新 commit 上的实际形态，与票 01 冻结的形态逐条比对（不是「他说改了」，而是读到代码）。
  第四处 `WireToGateSettings.Validate(production: true)` 的指纹强制最容易被漏改，必须单独确认；
- 票 01 列入「不要动」的两处 `IsForbiddenProductionHost` 是否仍在——若被顺手删掉，生产配置忘改样例值
  的保护就没了，须回报给 owner 而不是默认接受；
- 配置模板中 `wireToGate.useTls`、`serverCertificateSha256`、`vehicleSafety.endpoint` 的终态与服务端
  票 02 的实现**互相能用**——特别要排除一端删了字段而另一端仍要求该字段的情况；
- 该 commit 与 `31263b1` 的关系（`merge-base --is-ancestor` 确认它包含票 27 那半可见性修复，
  不是从更早基线分叉出来的）；
- 车载端自身测试的状态：他是否跑过、结果如何。若无法从远程判断，据实记为未知而不是推定通过。

判据设计要求：红侧必须证明检测器会响。例如比对形态时，把目标形态的关键字符翻掉应当报出差异；
`merge-base` 判据要在一个已知不含 `31263b1` 的 commit 上验证会返回否定。

上一轮的教训直接适用：托管构建每次新 MVID，`.dll` 哈希不构成内容证据；要证明改动进了二进制得用
新增／消失的**符号名**。本票只核验源码与 commit 关系，二进制层面的核验归票 08。
