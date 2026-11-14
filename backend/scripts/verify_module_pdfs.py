"""Read-only PDF content checks plus Poppler render sheets; requires bundled pypdf/Pillow."""
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "evidence/module-final"


def normalized(value):
    return " ".join(value.split())


def main():
    results = []
    for folder in (OUTPUT / "pdfs", OUTPUT / "deployed"):
        for path in sorted(folder.glob("*.pdf")):
            reader = PdfReader(path)
            attachments = reader.attachments
            report = json.loads(attachments["validated-report.json"][0])
            assert attachments["report.txt"][0] == report["export_text"].encode("utf-8")
            assert hashlib.sha256(report["parsed"]["raw_text"].encode()).hexdigest() == report["parsed"]["raw_sha256"]
            assert len(report["engine_review"]["evaluations"]) == 96
            assert report["clinical_analysis_enabled"] is False
            assert report["illustrations"] == []
            text = normalized(" ".join(page.extract_text() for page in reader.pages))
            comments = report["sections"] or report["observations"]
            for comment in comments:
                assert normalized(comment["text"]) in text, (path.name, comment.get("section_id", comment.get("tooth_ref")))
            assert "Illustrative attachment examples" not in text and "Illustrative sequencing examples" not in text
            assert "not for clinical use" in text.lower()
            render = OUTPUT / "renders" / (folder.name + "-" + path.stem)
            render.mkdir(parents=True, exist_ok=True)
            subprocess.run(["pdftoppm", "-scale-to", "1200", "-png", str(path), str(render / "page")], check=True, capture_output=True)
            pages = [Image.open(p).convert("RGB") for p in sorted(render.glob("page-*.png"))]
            width, height = max(p.width for p in pages), max(p.height for p in pages)
            sheet = Image.new("RGB", (width * min(2, len(pages)), (height + 24) * ((len(pages) + 1) // 2)), "#d9e2e1")
            draw = ImageDraw.Draw(sheet)
            for i, page in enumerate(pages):
                x, y = (i % 2) * width, (i // 2) * (height + 24)
                draw.text((x + 10, y + 4), f"{path.name} - page {i + 1}", fill="black")
                sheet.paste(page, (x, y + 24))
            sheet.save(render / "contact.png")
            results.append(dict(file=str(path.relative_to(ROOT)).replace("\\", "/"), pages=len(reader.pages),
                                comments=len(comments), exact_attachments=True, source_positions=len(report["parsed"]["measurements"])))
    (OUTPUT / "pdf-verification.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results))


if __name__ == "__main__":
    main()
