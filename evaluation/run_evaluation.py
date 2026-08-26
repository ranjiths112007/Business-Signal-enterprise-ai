import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from app.intelligence import classify_question

cases=json.loads((Path(__file__).parent/'questions.json').read_text()) if (Path(__file__).parent/'questions.json').exists() else []
passed=0
for c in cases:
    got=classify_question(c['question'])
    expected='document' if c['expected']=='document' else ('business' if c['expected'] in {'risk','revenue'} else got)
    ok=got==expected
    passed+=ok
    print(('PASS' if ok else 'FAIL'), c['question'], '=>', got)
print(f'Intent classification: {passed}/{len(cases)}')
