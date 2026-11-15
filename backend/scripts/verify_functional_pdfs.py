"""Check every final fictional-policy fact and exact attachments; render all pages."""
import hashlib
import argparse
import json
from pathlib import Path
import re
import subprocess
from pypdf import PdfReader
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]


def normalize(value):
    return ' '.join(value.split())


def main():
    args=argparse.ArgumentParser()
    args.add_argument('--evidence-dir',default='evidence/functional-planning')
    output=(ROOT/args.parse_args().evidence_dir).resolve()
    if not output.is_relative_to(ROOT/'evidence'):
        raise ValueError('Evidence output must remain inside the repository evidence directory')
    results=[]
    for path in sorted((output/'pdfs').glob('*.pdf')):
        reader=PdfReader(path)
        report=json.loads(reader.attachments['validated-report.json'][0])
        assert reader.attachments['report.txt'][0]==report['export_text'].encode()
        assert report==json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
        assert report['report_format']=='FUNCTIONAL_DEMO_V1'
        assert not report['functional_plan']['clinical_authorized'] and not report['clinical_analysis_enabled']
        assert hashlib.sha256(report['parsed']['raw_text'].encode()).hexdigest()==report['planning_context']['source_sha256']==report['functional_plan']['source_sha256']
        assert len(report['engine_review']['evaluations'])==96
        assert sum(e['execution']=='DISABLED' for e in report['engine_review']['evaluations'])==27
        lines=[line for page in reader.pages for line in page.extract_text().splitlines()
            if line not in {'Finova AlignIQ','Synthetic demonstration review / DRAFT','Results continued'}
            and not line.startswith('DRAFT / NOT CLINICAL ADVICE') and not re.fullmatch(r'Page \d+ of \d+',line)
            and not re.match(r'^[a-f0-9]{12} \| \d{4}-\d{2}-\d{2} UTC$',line)]
        text=normalize(' '.join(lines))
        for f in report['analytical_findings']:
            assert normalize(f['text']) in text,(path.name,f['finding_id'])
        for section in report['sections']:
            assert normalize(section['title']) in text
        assert '{F0' not in text
        folder=output/'renders'/path.stem
        folder.mkdir(parents=True,exist_ok=True)
        for old in folder.glob('page-*.png'): old.unlink()
        subprocess.run(['pdftoppm','-scale-to','1100','-png',str(path),str(folder/'page')],check=True,capture_output=True)
        pages=[Image.open(p).convert('RGB') for p in sorted(folder.glob('page-*.png'))]
        width,height=max(p.width for p in pages),max(p.height for p in pages)
        sheet=Image.new('RGB',(width*min(2,len(pages)),(height+24)*((len(pages)+1)//2)),'#d9e2e1')
        draw=ImageDraw.Draw(sheet)
        for i,page in enumerate(pages):
            x,y=i%2*width,i//2*(height+24)
            draw.text((x+10,y+4),f'{path.name} page {i+1}',fill='black');sheet.paste(page,(x,y+24))
        sheet.save(folder/'contact.png')
        results.append(dict(file=path.name,pages=len(reader.pages),findings=len(report['analytical_findings']),exact_attachments=True,all_visible_facts=True))
    assert len(results)==6,'Expected three modules at desktop and mobile widths'
    (output/'pdf-verification.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
