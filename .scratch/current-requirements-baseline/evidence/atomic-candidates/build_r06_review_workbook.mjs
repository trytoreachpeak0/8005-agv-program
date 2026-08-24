import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = process.argv[2];
if (!repoRoot) throw new Error("Usage: node build_r06_review_workbook.mjs <repo-root>");

const artifactDir = path.join(repoRoot, ".scratch", "current-requirements-baseline", "evidence", "atomic-candidates");
const candidatePath = path.join(artifactDir, "R06-atomic-candidates.tsv");
const historicalPath = path.join(artifactDir, "R06-drifted-historical-evidence.tsv");
const summaryPath = path.join(artifactDir, "R06-atomic-candidates-summary.json");
const outputDir = path.join(repoRoot, "outputs", "019fca8e-d853-7022-9f17-f8973206bf37");
const qaDir = path.join(artifactDir, "qa-xlsx-r06");

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

const candidateDataRaw = parseDelimited(await fs.readFile(candidatePath, "utf8"));
const historicalData = parseDelimited(await fs.readFile(historicalPath, "utf8"));
const summaryData = JSON.parse(await fs.readFile(summaryPath, "utf8"));
const headers = candidateDataRaw[0];
const rows = candidateDataRaw.slice(1);
const historicalHeaders = historicalData[0];
const historicalRows = historicalData.slice(1);
if (headers.length !== 18 || rows.length !== summaryData.total || summaryData.scenario_source_documents !== 52) {
  throw new Error(`Unexpected R06 ledger shape: rows=${rows.length} cols=${headers.length} sources=${summaryData.scenario_source_documents}`);
}
if (historicalHeaders.length !== 13 || historicalRows.length !== 4 || summaryData.new_identity_candidates !== 4) {
  throw new Error("R06 version-isolation shape mismatch");
}

const asExcelText = (value) => (typeof value === "string" && value.startsWith("=") ? `'${value}` : value);
const candidateData = [headers, ...rows.map((row) => row.map(asExcelText))];
const lastRow = rows.length + 1;
const lastColumn = columnName(candidateData[0].length - 1);

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const coverage = workbook.worksheets.add("Source Coverage");
const isolation = workbook.worksheets.add("Version Isolation");
const candidates = workbook.worksheets.add("Candidates");
for (const sheet of [summary, coverage, isolation, candidates]) sheet.showGridLines = false;

const navy = "#17324D";
const teal = "#0F766E";
const paleTeal = "#DDF3EF";
const paleAmber = "#FFF2CC";
const paleRed = "#FDE2E2";
const paleBlue = "#E8F0FE";
const lightGray = "#D9E0E7";
const ink = "#172033";
const bodyFont = { name: "Aptos", size: 10, color: ink };

summary.mergeCells("A1:F1");
summary.getRange("A1").values = [["R06 仓位、硬件与车队验收原子候选审阅"]];
summary.getRange("A1:F1").format = {
  fill: navy,
  font: { name: "Aptos Display", size: 18, bold: true, color: "#FFFFFF" },
  rowHeight: 34,
  verticalAlignment: "center",
};
summary.mergeCells("A2:F2");
summary.getRange("A2").values = [["候选分类，不是批准；52 份草案无执行证据，4 份旧 TC 仅作历史证据，四个当前语义使用全新候选身份。"]];
summary.getRange("A2:F2").format = { fill: paleAmber, font: { ...bodyFont, italic: true }, rowHeight: 32, wrapText: true };
summary.getRange("A4:B9").values = [
  ["指标", "值"],
  ["全部候选记录", null],
  ["52 份草案原子记录", null],
  ["当前 FR-016 新身份候选", null],
  ["旧稿历史证据", null],
  ["批准升级", null],
];
summary.getRange("B5").formulas = [[`=COUNTA('Candidates'!$A$2:$A$${lastRow})`]];
summary.getRange("B6").formulas = [["=B5-B7"]];
summary.getRange("B7").formulas = [[
  `=COUNTIF('Candidates'!$A$2:$A$${lastRow},"R06-N001")+COUNTIF('Candidates'!$A$2:$A$${lastRow},"R06-N002")+COUNTIF('Candidates'!$A$2:$A$${lastRow},"R06-N003")+COUNTIF('Candidates'!$A$2:$A$${lastRow},"R06-N004")`,
]];
summary.getRange("B8").formulas = [["=COUNTA('Version Isolation'!$A$5:$A$8)"]];
summary.getRange("B9").formulas = [[`=COUNTIF('Candidates'!$Q$2:$Q$${lastRow},"<>not-approved")`]];
summary.getRange("A4:B4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:A9").format = { fill: paleBlue, font: { ...bodyFont, bold: true } };
summary.getRange("B5:B9").format = { font: { ...bodyFont, bold: true }, numberFormat: "#,##0" };
summary.getRange("A4:B9").format.borders = { preset: "outside", style: "thin", color: lightGray };

