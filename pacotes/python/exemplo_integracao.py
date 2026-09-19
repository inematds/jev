"""Adaptador mínimo: resposta validada + política, sem executar ações."""
import argparse
import json
from pathlib import Path
from jev_lab.core import evaluate, policy, validate_request, validate_response


def decidir(request, *, sensitive=False, evaluator=evaluate):
    """Recebe um request e devolve a resposta com encaminhamento por pergunta.

    evaluator pode ser substituído por um provedor controlado em testes.
    O resultado é uma sugestão; o sistema chamador conserva suas permissões.
    """
    validate_request(request)
    response = evaluator(request)
    validate_response(request, response)
    return {
        'response': response,
        'decisions': {
            name: policy(answer, sensitive=sensitive)
            for name, answer in response['answers'].items()
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Envia o exemplo fictício à TypeSafe; requer chave e pode consumir créditos.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cases = json.loads((root / 'app/cases.json').read_text())
    case = next(c for c in cases if c['id'] == 'atendimento')
    evaluator = evaluate if args.live else lambda request: case['fixture']
    result = decidir(case['request'], sensitive=case.get('sensitive', False), evaluator=evaluator)
    result['origin'] = 'api' if args.live else 'simulation'
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
