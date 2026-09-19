import copy
import json
import tempfile
import unittest
from pathlib import Path
from jev_lab.core import LabError, validate_request, validate_response
from jev_lab.experiments import default_template, digest, run, save, compare

class Experiments(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.data=self.root/'items.jsonl'
        self.data.write_text('\n'.join(json.dumps(x) for x in [
            {'id':'a','text':'Cobrança duplicada','label':'cobranca'},
            {'id':'b','text':'Não sei quem resolve isso','label':'insuficiente'}]))
    def result(self,payload):
        options=payload['questions']['decisao']['criteria']
        return {'model':'modelo-controlado','answers':{'decisao':{'type':'choice','choice':'cobranca',
           'probabilities':{k:1.0 if k=='cobranca' else 0.0 for k in options},'confidence':.99}},
           'usage':{'input_tokens':100,'output_tokens':10}}
    def test_rules_no_fake_probabilities(self):
        report=run(self.data)
        self.assertEqual(report['metrics']['accuracy'],1)
        self.assertEqual(report['metrics']['coverage'],.5)
        self.assertIsNone(report['metrics']['brier'])
        self.assertTrue(all(r['probabilities'] is None for r in report['rows']))
    def test_budget_rejected_before_network(self):
        with self.assertRaisesRegex(LabError,'Orçamento'):run(self.data,provider='jev',max_calls=1,evaluator=lambda *a,**k:self.fail('network'))
    def test_failures_preserve_every_event_and_unknown_cost(self):
        def fail(*a,**k):raise LabError('Timeout')
        r=run(self.data,provider='jev',evaluator=fail)
        self.assertEqual(len(r['rows']),2);self.assertEqual(r['metrics']['accuracy'],0)
        self.assertEqual(r['metrics']['unknown_cost_observations'],2)
        self.assertFalse(r['metrics']['cost_complete'])
    def test_repeats_do_not_inflate_sample(self):
        r=run(self.data,repeats=3)
        self.assertEqual(r['metrics']['count'],2);self.assertEqual(r['metrics']['observations'],6)
        self.assertEqual(r['metrics']['repeat_label_agreement'],1)
    def test_retry_cost_remains_unknown(self):
        def ev(p,telemetry):telemetry.update(attempts=2);return self.result(p)
        r=run(self.data,provider='jev',evaluator=ev)
        self.assertEqual(r['metrics']['unknown_cost_observations'],2)
    def test_hybrid_only_unresolved_rule_calls_jev(self):
        calls=[]
        def ev(p,telemetry):calls.append(p);telemetry.update(attempts=1);return self.result(p)
        r=run(self.data,provider='hybrid',evaluator=ev)
        self.assertEqual(len(calls),1);self.assertEqual(r['rows'][0]['source'],'rules')
    def test_replay_hash_and_provenance(self):
        entries=[]
        for row in [json.loads(line) for line in self.data.read_text().splitlines()]:
            p=default_template();p['state']=row['text']
            entries.append({'id':row['id'],'request_sha256':digest(p),'response':self.result(p),
                            'origin':'simulation','latency_ms':None,'cost_usd':None})
        path=self.root/'replay.jsonl';path.write_text('\n'.join(json.dumps(r) for r in entries))
        report=run(self.data,provider='replay',replay=path)
        self.assertEqual(report['metrics']['accuracy'],.5)
        self.assertEqual(report['metrics']['brier'],1)
        self.assertTrue(all(r['source']=='replay-simulation' for r in report['rows']))
        entries[0]['request_sha256']='outro';path.write_text('\n'.join(json.dumps(r) for r in entries))
        self.assertEqual(run(self.data,provider='replay',replay=path)['metrics']['errors'],1)
    def test_replay_missing_event_rejected(self):
        path=self.root/'replay.jsonl';path.write_text(json.dumps({'id':'a'}))
        with self.assertRaisesRegex(LabError,'exatamente'):run(self.data,provider='replay',replay=path)
    def test_compare_requires_same_data(self):
        a=run(self.data);save(a,self.root/'a');b=copy.deepcopy(a);b['dataset_sha256']='different';save(b,self.root/'b')
        with self.assertRaisesRegex(LabError,'dataset'):compare([self.root/'a/report.json',self.root/'b/report.json'])
    def test_export_preserves_error_and_avoids_input_text(self):
        r=run(self.data);save(r,self.root/'out')
        self.assertNotIn('Cobrança duplicada',(self.root/'out/report.json').read_text())
        self.assertIn('expected',(self.root/'out/predictions.csv').read_text())
    def test_sensitive_rule_always_review(self):
        self.data.write_text(json.dumps({'id':'a','text':'cobrança','label':'cobranca','sensitive':True}))
        self.assertEqual(run(self.data)['metrics']['coverage'],0)
    def test_score_bounds_and_legend(self):
        p={'model':'test','state':'estado','questions':{'s':{'type':'score','instructions':'Gravidade?','criteria':['baixo','alto']}}}
        r={'model':'test','answers':{'s':{'type':'score','score':.5,'probabilities':{'0':.5,'1':.5},'confidence':.5}},'usage':{'input_tokens':1,'output_tokens':1}}
        with self.assertRaisesRegex(LabError,'legend'):validate_response(p,r)
        r['answers']['s']['legend']={'0':'baixo','1':'alto'};validate_response(p,r)
        r['answers']['s']['legend']['0']='outro'
        with self.assertRaisesRegex(LabError,'legend'):validate_response(p,r)
        p['questions']['s']['criteria']=['nível']*11
        with self.assertRaisesRegex(LabError,'2 a 10'):validate_request(p)
    def test_nonfinite_state_and_invalid_instructions(self):
        p=default_template();p['state']={'x':float('nan')}
        with self.assertRaises(LabError):validate_request(p)
        p['state']='texto';p['questions']['decisao']['instructions']=True
        with self.assertRaises(LabError):validate_request(p)

if __name__=='__main__':unittest.main()
