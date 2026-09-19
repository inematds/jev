"""Servidor local. Não usar como backend público. Não serve arquivos do repo."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from .core import ROOT, LabError, evaluate

class Handler(BaseHTTPRequestHandler):
    lock=threading.Lock()
    def log_message(self, *args): pass
    def send(self, status, data, content_type='application/json; charset=utf-8'):
        self.send_response(status); self.send_header('Content-Type',content_type)
        self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def host_ok(self):
        return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}' or self.headers.get('Host') == f'localhost:{self.server.server_port}'
    def do_GET(self):
        if not self.host_ok(): self.send(403,b'{}'); return
        path=urlsplit(self.path).path
        if path=='/api/status':
            from .core import load_key, selected_provider
            try: provider=selected_provider(); load_key(provider); configured=True
            except LabError: provider=None; configured=False
            self.send(200,json.dumps({'local':True,'configured':configured,'provider':provider}).encode()); return
        paths={'/':'index.html','/index.html':'index.html','/app.js':'app.js','/app.css':'app.css','/cases.json':'cases.json'}
        if path not in paths: self.send(404,b'{}'); return
        p=ROOT/'app'/paths[path]
        ct={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8'}[p.suffix]
        self.send(200,p.read_bytes(),ct)
    def do_POST(self):
        allowed={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
        if not self.host_ok() or self.headers.get('Origin') not in allowed or self.headers.get('X-Jev-Lab')!='1':
            self.send(403,b'{"error":"Origem recusada."}'); return
        if self.path!='/api/evaluate': self.send(404,b'{}'); return
        if self.headers.get('Content-Type','').split(';')[0]!='application/json': self.send(415,b'{}'); return
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=100_000: raise LabError('Use uma requisição entre 1 byte e 100 KB.')
            if not self.lock.acquire(blocking=False): self.send(429,b'{"error":"Uma chamada ja esta em andamento."}'); return
            try:
                self.connection.settimeout(5)
                payload=json.loads(self.rfile.read(length))
                result=evaluate(payload)
            finally: self.lock.release()
            self.send(200,json.dumps(result,ensure_ascii=False).encode())
        except (LabError, ValueError, TimeoutError):
            self.send(400,json.dumps({'error':'Não foi possível avaliar. Confira o JSON, a chave no servidor e a disponibilidade do provedor. Nenhuma ação executada.'}).encode())

def serve(port):
    with ThreadingHTTPServer(('127.0.0.1',port),Handler) as server:
        print(f'Laboratório local: http://127.0.0.1:{port}',flush=True)
        server.serve_forever()
