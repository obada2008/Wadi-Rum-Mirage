from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)
root=Path(__file__).resolve().parents[1]

def test_offline_scene_and_assets():
    r=client.get('/static/assets/wadi-rum-illustrated-panorama.svg')
    assert r.status_code==200 and b'<svg' in r.content
    script=client.get('/static/v24-features.js').text
    assert 'initPano()' in script and 'wrm-scene' in script
    assert 'window.pannellum' not in script
    assert 'power-cell' in script

def test_about_feature_inventory_both_languages():
    for lang in ('ar','en'):
        html=client.get('/?lang='+lang).text
        assert 'capability-grid' in html
        assert html.count('capability-item')==10
        assert 'power-bank' in html
        assert 'v=2.8.0' in html
