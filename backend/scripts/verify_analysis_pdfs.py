"""Read-only content/attachment checks and complete page renders of test PDFs."""
import hashlib
import argparse
import json
import re
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "evidence/analysis-pipeline"


def normalized(value):
    return " ".join(value.split())


def main():
    global OUTPUT
    args = argparse.ArgumentParser()
    args.add_argument("--output", default="evidence/analysis-pipeline")
    OUTPUT = (ROOT / args.parse_args().output).resolve()
    if not OUTPUT.is_relative_to(ROOT):
        raise ValueError("OUTPUT_OUTSIDE_PROJECT")
    results = []
    for path in sorted((OUTPUT / "pdfs").glob("*.pdf")):
        reader = PdfReader(path)
        report = json.loads(reader.attachments["validated-report.json"][0])
        assert reader.attachments["report.txt"][0] == report["export_text"].encode()
        assert report["report_format"] == "ANALYTICAL_V1"
        assert len(report["parsed"]["measurements"]) == 105
        assert len(report["parsed"]["teeth"]) == 15
        assert hashlib.sha256(report["parsed"]["raw_text"].encode()).hexdigest() == report["parsed"]["raw_sha256"]
        assert len(report["engine_review"]["evaluations"]) == 96 and not report["clinical_analysis_enabled"]
        # Page furniture can interrupt a section across page boundaries. Remove
        # only the renderer's repeated header/footer, retaining all report prose.
        lines = [line for page in reader.pages for line in page.extract_text().splitlines()
                 if line not in {"Finova AlignIQ", "Synthetic demonstration review / DRAFT"}
                 and not line.startswith("DRAFT / NOT CLINICAL ADVICE")
                 and not re.fullmatch(r"Page \d+ of \d+", line)
                 and not re.match(r"^[a-f0-9]{12} \| \d{4}-\d{2}-\d{2} UTC$", line)]
        visible = normalized(" ".join(lines))
        for section in report["sections"]:
            assert normalized(section["title"]) in visible
            assert normalized(section["text"]) in visible, (path.name, section["section_id"])
        assert "{F0" not in visible and "original tooth token" not in visible
        assert "Synthetic demonstration" in visible
        render = OUTPUT / "renders" / path.stem
        render.mkdir(parents=True, exist_ok=True)
        for previous in render.glob("page-*.png"):
            previous.unlink()
        subprocess.run(["pdftoppm", "-scale-to", "1100", "-png", str(path), str(render / "page")], check=True, capture_output=True)
        pages = [Image.open(p).convert("RGB") for p in sorted(render.glob("page-*.png"))]
        width, height = max(p.width for p in pages), max(p.height for p in pages)
        sheet = Image.new("RGB", (width * min(2, len(pages)), (height+24)*((len(pages)+1)//2)), "#d9e2e1")
        draw = ImageDraw.Draw(sheet)
        for i, page in enumerate(pages):
            x, y = i % 2 * width, i // 2 * (height+24)
            draw.text((x+10, y+4), f"{path.name} page {i+1}", fill="black")
            sheet.paste(page, (x, y+24))
        sheet.save(render / "contact.png")
        results.append(dict(file=path.name, pages=len(reader.pages), sections=len(report["sections"]),
            exact_attachments=True, all_visible_findings=True, positions=105))
    assert len(results) == 6, "Expected three modules at desktop and mobile widths"
    (OUTPUT / "pdf-verification.json").write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
