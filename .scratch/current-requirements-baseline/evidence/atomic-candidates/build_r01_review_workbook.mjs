import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = process.argv[2];
if (!repoRoot) throw new Error("Usage: node build_r01_review_workbook.mjs <repo-root>");

const sourcePath = path.join(
  repoRoot,
  ".scratch",
  "current-requirements-baseline",
  "evidence",
  "atomic-candidates",
  "R01-atomic-candidates.tsv",
);
const outputDir = path.join(repoRoot, "outputs", "019fc822-5233-78a0-8de6-14b894bf1f11");
const qaDir = path.join(
  repoRoot,
  ".scratch",
  "current-requirements-baseline",
  "evidence",
  "atomic-candidates",
  "qa-xlsx",
);

function parseDelimited(text, delimiter = "\t") {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
      continue;
    }
    if (char === '"') {
      quoted = true;
    } else if (char === delimiter) {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  return rows;
}

function columnName(index) {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    const remainder = (value - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    value = Math.floor((value - 1) / 26);
  }
  return result;
}

const text = await fs.readFile(sourcePath, "utf8");
const data = parseDelimited(text);
const headers = data[0];
const rows = data.slice(1);
if (headers.length !== 18 || rows.length !== 3091) {
  throw new Error(`Unexpected ledger shape: rows=${rows.length} cols=${headers.length}`);
}
const asExcelText = (value) => (typeof value === "string" && value.includes("=") ? `'${value}` : value);
const candidateData = [
  [...headers, "exact_duplicate_flag"],
  ...rows.map((row) => [...row.map(asExcelText), null]),
];

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const coverage = workbook.worksheets.add("Source Coverage");
const conflicts = workbook.worksheets.add("Conflict Register");
const candidates = workbook.worksheets.add("Candidates");

for (const sheet of [summary, coverage, conflicts, candidates]) sheet.showGridLines = false;

const navy = "#17324D";
const teal = "#0F766E";
const paleTeal = "#DDF3EF";
const paleAmber = "#FFF2CC";
const paleRed = "#FDE2E2";
const paleBlue = "#E8F0FE";
const lightGray = "#E5E7EB";
const bodyFont = { name: "Aptos", size: 10, color: "#172033" };

summary.mergeCells("A1:E1");
summary.getRange("A1").values = [["R01 原子候选分类审阅"]];
summary.getRange("A1:E1").format = {
  fill: navy,
  font: { name: "Aptos Display", size: 18, bold: true, color: "#FFFFFF" },
  rowHeight: 32,
  verticalAlignment: "center",
};
summary.mergeCells("A2:E2");
summary.getRange("A2").values = [["候选分类，不是批准；所有条目继续保留来源、冲突与批准缺口。"]];
summary.getRange("A2:E2").format = { fill: paleAmber, font: { ...bodyFont, italic: true }, rowHeight: 28, wrapText: true };

summary.getRange("A4:B8").values = [
  ["指标", "值"],
  ["原子声明", null],
  ["来源文档", null],
  ["精确重复（后出现行）", null],
  ["批准升级", null],
];
summary.getRange("B5").formulas = [["=COUNTA('Candidates'!$A$2:$A$3092)"]];
summary.getRange("B6").formulas = [["=COUNTA('Source Coverage'!$A$2:$A$14)"]];
summary.getRange("B7").formulas = [["=SUM('Candidates'!$S$2:$S$3092)"]];
summary.getRange("B8").formulas = [["=COUNTIF('Candidates'!$Q$2:$Q$3092,\"<>not-approved\")"]];
summary.getRange("A4:B4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:A8").format = { fill: paleBlue, font: { ...bodyFont, bold: true } };
summary.getRange("B5:B8").format = { font: { ...bodyFont, bold: true }, numberFormat: "#,##0" };
summary.getRange("A4:B8").format.borders = { preset: "outside", style: "thin", color: lightGray };

