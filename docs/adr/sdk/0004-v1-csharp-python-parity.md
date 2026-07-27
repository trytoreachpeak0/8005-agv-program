# 第一版 C# 与 Python 同步交付

第一版 DispatchLoop Facade 在 C# 与 Python 同步实现同一对外 seam 与能力清单，共用 Lab fixtures/BC 作为契约来源，避免一端可用另一端长期滞后。代价是每条能力的实现与单测工作量约翻倍。

**Status**: accepted

**Considered Options**: 先 C# 后 Python；先 Python 后 C#；双端同步（采纳）。
