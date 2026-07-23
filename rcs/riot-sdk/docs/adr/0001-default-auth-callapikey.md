# 第一版默认鉴权使用 CallApiKey

调度/MES 长期连接现场时，默认用 CallApiKey 作为 Bearer，不必每次 AdminLogin；AdminLogin / refresh 仅作备用。依据 Lab BC-AUTH-002；与「当前 Core 只有 login」的现状刻意相反，避免调用方把短时 AccessToken 当成默认路径。

**Status**: accepted

**Considered Options**: 默认 CallApiKey（采纳）；默认 AdminLogin、CallApiKey 作旁路；两者平等由调用方每次显式选择。
