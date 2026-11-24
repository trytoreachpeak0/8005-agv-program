# Local fake Messages API for probing what Claude Code puts into its requests.
# Saves every POST body under OUT/<probe-tag>/req-<n>.json.
# First main-loop request of a probe whose prompt carries "READ=<path>": answer with one Read tool_use.
# Any request that already carries a tool_result: answer with a short end_turn text. Everything else: text.
import http.server, sys, os, itertools, re, json
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True); n = itertools.count()

def sse(events):
    return b''.join(f"event: {e}\ndata: {json.dumps(d)}\n\n".encode() for e, d in events)

def reply(stream, block):
    msg = {"id": "msg_probe", "type": "message", "role": "assistant", "model": "probe", "content": [],
           "stop_reason": None, "stop_sequence": None, "usage": {"input_tokens": 1, "output_tokens": 1}}
    stop = "tool_use" if block["type"] == "tool_use" else "end_turn"
    if not stream:
        m = dict(msg); m["content"] = [block]; m["stop_reason"] = stop
        return "application/json", json.dumps(m).encode()
    if block["type"] == "tool_use":
        start = {"type": "tool_use", "id": block["id"], "name": block["name"], "input": {}}
        delta = {"type": "input_json_delta", "partial_json": json.dumps(block["input"])}
    else:
        start = {"type": "text", "text": ""}
        delta = {"type": "text_delta", "text": block["text"]}
    ev = [("message_start", {"type": "message_start", "message": msg}),
          ("content_block_start", {"type": "content_block_start", "index": 0, "content_block": start}),
          ("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": delta}),
          ("content_block_stop", {"type": "content_block_stop", "index": 0}),
          ("message_delta", {"type": "message_delta", "delta": {"stop_reason": stop, "stop_sequence": None}, "usage": {"output_tokens": 1}}),
          ("message_stop", {"type": "message_stop"})]
    return "text/event-stream", sse(ev)

class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('content-length', 0)))
        m = re.search(rb'PROBE-([A-Za-z0-9_-]+)', body)
        sub = os.path.join(OUT, m.group(1).decode() if m else '_other'); os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, f"req-{next(n)}.json"), 'wb') as f: f.write(body)
        try: j = json.loads(body)
        except Exception: j = {}
        stream = bool(j.get("stream"))
        tools = [t.get("name") for t in j.get("tools", []) if isinstance(t, dict)]
        rd = re.search(rb'READ=([^\s"\\]+)', body)
        if b'"tool_result"' in body or not rd or "Read" not in tools:
            block = {"type": "text", "text": "done"}
        else:
            block = {"type": "tool_use", "id": "toolu_probe_1", "name": "Read", "input": {"file_path": rd.group(1).decode()}}
        ctype, payload = reply(stream, block)
        self.send_response(200); self.send_header('content-type', ctype); self.send_header('content-length', str(len(payload))); self.end_headers(); self.wfile.write(payload)
    def do_GET(self):
        self.send_response(404); self.end_headers()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1])), H).serve_forever()
