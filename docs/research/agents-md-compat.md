# Claude Code 对 AGENTS.md 的兼容现状，以及 8005 项目同时兼容 CLAUDE.md 与 AGENTS.md 的方案

调研票 trytoreachpeak0/8005-agv-program#226。只调研，不改任何仓库现有的 `CLAUDE.md` 与 `.claude/`。

## 0. 结论先说

- **现状**：Claude Code 从 v2.1.277 起原生读 `AGENTS.md`，但默认规则是「有 `CLAUDE.md` 就只读 `CLAUDE.md`」。工作目录或任何上级目录里只要有 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`，`AGENTS.md` 就不会被读。这个默认值只能在用户级设置里改，项目里的 `.claude/settings.json` 改不了（实测证实）。
- **推荐方案甲**：规则正文搬进 `AGENTS.md`，`CLAUDE.md` 只留第一行 `@AGENTS.md` 加 Claude 专属内容。它不依赖 Claude Code 版本、不依赖任何人的用户级设置，实测不会重复注入，Windows 上也没有符号链接的问题。
- **工作区 v2 的跨目录导入现在不生效**：`8005-workspace-v2/CLAUDE.md` 第一行的 `@../8005-workspace/CLAUDE.md` 跨出了工作目录，要先批准一次才加载；本机这个工作区的批准位是 `false`，导入被静默丢弃，那份 822 行的上级规则从没进过 v2 工作区会话的上下文。三套方案都要面对它。推荐把 v2 需要的那几节规则搬进一个仓库（建议 `8005-agv-program`），两个工作区都从各自的 `repos/` 克隆里导入，这样不用批准、有版本记录、也不会两份漂移。详见第 4 节。

## 1. 出处

均读取于 2026-11-23（本机时间；抓包日志里是 UTC 2026-11-24 02:0x）。

| 出处 | 网址 | 用到的内容 |
| --- | --- | --- |
| 官方文档 Memory 页 | https://code.claude.com/docs/en/memory （Markdown 版 `…/memory.md`） | `## AGENTS.md` 整节、导入语法、外部导入批准、`.claude/rules/`、符号链接、`claudeMdExcludes` |
| 官方文档 Subagents 页 | https://code.claude.com/docs/en/sub-agents （`…/sub-agents.md`） | 「What loads at startup」、`omitClaudeMd` |
| 官方更新日志 | https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md （读取时最新版本 2.1.331） | 下表各条 |
| AGENTS.md 约定站 | https://agents.md/ | 约定本身、就近原则、支持的工具列表 |

更新日志里与本题有关的条目：

| 版本 | 条目（原文摘要） |
| --- | --- |
| 2.1.277 | 首次加入 AGENTS.md 支持：没有 `CLAUDE.md` 的项目改读 `AGENTS.md`，在 `/config` 的 "Project instructions" 里可改 |
| 2.1.281 | AGENTS.md 支持扩展到 Bedrock、Vertex、Foundry、LLM 网关和关闭遥测的会话（此前这些会话只读 `CLAUDE.md`） |
| 2.1.285 | 文档记载：内置插件 ID 由 `agents-md@builtin` 改为 `cc-plugin-agents-md@builtin`，两种写法都认 |
| 2.1.290 | 修复子目录 `AGENTS.md` 在 @ 提及文件时没附上；修复指向工作目录外的 `CLAUDE.md`／规则／`AGENTS.md` 符号链接绕过读权限限制 |
| 2.1.327 前后 | 修复 Windows 上 `claudeMdExcludes` 盘符大小写不匹配 |
| 2.1.330 | 修复 `/config` 里 Project instructions 选择器在 24 行窗口只显示一项 |

## 2. Claude Code 当前怎样读 AGENTS.md（文档所述）

### 2.1 读取条件与设置

设置项叫 **Project instructions**，有四个取值：

| 取值 | 行为 |
| --- | --- |
| `claude-md-or-agents-md`（默认） | 读 `CLAUDE.md`；工作目录及以上都没有 `CLAUDE.md`／`.claude/CLAUDE.md`／`CLAUDE.local.md` 时改读 `AGENTS.md` |
| `claude-md-and-agents-md` | 两者都读，同一目录先 `CLAUDE.md` 后 `AGENTS.md`；已经通过导入或符号链接读过的 `AGENTS.md` 不再读 |
| `claude-md` | 只读 `CLAUDE.md` |
| `managed-only` | 只读组织托管的 `CLAUDE.md` 和自动记忆 |

