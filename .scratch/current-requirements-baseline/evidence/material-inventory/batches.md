# 当前需求性材料无损清单批次

## 口径

- 唯一输入是已固定的 **../initial-snapshot/candidate-documents.tsv**；本清单没有重新扫描工作区，也没有读取后续变化覆盖快照身份。
- **material-inventory.tsv** 对快照的每一路径一对一保留 **git_status**、**sha256**、**bytes**、**last_write_utc**，再追加材料角色、批次与路由理由。
- **candidate-\*** 只表示值得调查，不表示真实、当前、适用、无冲突或已批准。
- **current-state-evidence** 包括实现、测试/实验、配置、日志、样本、转储和运行结果；它们只能证明观察到的现状，不得反推正确需求。
- **template-or-index** 和 **repository-governance** 不独立形成系统需求；前者可提供结构/指针，后者保留完整盘点但不进入系统需求候选调查。
- 路由按来源群组和单次调查规模组织；同一批次仍须逐文件、逐原子条目核实，不能整批批准。

## 对账

- 初始快照：1809 条。
- 清单：1809 条；路径重复 0，未分类 0，漏项 0。
- 候选调查批次：490 条；现状证据批次：1246 条；仓库治理元数据：73 条。

## 材料角色

| 角色 | 数量 |
|---|---:|
| `candidate-acceptance` | 133 |
| `candidate-data-constraint` | 9 |
| `candidate-decision` | 122 |
| `candidate-external-constraint` | 12 |
| `candidate-requirement` | 170 |
| `candidate-source` | 19 |
| `candidate-vocabulary` | 2 |
| `current-state-evidence` | 1260 |
| `repository-governance` | 73 |
| `template-or-index` | 9 |

## 批次

| 批次 | 名称 | 文件数 | 字节数 | 建立调查票 | 角色构成 |
|---|---|---:|---:|---|---|
| R01 | 客户、项目协议与原始需求输入 | 19 | 492055 | yes | candidate-source=19 |
| R02 | 需求库框架、愿景、干系人与业务规则 | 27 | 177931 | yes | candidate-requirement=20; template-or-index=7 |
| R03 | 用例 | 48 | 394091 | yes | candidate-requirement=48 |
| R04 | 功能需求 | 41 | 151697 | yes | candidate-requirement=41 |
| R05 | 现场操作验收场景 | 67 | 56722 | yes | candidate-acceptance=67 |
| R06 | 仓位、硬件、车队及其余测试案例 | 65 | 49980 | yes | candidate-acceptance=65 |
| R07 | 追溯规则与非功能需求 | 15 | 34667 | yes | candidate-requirement=15 |
| R08 | 跨域词汇与架构决定 | 57 | 202979 | yes | candidate-decision=55; candidate-vocabulary=2 |
| R09 | MES 与 SDK 架构决定 | 18 | 24235 | yes | candidate-decision=17; template-or-index=1 |
| R10 | 仓位模拟器需求与决定 | 46 | 2192376 | yes | candidate-requirement=46 |
| R11 | MES 数据、查询与工厂验证约束 | 11 | 25915 | yes | candidate-acceptance=1; candidate-data-constraint=9; template-or-index=1 |
| R12 | 历史本地 spec 与实施票据 | 50 | 118871 | yes | candidate-decision=50 |
| R13 | RIoT 外部接口与 SDK 约束 | 26 | 5532722 | yes | candidate-external-constraint=12; current-state-evidence=14 |
| E01 | 需求库与编辑器配置现状证据 | 8 | 3049 | no | current-state-evidence=8 |
| E02 | MES 实验、实现、样本与运行证据 | 135 | 1358379 | no | current-state-evidence=135 |
| E03 | RIoT 行为实验与配置现状证据 | 1046 | 11492028 | no | current-state-evidence=1046 |
| E04 | RIoT SDK 实现与接口转储现状证据 | 56 | 144952 | no | current-state-evidence=56 |
| E05 | 根目录事件转储现状证据 | 1 | 6618 | no | current-state-evidence=1 |
| G01 | 仓库代理、流程与工具元数据 | 73 | 235583 | no | repository-governance=73 |

## 调查约束

每个 **follow_up_ticket=yes** 批次的调查都必须记录：来源身份、捕获/形成时间、版本或历史关系、具名批准证据、批准适用范围、当前版本适用性、重复/派生关系和仍缺少的证据。调查只能做文档级证据分类；遇到真实冲突时另建逐项 HITL 票，遇到可独立批准的需求时留待后续原子需求分类与批准票。

现状证据批次不单独升级为需求调查票。候选批次可按路径和哈希引用它们来验证实现、环境或外部接口事实，但代码行为、测试通过、配置存在、日志/实验观察均不构成批准。

## Git 状态追加勘误

本清单保留初始快照的原始 `git_status` 字段，不静默重写。调查时必须叠加 [initial-snapshot/git-status-corrections.tsv](../initial-snapshot/git-status-corrections.tsv)：58 条非 ASCII 路径由 `untracked` 修正为 `tracked-clean`，有效统计为 `tracked-clean=1762`、`untracked=47`。根因、逐路径证据和验证方法见 [初始快照 Git 状态追加勘误](../initial-snapshot/git-status-correction.md)。