const routes = [
  "needs-source-and-explicit-approval",
  "hold-for-conflict-decision",
  "needs-question-resolution",
  "needs-signature-source-and-explicit-approval",
  "needs-signature-scope-and-explicit-approval",
  "evidence-only",
  "exclude-from-requirement-approval",
];
summary.getRange("A10:B17").values = [["处置路线", "数量"], ...routes.map((route) => [route, null])];
for (let row = 11; row <= 17; row += 1) {
  summary.getRange(`B${row}`).formulas = [[`=COUNTIF('Candidates'!$N$2:$N$3092,A${row})`]];
}
summary.getRange("A10:B10").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("A11:A17").format = { font: bodyFont };
summary.getRange("B11:B17").format = { font: bodyFont, numberFormat: "#,##0" };
summary.getRange("A10:B17").format.borders = { preset: "outside", style: "thin", color: lightGray };
summary.getRange("A1:E17").format.wrapText = true;
summary.getRange("A:A").format.columnWidth = 44;
summary.getRange("B:B").format.columnWidth = 16;
summary.getRange("C:E").format.columnWidth = 12;
summary.freezePanes.freezeRows(2);

const sourceRows = [
  ["R01-03", "mes/docs/待处理事项清单-MES-RIOT-应用.docx", 129],
  ["R01-04", "mes/docs/宿迁长电AGV项目MES数据接口需求确认.md", 179],
  ["R01-05", "mes/docs/AGV系统业务与MES任务模型.md", 546],
  ["R01-07", "mes/sources/customer/2026-07-16/operator-identity/README.md", 6],
  ["R01-08", "mes/sources/customer/2026-07-16/sublot-box-count/README.md", 6],
  ["R01-09", "mes/sources/customer/2026-07-24/mes-task-original-queries/README.md", 12],
  ["R01-10", "project_agreements/20260527-新基智能AGV小车技术协议-TR前线.docx", 137],
  ["R01-11", "project_agreements/生产指令书-8005 多仓位AGV.docx", 21],
  ["R01-13", "requirement-documents/07-customer-deliverables/客户需求讨论稿-多仓位AGV系统.md", 944],
  ["R01-14", "requirement-documents/07-customer-deliverables/宿迁长电多仓位AGV系统-需求讨论稿-2026-07-14.docx", 859],
  ["R01-15", "requirement-documents/07-customer-deliverables/assets/system-context.png", 14],
  ["R01-17", "requirement-documents/简易需求文档.md", 197],
  ["R01-19", "requirement-documents/user case.md", 41],
];
coverage.getRange("A1:E14").values = [["来源记录", "路径", "预期声明数", "实际声明数", "对账"], ...sourceRows.map((row) => [...row, null, null])];
for (let row = 2; row <= 14; row += 1) {
  coverage.getRange(`D${row}`).formulas = [[`=COUNTIF('Candidates'!$C$2:$C$3092,A${row})`]];
  coverage.getRange(`E${row}`).formulas = [[`=IF(C${row}=D${row},\"OK\",\"MISMATCH\")`]];
}
coverage.getRange("A1:E1").format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 25 };
coverage.getRange("A2:E14").format = { font: bodyFont, wrapText: true };
coverage.getRange("C2:D14").format.numberFormat = "#,##0";
coverage.getRange("E2:E14").conditionalFormats.add("containsText", { text: "MISMATCH", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
coverage.getRange("E2:E14").conditionalFormats.add("containsText", { text: "OK", format: { fill: paleTeal, font: { bold: true, color: "#0F5132" } } });
coverage.getRange("A1:E14").format.borders = { preset: "outside", style: "thin", color: lightGray };
coverage.getRange("A:A").format.columnWidth = 13;
coverage.getRange("B:B").format.columnWidth = 70;
coverage.getRange("C:E").format.columnWidth = 15;
coverage.freezePanes.freezeRows(1);

const conflictRows = [
  ["CF-R01-001", "运输需求业务键/幂等键口径", "potential-real-conflict", 19, "跨批次去重后若仍成立，进入 HITL 决策"],
  ["CF-R01-002", "当前阶段 MES 是否只读", "potential-real-conflict", 58, "分离系统回写、人工/PDA 动作与远期能力后再决策"],
  ["CF-R01-003", "AREA 映射模型", "cross-batch-conflict-lead", 5, "等待 R02/R03 原子拆分后复核"],
  ["AD-R01-001", "五类与六类运输任务", "apparent-version-difference", 5, "隔离 2026-07-14 冻结版；补客户批准证据"],
];
conflicts.getRange("A1:E5").values = [["指针", "主题", "性质", "命中行数", "后续处理"], ...conflictRows];
conflicts.getRange("A1:E1").format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 25 };
conflicts.getRange("A2:E5").format = { font: bodyFont, wrapText: true };
conflicts.getRange("C2:C3").format.fill = paleRed;
conflicts.getRange("C4:C5").format.fill = paleAmber;
conflicts.getRange("A1:E5").format.borders = { preset: "outside", style: "thin", color: lightGray };
conflicts.getRange("A:A").format.columnWidth = 16;
conflicts.getRange("B:B").format.columnWidth = 36;
conflicts.getRange("C:C").format.columnWidth = 28;
conflicts.getRange("D:D").format.columnWidth = 14;
conflicts.getRange("E:E").format.columnWidth = 58;
conflicts.freezePanes.freezeRows(1);

const lastColumn = columnName(candidateData[0].length - 1);
const lastRow = rows.length + 1;
candidates.getRange(`A1:${lastColumn}${lastRow}`).values = candidateData;
candidates.getRange("S2").formulas = [["=IF(ISNUMBER(SEARCH(\"exact-duplicate-of\",O2)),1,0)"]];
candidates.getRange(`S2:S${lastRow}`).fillDown();
candidates.getRange(`A1:${lastColumn}1`).format = {
  fill: navy,
  font: { ...bodyFont, bold: true, color: "#FFFFFF" },
  rowHeight: 28,
  wrapText: true,
};
candidates.getRange(`A2:${lastColumn}${lastRow}`).format = { font: bodyFont, verticalAlignment: "top" };
candidates.getRange(`G2:I${lastRow}`).format.wrapText = true;
candidates.getRange(`K2:R${lastRow}`).format.wrapText = true;
candidates.getRange(`A1:${lastColumn}${lastRow}`).format.borders = {
  insideHorizontal: { style: "thin", color: "#EDF0F3" },
  bottom: { style: "thin", color: lightGray },
};
candidates.tables.add(`A1:${lastColumn}${lastRow}`, true, "R01AtomicCandidatesTable");
candidates.freezePanes.freezeRows(1);
candidates.freezePanes.freezeColumns(3);
const widths = [14, 9, 13, 52, 22, 22, 42, 62, 68, 22, 34, 34, 32, 38, 58, 24, 16, 54, 18];
widths.forEach((width, index) => {
  candidates.getRange(`${columnName(index)}:${columnName(index)}`).format.columnWidth = width;
});

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });

