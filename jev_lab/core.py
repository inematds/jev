"""Validação e política independentes do provedor. Biblioteca padrão apenas."""
import json
import math
import os
import re
import time
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = 'jev-1.13.0'
PRICE = 0.042
ROOT = Path(__file__).resolve().parents[1]

class LabError(ValueError):
    pass

def number(value, low=0, high=1):
    return type(value) in (int, float) and math.isfinite(value) and low <= value <= high

def validate_request(payload):
    if not isinstance(payload, dict):
        raise LabError('A requisição precisa ser um objeto JSON.')
    if not isinstance(payload.get('model'), str) or not payload['model'].strip():
        raise LabError('Informe o modelo.')
    state = payload.get('state')
    if not isinstance(state, (str, list, dict)) or not state or isinstance(state, str) and not state.strip():
        raise LabError('Preencha o contexto (state).')
    questions = payload.get('questions')
    if not isinstance(questions, dict) or not 1 <= len(questions) <= 30:
        raise LabError('Use entre 1 e 30 perguntas por requisição neste laboratório.')
    for key, q in questions.items():
        if not isinstance(key, str) or not key or not isinstance(q, dict):
            raise LabError('Pergunta inválida.')
        if not q.get('instructions') or q.get('type') not in ('choice', 'noul', 'score'):
            raise LabError('Toda pergunta precisa de type e instructions.')
        criteria = q.get('criteria')
        if q['type'] == 'choice' and (not isinstance(criteria, dict) or not 2 <= len(criteria) <= 255 or any(not k or not isinstance(v, (str, type(None))) for k, v in criteria.items())):
            raise LabError('Choice precisa de 2 a 255 opções com descrições.')
        if q['type'] == 'score' and (not isinstance(criteria, list) or len(criteria) < 2 or not all(isinstance(x, str) and x for x in criteria)):
            raise LabError('Score precisa de pelo menos dois níveis descritos.')
        if q['type'] == 'noul' and criteria is not None and (not isinstance(criteria, dict) or set(criteria) != {'true', 'false'}):
            raise LabError('Critérios de Noul devem usar true e false.')
    if len(json.dumps(payload).encode()) > 100_000:
        raise LabError('Requisição maior que o limite de 100 KB do laboratório.')
    return payload

def validate_response(payload, response):
    validate_request(payload)
    if not isinstance(response, dict) or not isinstance(response.get('model'), str):
        raise LabError('Resposta sem identificação do modelo.')
    answers = response.get('answers')
    if not isinstance(answers, dict) or set(answers) != set(payload['questions']):
        raise LabError('Resposta não contém exatamente as perguntas enviadas.')
    for key, q in payload['questions'].items():
        a = answers[key]
        if not isinstance(a, dict) or a.get('type') != q['type']:
            raise LabError('Tipo inesperado na resposta.')
        if q['type'] == 'noul':
            if not number(a.get('noul')):
                raise LabError('Noul precisa ser uma probabilidade entre 0 e 1.')
            continue
        p = a.get('probabilities')
        expected = set(q['criteria']) if q['type'] == 'choice' else {str(i) for i in range(len(q['criteria']))}
        if not isinstance(p, dict) or set(p) != expected or not all(number(x) for x in p.values()) or not math.isclose(sum(p.values()), 1, abs_tol=0.001):
            raise LabError('Distribuição de probabilidades inválida.')
        if not number(a.get('confidence')):
            raise LabError('Confidence inválida.')
        if q['type'] == 'choice':
            if a.get('choice') not in expected or p[a['choice']] + 1e-6 < max(p.values()):
                raise LabError('Opção escolhida fora do conjunto ou inconsistente.')
        else:
            if not number(a.get('score'), 0, len(q['criteria'])-1):
                raise LabError('Score fora dos níveis.')
            if not math.isclose(a['score'], sum(int(k)*v for k,v in p.items()), abs_tol=0.01):
                raise LabError('Score inconsistente com as probabilidades.')
    usage = response.get('usage')
    if not isinstance(usage, dict) or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ('input_tokens', 'output_tokens')):
        raise LabError('Uso de tokens ausente ou inválido.')
    return response

def policy(answer, *, threshold=0.9, probability=0.9, sensitive=False):
    if not number(threshold) or not number(probability):
        raise LabError('Limiares devem estar entre 0 e 1.')
    if sensitive:
        return {'action': 'review', 'reason': 'Domínio supervisionado: revisão humana obrigatória.'}
    if answer.get('type') != 'choice':
        return {'action': 'review', 'reason': 'Noul e Score precisam de política específica do domínio.'}
    label = answer.get('choice')
    if label in ('insuficiente', 'incerto', 'outro', 'nenhum', 'ambiguo', 'conflito', 'revisar'):
        return {'action': 'review', 'reason': 'A alternativa requer revisão ou mais informação.'}
    if answer.get('confidence', 0) < threshold or answer.get('probabilities', {}).get(label, 0) < probability:
        return {'action': 'review', 'reason': 'Distribuição abaixo dos limiares didáticos.'}
    return {'action': 'suggest', 'reason': 'Sugestão em observação. Nenhuma ação externa executada.'}

