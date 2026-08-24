import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = process.argv[2];
if (!repoRoot) throw new Error("Usage: node build_consolidated_review_workbook.mjs <repo-root>");
const skipQa = process.argv.includes("--skip-qa");

const artifactDir = path.join(repoRoot, ".scratch", "current-requirements-baseline", "evidence", "atomic-candidates");
const outputDir = path.join(repoRoot, "outputs", "019fcb39-f5f0-7861-af1c-8a35895e8ae3");
const qaDir = path.join(artifactDir, "qa-xlsx-r01-r13-consolidated");
const outputPath = path.join(outputDir, "R01-R13-consolidated-atomic-candidates-review.xlsx");

function parseDelimited(text, delimiter = "\t") {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') { field += '"'; index += 1; }
      else if (char === '"') quoted = false;
      else field += char;
    } else if (char === '"') quoted = true;
    else if (char === delimiter) { row.push(field); field = ""; }
    else if (char === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
    else field += char;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
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

async function loadTsv(name) {
  return parseDelimited(await fs.readFile(path.join(artifactDir, name), "utf8"));
}

const consolidated = await loadTsv("R01-R13-consolidated-atomic-candidates.tsv");
const relations = await loadTsv("R01-R13-semantic-relations.tsv");
const clusters = await loadTsv("R01-R13-semantic-review-clusters.tsv");
const derivations = await loadTsv("R01-R13-source-derivations.tsv");
const conflicts = await loadTsv("R01-R13-conflict-review.tsv");
const approvalBatches = await loadTsv("R01-R13-approval-batch-suggestions.tsv");
const summaryData = JSON.parse(await fs.readFile(path.join(artifactDir, "R01-R13-consolidated-atomic-candidates-summary.json"), "utf8"));

if (consolidated.length !== 12453 || consolidated[0].length !== 28) {
  throw new Error(`Unexpected consolidated shape: rows=${consolidated.length} cols=${consolidated[0]?.length}`);
}

const asExcelText = (value) => (typeof value === "string" && value.startsWith("=") ? `'${value}` : value);
const safeRows = (matrix) => matrix.map((row) => row.map(asExcelText));
const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const coverage = workbook.worksheets.add("Batch Coverage");
const conflictSheet = workbook.worksheets.add("Conflict Review");
const approvalSheet = workbook.worksheets.add("Approval Batches");
const clusterSheet = workbook.worksheets.add("Semantic Clusters");
const relationSheet = workbook.worksheets.add("Relations");
const derivationSheet = workbook.worksheets.add("Source Derivations");
const consolidatedSheet = workbook.worksheets.add("Consolidated");
const sheets = [summary, coverage, conflictSheet, approvalSheet, clusterSheet, relationSheet, derivationSheet, consolidatedSheet];
for (const sheet of sheets) sheet.showGridLines = false;

const navy = "#17324D";
const teal = "#0F766E";
const amber = "#FFF2CC";
const paleRed = "#FDE2E2";
const paleTeal = "#DDF3EF";
const paleBlue = "#E8F0FE";
const paleGray = "#EEF1F4";
const lightGray = "#D9E0E7";
const ink = "#172033";
const bodyFont = { name: "Aptos", size: 10, color: ink };
const headerFormat = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 30, wrapText: true };

const consolidatedLastRow = consolidated.length;
const consolidatedLastColumn = columnName(consolidated[0].length - 1);
const relationLastRow = relations.length;
const clusterLastRow = clusters.length;
const approvalLastRow = approvalBatches.length;
const conflictLastRow = conflicts.length;
const derivationLastRow = derivations.length;

