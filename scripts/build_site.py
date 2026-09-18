"""Publica somente arquivos de interface; nunca fontes recebidas ou dados privados."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
out=root/'_site'
if out.exists():shutil.rmtree(out)
out.mkdir()
for name in ('app','guia','capa'):
    shutil.copytree(root/name,out/name)
shutil.copy2(root/'index.html',out/'index.html')
# O catálogo PRO resolve capas a partir da URL do guia.
(out/'guia/capa').mkdir(exist_ok=True)
shutil.copy2(root/'capa/capa.png',out/'guia/capa/capa.png')
(out/'.nojekyll').touch()
print('Site montado em _site: app, guia, capa e index. Fontes locais não incluídas.')
