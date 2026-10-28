from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

ROOT=Path(__file__).resolve().parent.parent
client=TestClient(app)

def test_all_new_sections_and_bilingual_navigation():
    for lang, direction in [('ar','rtl'),('en','ltr')]:
        page=client.get('/?lang='+lang)
        assert page.status_code==200
        assert f'dir="{direction}"' in page.text
        for name in ['links','tour','patterns','challenge','analyze','lab','bench','about']:
            assert f'id="view-{name}"' in page.text
            assert f'data-view="{name}"' in page.text
        for name in ['anatomy-output','wrm-pano','map-location-picks','learning-stops','pattern-grid','game-content','game-shields']:
            assert f'id="{name}"' in page.text
        assert '/static/v24-features.js?v=2.8.0' in page.text

def test_assets_and_preexisting_routes():
    for name in ['app.js','app-en.js','url-inspector.js','v24-features.js','styles.css']:
        resp=client.get('/static/'+name)
        assert resp.status_code==200
        assert len(resp.content)>500
    assert client.get('/api/health').json()['version']=='2.8.0'
    assert client.get('/api/benchmark').status_code==200
    assert client.post('/api/analyze',json={'message':'Send me your OTP now','locale':'en'}).status_code==200

def test_no_input_url_fetch_in_new_features():
    source=(ROOT/'frontend/v24-features.js').read_text()
    assert 'new URL(full)' in source
    assert 'wrm:url-analyzed' in source
    assert 'fetch(r.full)' not in source
    assert 'window.open(r.full)' not in source

def test_shields_and_correct_answer_feedback():
    source=(ROOT/'frontend/v24-features.js').read_text()
    assert 'shields:3' in source
    assert 'game.shields--' in source
    assert 'game.score+=100' in source
    assert 'game.answered=true' in source