- 改法：交互会话里 `/config`，或写进 `pluginConfigs."cc-plugin-agents-md@builtin".options.instructionFiles`。**只认用户级 `~/.claude/settings.json`、`--settings` 文件和托管设置；项目级、本地级设置文件里写了也被忽略。** 也就是说，一个仓库没办法替所有人把模式改成「两者都读」。
- 不阻断 `AGENTS.md` 的：用户级 `~/.claude/CLAUDE.md`、托管 `CLAUDE.md`、`.claude/rules/`。
- 读不到 `AGENTS.md` 的会话：版本早于 2.1.277；用 `/plugin` 关掉了内置插件；某些情况下升级后的第一个会话。

### 2.2 位置与子目录

- 启动时：工作目录及每一级上级目录里的 `AGENTS.md` 和 `.claude/AGENTS.md`。
- 工作中：Claude 用 Read 工具打开某个子目录里的文件，且该子目录自己没有三种 `CLAUDE.md` 之一时，加载该子目录的 `AGENTS.md`。
- 不读：`AGENTS.local.md`、`AGENTS.override.md`、`.agents/` 目录下的任何东西。文档没提用户级 `~/.claude/AGENTS.md`，实测不读（3.2 节 L/M）。

### 2.3 导入与重复注入

- `AGENTS.md` 里的 `@path` 导入同样会展开；最多 4 层；代码块和行内代码里的 `@` 不算导入。
- 跨出工作目录的导入（如 `@../x/CLAUDE.md`）需要每个项目批准一次。对 `CLAUDE.md`，交互会话会弹框；**对直接读入的 `AGENTS.md`，不弹框，只有此前已批准才加载。** 拒绝过一次以后不再弹框。
- `CLAUDE.md` 里写 `@AGENTS.md` 是文档推荐的共用写法，任何取值下都不会读两遍。

### 2.4 AGENTS.md 与 CLAUDE.md 的差异（直接读入时）

| | `CLAUDE.md` | 直接读入的 `AGENTS.md` |
| --- | --- | --- |
| `InstructionsLoaded` hook | 触发 | 不触发（经 `CLAUDE.md` 导入的照常触发） |
| `--add-dir` 加 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | 加载 | 不加载 |
| 外部导入 | 弹框请求批准 | 只在已批准时加载，不弹框 |

### 2.5 子代理

自定义子代理（如工作区的 `.claude/agents/reviewer.md`）启动时加载主会话加载的每一级指令，**包括作为项目指令读入的 `AGENTS.md`**；内置的 Explore、Plan、web-fetch 不加载，frontmatter 设了 `omitClaudeMd: true` 的也不加载。`reviewer.md` 没设这一项，所以无论哪套方案，审查代理读到的都和主会话一致。

## 3. 本机实测

### 3.1 方法

- 版本：本机 `claude` 不在 PATH 上，桌面应用自带 `claude.exe`，`--version` 输出 `2.1.330 (Claude Code)`。
- 这个命令行没有独立登录，不能直接让模型复述。改用更直接的办法：起一个本机假接口（`127.0.0.1:18765`），把 `ANTHROPIC_BASE_URL` 指过去，抓 Claude Code 发给模型的第一条请求正文，数里面注入了哪些文件、每个独特标记出现几次。API key 是占位值，只发往本机。同时用 `--debug-file` 看内置 AGENTS.md 插件的决定，例如日志行 `no CLAUDE.md found; AGENTS.md loaded: …\s\A\AGENTS.md`。
- 每个场景是 `C:/work/8005-scratch/agents-md-compat/s/` 下的一个临时目录，每个文件放一个形如 `MARKER-B-AGENTS` 的标记。没有在任何仓库或工作区根目录放试验文件。
- 脚本和原始结果在 [agents-md-compat-evidence/](agents-md-compat-evidence/)，可复跑。

### 3.2 结果

「注入」一栏是请求正文里出现的项目指令文件；标记都只出现一次，除非另注。

