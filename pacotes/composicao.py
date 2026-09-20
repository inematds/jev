"""Combina rubricas Score validadas; o índice não representa confiança."""
from jev_lab.core import LabError, number, validate_request, validate_response


def compor(request, response, pesos):
    """Pesos positivos; todas as rubricas selecionadas crescem no mesmo sentido.

    O chamador define o significado e a direção das rubricas. O resultado serve
    para ordenar itens, nunca para conceder autorização ou estimar probabilidade.
    """
    validate_request(request)
    result = validate_response(request, response)
    if not isinstance(pesos, dict) or not pesos:
        raise LabError('Informe pesos positivos para pelo menos uma pergunta Score.')
    parcelas = {}
    for key, weight in pesos.items():
        q = request['questions'].get(key)
        if not q or q['type'] != 'score':
            raise LabError('Composição aceita apenas perguntas Score existentes.')
        if not number(weight, 0, 1e6) or weight == 0:
            raise LabError('Pesos devem ser finitos, positivos e até um milhão.')
        parcelas[key] = {'peso': weight, 'normalizado': result['answers'][key]['score'] / (len(q['criteria']) - 1)}
    total = sum(pesos.values())
    return {'indice': sum(p['peso'] * p['normalizado'] for p in parcelas.values()) / total,
            'parcelas': parcelas, 'tipo': 'indice_composto_nao_probabilidade'}