summary.mergeCells("A1:H1");
summary.getRange("A1").values = [["R01–R13 原子候选合并与语义去重审阅"]];
summary.getRange("A1:H1").format = {
  fill: navy,
  font: { name: "Aptos Display", size: 18, bold: true, color: "#FFFFFF" },
  rowHeight: 36,
  verticalAlignment: "center",
};
summary.mergeCells("A2:H2");
summary.getRange("A2").values = [["这是审阅索引，不是需求基线：所有 12,452 条来源记录、版本/范围和未批准状态均保留；关系簇只用于共同审阅，绝不自动合并、删除或批准。"]];
summary.getRange("A2:H2").format = { fill: amber, font: { ...bodyFont, italic: true }, rowHeight: 34, wrapText: true };

summary.getRange("A4:B13").values = [
  ["指标", "值"],
  ["原子候选记录", null],
  ["来源文档", null],
  ["关系记录", null],
  ["语义审阅簇", null],
  ["批准候选（仍未批准）", null],
  ["建议批准批次", null],
  ["毕业为 HITL 的真实冲突", null],
  ["批准状态升级", null],
  ["输入批次", null],
];
summary.getRange("B5").formulas = [[`=COUNTA('Consolidated'!$A$2:$A$${consolidatedLastRow})`]];
summary.getRange("B6").formulas = [["=SUM('Batch Coverage'!$C$2:$C$14)-'Batch Coverage'!$C$15"]];
summary.getRange("B7").formulas = [[`=COUNTA('Relations'!$A$2:$A$${relationLastRow})`]];
summary.getRange("B8").formulas = [[`=COUNTA('Semantic Clusters'!$A$2:$A$${clusterLastRow})`]];
summary.getRange("B9").formulas = [[`=COUNTIF('Consolidated'!$Y$2:$Y$${consolidatedLastRow},"approval-candidate-not-approved")`]];
summary.getRange("B10").formulas = [[`=COUNTA('Approval Batches'!$A$2:$A$${approvalLastRow})`]];
summary.getRange("B11").formulas = [[`=COUNTIF('Conflict Review'!$C$2:$C$${conflictLastRow},"graduate-hitl-real-conflict")`]];
summary.getRange("B12").formulas = [[`=COUNTIF('Consolidated'!$Q$2:$Q$${consolidatedLastRow},"<>not-approved")`]];
summary.getRange("B13").formulas = [["=COUNTA('Batch Coverage'!$A$2:$A$14)"]];
summary.getRange("A4:B4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:A13").format = { fill: paleBlue, font: { ...bodyFont, bold: true } };
summary.getRange("B5:B13").format = { font: { ...bodyFont, bold: true }, numberFormat: "#,##0" };
summary.getRange("A4:B13").format.borders = { preset: "outside", style: "thin", color: lightGray };

