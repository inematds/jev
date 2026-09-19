import copy
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from jev_lab.core import LabError
from pacotes.integracao import carregar, fingerprint
from pacotes.lote import executar
from pacotes.qualidade import avaliar


class Flows(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.input=self.root/'events.jsonl'
        self.output=self.root/'results.jsonl'
        root,self.meta,self.request=carregar('reunioes')
        self.fixture=json.loads((root/'fixture.json').read_text())
        self.write_events([{'id':'a','state':self.request['state']},{'id':'b','state':'Outro texto fictício'}])

    def write_events(self,events):
        self.input.write_text(''.join(json.dumps(e)+'\n' for e in events))

    def run_batch(self,**kw):
        return executar('reunioes',self.input,self.output,interval=.1,**kw)

    def record(self):
        return {'id':'a','state':self.request['state'],'request_sha256':fingerprint(self.request),
                'expected':self.meta['expected_answers'],'response':copy.deepcopy(self.fixture),'origin':'simulation'}

    def test_preview_does_not_call_or_create_output(self):
        with patch('pacotes.lote.evaluate',side_effect=AssertionError('network')):
            r=self.run_batch()
        self.assertEqual(r['calls'],0)
        self.assertFalse(self.output.exists())

    def test_duplicate_or_invalid_later_event_prevents_all_calls(self):
        for events in [[{'id':'a','state':'ok'},{'id':'a','state':'ok'}],
                       [{'id':'a','state':'ok'},{'id':'b','state':''}]]:
            self.write_events(events)
            with patch('pacotes.lote.evaluate',side_effect=AssertionError('network')):
                with self.assertRaises(LabError):self.run_batch(live=True)
            self.assertFalse(self.output.exists())

    def test_concurrency_bound_and_resume(self):
        self.write_events([{'id':str(i),'state':'Evento fictício'} for i in range(4)])
        lock=threading.Lock();active=0;peak=0;calls=0
        def controlled(_):
            nonlocal active,peak,calls
            with lock:active+=1;peak=max(peak,active);calls+=1
            time.sleep(.16)
            with lock:active-=1
            return self.fixture
        result=self.run_batch(live=True,workers=2,evaluator=controlled)
        self.assertEqual(result['processed'],4)
        self.assertEqual(peak,2)
        resumed=self.run_batch(live=True,workers=2,evaluator=controlled)
        self.assertEqual(resumed['resumed'],4)
        self.assertEqual(calls,4)
        rows=[json.loads(x) for x in self.output.read_text().splitlines()]
        self.assertTrue(all(r['cost_usd'] is None for r in rows))
        self.assertTrue(all(r['result']['origin']=='controlled' for r in rows))
        self.assertNotIn('state',rows[0])

    def test_failure_is_checkpointed_as_review_not_retried_on_resume(self):
        def fail(_):raise LabError('Falha controlada')
        result=self.run_batch(live=True,evaluator=fail)
        self.assertEqual(result['new_errors'],2)
        self.assertEqual(self.run_batch(live=True,evaluator=fail)['processed'],0)
        row=json.loads(self.output.read_text().splitlines()[0])
        self.assertEqual(row['result']['action'],'review')
        self.assertIsNone(row['cost_usd'])

    def test_changed_input_or_provider_refuses_resume(self):
        self.run_batch(live=True,evaluator=lambda _:self.fixture,provider='typesafe')
        with self.assertRaisesRegex(LabError,'outro lote'):
            self.run_batch(live=True,evaluator=lambda _:self.fixture,provider='openrouter')
        self.write_events([{'id':'a','state':'alterado'}])
        with self.assertRaisesRegex(LabError,'outro lote'):
            self.run_batch(live=True,evaluator=lambda _:self.fixture)

    def test_lock_prevents_parallel_writer(self):
        self.output.with_suffix('.jsonl.lock').touch()
        with self.assertRaisesRegex(LabError,'lock'):
            self.run_batch(live=True,evaluator=lambda _:self.fixture)

    def test_retries_make_cost_unknown(self):
        def controlled(request,**kw):
            kw['telemetry']['attempts']=2
            return dict(self.fixture,usage={'input_tokens':10,'output_tokens':2,'cost':.001})
        with patch('pacotes.lote.evaluate',side_effect=controlled):self.run_batch(live=True)
        row=json.loads(self.output.read_text().splitlines()[0])
        self.assertEqual(row['attempts'],2)
        self.assertIsNone(row['cost_usd'])

    def test_partial_checkpoint_is_refused(self):
        self.output.write_text('{')
        with self.assertRaises(ValueError):self.run_batch(live=True,evaluator=lambda _:self.fixture)

    def test_quality_failure_stays_in_denominator(self):
        good=self.record();bad=self.record();bad.update(id='b',response={})
        report=avaliar(self.request,[good,bad])
        q=report['questions']['decisao']
        self.assertEqual(q['accuracy_all'],.5)
        self.assertEqual(q['coverage'],.5)
        self.assertEqual(q['errors'],1)
        self.assertAlmostEqual(report['questions']['tem_decisao']['brier'],.0009)

    def test_quality_requires_all_labels_hash_and_origin(self):
        for mutate in [lambda r:r['expected'].pop('tem_decisao'),
                       lambda r:r.update(request_sha256='old'),lambda r:r.update(origin='unknown'),
                       lambda r:r['expected'].update(tem_decisao='yes')]:
            r=copy.deepcopy(self.record());mutate(r)
            with self.assertRaises(LabError):avaliar(self.request,[r])

    def test_quality_score_uses_scale_error(self):
        root,meta,request=carregar('cortes')
        fixture=json.loads((root/'fixture.json').read_text())
        row={'id':'x','state':request['state'],'request_sha256':fingerprint(request),
             'expected':meta['expected_answers'],'response':fixture,'origin':'simulation'}
        q=avaliar(request,[row])['questions']['clareza_textual']
        self.assertAlmostEqual(q['mae'],.06)
        self.assertAlmostEqual(q['normalized_mae'],.03)
        row['expected']['clareza_textual']=100
        with self.assertRaises(LabError):avaliar(request,[row])


if __name__=='__main__':unittest.main()
