# Minimal local sink: saves each POST body to OUTDIR/<probe-tag>/req-<n>-<path>.json and answers 400 so the CLI stops.
import http.server, sys, os, itertools, re
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True); n = itertools.count()
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('content-length', 0)))
        m = re.search(rb'PROBE-([A-Za-z0-9_-]+)', body)
        sub = os.path.join(OUT, m.group(1).decode() if m else '_other'); os.makedirs(sub, exist_ok=True)
        name = self.path.strip('/').split('?')[0].replace('/', '_')
        with open(os.path.join(sub, f"req-{next(n)}-{name}.json"), 'wb') as f: f.write(body)
        msg = b'{"type":"error","error":{"type":"invalid_request_error","message":"capture sink"}}'
        self.send_response(400); self.send_header('content-type', 'application/json'); self.send_header('content-length', str(len(msg))); self.end_headers(); self.wfile.write(msg)
    def do_GET(self):
        self.send_response(404); self.end_headers()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1])), H).serve_forever()
