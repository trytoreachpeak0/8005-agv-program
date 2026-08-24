import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = process.argv[2];
if (!repoRoot) throw new Error("Usage: node build_r11_review_workbook.mjs <repo-root>");

const artifactDir = path.join(repoRoot, ".scratch", "current-requirements-baseline", "evidence", "atomic-candidates");
const candidatePath = path.join(artifactDir, "R11-atomic-candidates.tsv");
const summaryPath = path.join(artifactDir, "R11-atomic-candidates-summary.json");
const outputDir = path.join(repoRoot, "outputs", "019fcb0c-7791-7be3-89bf-b9b5ab964b02");
const qaDir = path.join(artifactDir, "qa-xlsx-r11");

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

const raw = parseDelimited(await fs.readFile(candidatePath, "utf8"));
const summaryData = JSON.parse(await fs.readFile(summaryPath, "utf8"));
const headers = raw[0];
const rows = raw.slice(1);
if (headers.length !== 18 || rows.length !== summaryData.total || summaryData.source_documents !== 6) {
  throw new Error(`Unexpected R11 ledger shape: rows=${rows.length} cols=${headers.length} sources=${summaryData.source_documents}`);
}

const asExcelText = (value) => (typeof value === "string" && value.startsWith("=") ? `'${value}` : value);
const candidateData = [headers, ...rows.map((row) => row.map(asExcelText))];
const lastRow = rows.length + 1;
const lastColumn = columnName(headers.length - 1);
const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const coverage = workbook.worksheets.add("Source Coverage");
const pointers = workbook.worksheets.add("Evidence Pointers");
const candidates = workbook.worksheets.add("Candidates");
for (const sheet of [summary, coverage, pointers, candidates]) sheet.showGridLines = false;

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
summary.getRange("A1").values = [["R11 MES 数据、查询与工厂验证原子候选审阅"]];
summary.getRange("A1:F1").format = {
  fill: navy,
  font: { name: "Aptos Display", size: 18, bold: true, color: "#FFFFFF" },
  rowHeight: 34,
  verticalAlignment: "center",
};
summary.mergeCells("A2:F2");
summary.getRange("A2").values = [["候选分类，不是批准；查询运行授权、run 观察、需求批准与长期验收结论彼此独立。"]];
summary.getRange("A2:F2").format = { fill: paleAmber, font: { ...bodyFont, italic: true }, rowHeight: 32, wrapText: true };

summary.getRange("A4:B12").values = [
  ["指标", "值"],
  ["全部原子记录", null],
  ["来源文档", null],
  ["文档级排除（未抽取）", summaryData.excluded_batch_documents_not_extracted],
  ["PACKAGE 容量规则", null],
  ["精确容量规则", summaryData.capacity_exact_rules],
  ["前缀容量规则", summaryData.capacity_prefix_rules],
  ["精确重复后出现记录", summaryData.exact_duplicate_rows],
  ["批准升级", null],
];
summary.getRange("B5").formulas = [[`=COUNTA('Candidates'!$A$2:$A$${lastRow})`]];
summary.getRange("B6").formulas = [["=COUNTA('Source Coverage'!$A$2:$A$7)"]];
summary.getRange("B8").formulas = [[`=COUNTIF('Candidates'!$C$2:$C$${lastRow},"R11-09")`]];
summary.getRange("B12").formulas = [[`=COUNTIF('Candidates'!$Q$2:$Q$${lastRow},"<>not-approved")`]];
summary.getRange("A4:B4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:A12").format = { fill: paleBlue, font: { ...bodyFont, bold: true } };
summary.getRange("B5:B12").format = { font: { ...bodyFont, bold: true }, numberFormat: "#,##0" };
summary.getRange("A4:B12").format.borders = { preset: "outside", style: "thin", color: lightGray };

const routes = Object.keys(summaryData.by_route).sort();
const routeEnd = 15 + routes.length;
summary.getRange(`A15:B${routeEnd}`).values = [["处置路线", "数量"], ...routes.map((route) => [route, null])];
for (let row = 16; row <= routeEnd; row += 1) {
  summary.getRange(`B${row}`).formulas = [[`=COUNTIF('Candidates'!$N$2:$N$${lastRow},A${row})`]];
}
summary.getRange("A15:B15").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange(`A16:B${routeEnd}`).format = { font: bodyFont, wrapText: true };
summary.getRange(`B16:B${routeEnd}`).format.numberFormat = "#,##0";
summary.getRange(`A15:B${routeEnd}`).format.borders = { preset: "outside", style: "thin", color: lightGray };

