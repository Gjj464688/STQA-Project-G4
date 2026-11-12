"""Run isolated API cases and retain the complete machine-readable evidence."""
from pathlib import Path
from datetime import datetime,timezone
import sys,os,json,subprocess,hashlib,platform,uuid
ROOT=Path(__file__).resolve().parent

class Recorder:
    def __init__(self):self.rows=[]
    def pytest_runtest_makereport(self,item,call):
        if call.when=='setup' and call.excinfo:
            self.rows.append({'case_id':item.callspec.params.get('case_id',item.nodeid),'status':'Error','failure':str(call.excinfo.value)})
        if call.when=='call':
            r=dict(getattr(item,'qa_record',{'case_id':item.nodeid}))
            r.update(status='Fail' if call.excinfo else 'Pass',node_id=item.nodeid)
            if call.excinfo:r['failure']=str(call.excinfo.value)
            self.rows.append(r)

def main():
    os.chdir(ROOT);out=ROOT/'Evidence'/'verified';out.mkdir(parents=True,exist_ok=True)
    if '--worker' not in sys.argv:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
        with (out/'api_pytest.txt').open('w',encoding='utf-8') as stream:
            proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker'],env=env,stdout=stream,stderr=subprocess.STDOUT)
        print((out/'api_pytest.txt').read_text(encoding='utf-8'))
        return proc.returncode
    import pytest
    from importlib.metadata import version
    sys.path.insert(0,str(ROOT/'tests'))
    from conftest import SOURCE,flask_app
    before={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.rglob('*') if p.is_file() and p.suffix in {'.py','.html','.css'} and not any(x in p.parts for x in ['venv','.venv','__pycache__'])}
    started=datetime.now(timezone.utc).isoformat();rec=Recorder();(ROOT/'.tmp').mkdir(exist_ok=True)
    exit_code=pytest.main(['tests/test_api.py','-v','--tb=short','-p','no:cacheprovider',f'--basetemp={ROOT/".tmp"/str(uuid.uuid4())}',f'--junitxml={out/"api_junit.xml"}'],plugins=[rec])
    after={key:hashlib.sha256((SOURCE/key).read_bytes()).hexdigest() for key in before}
    if before!=after:raise RuntimeError('Original application source changed during execution')
    data={'started_utc':started,'python':platform.python_version(),'platform':platform.platform(),'pytest':version('pytest'),'flask':version('Flask'),'source_directory':str(SOURCE),'source_hashes':before,'source_unchanged':True,'execution':'Agent-executed verification; original manual tester identity not recorded','exit_code':int(exit_code),'counts':{s:sum(x['status']==s for x in rec.rows) for s in ['Pass','Fail','Error']},'results':rec.rows}
    (out/'api_results.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    routes=[{'path':r.rule,'methods':sorted(r.methods)} for r in flask_app.app.url_map.iter_rules()]
    (out/'route_map.json').write_text(json.dumps(routes,indent=2),encoding='utf-8')
    print('RECORDED',data['counts'])
    return int(exit_code)

if __name__=='__main__':sys.exit(main())
