from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from backend.engine.analyzer import analyze
from backend.engine.explain import build_report

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title='Wadi Rum Mirage', version='2.8.0', description='Arabic trust transfer analysis — local demo')
app.mount('/static', StaticFiles(directory=ROOT/'frontend'), name='static')

class AnalysisRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    locale: str = 'ar-JO'
    mode: str = 'rules'

@app.get('/')
def index(request: Request):
    lang = request.query_params.get('lang', 'ar')
    return FileResponse(ROOT/'frontend'/('index-en.html' if lang.lower().startswith('en') else 'index.html'))

@app.get('/api/health')
def health():
    return {'status':'ok','version':'2.8.0','mode':'offline-rules'}

@app.post('/api/analyze')
def analyze_route(payload: AnalysisRequest):
    try:
        if payload.mode != 'rules':
            raise HTTPException(status_code=400, detail='Only rules mode is supported in v0.1')
        report = build_report(analyze(payload.message), payload.message)
        if payload.locale.lower().startswith('en'):
            from backend.engine.locale import localize
            return localize(report)
        return report
    except ValueError as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

@app.get('/api/examples')
def examples(request: Request):
    if request.query_params.get('lang', '').lower().startswith('en'):
        return [
            {'title':'Trust transfer','message':'A government agency announced a new online service. Therefore activate your account at https://example.invalid/verify and enter your OTP.'},
            {'title':'Safety advice','message':'Never share your verification code with anyone. Visit the official website yourself.'},
            {'title':'Insufficient evidence','message':'I heard about a new government service but have no official details.'},
            {'title':'Payment pressure','message':'Government agency: You must pay an activation fee immediately or your account will be suspended.'}
        ]
    return [
        {'title':'محاولة نقل ثقة','message':'أعلنت مؤسسة رسمية عن خدمة جديدة، ولهيك فعّل حسابك من الرابط https://example.invalid/verify وأدخل رمز التحقق OTP.'},
        {'title':'رسالة توعوية','message':'لا تبعت رمز التحقق لأي شخص. راجع الموقع الرسمي للمؤسسة بنفسك.'},
        {'title':'معلومات غير كافية','message':'سمعت عن خدمة جديدة في مؤسسة حكومية، لكن ما عندي تفاصيل رسمية.'},
        {'title':'ضغط مالي','message':'مؤسسة حكومية: لازم تدفع رسوم التفعيل فورا عشان ما يتم إيقاف حسابك.'}
    ]

@app.get('/api/rules')
def rules():
    return {'mode':'offline-rules','ids':['R01','R02','R03','R04','R05','R06'],'note':'Rules are heuristic, not a guarantee of safety.'}

@app.get('/api/project')
def project():
    return {'name':'Wadi Rum Mirage','version':'2.8.0','privacy':'No message persistence or external requests','ai_mode':'Rule-based, explainable; no trained AI claim','heritage':'https://whc.unesco.org/en/list/1377'}

@app.get('/api/benchmark')
def benchmark():
    import json
    path = ROOT / 'docs' / 'evaluation_results.json'
    return json.loads(path.read_text(encoding='utf-8'))

@app.get('/api/diagnostics')
def diagnostics():
    css = ROOT / 'frontend' / 'styles.css'
    js = ROOT / 'frontend' / 'app.js'
    return {'version':'2.8.0','css_present':css.is_file(),'css_bytes':css.stat().st_size if css.is_file() else 0,'js_present':js.is_file(),'js_bytes':js.stat().st_size if js.is_file() else 0,'expected_base':'http://127.0.0.1:8765'}
