from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_health():
    assert client.get('/api/health').json()['status']=='ok'

def test_api_analysis():
    r=client.post('/api/analyze',json={'message':'ارسل رمز التحقق OTP الآن'})
    assert r.status_code==200
    assert r.json()['status']=='warning'

def test_api_rejects_empty():
    assert client.post('/api/analyze',json={'message':''}).status_code==422

def test_api_rejects_unsupported_mode():
    assert client.post('/api/analyze',json={'message':'test','mode':'ai'}).status_code==400