const routes = Object.keys(summaryData.by_route).sort();
const routeEnd = 11 + routes.length;
summary.getRange(`A11:B${routeEnd}`).values = [["处置路线", "数量"], ...routes.map((route) => [route, null])];
for (let row = 12; row <= routeEnd; row += 1) {
  summary.getRange(`B${row}`).formulas = [[`=COUNTIF('Candidates'!$N$2:$N$${lastRow},A${row})`]];
}
summary.getRange("A11:B11").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange(`A12:B${routeEnd}`).format = { font: bodyFont, wrapText: true };
summary.getRange(`B12:B${routeEnd}`).format.numberFormat = "#,##0";
summary.getRange(`A11:B${routeEnd}`).format.borders = { preset: "outside", style: "thin", color: lightGray };

summary.getRange("D4:F4").values = [["证据/范围指针", "命中", "含义"]];
summary.getRange("D5:F7").values = [
  ["AD-R06-001", null, "旧 TC 与当前 FR-016 AC 的版本隔离；当前语义使用 R06-N001～N004"],
  ["EX-R06-001", null, "52 份草案均缺构建、环境、执行人、时间、实际结果与附件哈希"],
  ["SB-R06-001", null, "AGV 启停与仓位启停术语相似但对象不同，不得跨对象复用身份"],
];
summary.getRange("E5").formulas = [["=B7"]];
summary.getRange("E6").formulas = [[`=COUNTIF('Candidates'!$K$2:$K$${lastRow},"verification-traceability-evidence")`]];
summary.getRange("E7").formulas = [[
  `=COUNTIF('Candidates'!$C$2:$C$${lastRow},"R06-41")+COUNTIF('Candidates'!$C$2:$C$${lastRow},"R06-42")+COUNTIF('Candidates'!$C$2:$C$${lastRow},"R06-43")+COUNTIF('Candidates'!$C$2:$C$${lastRow},"R06-44")+COUNTIF('Candidates'!$C$2:$C$${lastRow},"R06-45")`,
]];
summary.getRange("D4:F4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("D5:F7").format = { font: bodyFont, wrapText: true };
summary.getRange("D5:D7").format.fill = paleBlue;
summary.getRange("E5:E7").format.numberFormat = "#,##0";
summary.getRange("D4:F7").format.borders = { preset: "outside", style: "thin", color: lightGray };
summary.getRange("A:A").format.columnWidth = 52;
summary.getRange("B:B").format.columnWidth = 15;
summary.getRange("C:C").format.columnWidth = 5;
summary.getRange("D:D").format.columnWidth = 18;
summary.getRange("E:E").format.columnWidth = 12;
summary.getRange("F:F").format.columnWidth = 58;
summary.freezePanes.freezeRows(2);

const sourceRows = Object.entries(summaryData.by_source).map(([recordId, count]) => {
  const first = rows.find((row) => row[2] === recordId);
  const sourceKind = recordId === "R04-17" ? "current-FR016-new-identity-source" : "R06-scenario-draft";
  return [recordId, sourceKind, first?.[3] ?? "", count, null, null];
});
const coverageEnd = sourceRows.length + 1;
coverage.getRange(`A1:F${coverageEnd}`).values = [["来源记录", "来源类型", "路径", "预期记录数", "实际记录数", "对账"], ...sourceRows];
for (let row = 2; row <= coverageEnd; row += 1) {
  coverage.getRange(`E${row}`).formulas = [[`=COUNTIF('Candidates'!$C$2:$C$${lastRow},A${row})`]];
  coverage.getRange(`F${row}`).formulas = [[`=IF(D${row}=E${row},"OK","MISMATCH")`]];
}
coverage.getRange("A1:F1").format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 26 };
coverage.getRange(`A2:F${coverageEnd}`).format = { font: bodyFont, wrapText: true, verticalAlignment: "top" };
coverage.getRange(`D2:E${coverageEnd}`).format.numberFormat = "#,##0";
coverage.getRange(`F2:F${coverageEnd}`).conditionalFormats.add("containsText", { text: "MISMATCH", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
coverage.getRange(`F2:F${coverageEnd}`).conditionalFormats.add("containsText", { text: "OK", format: { fill: paleTeal, font: { bold: true, color: "#0F5132" } } });
coverage.getRange(`A1:F${coverageEnd}`).format.borders = { preset: "outside", style: "thin", color: lightGray };
coverage.getRange("A:A").format.columnWidth = 14;
coverage.getRange("B:B").format.columnWidth = 34;
coverage.getRange("C:C").format.columnWidth = 76;
coverage.getRange("D:F").format.columnWidth = 15;
coverage.freezePanes.freezeRows(1);

isolation.mergeCells("A1:M1");
isolation.getRange("A1").values = [["版本隔离：旧 TC 身份保留，新语义另建身份"]];
isolation.getRange("A1:M1").format = { fill: navy, font: { name: "Aptos Display", size: 17, bold: true, color: "#FFFFFF" }, rowHeight: 32 };
isolation.mergeCells("A2:M2");
isolation.getRange("A2").values = [["TC-044～TC-047 不修改、不复用、不进入当前候选；它们固定到旧 FR-016 提交与 blob。"]];
isolation.getRange("A2:M2").format = { fill: paleAmber, font: { ...bodyFont, italic: true }, rowHeight: 28, wrapText: true };
isolation.getRange("A4:M8").values = [historicalHeaders, ...historicalRows.map((row) => row.map(asExcelText))];
isolation.getRange("A4:M4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, wrapText: true };
isolation.getRange("A5:M8").format = { font: bodyFont, wrapText: true, verticalAlignment: "top" };
isolation.getRange("A4:M8").format.borders = { preset: "outside", style: "thin", color: lightGray };
isolation.mergeCells("A10:H10");
isolation.getRange("A10").values = [["当前 FR-016 的四个新身份候选"]];
isolation.getRange("A10:H10").format = { fill: paleBlue, font: { ...bodyFont, bold: true }, rowHeight: 24 };
const newRows = rows.filter((row) => row[0].startsWith("R06-N")).map((row) => [row[0], row[2], row[4], row[5], row[7], row[13], row[14], row[16]]);
isolation.getRange("A11:H15").values = [["新候选 ID", "来源记录", "来源 SHA-256", "定位", "当前验收声明", "处置路线", "身份/派生", "批准状态"], ...newRows];
isolation.getRange("A11:H11").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, wrapText: true };
isolation.getRange("A12:H15").format = { font: bodyFont, wrapText: true, verticalAlignment: "top" };
isolation.getRange("A11:H15").format.borders = { preset: "outside", style: "thin", color: lightGray };
const isolationWidths = [15, 14, 56, 18, 76, 40, 80, 16, 28, 28, 28, 28, 64];
isolationWidths.forEach((width, index) => isolation.getRange(`${columnName(index)}:${columnName(index)}`).format.columnWidth = width);
isolation.freezePanes.freezeRows(4);

candidates.getRange(`A1:${lastColumn}${lastRow}`).values = candidateData;
candidates.getRange(`A1:${lastColumn}1`).format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 30, wrapText: true };
candidates.getRange(`A2:${lastColumn}${lastRow}`).format = { font: bodyFont, verticalAlignment: "top" };
candidates.getRange(`G2:I${lastRow}`).format.wrapText = true;
candidates.getRange(`K2:R${lastRow}`).format.wrapText = true;
candidates.getRange(`A1:${lastColumn}${lastRow}`).format.borders = {
  insideHorizontal: { style: "thin", color: "#EDF0F3" },
  bottom: { style: "thin", color: lightGray },
};
candidates.tables.add(`A1:${lastColumn}${lastRow}`, true, "R06AtomicCandidatesTable");
candidates.freezePanes.freezeRows(1);
candidates.freezePanes.freezeColumns(3);
const widths = [14, 9, 13, 58, 22, 20, 48, 70, 76, 22, 44, 42, 40, 48, 86, 24, 16, 76];
widths.forEach((width, index) => candidates.getRange(`${columnName(index)}:${columnName(index)}`).format.columnWidth = width);

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });
const inspections = [];
inspections.push(await workbook.inspect({ kind: "table", range: `Summary!A1:F${routeEnd}`, include: "values,formulas", tableMaxRows: 24, tableMaxCols: 6 }));
inspections.push(await workbook.inspect({ kind: "table", range: `Source Coverage!A1:F${coverageEnd}`, include: "values,formulas", tableMaxRows: 60, tableMaxCols: 6 }));
inspections.push(await workbook.inspect({ kind: "table", range: "Version Isolation!A1:M15", include: "values,formulas", tableMaxRows: 18, tableMaxCols: 13 }));
inspections.push(await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" }));
await fs.writeFile(path.join(qaDir, "inspect-summary.ndjson"), inspections.map((item) => item.ndjson).join("\n") + "\n", "utf8");

for (const [sheetName, range, fileName] of [
  ["Summary", `A1:F${routeEnd}`, "summary.png"],
  ["Source Coverage", `A1:F${coverageEnd}`, "source-coverage.png"],
  ["Version Isolation", "A1:M15", "version-isolation.png"],
  ["Candidates", "A1:S24", "candidates-top.png"],
  ["Candidates", `A${Math.max(1, lastRow - 23)}:S${lastRow}`, "candidates-bottom.png"],
]) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(path.join(qaDir, fileName), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
const outputPath = path.join(outputDir, "R06-atomic-candidates.xlsx");
await output.save(outputPath);
console.log(JSON.stringify({ rows: rows.length, columns: headers.length, output: outputPath }));
process.exit(0);
