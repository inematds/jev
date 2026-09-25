import copy
import json
import subprocess
import sys
import unittest
from unittest.mock import patch
from jev_lab.core import LabError
from pacotes.integracao import avaliar_area, carregar, demonstrar, listar


class Packages(unittest.TestCase):
    def test_all_offline_packages_have_valid_results_without_network(self):
        self.assertEqual(len(listar()), 18)
        with patch('urllib.request.OpenerDirector.open', side_effect=AssertionError('network')):
            for area in listar():
                with self.subTest(area=area):
                    _, meta, _ = carregar(area)
                    r = demonstrar(area)
                    self.assertIsNone(r['error'])
                    self.assertEqual(r['origin'], 'simulation')
                    self.assertEqual(r['response']['answers']['decisao']['choice'], meta['expected'])
                    if meta['sensitive'] or meta['expected']=='revisar':
                        self.assertEqual(r['action'],'review')

    def test_timeout_preserves_review_without_answer(self):
        def fail(_): raise LabError('Prazo excedido')
        r=avaliar_area('atendimento','Mensagem fictícia',evaluator=fail)
        self.assertEqual(r['action'],'review')
        self.assertIsNone(r['response'])
        self.assertEqual(r['origin'],'controlled')

    def test_invalid_provider_answer_cannot_be_suggested(self):
        r=avaliar_area('atendimento','Mensagem fictícia',evaluator=lambda _: {})
        self.assertEqual(r['action'],'review')
        self.assertTrue(r['error'])

    def test_custom_context_reaches_evaluator(self):
        root, _, _ = carregar('atendimento')
        fixture=json.loads((root/'fixture.json').read_text())
        seen=[]
        def controlled(request):
            seen.append(request['state']);return fixture
        avaliar_area('atendimento',{'ticket':'outro contexto'},evaluator=controlled)
        self.assertEqual(seen,[{'ticket':'outro contexto'}])

    def test_changed_template_refuses_old_fixture(self):
        root, meta, request=carregar('atendimento')
        request=copy.deepcopy(request);request['state']='alterado'
        with patch('pacotes.integracao.carregar',return_value=(root,meta,request)):
            with self.assertRaisesRegex(LabError,'alterado'):demonstrar('atendimento')

    def test_path_traversal_is_not_a_package(self):
        with self.assertRaises(LabError):carregar('../python')

    def test_cli_refuses_custom_state_offline(self):
        r=subprocess.run([sys.executable,'-m','pacotes.executar','atendimento','--state-file','qualquer.txt'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
        self.assertIn('exigem --live',r.stderr)

if __name__=='__main__':unittest.main()
