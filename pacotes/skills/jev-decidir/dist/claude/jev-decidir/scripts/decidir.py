#!/usr/bin/env python3
"""Ponte portátil para o cliente Jev existente; nunca armazena credenciais."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    inputs=parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('request',nargs='?',type=Path,help='JSON com state e questions.')
    inputs.add_argument('--demo',help='Área fictícia offline, como atendimento.')
    parser.add_argument('--live',action='store_true',help='Autoriza a consulta real ao OpenRouter.')
    args=parser.parse_args()
    if args.request and not args.live:
        parser.error('Use --live para consultar um request, ou --demo atendimento para exemplo sem API.')
    if args.demo and args.live:
        parser.error('--demo é somente offline; não combine com --live.')
    root=Path(os.environ.get('JEV_LAB_DIR',str(Path.home()/'projetos/jev'))).expanduser().resolve()
    if not (root/'jev_lab/core.py').is_file():
        print('Clone Jev não encontrado. Configure JEV_LAB_DIR para o clone de inematds/jev.',file=sys.stderr);return 2
    if args.demo:
        command=[sys.executable,'-m','pacotes.executar',args.demo]
    else:
        request=args.request.expanduser().resolve()
        if not request.is_file() or request.stat().st_size>100_000:
            print('Request ausente ou maior que 100 KB.',file=sys.stderr);return 2
        command=[sys.executable,'-m','jev_lab','ask',str(request),'--provider','openrouter']
    # Argumentos separados, sem shell e sem credenciais na linha de comando.
    return subprocess.run(command,cwd=root,check=False).returncode


if __name__=='__main__':
    sys.exit(main())
