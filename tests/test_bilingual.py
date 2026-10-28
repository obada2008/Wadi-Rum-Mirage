from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_ar_en_page_and_assets():
    assert 'lang="ar"' in client.get('/?lang=ar').text
    assert 'lang="en"' in client.get('/?lang=en').text
    assert client.get('/static/app-en.js').status_code == 200
    assert 'Mirage Lab' in client.get('/?lang=en').text

def test_english_trust_transfer():
    data=client.post('/api/analyze',json={'message':'An official government agency announced a new service. Therefore enter your OTP at https://example.invalid/verify immediately.', 'locale':'en-US'}).json()
    assert data['status']=='warning'
    assert any(x['id']=='R05' for x in data['rules'])
    assert 'Elevated risk' in data['title']
    assert 'Claim / mentioned organization' in [x['label'] for x in data['graph']['nodes']]

def test_english_warning_not_false_positive():
    data=client.post('/api/analyze',json={'message':'Never share your OTP with anyone.','locale':'en-US'}).json()
    assert data['status']=='no_indicators'

def test_english_payment_pressure():
    data=client.post('/api/analyze',json={'message':'Government agency: Pay the activation fee immediately.','locale':'en-US'}).json()
    assert data['status'] in ('warning','caution')
    assert 'R03' in [r['id'] for r in data['rules']]

def test_english_examples():
    data=client.get('/api/examples?lang=en').json()
    assert len(data)==4 and 'agency' in data[0]['message']
