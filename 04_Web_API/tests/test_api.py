"""API specifications, explicit assumptions and parser observations.

Every record includes actual request/response data. Failing assertions are kept.
"""
import pytest

CASES=[
('API-01','categories',200),('API-02','unauth_tasks',401),
('API-03','register',201),('API-04','bad_username',400),('API-05','bad_password',400),
('API-06','login',200),('API-07','bad_login',401),('API-08','create',201),
('API-09','missing_title',400),('API-10','list',200),('API-11','get',200),
('API-12','get_missing',404),('API-13','update',200),('API-14','update_missing',404),
('API-15','unauth_dashboard',401),('API-16','dashboard',200),('API-17','dashboard_task',200),
('API-18','filter',200),('API-19','search',200),('API-20','page0',200),('API-21','page1',200),
('API-22','null_title',400),('API-23','spaces_title',400),('API-24','delete',200),
('API-25','delete_other',404),('API-26','delete_missing',404),
('API-27','bad_page',400),('API-28','bad_perpage',400),('API-29','negative_page',400),
('API-30','zero_perpage',400),('API-31','large_perpage',400),('API-32','integer_title',400),
('API-33','integer_description',400),('API-34','null_description',400),
('API-35','update_integer',400),('API-36','update_preserves_title',200),
('API-37','duplicate_username',201),('API-38','unauth_create',401),
('API-39','update_empty',400),('API-40','update_spaces',400),('API-41','partial_update',200),
('API-42','update_null',400),('API-43','nonnumeric_id',404),('API-44','negative_id',404),
('API-45','unsupported_collection',405),('API-46','unsupported_login',405),
('API-47','malformed',400),('API-48','text_plain',400),('API-49','invalid_date',400),
('API-50','list_after_invalid_date',200),('API-51','complete',200),
('API-52','get_other',404),('API-53','update_other',404),
]
ASSUMPTIONS={'delete_missing','bad_page','bad_perpage','negative_page','zero_perpage','large_perpage','integer_description','null_description','update_integer','update_preserves_title','update_empty','update_spaces'}
CHARACTERIZATION={'duplicate_username','nonnumeric_id','negative_id','malformed','text_plain'}

