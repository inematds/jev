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
    p=sub.add_parser('batch'); p.add_argument('file'); p.add_argument('--out', required=True)
    p=sub.add_parser('serve'); p.add_argument('--port', type=int, default=8765)
    args=parser.parse_args()
    try:
        if args.command=='serve':
            from .server import serve
            serve(args.port); return
        if args.command=='batch':
            result=batch(args.file); out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
            (out/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            with (out/'predictions.csv').open('w',newline='') as f:
                writer=csv.DictWriter(f, fieldnames=['id','expected','predicted','correct'],lineterminator='\n'); writer.writeheader(); writer.writerows(result['rows'])
            print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2)); return
        payload=json.loads(Path(args.file).read_text())
        if args.command=='validate':
            validate_request(payload); print('Contrato válido. Nenhuma chamada à API.'); return
        result=evaluate(payload)
        result['estimated_cost_usd']=result['usage']['input_tokens']/1_000_000*PRICE
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (LabError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr); sys.exit(2)
if __name__=='__main__': main()
