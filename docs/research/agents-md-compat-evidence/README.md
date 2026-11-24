# agents-md-compat 实测脚本

`docs/research/agents-md-compat.md` 第 3 节的实测用的脚本与结果，供复跑。

- `setup.sh`：在 `C:/work/8005-scratch/agents-md-compat/s/` 下建各场景目录，每个文件里放一个独特的 `MARKER-…` 标记。
- `capture.py`：本机假接口，监听 `127.0.0.1:18765`，把 Claude Code 发给模型的请求正文原样存盘，回 400 让会话结束。
- `cap.sh <目录> <标签> [claude 参数]`：在该目录起一次 `claude -p`，`ANTHROPIC_BASE_URL` 指向假接口、`ANTHROPIC_API_KEY` 用占位值（只发往本机），同时写 `--debug-file`。`cap2.sh` 另可用 `CFG=<目录>` 指定 `CLAUDE_CONFIG_DIR`，用来测用户级文件与外部导入批准位。
- `analyze.py . <标签前缀>`：读每次运行的第一条请求，列出注入的项目指令文件（`Contents of … (`）与各标记出现次数。
- `results.txt`：本次结果。

本机 `claude` 不在 PATH 上，用的是桌面应用自带的 `claude.exe`（2.1.330）。它没有独立登录，所以不能直接问模型「你读到了什么」；抓请求正文比让模型复述更可靠，因为能数出重复注入。
