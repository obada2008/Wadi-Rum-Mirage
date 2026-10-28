from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
C=TestClient(app)
ROOT=Path(__file__).resolve().parents[1]
def test_two_languages_topbar():
    for lang in ('ar','en'):
        h=C.get('/?lang='+lang).text
        assert 'id="top-nav"' in h and 'id="menu"' in h
        assert 'class="sidebar"' not in h
        assert 'من هون أنا' not in h and '#من_هون_أنا' not in h and '#From_Here_I_Am' not in h
        for name in ('home','analyze','lab','bench','links','tour','patterns','challenge','about'):
            assert 'data-view="'+name+'"' in h
def test_frontend_mobile_assets():
    css=C.get('/static/styles.css').text
    assert '@media(max-width:1190px)' in css and '.top-nav.open' in css
    for name in ('app.js','app-en.js'):
        js=C.get('/static/'+name).text
        assert "$('top-nav')" in js
