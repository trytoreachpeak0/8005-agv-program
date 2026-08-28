# 07-customer-deliverables 客户交付物

本目录存放面向客户讨论的需求文档，与内部 Obsidian vault（BR/UC 追溯）分离维护。

| 文件 | 说明 |
| --- | --- |
| `客户需求讨论稿-多仓位AGV系统.md` | Markdown 源稿（业务语言，无内部 wikilink） |
| `宿迁长电多仓位AGV系统-需求讨论稿-2026-07-14.docx` | 由 pandoc 从源稿生成的 Word，可直接发给客户 |
| `assets/system-context.png` | 系统边界示意图 |

重新生成 Word：

```bash
pandoc "客户需求讨论稿-多仓位AGV系统.md" -o "宿迁长电多仓位AGV系统-需求讨论稿-2026-07-14.docx" --resource-path=.
```
