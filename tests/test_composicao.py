import unittest
from copy import deepcopy
from jev_lab.core import LabError
from pacotes.composicao import compor

class Composite(unittest.TestCase):
    def setUp(self):
        self.request={'model':'teste-controlado','state':'Exemplo fictício','questions':{}}
        self.response={'model':'teste-controlado','answers':{},'usage':{'input_tokens':0,'output_tokens':0}}
        for key,n,score in [('relevancia',5,3),('urgencia',3,1)]:
            criteria=[f'Nível {i}' for i in range(n)]
            self.request['questions'][key]={'type':'score','instructions':'Qual a prioridade?','criteria':criteria}
            self.response['answers'][key]={'type':'score','score':score,'confidence':.8,'legend':{str(i):c for i,c in enumerate(criteria)},'probabilities':{str(i):float(i==score) for i in range(n)}}
    def test_different_scales_and_unnormalized_weights(self):
        self.assertAlmostEqual(compor(self.request,self.response,{'relevancia':2,'urgencia':1})['indice'],2/3)
    def test_invalid_weights_and_question(self):
        for weights in [{},{'relevancia':True},{'relevancia':0},{'urgencia':-1},{'urgencia':float('nan')},{'missing':1}]:
            with self.subTest(weights=weights),self.assertRaises(LabError):compor(self.request,self.response,weights)
    def test_reject_inconsistent_response_even_unused_question(self):
        self.response['answers']['urgencia']['score']=2
        with self.assertRaises(LabError):compor(self.request,self.response,{'relevancia':1})
    def test_preserve_inputs_and_require_score(self):
        before=deepcopy(self.response);compor(self.request,self.response,{'relevancia':1});self.assertEqual(before,self.response)
        self.request['questions']['urgencia']={'type':'noul','instructions':'Urgente?','criteria':{'true':'Urgente','false':'Não urgente'}}
        self.response['answers']['urgencia']={'type':'noul','noul':.8}
        with self.assertRaises(LabError):compor(self.request,self.response,{'urgencia':1})
