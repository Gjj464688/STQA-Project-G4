"""Load the original supplied app and isolate every case in a temporary DB."""
from pathlib import Path
import os,sys,hashlib,importlib.util
import pytest

EXPECTED='050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f'
SOURCE=Path(os.environ.get('PYTODO_SOURCE_DIR',Path(__file__).resolve().parents[3]/'pytodo_pro_student')).resolve()
if not (SOURCE/'app.py').is_file():
    raise RuntimeError('Set PYTODO_SOURCE_DIR to the original pytodo_pro_student folder')
if hashlib.sha256((SOURCE/'app.py').read_bytes()).hexdigest()!=EXPECTED:
    raise RuntimeError('Application version differs from the recorded original source')
sys.path.insert(0,str(SOURCE))
spec=importlib.util.spec_from_file_location('week4_target',SOURCE/'app.py')
flask_app=importlib.util.module_from_spec(spec)
spec.loader.exec_module(flask_app)

@pytest.fixture
def target(tmp_path,monkeypatch):
    monkeypatch.setattr(flask_app,'DATABASE',str(tmp_path/'test.sqlite3'))
    flask_app.app.config.update(TESTING=True,SECRET_KEY='isolated-qa')
    flask_app.init_db()
    return flask_app

@pytest.fixture
def client(target):
    return target.app.test_client()

@pytest.fixture
def authenticated_client(client):
    response=client.post('/api/register',json={'username':'qa_user','password':'TestPass123'})
    assert response.status_code==201
    return client