| 场景 | 布局 | 模式 | 注入 | 说明 |
| --- | --- | --- | --- | --- |
| A | 只有 `AGENTS.md` | 默认 | `AGENTS.md` | 原生读取成立 |
| A3 | 只有 `AGENTS.md` | `claude-md`（`--settings`） | 无 | 有人把模式改成只读 CLAUDE.md 时，纯 AGENTS.md 仓库什么都不读 |
| B | `CLAUDE.md` + `AGENTS.md`，无导入 | 默认 | 仅 `CLAUDE.md` | `AGENTS.md` 被忽略 |
| B2 | 同 B | 两者都读 | 两份 | |
| P | 同 B，项目 `.claude/settings.json` 写「两者都读」 | 默认 | 仅 `CLAUDE.md` | **项目级设置无效**，与文档一致 |
| C | `CLAUDE.md` 首行 `@AGENTS.md` + 专属段 | 默认 | `CLAUDE.md`、`AGENTS.md` | 各一次 |
| C2 | 同 C | 两者都读 | `CLAUDE.md`、`AGENTS.md` | 各一次，没有重复 |
| D | `CLAUDE.local.md` + `AGENTS.md` | 默认 | 仅 `CLAUDE.local.md` | 一份个人本地文件就能让 `AGENTS.md` 失效 |
| D2 | 同 D | 两者都读 | 两份 | |
| E | 只有 `.claude/AGENTS.md` | 默认 | `.claude/AGENTS.md` | |
| F | 上级 `CLAUDE.md`，会话在 `sub/`，`sub/AGENTS.md` | 默认 | 仅上级 `CLAUDE.md` | 上级有 `CLAUDE.md` 就阻断下级 `AGENTS.md` |
| F2 | 同 F | 两者都读 | 两份 | |
| G | 上级、下级各一个 `AGENTS.md` | 默认 | 两份 | 先上级后下级 |
| H | `proj/CLAUDE.md` 写 `@../shared/CLAUDE.md`，未批准 | 默认 | 仅 `proj/CLAUDE.md` | 外部导入被静默丢弃 |
| H（批准后） | 同上，配置目录里批准位为 true | 默认 | 两份 | |
| H2 | `proj2/AGENTS.md` 写 `@../shared/AGENTS.md`，未批准／已批准 | 默认 | 未批准仅 `proj2/AGENTS.md`；批准后两份 | |
| I | `AGENTS.md` 写 `@extra.md` | 默认 | `AGENTS.md`、`extra.md` | `AGENTS.md` 内的导入会展开 |
| K | `AGENTS.md` 里代码块中、行内代码中各有一个 `@` | 默认 | 仅 `AGENTS.md` | 代码里的 `@` 不展开 |
| L | 用户配置目录放 `CLAUDE.md` 和 `AGENTS.md`，项目只有 `AGENTS.md` | 默认 | 用户 `CLAUDE.md`、项目 `AGENTS.md` | 用户级 `CLAUDE.md` 不阻断；用户级 `AGENTS.md` 不读 |
| N | `CLAUDE.md` 与 `AGENTS.md` 逐字节相同 | 两者都读 | 仅 `CLAUDE.md` | 相同内容被去重（机制文档未写，推测按内容比对） |
| N3 | 两份文字相同，`AGENTS.md` 用 CRLF 换行 | 两者都读 | 两份，标记出现 2 次 | **只差换行符就会重复注入** |
| J | 仓库里提交 `CLAUDE.md → AGENTS.md` 符号链接，按 Windows 默认 `core.symlinks=false` 克隆 | 默认 | `CLAUDE.md`（内容是 `AGENTS.md` 这 9 个字节） | 规则全丢：这个一行文本的 `CLAUDE.md` 还挡住了真正的 `AGENTS.md` |

另外，同一个仓库用 `core.symlinks=true` 克隆，本机直接报 `error: unable to create symlink CLAUDE.md: Permission denied`，检出失败。本机没开开发者模式，git 是 2.56.0.windows.4，全局与系统都没设 `core.symlinks`。

### 3.3 结论

文档描述的行为在 2.1.330 上全部复现。对本项目最要紧的三点：

1. **混用两种文件时，默认只认 `CLAUDE.md`，而默认值改不了。** 一个仓库不可能「同时有 `CLAUDE.md` 和 `AGENTS.md`、两份都靠 Claude 自己读」，除非每个人都改用户级设置（P、B、B2）。
2. **用 `@AGENTS.md` 导入是唯一不受模式影响、也不重复的共用办法**（C、C2）。
3. **复制生成和符号链接在 Windows 上都会出事**：生成的副本只要换行符被 git 改成 CRLF，在「两者都读」模式下就注入两遍（N3）；符号链接按默认设置克隆会变成一行文本，规则整份丢失（J）。

## 4. 工作区 v2 的跨目录导入

### 4.1 现状与证据

