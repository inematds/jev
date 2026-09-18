import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from jev_lab.core import ROOT, LabError, batch, evaluate, policy, validate_request, validate_response

class Contracts(unittest.TestCase):
    def setUp(self):
        self.cases=json.loads((ROOT/'app/cases.json').read_text())
        self.p=copy.deepcopy(self.cases[1]['request']); self.r=copy.deepcopy(self.cases[1]['fixture'])
    def test_all_ten_cases(self):
        self.assertEqual(len(self.cases),10)
        for c in self.cases: validate_response(c['request'],c['fixture'])
    def test_unknown_option(self):
        self.r['answers']['decisao']['choice']='transferir-dinheiro'
        with self.assertRaises(LabError):validate_response(self.p,self.r)
    def test_non_finite_and_wrong_distribution(self):
        for value in [float('nan'),float('inf'),-1,True,2]:
            r=copy.deepcopy(self.r);r['answers']['decisao']['confidence']=value
            with self.assertRaises(LabError):validate_response(self.p,r)
        self.r['answers']['decisao']['probabilities']['suporte']=.9
        with self.assertRaises(LabError):validate_response(self.p,self.r)
    def test_missing_answer_usage(self):
        for key in ['answers','usage']:
            r=copy.deepcopy(self.r);del r[key]
            with self.assertRaises(LabError):validate_response(self.p,r)
    def test_empty_request(self):
        for state in ['', '  ', None, {}, []]:
            self.p['state']=state
            with self.assertRaises(LabError):validate_request(self.p)
    def test_noul_and_score(self):
        p={'model':'test','state':'texto','questions':{'x':{'type':'noul','instructions':'sim?'}}}
        r={'model':'test','answers':{'x':{'type':'noul','noul':.05}},'usage':{'input_tokens':2,'output_tokens':1}}
        validate_response(p,r)
        p['questions']['x']={'type':'score','instructions':'nível?','criteria':['baixo','alto']}
        r['answers']['x']={'type':'score','score':.7,'probabilities':{'0':.3,'1':.7},'confidence':.5}
        validate_response(p,r)
        r['answers']['x']['score']=.2
        with self.assertRaises(LabError):validate_response(p,r)
    def test_sensitive_always_review(self):
        a=self.r['answers']['decisao'];a['confidence']=1
        self.assertEqual(policy(a,sensitive=True)['action'],'review')
        self.assertEqual(policy(a,threshold=.99)['action'],'suggest')
        self.assertEqual(policy(a,probability=.99)['action'],'review')
    def test_success_and_auth_header(self):
        def mock(req,timeout):
            self.assertEqual(req.get_header('Authorization'),'Bearer test-only')
            self.assertGreater(timeout,0)
            return io.BytesIO(json.dumps(self.r).encode())
        self.assertEqual(evaluate(self.p,key='test-only',opener=mock),self.r)
    def test_auth_error_is_not_retried_or_leaked(self):
        calls=[]
        def mock(req,timeout):
            calls.append(1);raise HTTPError(req.full_url,401,'secret-provider-message',{},None)
        with self.assertRaisesRegex(LabError,'HTTP 401') as c:evaluate(self.p,key='test-only',opener=mock)
        self.assertNotIn('secret',str(c.exception));self.assertEqual(len(calls),1)
    def test_long_retry_after_stops_without_wait(self):
        def mock(req,timeout):raise HTTPError(req.full_url,429,'busy',{'Retry-After':'99'},None)
        with self.assertRaisesRegex(LabError,'Retry-After'):evaluate(self.p,key='test-only',opener=mock)
    def test_retry_then_success(self):
        calls=[]
        def mock(req,timeout):
            calls.append(1)
            if len(calls)==1:raise HTTPError(req.full_url,529,'busy',{},None)
            return io.BytesIO(json.dumps(self.r).encode())
        evaluate(self.p,key='test-only',opener=mock);self.assertEqual(len(calls),2)
    def test_invalid_provider_json(self):
        with self.assertRaisesRegex(LabError,'JSON inválido'):evaluate(self.p,key='test-only',opener=lambda *a,**kw:io.BytesIO(b'<html>error</html>'))
    def test_batch_reports_real_errors(self):
        r=batch(ROOT/'data/tickets-sinteticos.jsonl')
        self.assertEqual(r['count'],24);self.assertLess(r['accuracy'],1);self.assertEqual(r['provider'],'regras-lexicais')
    def test_duplicate_id_not_silent(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.jsonl';p.write_text('\n'.join([json.dumps({'id':'1','text':'senha','label':'suporte'})]*2))
            with self.assertRaisesRegex(LabError,'duplicado'):batch(p)
if __name__=='__main__':unittest.main()
