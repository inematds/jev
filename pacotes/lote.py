"""Lote JSONL com prévia, concorrência limitada e retomada por conteúdo."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import json
import os
from pathlib import Path
import threading
import time
from jev_lab.core import LabError, evaluate, selected_provider, validate_request, validate_response
from .integracao import carregar, fingerprint, _executar


def preparar(area, entrada, max_events=100):
    if type(max_events) is not int or not 1 <= max_events <= 10000:
        raise LabError('max-events deve estar entre 1 e 10000.')
    path = Path(entrada)
    if path.stat().st_size > 10_000_000:
        raise LabError('Entrada excede 10 MB; divida o lote.')
    _, meta, template = carregar(area)
    events, ids = [], set()
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict) or not isinstance(event.get('id'), str) or not event['id'].strip():
            raise LabError('Cada evento exige id textual e state.')
        if event['id'] in ids:
            raise LabError('ID duplicado no lote.')
        ids.add(event['id'])
        request = dict(template, state=event.get('state'))
        validate_request(request)
        events.append({'id':event['id'], 'request':request})
        if len(events) > max_events:
            raise LabError('Limite de eventos excedido; aumente --max-events explicitamente.')
    if not events:
        raise LabError('Lote vazio.')
    return meta, events


@contextmanager
def exclusividade(path):
    lock = path.with_name(path.name+'.lock')
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise LabError('Outro executor ou lock residual protege esta saída. Consulte o guia.') from None
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def executar(area, entrada, saida, *, live=False, provider=None, workers=1,
             interval=1.0, max_events=100, evaluator=None):
    if type(workers) is not int or not 1 <= workers <= 4:
        raise LabError('Use de 1 a 4 workers.')
    if type(interval) not in (int,float) or not 0.1 <= interval <= 60:
        raise LabError('Intervalo deve estar entre 0,1 e 60 segundos.')
    meta, events = preparar(area, entrada, max_events)
    resolved = selected_provider(provider, events[0]['request']['model'])
    path = Path(saida)
    if path.resolve() == Path(entrada).resolve():
        raise LabError('Entrada e saída precisam ser arquivos diferentes.')
    if not live:
        return {'mode':'preview','area':area,'events':len(events),'provider':resolved,
                'workers':workers,'interval_seconds':interval,'calls':0}
    origin = 'controlled' if evaluator is not None else 'api'
    signature = fingerprint({'area':area,'events':events,'provider':resolved,
                             'sensitive':meta['sensitive'],'origin':origin,'format':1})
    path.parent.mkdir(parents=True, exist_ok=True)
    with exclusividade(path):
        done = set()
        requests = {e["id"]: e["request"] for e in events}
        if path.exists():
            # Uma linha incompleta após queda é recusada, nunca ignorada silenciosamente.
            for line in path.read_text(encoding='utf-8').splitlines():
                row = json.loads(line)
                if not isinstance(row,dict) or row.get('signature') != signature:
                    raise LabError('Saída pertence a outro lote, template ou provedor; use outro arquivo.')
                if row.get('id') not in requests or row['id'] in done or not isinstance(row.get('result'),dict):
                    raise LabError('Checkpoint inválido ou duplicado.')
                result = row['result']
                if result.get('origin') != origin or result.get('area') != area or result.get('action') not in ('suggest','review') or 'error' not in result:
                    raise LabError('Resultado do checkpoint inválido.')
                if result['error'] is None:
                    validate_response(requests[row['id']], result.get('response'))
                elif result.get('response') is not None or result['action'] != 'review':
                    raise LabError('Falha inconsistente no checkpoint.')
                done.add(row['id'])
        pending = [e for e in events if e['id'] not in done]
        gate, next_start = threading.Lock(), [0.0]

        def process(event):
            with gate:
                time.sleep(max(0, next_start[0]-time.monotonic()))
                next_start[0] = time.monotonic()+interval
            telemetry = {}
            def call(request):
                if evaluator is not None:
                    return evaluator(request)
                return evaluate(request, provider=resolved, telemetry=telemetry)
            start = time.monotonic()
            result = _executar(area, meta, event['request'], call, origin)
            response = result.get('response') or {}
            cost = response.get('usage',{}).get('cost')
            if origin != 'api' or telemetry.get('attempts') != 1:
                cost = None
            return {'signature':signature, 'id':event['id'], 'result':result,
                    'latency_ms':round((time.monotonic()-start)*1000,3),
                    'attempts':telemetry.get('attempts'), 'cost_usd':cost}

        # Um único escritor; cada resultado concluído é persistido antes do próximo.
        with path.open('a', encoding='utf-8') as output, ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(process,e) for e in pending]
            errors = 0
            for future in as_completed(futures):
                row = future.result()
                output.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n')
                output.flush()
                os.fsync(output.fileno())
                errors += bool(row['result']['error'])
        return {'mode':origin,'events':len(events),'processed':len(pending),
                'resumed':len(done),'new_errors':errors,'out':str(path)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('area')
    p.add_argument('input',type=Path)
    p.add_argument('--out',type=Path,default=Path('runs/lote.jsonl'))
    p.add_argument('--live',action='store_true',help='Envia cada evento ao provedor; consome créditos.')
    p.add_argument('--provider',choices=['typesafe','openrouter'])
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--interval',type=float,default=1.0,help='Intervalo mínimo entre inícios; não controla retries HTTP internos.')
    p.add_argument('--max-events',type=int,default=100)
    args=p.parse_args()
    try:
        result=executar(args.area,args.input,args.out,live=args.live,provider=args.provider,
                       workers=args.workers,interval=args.interval,max_events=args.max_events)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if result.get('new_errors') else 0
    except (LabError,OSError,ValueError) as exc:
        p.exit(2,str(exc)+'\n')


if __name__=='__main__':
    raise SystemExit(main())
