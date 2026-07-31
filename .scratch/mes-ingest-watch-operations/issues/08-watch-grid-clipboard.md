# 08 — TransportDemands/Alerts 单元格与整行复制

**What to build:** 为两张 DataGrid 提供一致的 Ctrl+C 和右键复制，支持单元格、整行及含列名整行，输出可直接粘贴到 Excel。

**Blocked by:** 07 — Watch 分页表格形态（可先实现通用 clipboard helper）

**Status:** ready-for-agent

- [ ] 普通单元格 + Ctrl+C 复制当前单元格显示值
- [ ] 行头选中 + Ctrl+C 按当前可见列顺序复制整行
- [ ] 右键提供“复制单元格”“复制整行”“复制整行（含列名）”
- [ ] 右键未选中单元格先切换当前选择，避免复制旧 selection
- [ ] 整行用 Tab 分隔；含列名使用 header 行 + value 行
- [ ] null 值输出字面量 `null`，不输出空字符串
- [ ] 时间输出当前本机时区的完整显示文本
- [ ] TransportDemands/Alerts 共用 helper，并以纯文本投影测试列顺序、null、Tab/换行转义

## Comments

- Clipboard behavior applies only to loaded/selected rows; it is not an export-all API.

