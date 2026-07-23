# 实验定义

实验定义说明如何安全、可重复地获取证据，不直接承载某一轮结果。

- [`catalog.md`](./catalog.md)：当前 A～H 实验卡（含 A2 调用密钥鉴权）。
- [`minimal-closed-loop.md`](./minimal-closed-loop.md)：建单、状态、到站、幂等和取消闭环（**2026-07-20 起非 P0**；待 Q-015 确认后再重开）。
- 每张实验卡应关联至少一个 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) 中的问题。
- 预期结果必须区分“用于校验执行是否正常的结构预期”和“等待实验验证的行为假设”。
- 某轮实际参数、响应和结论只写入 [`../evidence/rounds/`](../evidence/rounds/)。

后续调整实验卡时，应优先围绕当前 open-questions 的 P0 组织，不再单纯按接口模块扩张。
