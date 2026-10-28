from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_new_features_both_locales():
    for lang in ('ar','en'):
        r=client.get('/?lang='+lang)
        assert r.status_code==200
        text=r.text
        for id_ in ('view-case','case-analyze','case-export','auto-redact','manual-redact','graph-edges'):
            assert f'id="{id_}"' in text
        assert 'v27-experience.js?v=2.8.0' in text
        assert 'data-view="links"' in text and 'data-view="challenge"' in text
        assert 'data-view="case"' in text and 'data-view="academy"' not in text

def test_assets_and_api_regression():
    for name in ('v27-experience.js','styles.css','v24-features.js','url-inspector.js'):
        r=client.get('/static/'+name)
        assert r.status_code==200 and len(r.content)>100
    assert client.get('/api/health').json()['version']=='2.8.0'
    resp=client.post('/api/analyze',json={'message':'A government agency announced a new service. Enter OTP 123456.' ,'locale':'en-US','mode':'rules'})
    assert resp.status_code==200
    assert 'risk_score' in resp.json()

def test_no_broken_navigation_ids():
    from bs4 import BeautifulSoup
    for lang in ('ar','en'):
        soup=BeautifulSoup(client.get('/?lang='+lang).text,'html.parser')
        ids=[x.get('id') for x in soup.select('[id]')]
        assert len(ids)==len(set(ids))
        for nav in soup.select('#top-nav [data-view]'):
            assert soup.select_one('#view-'+nav['data-view']) is not None
