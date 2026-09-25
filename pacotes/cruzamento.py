"""Cruza respostas Choice de um item com perfis: o Jev extrai, a regra decide.

Cada item é avaliado uma vez; o custo cresce com os itens, não com itens × perfis.
Respostas em revisão nunca viram compatibilidade: o perfil fica em `revisar`.
"""
import argparse
import json
import sys
from pathlib import Path
from jev_lab.core import LabError, number
from .integracao import AREAS, carregar, demonstrar


def cruzar(request, resultado, perfis, *, preco=None):
    """Compara o resultado validado de `demonstrar`/`avaliar_area` com os perfis.

    `preco` é dado estruturado do sistema chamador, não resposta do modelo.
    Retorna um status por perfil: compativel, incompativel ou revisar.
    """
    if resultado.get('error') or not resultado.get('response'):
        raise LabError('Resultado sem resposta válida: encaminhe o item para revisão.')
    if preco is not None and not number(preco, 0, 1e9):
        raise LabError('Preço deve ser número não negativo.')
    questions = request['questions']
    answers = resultado['response']['answers']
    decisions = resultado['decisions']
    saida, vistos = [], set()
    for perfil in perfis:
        pid = perfil.get('id') if isinstance(perfil, dict) else None
        if not isinstance(pid, str) or not pid or pid in vistos:
            raise LabError('Perfis exigem id textual e único.')
        vistos.add(pid)
        requisitos = perfil.get('requisitos', {})
        desejaveis = perfil.get('desejaveis', [])
        if not isinstance(requisitos, dict) or not isinstance(desejaveis, list):
            raise LabError(f'Perfil {pid}: requisitos deve ser objeto e desejaveis, lista.')
        motivos, pendentes = [], []
        for key, aceitos in requisitos.items():
            q = questions.get(key)
            if not q or q['type'] != 'choice':
                raise LabError(f'Perfil {pid}: requisito {key!r} não é pergunta Choice do pacote.')
            if not isinstance(aceitos, list) or not aceitos or not set(aceitos) <= set(q['criteria']):
                raise LabError(f'Perfil {pid}: rótulos aceitos inválidos em {key!r}.')
            if decisions[key]['action'] != 'suggest':
                pendentes.append(key)
            elif answers[key]['choice'] not in aceitos:
                motivos.append(f"{key}={answers[key]['choice']}")
        orcamento = perfil.get('orcamento_diaria')
        if orcamento is not None:
            if not number(orcamento, 0, 1e9):
                raise LabError(f'Perfil {pid}: orçamento inválido.')
            if preco is not None and preco > orcamento:
                motivos.append(f'preco {preco} > orcamento {orcamento}')
        for key in desejaveis:
            if key not in questions:
                raise LabError(f'Perfil {pid}: desejável {key!r} não existe no pacote.')
        extras = [k for k in desejaveis if decisions[k]['action'] == 'suggest' and answers[k].get('choice') == 'atende']
        status = 'incompativel' if motivos else 'revisar' if pendentes else 'compativel'
        saida.append({'id': pid, 'status': status, 'motivos': motivos, 'pendentes': pendentes, 'desejaveis_atendidos': extras})
    return {'perfis': saida, 'tipo': 'sugestao_em_observacao', 'origin': resultado.get('origin')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('area', nargs='?', default='viagens')
    parser.add_argument('--perfis', type=Path, help='JSON com a chave "perfis"; padrão: perfis.json do pacote.')
    parser.add_argument('--preco', type=float, help='Preço da diária vindo do seu sistema.')
    args = parser.parse_args()
    try:
        _, _, request = carregar(args.area)
        path = args.perfis or AREAS/args.area/'perfis.json'
        perfis = json.loads(path.read_text(encoding='utf-8'))['perfis']
        result = cruzar(request, demonstrar(args.area), perfis, preco=args.preco)
    except (LabError, OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
