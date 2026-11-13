"""Build original synthetic source/gold WITHOUT importing or invoking extraction."""
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.parser.contracts import SyntheticFixture  # noqa: E402
from app.parser.generated import generate  # noqa: E402

root=Path(__file__).resolve().parents[2]
records=[]
for recipe in SyntheticFixture.model_fields['recipe'].annotation.__args__:
    for seed in (0,1,2,3,7,17):
        identity=SyntheticFixture(recipe=recipe,seed=seed); sample=generate(identity)
        records.append({'identity':identity.model_dump(),'category':sample.category,'raw_text':sample.raw_text,'gold':sample.gold})
(root/'examples/phase4-synthetic-dataset.json').write_text(json.dumps({
    'kind':'ORIGINAL_SYNTHETIC_NOT_VENDOR_EVIDENCE','gold_method':'Independent original source construction: labels, Decimal strings and offsets declared before parsing',
    'fixtures':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sample=next(r for r in records if r['identity']=={'recipe':'wrapped','seed':0})
(root/'frontend/src/phase4Example.json').write_text(json.dumps({'identity':sample['identity'],'raw_text':sample['raw_text']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('SYNTHETIC_DATASET_BUILT: 78 original fixtures; no parser or network used.')