`8005-workspace-v2` 不是 git 仓库，它的 `CLAUDE.md` 第 3 行是 `@../8005-workspace/CLAUDE.md`，下面紧接着写「上面导入的文件是写权限、语言、脚本基线和共享资源规则（含 agv02/agv03 隔离）的权威」。被导入的 `8005-workspace/CLAUDE.md` 有 822 行，分节是写权限、脚本基线、协作与语言、CI、CD、v2 实车隔离、.NET 工具链、工作区布局、实验虚拟机。

这条导入现在不生效：

1. **批准位**：`~/.claude.json` 里 `C:/work/8005-workspace-v2` 与 `C:/work/8005-workspace` 两项都是 `hasClaudeMdExternalIncludesApproved: false`、`hasClaudeMdExternalIncludesWarningShown: false`。按文档，跨出工作目录的导入要每个项目批准一次，未批准就不加载。`WarningShown` 也是 `false`，说明批准框从没弹出过（推的：桌面应用里起的会话可能根本不弹这个框）。
2. **抓包**：用 3.1 节的方法在 `C:/work/8005-workspace-v2` 本身起会话（只读，不改任何文件），请求里注入的只有 `~/.claude/CLAUDE.md`、`8005-workspace-v2/CLAUDE.md`（字面带着 `@../8005-workspace/CLAUDE.md` 这一行）和自动记忆索引。上级文件的第一句 "A workspace of independent git repositories, not a monorepo" 不在请求里（`results.txt` 的 `r3-WSV2`）。
3. **对照**：临时目录里同样的跨目录导入，未批准时丢弃（H），把批准位设为 `true` 后正常展开（H 批准后），说明问题只在批准位。
4. **会话自证**：本调研会话就是在 v2 工作区起的，它的系统提示里也只有那一行字面导入，没有上级文件的内容。

### 4.2 影响

- **在 v2 工作区起的会话**（调度、直接在工作区里干活的会话）：模型看不到上级文件，只能看到「那份文件是权威」这句话和一行看不懂的 `@`。它会不会自己去打开那个文件，取决于模型临场判断。v2 `CLAUDE.md` 自己转述过的规则（例如「只有四类要先问」、worktree 放哪）照常生效；只在上级文件里写的规则（写权限的完整清单、`.NET` 工具链基线、CI/CD 细节、实验虚拟机、v2 实车隔离的细节）实际没有约束力。
- **`C:/work/8005-wt/` 下 worktree 里干活的会话**：工作目录是 `C:/work/8005-wt/<票>-<仓库>`，往上的 `C:/work/8005-wt`、`C:/work` 都没有指令文件，所以它们本来就只读仓库自己的 `CLAUDE.md`，既不读 v2 工作区的 `CLAUDE.md`，也不读上级文件。这和导入批不批准无关：修好这条导入也到不了它们。它们拿到工作区规则的途径只有调度派票时写进提示的那部分，以及仓库 `CLAUDE.md` 里的转述（如 `8005-agv-program/CLAUDE.md` 的「The workspace root `CLAUDE.md` is the authority. In short: …」）。
- **审查代理** `reviewer`：作为子代理继承主会话的指令（2.5 节），在 v2 工作区里被调起时同样读不到上级文件。

### 4.3 可选的解法与实测