const relationTypes = [
  ["exact-text-duplicate", "完全相同文本"],
  ["normalized-text-duplicate", "规范化相同"],
  ["semantic-near-review", "语义近似审阅"],
];
summary.getRange("D4:F7").values = [["关系类型", "关系数", "说明"], ...relationTypes.map(([type, label]) => [type, null, label])];
for (let row = 5; row <= 7; row += 1) {
  summary.getRange(`E${row}`).formulas = [[`=COUNTIF('Relations'!$B$2:$B$${relationLastRow},D${row})`]];
}
summary.getRange("D4:F4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("D5:F7").format = { font: bodyFont, wrapText: true };
summary.getRange("D4:F7").format.borders = { preset: "outside", style: "thin", color: lightGray };
summary.getRange("E5:E7").format.numberFormat = "#,##0";

summary.getRange("D10:H15").values = [
  ["冲突处置", "数量", "地图动作", "", ""],
  ["真实冲突", null, "生成独立 HITL grilling 票", "", ""],
  ["版本差异已收敛", null, "保留版本证据，不再生成票", "", ""],
  ["范围外技术复核", null, "不进入本地图需求决定", "", ""],
  ["关系簇使用边界", "", "共同审阅，不自动合并", "", ""],
  ["批准批次上限", "", "每批最多 180 行 / 120 个审阅单元", "", ""],
];
summary.getRange("E11").formulas = [[`=COUNTIF('Conflict Review'!$C$2:$C$${conflictLastRow},"graduate-hitl-real-conflict")`]];
summary.getRange("E12").formulas = [[`=COUNTIF('Conflict Review'!$C$2:$C$${conflictLastRow},"apparent-version-difference-converged")`]];
summary.getRange("E13").formulas = [[`=COUNTIF('Conflict Review'!$C$2:$C$${conflictLastRow},"out-of-scope-technical-review")`]];
summary.getRange("D10:H10").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("D11:H15").format = { font: bodyFont, wrapText: true, verticalAlignment: "top" };
summary.getRange("D10:H15").format.borders = { preset: "outside", style: "thin", color: lightGray };
summary.getRange("A:A").format.columnWidth = 32;
summary.getRange("B:B").format.columnWidth = 14;
summary.getRange("C:C").format.columnWidth = 4;
summary.getRange("D:D").format.columnWidth = 36;
summary.getRange("E:E").format.columnWidth = 12;
summary.getRange("F:H").format.columnWidth = 26;
summary.freezePanes.freezeRows(2);

const batchRows = Object.entries(summaryData.batches).map(([batch, count]) => [batch, count, null, null, null, null]);
const sourceBatches = new Map();
for (const row of consolidated.slice(1)) {
  if (!sourceBatches.has(row[2])) sourceBatches.set(row[2], new Set());
  sourceBatches.get(row[2]).add(row[1]);
}
const crossBatchSourceReuse = [...sourceBatches.values()].reduce((total, batches) => total + Math.max(0, batches.size - 1), 0);
coverage.getRange("A1:F15").values = [
  ["批次", "预期记录数", "来源文档", "实际记录数", "未批准记录", "对账"],
  ...batchRows,
  ["跨批次复用来源身份（扣除）", "", crossBatchSourceReuse, "", "", "INFORMATION"],
];
for (let row = 2; row <= 14; row += 1) {
  const batch = batchRows[row - 2][0];
  const sourceCount = new Set(consolidated.slice(1).filter((item) => item[1] === batch).map((item) => item[2])).size;
  coverage.getRange(`C${row}`).values = [[sourceCount]];
  coverage.getRange(`D${row}`).formulas = [[`=COUNTIF('Consolidated'!$B$2:$B$${consolidatedLastRow},A${row})`]];
  coverage.getRange(`E${row}`).formulas = [[`=COUNTIFS('Consolidated'!$B$2:$B$${consolidatedLastRow},A${row},'Consolidated'!$Q$2:$Q$${consolidatedLastRow},"not-approved")`]];
  coverage.getRange(`F${row}`).formulas = [[`=IF(AND(B${row}=D${row},D${row}=E${row}),"OK","MISMATCH")`]];
}
coverage.getRange("A1:F1").format = headerFormat;
coverage.getRange("A2:F15").format = { font: bodyFont };
coverage.getRange("A15:F15").format = { fill: amber, font: { ...bodyFont, italic: true } };
coverage.getRange("B2:E14").format.numberFormat = "#,##0";
coverage.getRange("F2:F14").conditionalFormats.add("containsText", { text: "OK", format: { fill: paleTeal, font: { bold: true, color: "#0F5132" } } });
coverage.getRange("F2:F14").conditionalFormats.add("containsText", { text: "MISMATCH", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
coverage.getRange("A1:F15").format.borders = { preset: "outside", style: "thin", color: lightGray };
coverage.getRange("A:A").format.columnWidth = 12;
coverage.getRange("B:E").format.columnWidth = 17;
coverage.getRange("F:F").format.columnWidth = 16;
coverage.freezePanes.freezeRows(1);

function addRawSheet(sheet, matrix, tableName, widths, wrapColumns = []) {
  const lastRow = matrix.length;
  const lastColumn = columnName(matrix[0].length - 1);
  sheet.getRange(`A1:${lastColumn}${lastRow}`).values = safeRows(matrix);
  sheet.getRange(`A1:${lastColumn}1`).format = headerFormat;
  sheet.getRange(`A2:${lastColumn}${lastRow}`).format = { font: bodyFont, verticalAlignment: "top" };
  for (const column of wrapColumns) sheet.getRange(`${column}2:${column}${lastRow}`).format.wrapText = true;
  sheet.getRange(`A1:${lastColumn}${lastRow}`).format.borders = {
    insideHorizontal: { style: "thin", color: "#EDF0F3" },
    bottom: { style: "thin", color: lightGray },
  };
  sheet.tables.add(`A1:${lastColumn}${lastRow}`, true, tableName);
  widths.forEach((width, index) => { sheet.getRange(`${columnName(index)}:${columnName(index)}`).format.columnWidth = width; });
  sheet.freezePanes.freezeRows(1);
  return { lastRow, lastColumn };
}

addRawSheet(conflictSheet, conflicts, "ConflictReviewTable", [18, 34, 36, 14, 18, 24, 76, 48, 92], ["B", "G", "H", "I"]);
conflictSheet.getRange(`A2:I${conflictLastRow}`).format.rowHeight = 60;
conflictSheet.getRange(`C2:C${conflictLastRow}`).conditionalFormats.add("containsText", { text: "graduate-hitl", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
conflictSheet.getRange(`C2:C${conflictLastRow}`).conditionalFormats.add("containsText", { text: "converged", format: { fill: paleTeal, font: { bold: true, color: "#0F5132" } } });
conflictSheet.getRange(`C2:C${conflictLastRow}`).conditionalFormats.add("containsText", { text: "out-of-scope", format: { fill: paleGray, font: { color: navy } } });

addRawSheet(approvalSheet, approvalBatches, "ApprovalBatchSuggestionsTable", [20, 24, 48, 16, 18, 18, 28, 30, 84], ["B", "C", "G", "H", "I"]);
approvalSheet.getRange(`A2:I${approvalLastRow}`).format.rowHeight = 42;
for (let row = 2; row <= approvalLastRow; row += 1) {
  approvalSheet.getRange(`D${row}`).formulas = [[`=COUNTIF('Consolidated'!$Z$2:$Z$${consolidatedLastRow},A${row})`]];
}
approvalSheet.getRange(`G2:G${approvalLastRow}`).conditionalFormats.add("notContainsBlanks", { format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
approvalSheet.getRange(`H2:H${approvalLastRow}`).conditionalFormats.add("containsText", { text: "after-conflict", format: { fill: amber, font: { color: "#7A4E00" } } });

addRawSheet(clusterSheet, clusters, "SemanticReviewClustersTable", [16, 18, 14, 12, 12, 38, 46, 70, 28, 90, 88, 78], ["F", "G", "H", "I", "J", "K", "L"]);
clusterSheet.getRange(`A2:L${clusterLastRow}`).format.rowHeight = 54;
clusterSheet.getRange(`I2:I${clusterLastRow}`).conditionalFormats.add("notContainsBlanks", { format: { fill: amber, font: { color: "#7A4E00" } } });

addRawSheet(relationSheet, relations, "SemanticRelationsTable", [16, 24, 18, 18, 12, 12, 16, 16, 14, 14, 14, 16, 26, 34, 54, 44], ["M", "N", "O", "P"]);
relationSheet.getRange(`A2:P${relationLastRow}`).format.rowHeight = 30;
relationSheet.getRange(`B2:B${relationLastRow}`).conditionalFormats.add("containsText", { text: "semantic-near", format: { fill: paleTeal, font: { color: "#0F5132" } } });
relationSheet.getRange(`P2:P${relationLastRow}`).conditionalFormats.add("containsText", { text: "retain-separate", format: { fill: amber, font: { color: "#7A4E00" } } });

addRawSheet(derivationSheet, derivations, "SourceDerivationsTable", [16, 18, 18, 12, 12, 18, 60, 90, 84], ["G", "H", "I"]);
derivationSheet.getRange(`A2:I${derivationLastRow}`).format.rowHeight = 52;

addRawSheet(consolidatedSheet, consolidated, "ConsolidatedAtomicCandidatesTable", [
  16, 10, 14, 64, 22, 24, 48, 78, 78, 22, 46, 54, 48, 58, 84, 28, 16, 88,
  22, 22, 16, 16, 16, 26, 38, 20, 28, 28,
], ["G", "H", "I", "K", "L", "M", "N", "O", "P", "R", "X", "Y", "AA", "AB"]);
consolidatedSheet.freezePanes.freezeColumns(3);
consolidatedSheet.getRange(`Y2:Y${consolidatedLastRow}`).conditionalFormats.add("containsText", { text: "approval-candidate", format: { fill: paleTeal, font: { color: "#0F5132" } } });
consolidatedSheet.getRange(`Y2:Y${consolidatedLastRow}`).conditionalFormats.add("containsText", { text: "hold-for-hitl", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
consolidatedSheet.getRange(`Y2:Y${consolidatedLastRow}`).conditionalFormats.add("containsText", { text: "hold-for-question", format: { fill: amber, font: { color: "#7A4E00" } } });
consolidatedSheet.getRange(`Y2:Y${consolidatedLastRow}`).conditionalFormats.add("containsText", { text: "excluded", format: { fill: paleGray, font: { color: navy } } });
consolidatedSheet.getRange(`Q2:Q${consolidatedLastRow}`).conditionalFormats.add("notContainsText", { text: "not-approved", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });
if (!skipQa) {
  const inspections = [];
  inspections.push(await workbook.inspect({ kind: "table", range: "Summary!A1:H15", include: "values,formulas", tableMaxRows: 18, tableMaxCols: 8 }));
  inspections.push(await workbook.inspect({ kind: "table", range: "Batch Coverage!A1:F15", include: "values,formulas", tableMaxRows: 16, tableMaxCols: 6 }));
  inspections.push(await workbook.inspect({ kind: "table", range: `Conflict Review!A1:I${conflictLastRow}`, include: "values,formulas", tableMaxRows: 10, tableMaxCols: 9 }));
  inspections.push(await workbook.inspect({ kind: "table", range: `Approval Batches!A1:I${Math.min(approvalLastRow, 16)}`, include: "values,formulas", tableMaxRows: 16, tableMaxCols: 9 }));
  inspections.push(await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 200 }, summary: "final formula error scan" }));
  await fs.writeFile(path.join(qaDir, "inspect-summary.ndjson"), inspections.map((item) => item.ndjson).join("\n") + "\n", "utf8");

  const previews = [
    ["Summary", "A1:H15", "summary.png"],
    ["Batch Coverage", "A1:F15", "batch-coverage.png"],
    ["Conflict Review", `A1:I${conflictLastRow}`, "conflict-review.png"],
    ["Approval Batches", `A1:I${Math.min(approvalLastRow, 18)}`, "approval-batches.png"],
    ["Semantic Clusters", `A1:L${Math.min(clusterLastRow, 14)}`, "semantic-clusters.png"],
    ["Relations", `A1:P${Math.min(relationLastRow, 14)}`, "relations.png"],
    ["Source Derivations", `A1:I${Math.min(derivationLastRow, 16)}`, "source-derivations.png"],
    ["Consolidated", `A1:${consolidatedLastColumn}16`, "consolidated-top.png"],
    ["Consolidated", `A${consolidatedLastRow - 14}:${consolidatedLastColumn}${consolidatedLastRow}`, "consolidated-bottom.png"],
  ];
  for (const [sheetName, range, fileName] of previews) {
    const preview = await workbook.render({ sheetName, range, scale: 0.9, format: "png" });
    await fs.writeFile(path.join(qaDir, fileName), new Uint8Array(await preview.arrayBuffer()));
  }
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(JSON.stringify({ outputPath, qaDir, sheets: sheets.length, rows: consolidatedLastRow - 1 }));
