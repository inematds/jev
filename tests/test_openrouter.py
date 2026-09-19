import copy
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from jev_lab.core import ROOT, MODEL, OPENROUTER_MODEL, LabError, evaluate, load_key, validate_response
from pacotes.integracao import avaliar_area


class OpenRouter(unittest.TestCase):
    def setUp(self):
        self.environment=patch.dict(os.environ,{},clear=True);self.environment.start();self.addCleanup(self.environment.stop)
        case=json.loads((ROOT/'app/cases.json').read_text())[1]
        self.p=copy.deepcopy(case['request']);self.r=copy.deepcopy(case['fixture'])
        self.r['model']='typesafe/jev-1.13-20260917';self.r['usage']['cost']=.00001

    def test_explicit_route_preserves_input_and_typed_response(self):
        original=copy.deepcopy(self.p);telemetry={}
        def opener(req,timeout):
            self.assertEqual(req.full_url,'https://openrouter.ai/api/alpha/decisions')
            self.assertEqual(req.get_header('Authorization'),'Bearer controlled-key')
            sent=json.loads(req.data)
            self.assertEqual(sent['model'],OPENROUTER_MODEL)
            self.assertEqual(sent['questions'],original['questions'])
            return io.BytesIO(json.dumps(self.r).encode())
        self.assertEqual(evaluate(self.p,provider='openrouter',key='controlled-key',opener=opener,telemetry=telemetry),self.r)
        self.assertEqual(self.p,original);self.assertEqual(telemetry['provider'],'openrouter')

    def test_alias_selects_openrouter_and_stable_id_is_not_replaced(self):
        for model in (OPENROUTER_MODEL,'typesafe/jev-1.13'):
            self.p['model']=model
            def opener(req,timeout):
                self.assertIn('/alpha/decisions',req.full_url)
                self.assertEqual(json.loads(req.data)['model'],model)
                return io.BytesIO(json.dumps(self.r).encode())
            evaluate(self.p,key='controlled-key',opener=opener)

    def test_direct_route_does_not_receive_openrouter_model(self):
        self.p['model']=OPENROUTER_MODEL
        with self.assertRaisesRegex(LabError,'exige provider'):evaluate(self.p,provider='typesafe',key='controlled')

    def test_keys_are_separate_and_loaded_at_runtime(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'projetos/openpcbotv2';p.mkdir(parents=True)
            (p/'.env').write_text('OPENROUTER_API_KEY="controlled-openrouter"\nTYPESAFE_API_KEY=controlled-typesafe\n')
            with patch('jev_lab.core.Path.home',return_value=Path(d)):
                self.assertEqual(load_key('openrouter'),'controlled-openrouter')
                self.assertEqual(load_key('typesafe'),'controlled-typesafe')
                (p/'.env').write_text('TYPESAFE_API_KEY=controlled-typesafe\n')
                with self.assertRaisesRegex(LabError,'OPENROUTER_API_KEY'):load_key('openrouter')

    def test_unknown_provider_or_unrelated_model_never_connects(self):
        with self.assertRaises(LabError):evaluate(self.p,provider='unknown',key='controlled')
        self.p['model']='unrelated/model'
        with self.assertRaises(LabError):evaluate(self.p,provider='openrouter',key='controlled')

    def test_invalid_reported_cost_rejected(self):
        for cost in (-1,float('nan'),True):
            self.r['usage']['cost']=cost
            with self.assertRaisesRegex(LabError,'Custo'):validate_response(self.p,self.r)

    def test_package_refuses_provider_with_controlled_evaluator(self):
        with self.assertRaises(LabError):
            avaliar_area('atendimento','teste',evaluator=lambda _:self.r,provider='openrouter')

if __name__=='__main__':unittest.main()
