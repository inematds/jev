"""Executor comum: exemplos offline e integração explícita à API."""
import argparse
import json
import sys
from pathlib import Path
from jev_lab.core import LabError
from .integracao import avaliar_area, carregar, demonstrar, listar


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('area', nargs='?')
    parser.add_argument('--list', action='store_true', help='Lista as dez áreas.')
    parser.add_argument('--provider', choices=['typesafe','openrouter'], help='Provedor da consulta real; também configurável por JEV_PROVIDER.')
    parser.add_argument('--live', action='store_true', help='Consulta real; envia contexto à TypeSafe e pode consumir créditos.')
    parser.add_argument('--state-file', type=Path, help='Arquivo UTF-8 com o contexto completo.')
    parser.add_argument('--state-format', choices=['text','json'], default='text')
    args = parser.parse_args()
    if args.list:
        print('\n'.join(listar())); return
    if not args.area:
        parser.error('Escolha uma área ou use --list.')
    if args.state_file and not args.live:
        parser.error('Dados próprios exigem --live; a fixture só vale para o exemplo original.')
    try:
        if args.live:
            _, _, request = carregar(args.area)
            state = request['state']
            if args.state_file:
                if args.state_file.stat().st_size > 100_000:
                    raise LabError('Arquivo de contexto excede 100 KB.')
                text = args.state_file.read_text(encoding='utf-8')
                state = json.loads(text) if args.state_format == 'json' else text
            result = avaliar_area(args.area, state, provider=args.provider)
        else:
            result = demonstrar(args.area)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['error']:
            return 2
    except (LabError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
