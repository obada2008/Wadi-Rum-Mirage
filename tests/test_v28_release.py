from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)
root = Path(__file__).resolve().parent.parent
def test_clean_release_locales():
    for lang in ('ar','en'):
        t = client.get('/?lang='+lang).text
        assert 'id="theme-toggle"' not in t
        assert 'data-view="academy"' not in t
        assert 'id="view-academy"' not in t
        assert 'data-view="case"' in t
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(t,'html.parser')
        for b in soup.select('#top-nav .nav-item'):
            assert not b.find('span')
        assert len(soup.select('#top-nav .nav-item')) >= 8
def test_release_assets():
    js=(root/'frontend/v27-experience.js').read_text()
    assert "fetch('/static/v27-" not in js
    assert 'localStorage.setItem(themeKey' not in js
    css=(root/'frontend/styles.css').read_text()
    assert 'html[data-theme="light"]' not in css
    assert client.get('/api/health').json()['version']=='2.8.0'
