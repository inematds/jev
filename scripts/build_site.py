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
(out/'.nojekyll').touch()
print('Site montado em _site: app, guia, capa e index. Fontes locais não incluídas.')
