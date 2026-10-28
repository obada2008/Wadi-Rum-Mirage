"""Synthetic-template benchmark. No claim of real-world generalization."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from backend.engine.analyzer import analyze,normalize

def keyword_baseline(message):
    t=normalize(message)
    return bool(re.search(r'رمز\s*(?:التحقق|التاكيد)|\botp\b|كلمه\s*المرور|رسوم\s*التفعيل',t))

def score(pairs):
    pairs=list(pairs)
    tp=sum(pred and actual for actual,pred in pairs)
    tn=sum(not pred and not actual for actual,pred in pairs)
    fp=sum(pred and not actual for actual,pred in pairs)
    fn=sum(not pred and actual for actual,pred in pairs)
    precision=tp/(tp+fp) if tp+fp else 0
    recall=tp/(tp+fn) if tp+fn else 0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0
    return {'n':len(pairs),'tp':tp,'fp':fp,'tn':tn,'fn':fn,'precision':round(precision,4),'recall':round(recall,4),'f1':round(f1,4)}

def evaluate():
    data=json.loads((ROOT/'data/test_cases.json').read_text(encoding='utf8'))
    y=[(row['label']=='trust_transfer') for row in data]
    baseline=[keyword_baseline(row['message']) for row in data]
    model=[bool(analyze(row['message'])['trust_transfers']) for row in data]
    return {'warning':'In-sample synthetic templates, not independent validation; not a claim of AI model performance','task':'detect trust_transfer (not general phishing)','total':len(data),'keyword_baseline':score(zip(y,baseline)),'trust_graph_rules':score(zip(y,model)),'split':'No independent train/test split; fixed deterministic rules. Template variants are highly correlated.'}

if __name__=='__main__':
    out=evaluate();(ROOT/'docs/evaluation_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False,indent=2))
