"""Entrada reutilizável para os dez pacotes. Sem execução de ações externas."""
import hashlib
import json
from pathlib import Path
from jev_lab.core import LabError, evaluate, validate_request
from pacotes.python.exemplo_integracao import decidir

AREAS = Path(__file__).resolve().parent / 'areas'


def fingerprint(request):
    return hashlib.sha256(json.dumps(request, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()).hexdigest()


def listar():
    return sorted(p.name for p in AREAS.iterdir() if p.is_dir() and (p/'pacote.json').is_file())


def carregar(area):
    if area not in listar():
        raise LabError('Área desconhecida. Use --list para ver as opções.')
    root = AREAS/area
    meta = json.loads((root/'pacote.json').read_text(encoding='utf-8'))
    request = json.loads((root/'request.json').read_text(encoding='utf-8'))
    validate_request(request)
    return root, meta, request


def _executar(area, meta, request, evaluator, origin):
    try:
        result = decidir(request, sensitive=meta['sensitive'], evaluator=evaluator)
        review = any(d['action'] == 'review' for d in result['decisions'].values())
        return dict(result, area=area, origin=origin, action='review' if review else 'suggest', error=None)
    except LabError as exc:
        return {'area':area, 'origin':origin, 'action':'review', 'error':str(exc), 'response':None, 'decisions':{}}


def avaliar_area(area, state, *, evaluator=evaluate):
    """Consulta real por padrão; passe evaluator para testes controlados.

    Preserve o evento original no seu sistema. Falhas esperadas retornam revisão.
    state substitui todo o contexto: inclua briefing, rubrica ou catálogo exigido.
    """
    _, meta, request = carregar(area)
    request['state'] = state
    return _executar(area, meta, request, evaluator, 'api' if evaluator is evaluate else 'controlled')


def demonstrar(area):
    root, meta, request = carregar(area)
    if fingerprint(request) != meta.get('fixture_request_sha256'):
        raise LabError('O request foi alterado. A fixture original não pode demonstrar este contexto.')
    fixture = json.loads((root/'fixture.json').read_text(encoding='utf-8'))
    return _executar(area, meta, request, lambda _: fixture, 'simulation')