const pointerEntries = Object.entries(summaryData.pointer_definitions);
const pointerEnd = 4 + pointerEntries.length;
summary.getRange(`D4:F${pointerEnd}`).values = [["决定/证据指针", "命中", "含义"], ...pointerEntries.map(([pointer, meaning]) => [pointer, null, meaning])];
for (let row = 5; row <= pointerEnd; row += 1) summary.getRange(`E${row}`).formulas = [[`='Evidence Pointers'!C${row}`]];
summary.getRange("D4:F4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" } };
summary.getRange(`D5:F${pointerEnd}`).format = { font: bodyFont, wrapText: true, verticalAlignment: "top" };
summary.getRange(`D5:D${pointerEnd}`).format.fill = paleBlue;
summary.getRange(`E5:E${pointerEnd}`).format.numberFormat = "#,##0";
summary.getRange(`D4:F${pointerEnd}`).format.borders = { preset: "outside", style: "thin", color: lightGray };
summary.getRange("A:A").format.columnWidth = 64;
summary.getRange("B:B").format.columnWidth = 14;
summary.getRange("C:C").format.columnWidth = 5;
summary.getRange("D:D").format.columnWidth = 18;
summary.getRange("E:E").format.columnWidth = 12;
summary.getRange("F:F").format.columnWidth = 70;
summary.freezePanes.freezeRows(2);

const sourceRows = Object.entries(summaryData.by_source).map(([recordId, count]) => {
  const first = rows.find((row) => row[2] === recordId);
  return [recordId, first?.[3] ?? "", first?.[4] ?? "", count, null, null];
});
const coverageEnd = sourceRows.length + 1;
coverage.getRange(`A1:F${coverageEnd}`).values = [["来源记录", "路径", "SHA-256", "预期记录数", "实际记录数", "对账"], ...sourceRows];
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
coverage.getRange("B:B").format.columnWidth = 78;
coverage.getRange("C:C").format.columnWidth = 70;
coverage.getRange("D:F").format.columnWidth = 15;
coverage.freezePanes.freezeRows(1);

pointers.mergeCells("A1:E1");
pointers.getRange("A1").values = [["R11 查询授权、限定观察、容量证据与跨批次边界"]];
pointers.getRange("A1:E1").format = { fill: navy, font: { name: "Aptos Display", size: 17, bold: true, color: "#FFFFFF" }, rowHeight: 32 };
pointers.mergeCells("A2:E2");
pointers.getRange("A2").values = [["指针保存复核上下文；run 完成、勾选状态和内部 query README 都不构成当前需求批准。"]];
pointers.getRange("A2:E2").format = { fill: paleAmber, font: { ...bodyFont, italic: true }, rowHeight: 30, wrapText: true };
const pointerSheetEnd = 4 + pointerEntries.length;
pointers.getRange(`A4:E${pointerSheetEnd}`).values = [["指针", "类型", "命中数", "含义", "处理边界"], ...pointerEntries.map(([pointer, meaning]) => [
  pointer,
  pointer.startsWith("RES-") ? "resolved-decision" : pointer.startsWith("EVID-") ? "bounded-evidence" : pointer.startsWith("CF-") ? "cross-batch-conflict" : pointer.startsWith("GAP-") ? "evidence-gap" : "scope-or-governance-boundary",
  summaryData.pointer_counts[pointer] ?? 0,
  meaning,
  "保留到跨批次去重与批准批次；不得由运行授权、单次 run、迁移 CSV 或内部设计反推批准",
])];
pointers.getRange("A4:E4").format = { fill: teal, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, wrapText: true };
pointers.getRange(`A5:E${pointerSheetEnd}`).format = { font: bodyFont, wrapText: true, verticalAlignment: "top" };
pointers.getRange(`C5:C${pointerSheetEnd}`).format.numberFormat = "#,##0";
pointers.getRange(`A4:E${pointerSheetEnd}`).format.borders = { preset: "outside", style: "thin", color: lightGray };
pointers.getRange("A:A").format.columnWidth = 18;
pointers.getRange("B:B").format.columnWidth = 24;
pointers.getRange("C:C").format.columnWidth = 12;
pointers.getRange("D:D").format.columnWidth = 76;
pointers.getRange("E:E").format.columnWidth = 76;
pointers.freezePanes.freezeRows(4);

