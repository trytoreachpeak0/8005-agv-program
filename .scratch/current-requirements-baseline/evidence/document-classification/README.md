# 文档级证据分类账

本目录把已完成调查中的逐文档结论归一为同一数据结构，供后续原子需求级分类和批准批次生成使用。它是文档级证据索引，不是需求批准记录，也不修改任何原始材料。

## 资产

- `R01-R05-document-evidence-ledger.tsv`：规范化主分类账；202 行数据，可由脚本重建和逐字段复核。
- `R01-R05-document-evidence-ledger.xlsx`：同一分类账的筛选审阅副本；含 `Summary` 和 `Ledger` 两个工作表。
- `build-and-verify-r01-r05-ledger.ps1`：从固定清单与 R01–R05 调查报告重建 TSV，并核验覆盖、唯一性、当前文件哈希和批准隔离边界。
- `R06-R10-document-evidence-ledger.tsv`：规范化主分类账；201 行数据，覆盖测试草案、NFR、词汇/ADR、MES/SDK 决定及模拟器规划。
- [R06–R10 XLSX 审阅副本](../../../../outputs/019fc6a3-e36c-7b63-ad6e-0e8d07af8ade/R06-R10-document-evidence-ledger.xlsx)：含公式驱动的 `Summary` 和可筛选的 `Ledger` 两个工作表。
- `build-and-verify-r06-r10-ledger.ps1`：从固定清单与 R06–R10 调查报告重建 TSV，并核验覆盖、唯一性、当前文件哈希、批准隔离和供应商资料排除边界。
- `R11-R13-document-evidence-ledger.tsv`：规范化主分类账；87 行数据，覆盖 MES 数据/验证材料、历史本地 spec/实施票据及 RIoT 接口/SDK 材料。
- [R11–R13 XLSX 审阅副本](../../../../outputs/019fc6b2-9251-7a80-a62b-af9901373337/R11-R13-document-evidence-ledger.xlsx)：含公式驱动的 `Summary` 和可筛选的 `Ledger` 两个工作表。
- `build-and-verify-r11-r13-ledger.ps1`：从固定清单和 R11–R13 调查报告重建 TSV，并核验覆盖、唯一性、当前文件哈希、批准隔离、历史实施票隔离、schema 快照待绑定及供应商资料排除边界。
- `R01-R13-document-evidence-ledger.tsv`：三份分区账的规范化总账；490 行原始分类字段后追加 `route_class` 与 `candidate_group_id` 两个可重建派生字段。
- `R01-R13-candidate-groups.tsv`：后续原子需求级分类的 13 个候选组，固定每组记录 ID、前置门槛、建议票据名称与处理边界。
- [R01–R13 XLSX 审阅副本](../../../../outputs/019fc6c3-bdc0-77e3-9227-561dc20d7284/R01-R13-document-evidence-ledger.xlsx)：含公式驱动的 `Summary`、`Candidate Groups` 和可筛选的 `Ledger` 三张工作表。
- `build-and-verify-consolidated-ledger.ps1`：从三份分区账重建总账和候选组，并以失败式约束核验字段顺序、固定清单对账、路径/记录唯一性、当前哈希、分类枚举、Git 状态勘误和批准隔离。

## 覆盖与核验结果

R01–R05 固定全集为 202 行：R01 19 行、R02 27 行、R03 48 行、R04 41 行、R05 67 行。R06–R10 固定全集为 201 行：R06 65 行、R07 15 行、R08 57 行、R09 18 行、R10 46 行。R11–R13 固定全集为 87 行：R11 11 行、R12 50 行、R13 26 行。三个重建脚本都要求覆盖各自固定全集，并对当前工作树重新计算 SHA-256；当前结果分别为 202/202、201/201 和 87/87，均为零漏项、零重复、零哈希漂移。

## 字段边界

每条记录固定路径、完整 SHA-256、字节数、清单原始快照 Git 状态、勘误覆盖后的有效 Git 状态和原清单材料角色，并统一记录：

- 文档级分类与来源类型；
- 当前适用性；
- 形成、历史或派生关系；
- 具名批准人、批准日期、批准范围、版本绑定四要素；
- 原子需求提取路由；
- 需要保留的证据、冲突和调查报告指针。

R01–R13 的现有证据都没有同时建立批准四要素，因此四列一律保留为 `not-found`，`document_approval_state` 一律为 `not-approved-by-this-classification`。这表示“本轮证据不能批准”，不表示内容错误、永久否决或已经废弃。

R01–R05 中 26 份材料明确不从该文档本身提取需求；其余 176 份只被路由到后续拆分、补证、冲突裁决和显式批准，不因进入提取路由而升级为需求或权威来源。原子批准仍以最终批准人的逐项决定为准。

R06–R10 另有 101 份材料进入候选提取路由，4 份 R06 旧测试草案因上游语义漂移被阻塞。设计/ADR、测试执行、模拟器规划和主系统约束线索分别路由，不能从设计或实现反推需求。R10 的厂商 PDF 与派生寄存器表按用户范围决定仅保留无损身份及来源关系，2 份纯供应商记录明确不进入提取或继续适用性调查。

R11–R13 共有 24 份材料进入候选提取路由：R11 6、R12 2、R13 16。这仍只代表后续拆分和补证入口。R12 只有两份混合 spec 可继续拆分，其余 48 张实施、评审或修复票只作实施史/现状证据；R13 的 14 份静态 schema 必须先完成受控环境与版本绑定、按操作拆分并取得 API 白名单批准，4 份 SDK schema 副本不得重复计数。两份供应商 PDF 继续按用户范围决定排除内容，只保留无损身份与来源史。

总账将 490 行统一归并为 `candidate=301`、`blocked=4`、`excluded=185`，并以 R01–R13 一批一组生成 13 个候选组。候选组仅定义原子拆分边界和前置门槛，不会把任何文档或条目升级为已批准需求。R06 的 4 份上游漂移旧稿明确保持在候选组之外，等待独立版本归属决定。

## 复核

在仓库根目录运行：

```powershell
& '.scratch\current-requirements-baseline\evidence\document-classification\build-and-verify-r01-r05-ledger.ps1' -VerifyOnly
```

成功结果必须同时报告 `total=202`、各批次数量、`missing=0`、`duplicates=0`、`hash_drift=0` 和 `approved_by_classification=0`。

R06–R10 复核：

```powershell
& '.scratch\current-requirements-baseline\evidence\document-classification\build-and-verify-r06-r10-ledger.ps1' -VerifyOnly
```

成功结果必须同时报告 `total=201`、R06–R10 各批次数量、`missing=0`、`duplicates=0`、`hash_drift=0`、`approved_by_classification=0`，并给出候选、漂移阻塞和供应商排除路由计数。

R11–R13 复核：

```powershell
& '.scratch\current-requirements-baseline\evidence\document-classification\build-and-verify-r11-r13-ledger.ps1' -VerifyOnly
```

成功结果必须同时报告 `total=87`、R11–R13 各批次数量、`missing=0`、`duplicates=0`、`hash_drift=0`、`approved_by_classification=0`，并给出候选路由、历史实施票隔离、schema 快照待绑定、供应商排除和 Git 状态勘误计数。

总账复核：

```powershell
& '.scratch\current-requirements-baseline\evidence\document-classification\build-and-verify-consolidated-ledger.ps1' -VerifyOnly
```

成功结果必须同时报告 `total=490`、R01–R13 各批次数量、`missing=0`、`duplicates=0`、`hash_drift=0`、`approved_by_classification=0`、`candidates=301`、`blocked=4`、`excluded=185` 和 `candidate_groups=13`。
