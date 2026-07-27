# 第一版明确排除的能力

第一版具名 Facade 不包含：interrupt；task/v1/order 建单主路径；几何 path；阻塞 Wait* 跟单；将 devices 列表作为可调度车发现；多段 mission 编排 DSL/流程引擎；CallApiKey 轮换与过期策略。devices 列表若暴露则仅作设备查询，派车发现必须走可调度车接口。需要时可用 RawEscape 或后续版本扩展。

**Status**: accepted