candidates.getRange(`A1:${lastColumn}${lastRow}`).values = candidateData;
candidates.getRange(`A1:${lastColumn}1`).format = { fill: navy, font: { ...bodyFont, bold: true, color: "#FFFFFF" }, rowHeight: 30, wrapText: true };
candidates.getRange(`A2:${lastColumn}${lastRow}`).format = { font: bodyFont, verticalAlignment: "top" };
candidates.getRange(`G2:I${lastRow}`).format.wrapText = true;
candidates.getRange(`K2:R${lastRow}`).format.wrapText = true;
candidates.getRange(`A1:${lastColumn}${lastRow}`).format.borders = {
  insideHorizontal: { style: "thin", color: "#EDF0F3" },
  bottom: { style: "thin", color: lightGray },
};
candidates.tables.add(`A1:${lastColumn}${lastRow}`, true, "R11AtomicCandidatesTable");
candidates.getRange(`N2:N${lastRow}`).conditionalFormats.add("containsText", { text: "exclude-from-requirement-approval", format: { fill: paleBlue, font: { color: navy } } });
candidates.getRange(`N2:N${lastRow}`).conditionalFormats.add("containsText", { text: "limited-environment-observation", format: { fill: paleTeal, font: { color: "#0F5132" } } });
candidates.getRange(`N2:N${lastRow}`).conditionalFormats.add("containsText", { text: "historical-governance", format: { fill: paleAmber, font: { color: "#7A4E00" } } });
candidates.getRange(`Q2:Q${lastRow}`).conditionalFormats.add("notContainsText", { text: "not-approved", format: { fill: paleRed, font: { bold: true, color: "#9B1C1C" } } });
candidates.freezePanes.freezeRows(1);
candidates.freezePanes.freezeColumns(3);
const widths = [14, 9, 13, 64, 22, 20, 54, 78, 84, 22, 54, 56, 52, 62, 88, 32, 16, 92];
widths.forEach((width, index) => { candidates.getRange(`${columnName(index)}:${columnName(index)}`).format.columnWidth = width; });

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(qaDir, { recursive: true });
const inspections = [];
inspections.push(await workbook.inspect({ kind: "table", range: `Summary!A1:F${Math.max(routeEnd, pointerEnd)}`, include: "values,formulas", tableMaxRows: 40, tableMaxCols: 6 }));
inspections.push(await workbook.inspect({ kind: "table", range: `Source Coverage!A1:F${coverageEnd}`, include: "values,formulas", tableMaxRows: 10, tableMaxCols: 6 }));
inspections.push(await workbook.inspect({ kind: "table", range: `Evidence Pointers!A1:E${pointerSheetEnd}`, include: "values,formulas", tableMaxRows: 20, tableMaxCols: 5 }));
inspections.push(await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" }));
await fs.writeFile(path.join(qaDir, "inspect-summary.ndjson"), inspections.map((item) => item.ndjson).join("\n") + "\n", "utf8");

for (const [sheetName, range, fileName] of [
  ["Summary", `A1:F${Math.max(routeEnd, pointerEnd)}`, "summary.png"],
  ["Source Coverage", `A1:F${coverageEnd}`, "source-coverage.png"],
  ["Evidence Pointers", `A1:E${pointerSheetEnd}`, "evidence-pointers.png"],
  ["Candidates", "A1:R24", "candidates-top.png"],
  ["Candidates", `A${Math.max(1, lastRow - 23)}:R${lastRow}`, "candidates-bottom.png"],
]) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(path.join(qaDir, fileName), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
const outputPath = path.join(outputDir, "R11-atomic-candidates.xlsx");
await output.save(outputPath);
console.log(JSON.stringify({ rows: rows.length, columns: headers.length, output: outputPath }));
process.exit(0);
