"""Avaliação offline por pergunta: Choice, Noul e Score contra referência explícita."""
import argparse
import json
from pathlib import Path
import statistics
from jev_lab.core import LabError, number, validate_request, validate_response
from .integracao import carregar, fingerprint


def avaliar(request, records):
    validate_request(request)
    if not records:
        raise LabError('Referência vazia.')
    questions=request['questions']
    values={k:[] for k in questions}
    seen=set()
    errors=0
    for row in records:
        if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or row['id'] in seen:
            raise LabError('IDs devem ser textuais, presentes e únicos.')
        seen.add(row['id'])
        expected=row.get('expected')
        if not isinstance(expected,dict) or set(expected)!=set(questions):
            raise LabError('Referência exige todas as perguntas, sem extras.')
        for key,q in questions.items():
            y=expected[key]
            if q['type']=='choice' and (not isinstance(y,str) or y not in q['criteria']):
                raise LabError('Rótulo Choice inválido.')
            if q['type']=='noul' and type(y) is not bool:
                raise LabError('Referência Noul deve ser true/false.')
            if q['type']=='score' and not number(y,0,len(q['criteria'])-1):
                raise LabError('Referência Score fora da rubrica.')
        current=dict(request,state=row.get('state'))
        validate_request(current)
        if row.get('request_sha256') != fingerprint(current):
            raise LabError('Hash não corresponde à requisição avaliada.')
        if row.get('origin') not in ('simulation','measured'):
            raise LabError('Declare origin simulation ou measured.')
        try:
            response=validate_response(current,row.get('response'))
        except LabError:
            errors+=1
            continue
        for key,q in questions.items():
            y=expected[key];a=response['answers'][key]
            if q['type']=='choice':
                values[key].append({'correct':a['choice']==y})
            elif q['type']=='noul':
                values[key].append({'correct':(a['noul']>=.5)==y,'brier':(a['noul']-y)**2})
            else:
                values[key].append({'mae':abs(a['score']-y),'normalized_mae':abs(a['score']-y)/(len(q['criteria'])-1)})
    result={}
    for key,q in questions.items():
        rows=values[key]
        metrics={'type':q['type'],'total':len(records),'valid':len(rows),'errors':errors,
                 'coverage':len(rows)/len(records)}
        if q['type'] in ('choice','noul'):
            metrics['accuracy_all']=sum(r['correct'] for r in rows)/len(records)
        for metric in ('brier','mae','normalized_mae'):
            if rows and metric in rows[0]:metrics[metric]=statistics.mean(r[metric] for r in rows)
            elif (q['type']=='noul' and metric=='brier') or (q['type']=='score' and metric!='brier'):
                metrics[metric]=None
        result[key]=metrics
    return {'schema_version':1,'origins':sorted({r['origin'] for r in records}),
            'count':len(records),'questions':result,
            'note':'Referência fornecida pelo avaliador; origin não autentica procedência. Noul usa corte 0,5 somente para métrica. Erros reduzem cobertura e acurácia; MAE/Brier usam respostas válidas.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('area')
    p.add_argument('--input',type=Path,help='JSONL rotulado; sem este argumento avalia somente a fixture simulada.')
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    try:
        root,meta,request=carregar(args.area)
        if args.input:
            if args.input.stat().st_size>10_000_000:raise LabError('Entrada excede 10 MB.')
            records=[json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
        else:
            if fingerprint(request)!=meta['fixture_request_sha256']:
                raise LabError('Fixture antiga: request alterado.')
            if 'expected_answers' not in meta:
                raise LabError('Este pacote ainda não possui referência para todas as perguntas.')
            records=[{'id':'exemplo-ficticio','state':request['state'],
                      'request_sha256':fingerprint(request),'expected':meta['expected_answers'],
                      'origin':'simulation','response':json.loads((root/'fixture.json').read_text())}]
        result=avaliar(request,records)
        encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
        if args.out:
            if args.input and args.out.resolve()==args.input.resolve():raise LabError('Saída não pode sobrescrever entrada.')
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(encoded,encoding='utf-8')
        print(encoded,end='')
    except (LabError,OSError,ValueError) as exc:p.exit(2,str(exc)+'\n')


if __name__=='__main__':main()
