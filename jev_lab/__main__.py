import argparse
import csv
import json
import sys
from pathlib import Path
from .core import LabError, batch, evaluate, validate_request, PRICE
from . import __version__

def main():
    parser = argparse.ArgumentParser(description='Jev Decision Lab — laboratório local')
    parser.add_argument('--version', action='version', version=__version__)
    sub=parser.add_subparsers(dest='command', required=True)
    for name in ('validate', 'ask'):
        p=sub.add_parser(name); p.add_argument('file')
        if name == 'ask': p.add_argument('--provider', choices=['typesafe','openrouter'])
    p=sub.add_parser('batch'); p.add_argument('file'); p.add_argument('--out', required=True)
    p=sub.add_parser('serve'); p.add_argument('--port', type=int, default=8765)
    p=sub.add_parser('experiment', help='Avaliar dataset rotulado com regras, Jev, híbrido ou replay')
    p.add_argument('file'); p.add_argument('--out', required=True)
    p.add_argument('--provider', choices=['rules','jev','hybrid','replay'], default='rules')
    p.add_argument('--template'); p.add_argument('--question', default='decisao'); p.add_argument('--replay')
    p.add_argument('--repeats', type=int, default=1); p.add_argument('--max-calls', type=int, default=100)
    p.add_argument('--confidence',type=float,default=.9);p.add_argument('--probability',type=float,default=.9)
    p=sub.add_parser('compare', help='Comparar relatórios do mesmo dataset');p.add_argument('files',nargs='+')
    p=sub.add_parser('cases',help='Listar ou exportar um dos casos autorais');p.add_argument('--id');p.add_argument('--out')
    args=parser.parse_args()
    try:
        if args.command=='serve':
            from .server import serve
            serve(args.port); return
        if args.command=='cases':
            from .core import ROOT
            cases=json.loads((ROOT/'app/cases.json').read_text())
            if not args.id:
                for c in cases:print(c['id']+' — '+c['title'])
                return
            case=next((c for c in cases if c['id']==args.id),None)
            if not case:raise LabError('Caso desconhecido. Use cases para listar.')
            text=json.dumps(case['request'],ensure_ascii=False,indent=2)+'\n'
            if args.out:Path(args.out).write_text(text)
            else:print(text,end='')
            return
        if args.command=='experiment':
            from .experiments import run,save
            template=json.loads(Path(args.template).read_text()) if args.template else None
            result=run(args.file,provider=args.provider,template=template,question=args.question,
                       replay=args.replay,repeats=args.repeats,max_calls=args.max_calls,
                       threshold=args.confidence,probability=args.probability)
            save(result,args.out)
            print(json.dumps(result['metrics'],ensure_ascii=False,indent=2))
            if result['metrics']['errors']:sys.exit(2)
            return
        if args.command=='compare':
            from .experiments import compare
            print(json.dumps(compare(args.files),ensure_ascii=False,indent=2));return
        if args.command=='batch':
            result=batch(args.file); out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
            (out/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            with (out/'predictions.csv').open('w',newline='') as f:
                writer=csv.DictWriter(f, fieldnames=['id','expected','predicted','correct'],lineterminator='\n'); writer.writeheader(); writer.writerows(result['rows'])
            print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2)); return
        payload=json.loads(Path(args.file).read_text())
        if args.command=='validate':
            validate_request(payload); print('Contrato válido. Nenhuma chamada à API.'); return
        result=evaluate(payload, provider=args.provider)
        if 'cost' not in result['usage']:
            result['estimated_cost_usd']=result['usage']['input_tokens']/1_000_000*PRICE
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (LabError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr); sys.exit(2)
if __name__=='__main__': main()