const inspectSummary = await workbook.inspect({ kind: "table", range: "Summary!A1:E17", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 5 });
const inspectCoverage = await workbook.inspect({ kind: "table", range: "Source Coverage!A1:E14", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 6 });
const inspectConflicts = await workbook.inspect({ kind: "table", range: "Conflict Register!A1:E5", include: "values,formulas", tableMaxRows: 10, tableMaxCols: 6 });
const inspectErrors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
await fs.writeFile(path.join(qaDir, "inspect-summary.ndjson"), `${inspectSummary.ndjson}\n${inspectCoverage.ndjson}\n${inspectConflicts.ndjson}\n${inspectErrors.ndjson}\n`, "utf8");

for (const [sheetName, range, fileName] of [
  ["Summary", "A1:E17", "summary.png"],
  ["Source Coverage", "A1:E14", "source-coverage.png"],
  ["Conflict Register", "A1:E5", "conflict-register.png"],
  ["Candidates", "A1:S24", "candidates-top.png"],
  ["Candidates", "A3069:S3092", "candidates-bottom.png"],
]) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(path.join(qaDir, fileName), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "R01-atomic-candidates.xlsx"));
console.log(JSON.stringify({ rows: rows.length, columns: headers.length, output: path.join(outputDir, "R01-atomic-candidates.xlsx") }));
process.exit(0);
