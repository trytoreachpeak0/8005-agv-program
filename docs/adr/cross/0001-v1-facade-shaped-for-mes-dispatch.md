# 第一版 Facade 按 MES 派车闭环定形，Lab 共用

第一版对外能力以 MES/调度「能派一单并跟完」为边界；behavior-lab 与脚本复用同一套 Facade，不为实验探针单独扩 API。避免 Lab 与生产两套客户端分叉。

**Status**: accepted

**Considered Options**: 仅服务 MES；仅服务 Lab；同一套 Facade、形状按 MES 闭环（采纳）。
