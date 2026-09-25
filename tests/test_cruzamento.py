import copy
import json
import unittest
from jev_lab.core import LabError
from pacotes.cruzamento import cruzar
from pacotes.integracao import AREAS, avaliar_area, carregar, demonstrar


class Cruzamento(unittest.TestCase):
    def setUp(self):
        _, _, self.request = carregar('viagens')
        self.result = demonstrar('viagens')
        self.perfis = json.loads((AREAS/'viagens'/'perfis.json').read_text())['perfis']

    def status(self, perfis, preco=420):
        return {p['id']: p['status'] for p in cruzar(self.request, self.result, perfis, preco=preco)['perfis']}

    def test_demo_profiles(self):
        s = self.status(self.perfis)
        self.assertEqual(len(s), 12)
        self.assertEqual({k for k, v in s.items() if v == 'compativel'}, {'v02', 'v03', 'v09', 'v12'})
        self.assertEqual({k for k, v in s.items() if v == 'revisar'}, {'v06', 'v07', 'v10'})
        self.assertEqual(s['v01'], 'incompativel')
        self.assertEqual(s['v05'], 'incompativel')

    def test_insufficient_never_becomes_compatible(self):
        s = self.status([{'id': 'x', 'requisitos': {'decisao': ['dinheiro', 'credito_hotel', 'sem_reembolso', 'insuficiente']}}])
        self.assertEqual(s['x'], 'revisar')

    def test_low_confidence_goes_to_review(self):
        root, _, _ = carregar('viagens')
        fixture = json.loads((root/'fixture.json').read_text())
        fixture['answers']['piscina_inclusa']['confidence'] = 0.5
        result = avaliar_area('viagens', self.request['state'], evaluator=lambda _: fixture)
        s = cruzar(self.request, result, [{'id': 'x', 'requisitos': {'piscina_inclusa': ['atende']}}])
        self.assertEqual(s['perfis'][0]['status'], 'revisar')

    def test_without_price_budget_is_not_judged(self):
        self.assertEqual(self.status(self.perfis[:1], preco=None)['v01'], 'compativel')

    def test_invalid_profiles_are_rejected(self):
        for perfis in ([{'id': 'x', 'requisitos': {'inexistente': ['atende']}}],
                       [{'id': 'x', 'requisitos': {'piscina_inclusa': ['talvez']}}],
                       [{'id': 'x', 'requisitos': {'piscina_inclusa': []}}],
                       [{'id': 'x'}, {'id': 'x'}],
                       [{'requisitos': {}}]):
            with self.subTest(perfis=perfis), self.assertRaises(LabError):
                cruzar(self.request, self.result, perfis)

    def test_failed_evaluation_refuses_matching(self):
        def fail(_): raise LabError('Prazo excedido')
        result = avaliar_area('viagens', self.request['state'], evaluator=fail)
        with self.assertRaisesRegex(LabError, 'revisão'):
            cruzar(self.request, result, self.perfis)

    def test_input_is_not_mutated(self):
        before = copy.deepcopy(self.perfis)
        cruzar(self.request, self.result, self.perfis, preco=420)
        self.assertEqual(self.perfis, before)


if __name__ == '__main__':
    unittest.main()
