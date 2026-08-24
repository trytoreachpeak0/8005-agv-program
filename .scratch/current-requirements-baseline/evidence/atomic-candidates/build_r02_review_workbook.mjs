import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = process.argv[2];
if (!repoRoot) throw new Error("Usage: node build_r02_review_workbook.mjs <repo-root>");

const artifactDir = path.join(repoRoot, ".scratch", "current-requirements-baseline", "evidence", "atomic-candidates");
const sourcePath = path.join(artifactDir, "R02-atomic-candidates.tsv");
const summaryPath = path.join(artifactDir, "R02-atomic-candidates-summary.json");
const outputDir = path.join(repoRoot, "outputs", "019fc847-5ff0-77b3-b61d-6d9b1e4e11cb");
const qaDir = path.join(artifactDir, "qa-xlsx-r02");

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
    } else if (char === '"') {
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
const summaryData = JSON.parse(await fs.readFile(summaryPath, "utf8"));
const data = parseDelimited(text);
const headers = data[0];
const rows = data.slice(1);
if (headers.length !== 18 || rows.length !== summaryData.total || summaryData.source_documents !== 19) {
  throw new Error(`Unexpected ledger shape: rows=${rows.length} cols=${headers.length} sources=${summaryData.source_documents}`);
}

const asExcelText = (value) => (typeof value === "string" && value.startsWith("=") ? `'${value}` : value);
const candidateData = [[...headers, "exact_duplicate_flag"], ...rows.map((row) => [...row.map(asExcelText), null])];
const lastRow = rows.length + 1;
const lastColumn = columnName(candidateData[0].length - 1);

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
summary.getRange("A1").values = [["R02 原子候选分类审阅"]];
summary.getRange("A1:E1").format = {
  fill: navy,
  font: { name: "Aptos Display", size: 18, bold: true, color: "#FFFFFF" },
  rowHeight: 32,
  verticalAlignment: "center",
};
summary.mergeCells("A2:E2");
summary.getRange("A2").values = [["候选分类，不是批准；用户澄清摘要、内部建模和上游派生保持隔离。"]];
summary.getRange("A2:E2").format = { fill: paleAmber, font: { ...bodyFont, italic: true }, rowHeight: 28, wrapText: true };
summary.getRange("A4:B8").values = [
  ["指标", "值"],
  ["原子声明", null],
  ["来源文档", null],
  ["精确重复（后出现行）", null],
  ["批准升级", null],
];
summary.getRange("B5").formulas = [[`=COUNTA('Candidates'!$A$2:$A$${lastRow})`]];
summary.getRange("B6").formulas = [["=COUNTA('Source Coverage'!$A$2:$A$20)"]];
summary.getRange("B7").formulas = [[`=SUM('Candidates'!$S$2:$S$${lastRow})`]];
summary.getRange("B8").formulas = [[`=COUNTIF('Candidates'!$Q$2:$Q$${lastRow},"<>not-approved")`]];
summary.getRange("A4:B4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:A8").format = { fill: paleBlue, font: { ...bodyFont, bold: true } };
summary.getRange("B5:B8").format = { font: { ...bodyFont, bold: true }, numberFormat: "#,##0" };
summary.getRange("A4:B8").format.borders = { preset: "outside", style: "thin", color: lightGray };

const routes = Object.keys(summaryData.by_route).sort();
summary.getRange(`A10:B${10 + routes.length}`).values = [["处置路线", "数量"], ...routes.map((route) => [route, null])];
for (let row = 11; row <= 10 + routes.length; row += 1) {
  summary.getRange(`B${row}`).formulas = [[`=COUNTIF('Candidates'!$N$2:$N$${lastRow},A${row})`]];
}
summary.getRange("A10:B10").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange(`A11:A${10 + routes.length}`).format = { font: bodyFont };
summary.getRange(`B11:B${10 + routes.length}`).format = { font: bodyFont, numberFormat: "#,##0" };
summary.getRange(`A10:B${10 + routes.length}`).format.borders = { preset: "outside", style: "thin", color: lightGray };
summary.getRange(`A1:E${10 + routes.length}`).format.wrapText = true;
summary.getRange("A:A").format.columnWidth = 48;
summary.getRange("B:B").format.columnWidth = 16;
summary.getRange("C:E").format.columnWidth = 12;
summary.freezePanes.freezeRows(2);

const sourceRows = Object.entries(summaryData.by_source).map(([recordId, count]) => {
  const first = rows.find((row) => row[2] === recordId);
  return [recordId, first?.[3] ?? "", count, null, null];
});
coverage.getRange("A1:E20").values = [["来源记录", "路径", "预期声明数", "实际声明数", "对账"], ...sourceRows];
for (let row = 2; row <= 20; row += 1) {
  coverage.getRange(`D${row}`).formulas = [[`=COUNTIF('Candidates'!$C$2:$C$${lastRow},A${row})`]];
  coverage.getRange(`E${row}`).formulas = [[`=IF(C${row}=D${row},"OK","MISMATCH")`]];
}
coverage.getRange("A1:E1").format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 25 };
coverage.getRange("A2:E20").format = { font: bodyFont, wrapText: true };
coverage.getRange("C2:D20").format.numberFormat = "#,##0";
coverage.getRange("E2:E20").conditionalFormats.add("containsText", { text: "MISMATCH", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
coverage.getRange("E2:E20").conditionalFormats.add("containsText", { text: "OK", format: { fill: paleTeal, font: { bold: true, color: "#0F5132" } } });
coverage.getRange("A1:E20").format.borders = { preset: "outside", style: "thin", color: lightGray };
coverage.getRange("A:A").format.columnWidth = 13;
coverage.getRange("B:B").format.columnWidth = 72;
coverage.getRange("C:E").format.columnWidth = 15;
coverage.freezePanes.freezeRows(1);

const conflictRows = [
  ["CF-R01-001", "运输需求业务键/幂等键口径", "跨批次冲突线索", null, "完成其余批次原子化与跨批去重后复核"],
  ["CF-R01-002", "当前阶段 MES 是否只读", "跨批次冲突线索", null, "分离系统回写、人工/PDA 动作与远期能力后复核"],
  ["CF-R01-003", "AREA 映射模型", "跨批次冲突线索", null, "等待 R03 相关用例原子拆分后复核"],
  ["AD-R01-001", "五类与六类运输任务", "表面版本差异", null, "保持版本隔离并补第六类批准证据"],
];
conflicts.getRange("A1:E5").values = [["指针", "主题", "性质", "命中行数", "后续处理"], ...conflictRows];
for (let row = 2; row <= 5; row += 1) {
  conflicts.getRange(`D${row}`).formulas = [[`=COUNTIF('Candidates'!$P$2:$P$${lastRow},A${row})`]];
}
conflicts.getRange("A1:E1").format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 25 };
conflicts.getRange("A2:E5").format = { font: bodyFont, wrapText: true };
conflicts.getRange("C2:C4").format.fill = paleRed;
conflicts.getRange("C5").format.fill = paleAmber;
conflicts.getRange("A1:E5").format.borders = { preset: "outside", style: "thin", color: lightGray };
conflicts.getRange("A:A").format.columnWidth = 16;
conflicts.getRange("B:B").format.columnWidth = 38;
conflicts.getRange("C:C").format.columnWidth = 24;
conflicts.getRange("D:D").format.columnWidth = 14;
conflicts.getRange("E:E").format.columnWidth = 56;
conflicts.freezePanes.freezeRows(1);

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
candidates.tables.add(`A1:${lastColumn}${lastRow}`, true, "R02AtomicCandidatesTable");
candidates.freezePanes.freezeRows(1);
candidates.freezePanes.freezeColumns(3);
const widths = [14, 9, 13, 54, 22, 20, 48, 68, 72, 22, 38, 40, 34, 42, 68, 24, 16, 62, 18];
widths.forEach((width, index) => candidates.getRange(`${columnName(index)}:${columnName(index)}`).format.columnWidth = width);

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });
const inspectSummary = await workbook.inspect({ kind: "table", range: `Summary!A1:E${10 + routes.length}`, include: "values,formulas", tableMaxRows: 24, tableMaxCols: 5 });
const inspectCoverage = await workbook.inspect({ kind: "table", range: "Source Coverage!A1:E20", include: "values,formulas", tableMaxRows: 22, tableMaxCols: 5 });
const inspectConflicts = await workbook.inspect({ kind: "table", range: "Conflict Register!A1:E5", include: "values,formulas", tableMaxRows: 8, tableMaxCols: 5 });
const inspectErrors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
await fs.writeFile(path.join(qaDir, "inspect-summary.ndjson"), `${inspectSummary.ndjson}\n${inspectCoverage.ndjson}\n${inspectConflicts.ndjson}\n${inspectErrors.ndjson}\n`, "utf8");

for (const [sheetName, range, fileName] of [
  ["Summary", `A1:E${10 + routes.length}`, "summary.png"],
  ["Source Coverage", "A1:E20", "source-coverage.png"],
  ["Conflict Register", "A1:E5", "conflict-register.png"],
  ["Candidates", "A1:S24", "candidates-top.png"],
  ["Candidates", `A${lastRow - 23}:S${lastRow}`, "candidates-bottom.png"],
]) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(path.join(qaDir, fileName), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
const outputPath = path.join(outputDir, "R02-atomic-candidates.xlsx");
await output.save(outputPath);
console.log(JSON.stringify({ rows: rows.length, columns: headers.length, output: outputPath }));
process.exit(0);
