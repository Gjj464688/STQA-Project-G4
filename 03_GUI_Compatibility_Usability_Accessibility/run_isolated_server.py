"""Serve unchanged PyTodo on localhost with a disposable temporary database."""
from pathlib import Path
import os,sys,hashlib,importlib.util,tempfile

source=Path(os.environ.get('PYTODO_SOURCE_DIR',Path(__file__).resolve().parents[2]/'pytodo_pro_student')).resolve()
if hashlib.sha256((source/'app.py').read_bytes()).hexdigest()!='050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f':
    raise RuntimeError('Application source differs from the recorded original')
sys.path.insert(0,str(source))
spec=importlib.util.spec_from_file_location('week3_target',source/'app.py')
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
temp_root=Path(__file__).resolve().parent/'.tmp';temp_root.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='pytodo-week34-',dir=temp_root) as work:
    module.DATABASE=str(Path(work)/'qa.sqlite3');module.init_db()
    module.app.run(host='127.0.0.1',port=int(os.environ.get('QA_PORT','5013')),debug=False,use_reloader=False)