@pytest.mark.parametrize('case_id,scenario,expected_status',CASES,ids=[c[0] for c in CASES])
def test_api_case(case_id,scenario,expected_status,target,client,authenticated_client,request):
    auth=authenticated_client
    anonymous=target.app.test_client()
    r={'case_id':case_id,'scenario':scenario,'expected_status':expected_status,
       'basis':'Assumption' if scenario in ASSUMPTIONS else 'Characterization' if scenario in CHARACTERIZATION else 'Specification / robustness',
       'requests':[],'expected_body':None}
    request.node.qa_record=r
    def call(method,path,**kw):
        c=kw.pop('using',auth)
        trace={'method':method,'path':path,'input':kw,'authenticated':c is auth}
        r['requests'].append(trace)
        try:
            response=c.open(path,method=method,**kw)
            trace.update(status=response.status_code,json=response.get_json(silent=True),content_type=response.content_type)
            r.update(actual_status=response.status_code,actual_body=response.get_json(silent=True))
            return response
        except Exception as e:
            trace['exception']=f'{type(e).__name__}: {e}'
            r.update(actual_status=None,actual_body=trace['exception'])
            raise
    def seed(title='Original task',**kw):
        response=call('POST','/api/tasks',json={'title':title,**kw})
        assert response.status_code==201
        return response.get_json()['id']
    def check(response,body=None):
        r['expected_body']=body
        r.update(actual_status=response.status_code,actual_body=response.get_json(silent=True))
        assert response.status_code==expected_status
        if expected_status in {200,201,400,401}:assert response.is_json
        if body is not None:
            data=response.get_json()
            if isinstance(body,dict):
                for k,v in body.items():assert data[k]==v
            else:assert data==body
    s=scenario
    if s=='categories':
        response=call('GET','/api/categories',using=anonymous);check(response)
        assert {d['name'] for d in response.get_json()}=={'Work','Personal','Study','Urgent'}
    elif s.startswith('unauth_'):
        method,path,payload={'unauth_tasks':('GET','/api/tasks',None),'unauth_dashboard':('GET','/api/dashboard',None),'unauth_create':('POST','/api/tasks',{'title':'Auth check'})}[s]
        check(call(method,path,using=anonymous,**({'json':payload} if payload else {})),{'error':'authentication required'})
    elif s in {'register','bad_username','bad_password','duplicate_username'}:
        payload={'username':'new_user','password':'TestPass123'}
        if s=='bad_username':payload['username']='ab'
        if s=='bad_password':payload['password']='1234567'
        if s=='duplicate_username':payload['username']='qa_user'
        check(call('POST','/api/register',json=payload,using=anonymous),{'error':'invalid username' if s=='bad_username' else 'invalid password'} if s in {'bad_username','bad_password'} else {'username':payload['username']})
        if s=='duplicate_username':
            with target.app.app_context():assert target.get_db().execute('SELECT COUNT(*) FROM users WHERE username=?',('qa_user',)).fetchone()[0]==2
    elif s in {'login','bad_login'}:
        check(call('POST','/api/login',using=anonymous,json={'username':'qa_user','password':'WrongPassword' if s=='bad_login' else 'TestPass123'}),{'error':'invalid credentials'} if s=='bad_login' else {'username':'qa_user'})
    elif s in {'create','missing_title','null_title','spaces_title','integer_title','integer_description','null_description'}:
        payload={'title':'API created task'}
        if s=='missing_title':payload={}
        if s=='null_title':payload={'title':None}
        if s=='spaces_title':payload={'title':'   '}
        if s=='integer_title':payload={'title':123}
        if s=='integer_description':payload['description']=12345
        if s=='null_description':payload['description']=None
        check(call('POST','/api/tasks',json=payload))
        if s=='create':assert r['actual_body']['title']==payload['title']
    elif s in {'list','get','get_missing','update','update_missing','delete','delete_missing','complete','partial_update','update_integer','update_preserves_title','update_empty','update_spaces','update_null'}:
        task_id=seed()
        path=f'/api/tasks/{task_id}'
        if s=='list':check(call('GET','/api/tasks'));assert len(r['actual_body'])==1
        elif s=='get':check(call('GET',path),{'title':'Original task'})
        elif s=='get_missing':check(call('GET','/api/tasks/99999'),{'error':'not found'})
        elif s=='update_missing':check(call('PUT','/api/tasks/99999',json={'title':'Updated'}),{'error':'not found'})
        elif s=='delete':
            response=call('DELETE',path);assert call('GET',path).status_code==404
            check(response,{'result':'ok'})
        elif s=='delete_missing':check(call('DELETE','/api/tasks/99999'))
        elif s=='complete':check(call('PUT',path,json={'done':True}),{'done':True,'urgency':'Done'});assert r['actual_body']['completed_at']
        else:
            payload={'update':{'title':'Updated task'},'partial_update':{'description':'Description-only update'},'update_integer':{'title':12345},'update_preserves_title':{'title':12345},'update_empty':{'title':''},'update_spaces':{'title':'   '},'update_null':{'title':None}}[s]
            response=call('PUT',path,json=payload)
            if s=='update_preserves_title':
                after=call('GET',path);r['expected_body']={'title':'Original task'}
                assert after.get_json()['title']=='Original task'
            else:check(response,{'title':'Updated task'} if s=='update' else {'title':'Original task','description':'Description-only update'} if s=='partial_update' else None)
    elif s in {'dashboard','dashboard_task'}:
        if s=='dashboard_task':seed()
        check(call('GET','/api/dashboard'),{'total':int(s=='dashboard_task'),'open':int(s=='dashboard_task'),'overdue':0,'due_soon':0,'completed_this_week':0})
    elif s in {'filter','search','page0','page1'}:
        first=seed('First target');second=seed('Second target')
        if s=='filter':call('PUT',f'/api/tasks/{first}',json={'done':True});path='/api/tasks?status=done'
        elif s=='search':path='/api/tasks?q=First'
        else:path='/api/tasks?page='+('0' if s=='page0' else '1')+'&per_page=1'
        check(call('GET',path));assert len(r['actual_body'])==1
        assert r['actual_body'][0]['id']==(second if s=='page0' else first)
    elif s in {'bad_page','bad_perpage','negative_page','zero_perpage','large_perpage'}:
        seed();query={'bad_page':'page=abc','bad_perpage':'per_page=abc','negative_page':'page=-1','zero_perpage':'per_page=0','large_perpage':'per_page=1000000'}[s]
        check(call('GET','/api/tasks?'+query))
    elif s in {'delete_other','get_other','update_other'}:
        task_id=seed();other=target.app.test_client()
        other.post('/api/register',json={'username':'other_user','password':'TestPass123'})
        method={'delete_other':'DELETE','get_other':'GET','update_other':'PUT'}[s]
        response=call(method,f'/api/tasks/{task_id}',using=other,**({'json':{'title':'Stolen'}} if method=='PUT' else {}))
        with target.app.app_context():r['owner_record_exists']=target.get_db().execute('SELECT id FROM tasks WHERE id=?',(task_id,)).fetchone() is not None
        check(response)
    elif s in {'nonnumeric_id','negative_id','unsupported_collection','unsupported_login','malformed','text_plain'}:
        method,path,kw={'nonnumeric_id':('GET','/api/tasks/abc',{}),'negative_id':('GET','/api/tasks/-1',{}),'unsupported_collection':('PUT','/api/tasks',{}),'unsupported_login':('PUT','/api/login',{}),'malformed':('POST','/api/tasks',{'data':'{"title":','content_type':'application/json'}),'text_plain':('POST','/api/tasks',{'data':'title=Example','content_type':'text/plain'})}[s]
        check(call(method,path,**kw))
    elif s in {'invalid_date','list_after_invalid_date'}:
        try:response=call('POST','/api/tasks',json={'title':'Invalid Date Test','due_date':'not-a-date'})
        except ValueError:
            with target.app.app_context():r['invalid_record_persisted']=target.get_db().execute("SELECT COUNT(*) FROM tasks WHERE due_date='not-a-date'").fetchone()[0]
            if s=='invalid_date':raise
        if s=='invalid_date':check(response)
        else:check(call('GET','/api/tasks'))
    else:raise AssertionError('Unimplemented test scenario '+s)