def load_key():
    if os.environ.get('TYPESAFE_API_KEY', '').strip():
        return os.environ['TYPESAFE_API_KEY'].strip()
    for project in ('openpcbotv2', 'wifi'):
        path = Path.home()/'projetos'/project/'.env'
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            match = re.match(r'^\s*(?:export\s+)?TYPESAFE_API_KEY\s*=\s*(.*?)\s*$', line)
            if match:
                value = match[1].strip().strip('"\'')
                if value:
                    return value
    raise LabError('TYPESAFE_API_KEY não configurada no ambiente ou nos arquivos autorizados. Use os exemplos offline; não envie chaves pelo navegador.')

def evaluate(payload, *, key=None, timeout=5, opener=urlopen):
    validate_request(payload)
    key = key or load_key()
    deadline = time.monotonic() + timeout
    for attempt in range(3):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise LabError('Prazo de inferência excedido. Encaminhe para revisão.')
        req = Request('https://api.typesafe.ai/v1/systemone', data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer '+key, 'Content-Type': 'application/json', 'User-Agent': 'JevDecisionLab/1.1.1'}, method='POST')
        try:
            with opener(req, timeout=remaining) as res:
                raw = res.read(1_000_001)
            if len(raw) > 1_000_000:
                raise LabError('Resposta excede o limite do laboratório.')
            result = json.loads(raw)
            validate_response(payload, result)
            return result
        except HTTPError as exc:
            if exc.code not in (429, 529, 502, 503, 504) or attempt == 2:
                raise LabError(f'Provedor retornou HTTP {exc.code}. Nenhuma decisão executada.') from None
            retry = exc.headers.get('Retry-After', '')
            try:
                delay = max(float(retry), 0.25 * 2**attempt) if retry else 0.25 * 2**attempt
            except ValueError:
                from email.utils import parsedate_to_datetime
                try: delay = max(0.25 * 2**attempt, parsedate_to_datetime(retry).timestamp() - time.time())
                except (ValueError, TypeError, OverflowError): delay = 0.25 * 2**attempt
            if not math.isfinite(delay) or delay >= deadline - time.monotonic():
                raise LabError('Retry-After excede o prazo. Encaminhe para revisão.') from None
            time.sleep(delay)
        except (URLError, TimeoutError, OSError):
            raise LabError('Não foi possível concluir a conexão. Nenhuma decisão executada.') from None
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise LabError('Provedor retornou JSON inválido.') from None
    raise LabError('Tentativas esgotadas.')

def baseline(text):
    """Regra lexical transparente, sem probabilidades inventadas."""
    clean = ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if not unicodedata.combining(c))
    rules = {'cobranca': ['cobranca', 'fatura', 'paguei', 'estorno'], 'suporte': ['senha', 'acesso', 'erro', 'login'], 'vendas': ['contratar', 'preco', 'plano', 'comprar']}
    hits = [label for label, words in rules.items() if any(re.search(r'\b'+w+r'\b', clean) for w in words)]
    return hits[0] if len(hits) == 1 else 'insuficiente'

def batch(path):
    """Avalia a baseline de regras em dados rotulados. Não mede Jev."""
    rows, seen = [], set()
    for line_no, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip(): continue
        try: item = json.loads(line)
        except json.JSONDecodeError: raise LabError(f'JSON inválido na linha {line_no}.') from None
        if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k].strip() for k in ('id', 'text', 'label')):
            raise LabError(f'Linha {line_no}: informe id, text e label.')
        if item['label'] not in ('suporte', 'cobranca', 'vendas', 'insuficiente'):
            raise LabError(f'Linha {line_no}: rótulo desconhecido.')
        if item['id'] in seen: raise LabError(f'ID duplicado na linha {line_no}.')
        seen.add(item['id'])
        pred = baseline(item['text'])
        rows.append({'id': item['id'], 'expected': item['label'], 'predicted': pred, 'correct': pred == item['label']})
    if not rows: raise LabError('Dataset vazio.')
    matrix = {}
    for row in rows:
        matrix.setdefault(row['expected'], {})[row['predicted']] = matrix.get(row['expected'], {}).get(row['predicted'], 0)+1
    classes = sorted({r['expected'] for r in rows} | {r['predicted'] for r in rows})
    f1s=[]
    for cls in classes:
        tp=sum(r['expected']==cls and r['predicted']==cls for r in rows)
        fp=sum(r['expected']!=cls and r['predicted']==cls for r in rows)
        fn=sum(r['expected']==cls and r['predicted']!=cls for r in rows)
        f1s.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0)
    return {'provider': 'regras-lexicais', 'dataset': str(path), 'count': len(rows), 'accuracy': sum(r['correct'] for r in rows)/len(rows), 'macro_f1': sum(f1s)/len(f1s), 'confusion': matrix, 'rows': rows, 'note': 'Resultado da baseline local; não é benchmark Jev.'}