| 解法 | 怎么做 | 实测 | 代价 |
| --- | --- | --- | --- |
| ① 批准外部导入 | 在 v2 工作区跑一次交互式 `claude`，批准框里选同意；或手改 `~/.claude.json` 的批准位 | 批准位为 `true` 时导入展开（H 批准后） | 批准记在每台机器、每个用户的 `~/.claude.json` 里，不进版本库；换机器（10-20 刚换过）、换账号、新建工作区都要再批一次，没批时没有任何报错。一旦批准，这个项目里所有外部导入都放行。桌面应用里看起来不弹框，要用自带的 `claude.exe` 在终端里批 |
| ② 把内容搬进 v2 | 把 v2 需要的几节复制进 `8005-workspace-v2/CLAUDE.md` 或同目录的文件 | 工作目录内的导入不需批准（I） | v1 工作区还在用那份文件，复制后两份会漂移；v2 不是 git，改动没有版本记录也没有审查 |
| ③ 改成工作区内路径：目录联接 | 在 v2 里建一个指向 `../8005-workspace` 的 junction（不需要管理员），导入 `@link/CLAUDE.md` | **不加载**（X1）：Claude Code 按真实路径判断，联接仍算外部 | 不可用 |
| ④ 改成工作区内路径：放进仓库 | 把两个工作区共用的规则放进一个仓库里的文件（例如 `8005-agv-program` 的 `docs/agents/workspace-rules.md`），v2 导入 `@repos/8005-agv-program/docs/agents/workspace-rules.md`，v1 也从自己的 `repos/8005-agv-program` 导入 | 工作目录内子目录的导入正常（X4）；两个工作区的 `repos/8005-agv-program` 都存在 | 规则改动走 PR，有审查和历史；生效要等调度把 `repos/` 克隆快进到 `main`。被导入文件里再用相对路径导入别的文件时，路径相对于克隆，原工作区里的 `@repos/8005-test-lab/CLAUDE.md` 这种写法在克隆里找不到目标，会被静默丢弃（X4 里嵌套导入的目标不存在，没有报错），所以搬的时候要去掉或改写这类嵌套导入 |
| ⑤ 启动 hook 打印文件 | v2 `.claude/settings.json` 加一个 `SessionStart` hook，`cat ../8005-workspace/CLAUDE.md` | 内容进了上下文（X3），不需批准 | 进来的是 hook 输出，不是项目指令：自定义子代理（含 `reviewer`）读不到（推的：文档说子代理加载的是指令文件层级，没提主会话的 hook 输出）；以后要是批准了导入，就会出现两份 |
| ⑥ 附加目录 | `--add-dir ../8005-workspace` 加环境变量 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` | 命令行带 `--add-dir` 时加载（X2c）；写进项目设置的 `permissions.additionalDirectories` 加 `env` 不加载（X2、X2d，工作区受信任后的 X2e、X2f 也一样） | 桌面应用起的会话没法逐个带命令行参数，不实用 |

### 4.4 推荐

推荐 **④ 放进仓库**，并且只搬 v2 真正需要的那几节，不是整份 822 行。理由：

- 它不依赖任何一台机器上的批准状态，换机器、换会话都一样；
- 规则从此有版本库、有 PR 审查，v1、v2 两个工作区读的是同一份，不会漂移；
- 和本报告推荐的方案甲（第 6 节）用的是同一个机制，即工作目录内的 `@` 导入，没有第二种要维护的东西；
- 只搬两个工作区都要守的部分，只和 v1 有关的节留在 v1，v2 会话的上下文更干净。哪些节算共用，要由实施票逐节判断；v2 `CLAUDE.md` 点名的是写权限、语言、脚本基线和共享资源规则（含 agv02/agv03 隔离）。

① 批准外部导入可以作为过渡：一分钟能做完，但它只在这台机器上有效，而且出问题时没有任何提示，所以不建议作为长期做法。②、⑤ 都会造成两份内容；③、⑥ 实测不可用或不实用。

worktree 会话（4.2 节第二条）不受这条导入影响，任何解法都到不了它们。要让它们也读到工作区规则，只能写进各仓库自己的指令文件（方案甲里就是仓库的 `AGENTS.md`），或者继续由调度在派票提示里带上。

## 5. 只有 CLAUDE.md 那一侧有的东西

先分清两类：一类是**文件里的写法**，换到 `AGENTS.md` 可能会变；一类是 **`.claude/` 目录下的机制**，和规则正文放在哪个文件无关，无论选哪套方案都照常工作。

| 东西 | 本项目在用的地方 | 放进 `AGENTS.md` 后 |
| --- | --- | --- |
| `@path` 导入 | `8005-workspace/CLAUDE.md` 导入 `repos/8005-test-lab/CLAUDE.md`；v2 工作区导入上级 | Claude 照样展开（I、H2）；**其他工具不认识这个写法，只看到一行字面文本**（推的：agents.md 约定和本次读到的资料里都没有导入语法） |
| 外部导入批准 | v2 工作区 | 直接读入的 `AGENTS.md` 不会弹批准框，只能事先在 `CLAUDE.md` 那条路径上批准过 |
| `.claude/rules/*.md`（按 `paths` 按需加载） | `8005-agv-program/.claude/rules/legacy-sql.md` | 不受影响，它不在指令文件里；其他工具不认识，按需加载的规则只有 Claude 有 |
| skills | 两处 `.claude/skills/ponytail*`、用户级插件 | 不受影响；其他工具不认识 |
| hooks | `8005-workspace-v2/.claude/hooks/`（如 `onboard-target-guard.ps1`） | 不受影响；本项目没有用 `InstructionsLoaded` hook，所以 2.4 节那条差异不影响我们 |
| `settings.json` 权限规则 | 两个工作区 | 不受影响 |
| 子代理定义 | `8005-workspace-v2/.claude/agents/reviewer.md` | 不受影响，且会加载 `AGENTS.md`（2.5 节） |
| 正文里写给 Claude 的专属说明 | `8005-agv-program/CLAUDE.md` 的 `## Claude Code` 一节（插件命名空间、`/code-review` 冲突）；v2 工作区的 `SendMessage`、`start_session`、桌面应用相关规则 | 适合留在 `CLAUDE.md`，放进 `AGENTS.md` 对其他工具是噪音 |

所以「迁移会丢什么」的答案是：对 Claude 什么都不丢；对其他工具，`.claude/` 下的按需规则、skills、hooks、权限本来就用不上，正文里的 `@` 导入它们读不懂。

## 6. 方案

现有布局（票面列出、本次核对）：

| 位置 | 现有文件 |
| --- | --- |
| `8005-agv-control-server` | `CLAUDE.md`（345 行） |
| `8005-agv-program` | `CLAUDE.md`（148 行）、`.claude/rules/legacy-sql.md`、`.claude/skills/ponytail*`。2026-09-01 的 `cba1edd4` 正是把当时的根目录 `AGENTS.md` 并进了 `CLAUDE.md` |
| `8005-agv-protocol` | `CLAUDE.md`（128 行） |
| `8005-agv-onboard-hmi`、`slots-simulator` | 无 |
| `8005-workspace`（git） | `CLAUDE.md`（822 行，导入 `repos/8005-test-lab/CLAUDE.md`）、`.claude/settings.json`、`.claude/skills/ponytail*` |
| `8005-workspace-v2`（非 git） | `CLAUDE.md`（`@../8005-workspace/CLAUDE.md`，当前未生效）、`.claude/settings.json`、`.claude/hooks/`、`.claude/agents/reviewer.md` |

### 方案甲：`AGENTS.md` 为正文，`CLAUDE.md` 首行 `@AGENTS.md` 加 Claude 专属内容

- **改哪些文件**：每个有 `CLAUDE.md` 的仓库，把与工具无关的规则移到新建的根目录 `AGENTS.md`；`CLAUDE.md` 改成第一行 `@AGENTS.md`，下面只留 Claude 专属段（插件、skills、`SendMessage`、桌面应用会话规则等）。正文里的 `@` 导入改成两种写法之一：Claude 需要在会话开始就读到的，留在 `CLAUDE.md` 里导入；同时在 `AGENTS.md` 里用文字写明「另见 某路径」，给其他工具看。
- **对现有会话与审查代理**：Claude 读到的总内容不变，只是分成两个文件、`AGENTS.md` 的部分先出现（C）。审查代理同步拿到。已在跑的会话下次启动生效，不需要谁改用户级设置。旧版本（2.1.277 之前）也能用，因为只用到导入。
- **漂移风险**：没有，只有一份正文。守护办法：CI 里加一条很轻的检查，确认 `CLAUDE.md` 第一行非空内容是 `@AGENTS.md`，且 `AGENTS.md` 存在。
- **非 git 工作区**：v2 工作区不是 git 仓库，没有 CI，首行检查只能靠约定。
- **跨目录导入怎么解**：把导入目标换个名字解决不了问题，指向 `../8005-workspace/AGENTS.md` 和指向 `CLAUDE.md` 一样是外部导入，一样要批准。甲方案下推荐配 4.3 节的 ④：两个工作区共用的规则放进 `8005-agv-program` 里的一个文件，v1、v2 的 `CLAUDE.md` 都写 `@repos/8005-agv-program/<该文件>`。这和甲本身用的是同一种导入，导入行留在 `CLAUDE.md` 里，不放进 `AGENTS.md`。如果想让其他工具也读到，就在工作区的 `AGENTS.md` 里用文字写一句「另见 `repos/8005-agv-program/<该文件>`」。过渡期可以先用 ① 批准外部导入。
- **代价**：每个仓库多一个文件；要人判断哪些段落算「Claude 专属」。

### 方案乙：保留 `CLAUDE.md` 为正文，`AGENTS.md` 用符号链接或生成脚本同步

- **乙一，符号链接**：本机实测不可行。没开开发者模式时 `core.symlinks=true` 检出失败；按 Windows 默认设置克隆，链接变成一行文本（J）。若链接方向是 `AGENTS.md → CLAUDE.md`，Claude 不受影响，但其他工具在 Windows 克隆里只读到一行 `CLAUDE.md`，兼容的目的落空。车载机、vm-win-01、笔记本都是 Windows。
- **乙二，生成脚本**：脚本把 `CLAUDE.md` 复制成 `AGENTS.md`（可选地去掉 Claude 专属段、展开 `@` 导入）。
  - 改哪些文件：每个仓库加生成脚本、生成的 `AGENTS.md`、CI 一致性检查；可加 `.gitattributes` 把这两个文件钉成 `eol=lf`。
  - 对会话：默认模式下 Claude 只读 `CLAUDE.md`，`AGENTS.md` 只给其他工具看，所以没影响。**但只要有人把模式设成「两者都读」，两份内容就都进上下文**：逐字节相同时会被去重（N），一旦脚本做了任何改写（去掉专属段、展开导入）或换行符被 git 转换，就注入两遍（N3、B2）。
  - 漂移风险：高。有人手改了 `AGENTS.md`、或忘了跑脚本，两份就不一致；需要 CI 检查「重新生成后与提交的内容一致」。v2 工作区不是 git，没有 CI，只能靠 hook 或人工。
  - 跨目录导入怎么解：乙不改 `CLAUDE.md`，所以 v2 的 `@../8005-workspace/CLAUDE.md` 原样留着，照样要靠 ① 批准，或者另做 ④。生成脚本可以顺手把上级文件展开写进 v2 的 `AGENTS.md`，但这等于 4.3 节的 ②：v2 里多一份 800 多行的复制品，上级一改就过时，而 v2 没有 CI 能发现。而且 Claude 默认不读这份 `AGENTS.md`（v2 有 `CLAUDE.md`），展开了也只对其他工具有用。
- **代价**：要维护脚本和检查，而换来的只是「其他工具也能读」；对 Claude 没有任何好处。

### 方案丙：只留 `AGENTS.md`，删掉 `CLAUDE.md`

- **改哪些文件**：每个仓库把 `CLAUDE.md` 改名为 `AGENTS.md`，Claude 专属段要么混进去，要么挪到 `.claude/rules/`（无 `paths` 的规则文件会在启动时加载，且不阻断 `AGENTS.md`）。
- **对会话**：实测在干净目录里成立（A、E、G）。但它在本项目会被多处条件破坏：
  - **上级有 `CLAUDE.md` 就失效**（F）。`8005-workspace` 和 `8005-workspace-v2` 根目录都有 `CLAUDE.md`；只要会话在工作区里、或者在 `repos/<仓库>` 里启动，仓库的 `AGENTS.md` 都不在启动时读入。若把工作区根目录也改成 `AGENTS.md`，又牵出下一条。
  - **任何人放一个 `CLAUDE.local.md`，整份规则就消失**（D），而且没有报错。
  - 有人把模式设为 `claude-md`，规则全丢（A3）；直接读入的 `AGENTS.md` 外部导入不弹批准框（2.4），v2 的跨目录导入会更难发现。
  - 子目录 `AGENTS.md` 的按需加载只在 Read 工具打开文件时触发（文档），本次实测没法驱动工具调用，未验证。
- **跨目录导入怎么解**：丙下 v2 工作区的指令变成 `AGENTS.md`，导入行也跟着搬进去。直接读入的 `AGENTS.md` 遇到外部导入**不弹批准框**，只在此前已经批准过时加载（2.4 节，H2 实测）。也就是说 ① 只能靠手改 `~/.claude.json` 或先在 `CLAUDE.md` 那条路径上批准过，比甲、乙更难做到、更难发现。可行的只有 ④（`@repos/8005-agv-program/<该文件>` 在工作目录内，不需要批准，I、X4 实测）。
- **漂移风险**：没有。
- **代价**：要依赖 2.1.277 以后的版本和默认设置都不被改；出了问题是「静默少了规则」，最难查。

### 对比

| | 甲：`AGENTS.md` 正文 + `CLAUDE.md` 导入 | 乙一：符号链接 | 乙二：生成脚本 | 丙：只留 `AGENTS.md` |
| --- | --- | --- | --- | --- |
| Claude 读到完整规则 | 是，任何模式、任何 2.1.x 版本 | Windows 默认克隆下否（J） | 是 | 只在默认模式、上级无 `CLAUDE.md`、无 `CLAUDE.local.md` 时 |
| 其他工具读到规则 | 是（`@` 行除外） | Windows 下否 | 是 | 是 |
| 重复注入 | 无（C、C2） | 无 | 「两者都读」模式下有（N3） | 无 |
| 两份漂移 | 无 | 无 | 有，要 CI 守 | 无 |
| 要改的东西 | 每仓 2 个文件 + 一条轻检查 | 每仓 1 个链接 + 每台机器开开发者模式和 `core.symlinks` | 每仓脚本、生成物、CI 检查、`.gitattributes` | 每仓改名，专属段挪去 `.claude/rules/` |
| 非 git 的 v2 工作区 | 照常，没有 CI 守首行 | 不适用 | 没有 CI 守 | 被上级 `CLAUDE.md` 阻断 |
| v2 跨目录导入（第 4 节） | 配 ④，导入行留在 `CLAUDE.md`；过渡期可先 ① | 同乙二 | 原样留着，要 ① 或 ④；展开进 `AGENTS.md` 等于 ②，会漂移 | 只能 ④；① 不弹框，几乎做不到 |
| 风险性质 | 低 | 静默丢规则 | 内容不一致 | 静默丢规则 |

## 7. 推荐与迁移步骤

**推荐甲。** 理由：它是官方文档推荐的共用写法；对 Claude 行为不变，不需要任何人改用户级设置；实测不重复注入；没有 Windows 符号链接和换行符的坑；只有一份正文，不会漂移。乙只在「必须让 `CLAUDE.md` 保持原样」时才值得考虑，而本项目没有这个约束；丙在本项目的工作区布局下会静默丢规则。

迁移步骤（另开实施票，按仓库一张或一组，顺序如下）：

1. **先修 v2 工作区的跨目录导入**（第 4 节，不论选哪套方案都要做）。取舍：长期做 ④，在 `8005-agv-program` 建一个两个工作区共用的规则文件（例如 `docs/agents/workspace-rules.md`），从 `8005-workspace/CLAUDE.md` 搬入 v2 也要守的那几节，并去掉里面的相对路径嵌套导入；合入后调度快进两个工作区的 `repos/8005-agv-program`，再把 v1、v2 的 `CLAUDE.md` 改成导入它，v1 原文里的对应节删掉。④ 合入之前，如果用户要立刻让 v2 会话读到规则，可以先做 ①（在 v2 工作区用自带的 `claude.exe` 起一次交互会话并批准）。① 只在本机有效，④ 落地后可以不管它。两种做法完成后，都用 3.1 节的抓包脚本在 v2 工作区复核：上级规则的标志句应出现在请求里。
2. **`8005-agv-protocol`**（128 行，Claude 专属内容最少，先拿它试做法）：新建 `AGENTS.md` 放正文，`CLAUDE.md` 改为 `@AGENTS.md` 加专属段；加 CI 首行检查。
3. **`8005-agv-program`**：同上；`.claude/rules/legacy-sql.md` 和 `.claude/skills/` 不动；`## Claude Code` 一节留在 `CLAUDE.md`。本文件本身也在这个仓库，`docs/agents/` 的语言规则（英文）沿用。
4. **`8005-agv-control-server`**（345 行）：同上。
5. **`8005-workspace`**：第 1 步搬走共用节以后剩下的部分，含 `@repos/8005-test-lab/CLAUDE.md` 导入。拆分时把导入行留在 `CLAUDE.md`，在 `AGENTS.md` 里写一句文字指引。这一步改动最大，涉及所有在 v1 工作区干活的会话。
6. **`8005-workspace-v2`**：内容几乎都是 Claude 会话、调度、`SendMessage` 相关的规则，可以继续只有 `CLAUDE.md`，或者只把通用部分拆出。共用规则通过第 1 步的 `@repos/8005-agv-program/…` 导入拿到。
7. `8005-agv-onboard-hmi`、`slots-simulator` 目前没有指令文件，不用动；以后新增时直接按甲的形状建。

**和在途票的关系**：实施只改各仓库的指令文件和一条 CI 检查，不碰产品代码。派票队列里的 trytoreachpeak0/8005-agv-onboard-hmi#415（录入提交防重复）和 trytoreachpeak0/8005-workspace#68（关闸开窗判定）从标题看都是产品代码或脚本改动，不碰指令文件，冲突面小（推的，未读它们的分支）。真正要避开的是同期修改同一个 `CLAUDE.md` 的票，以及正在跑的工作会话：会话只在启动时读一次指令，中途改文件不影响它，但同一仓库两张票都改 `CLAUDE.md` 会合并冲突。建议在派票空档逐仓做，每仓一个小 PR；先做 1、2 两步看一轮，再决定是否继续。
