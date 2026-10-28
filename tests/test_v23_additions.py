from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parent.parent
client=TestClient(app)

def test_version_and_old_routes():
    assert client.get('/api/health').json()['version']=='2.8.0'
    assert client.get('/api/benchmark').status_code==200
    assert client.post('/api/analyze',json={'message':'لا تبعت رمز التحقق لأي شخص'}).status_code==200

def test_pages_and_direction():
    for lang,direction in [('ar','rtl'),('en','ltr')]:
        r=client.get('/?lang='+lang)
        assert r.status_code==200
        assert f'dir="{direction}"' in r.text
        assert 'data-view="links"' in r.text and 'data-view="tour"' in r.text
        assert 'id="url-input"' in r.text and 'id="url-report"' in r.text
        assert 'openstreetmap.org/export/embed.html' in r.text
        assert r.text.count('class="tour-stop"')==4
        assert '/static/url-inspector.js?v=2.8.0' in r.text

def test_static_assets():
    for name in ['styles.css','app.js','app-en.js','url-inspector.js']:
        r=client.get('/static/'+name)
        assert r.status_code==200 and len(r.content)>200

def test_new_top_nav_style():
    css=(ROOT/'frontend/styles.css').read_text()
    assert '.topbar-inner' in css and '.top-nav.open' in css
