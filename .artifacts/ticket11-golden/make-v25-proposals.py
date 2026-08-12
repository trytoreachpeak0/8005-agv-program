from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\szy\Desktop\8005---AGV")
BEFORE = ROOT / r"mes\ingest\csharp\MesIngest.Watch.UiTests\Baselines\SelectedUi"
AFTER = ROOT / r".artifacts\ticket11-golden\final-review-fixes-v25-stability\Candidate-run-1"
OUT = ROOT / r".artifacts\ticket11-golden\final-review-fixes-v25-stability\proposals"


def fit(image: Image.Image, width: int = 640) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


OUT.mkdir(parents=True, exist_ok=True)
rows: list[dict[str, object]] = []
font = ImageFont.load_default()

for after_path in sorted(AFTER.glob("*.received.png")):
    scenario = after_path.name.removesuffix(".received.png")
    before_path = BEFORE / f"{scenario}.verified.png"
    if not before_path.exists():
        raise FileNotFoundError(before_path)

    before = Image.open(before_path).convert("RGBA")
    after = Image.open(after_path).convert("RGBA")
    if before.size != after.size:
        raise ValueError(f"Size mismatch for {scenario}: {before.size} != {after.size}")

    raw_diff = ImageChops.difference(before, after)
    bbox = raw_diff.getbbox()
    changed = 0
    if bbox:
        changed = sum(1 for px in raw_diff.getdata() if px[:3] != (0, 0, 0))

    scenario_dir = OUT / scenario
    scenario_dir.mkdir(exist_ok=True)
    before.convert("RGB").save(scenario_dir / "before.png")
    after.convert("RGB").save(scenario_dir / "after.png")

    boosted = raw_diff.convert("RGB").point(lambda value: min(255, value * 4))
    boosted.save(scenario_dir / "diff.png")

    panels = [fit(before.convert("RGB")), fit(after.convert("RGB")), fit(boosted)]
    label_height = 28
    sheet = Image.new("RGB", (sum(p.width for p in panels), max(p.height for p in panels) + label_height), "white")
    x = 0
    for label, panel in zip(("BEFORE", "AFTER", "DIFF x4"), panels):
        sheet.paste(panel, (x, label_height))
        ImageDraw.Draw(sheet).text((x + 8, 8), label, fill="black", font=font)
        x += panel.width
    sheet.save(scenario_dir / "comparison.png")

    rows.append(
        {
            "scenario": scenario,
            "width": before.width,
            "height": before.height,
            "changed_pixels": changed,
            "changed_percent": f"{changed * 100 / (before.width * before.height):.4f}",
            "diff_bbox": "" if bbox is None else ",".join(map(str, bbox)),
        }
    )

with (OUT / "manifest.csv").open("w", newline="", encoding="utf-8-sig") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} proposals to {OUT}")
