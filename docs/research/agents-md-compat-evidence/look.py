# For each probe tag: per request, which instruction files appear ("Contents of ... (") and which MARKER-* occur,
# plus whether the request carries a tool_result and whether that result looks like an error.
import json, glob, re, os, sys
def texts(o):
    if isinstance(o, dict):
        for v in o.values(): yield from texts(v)
    elif isinstance(o, list):
        for v in o: yield from texts(v)
    elif isinstance(o, str): yield o
root = sys.argv[1]
for d in sorted(glob.glob(os.path.join(root, 'cap', sys.argv[2] + '*'))):
    files = sorted(glob.glob(os.path.join(d, 'req-*.json')), key=lambda p: int(re.search(r'req-(\d+)', p).group(1)))
    print('==', os.path.basename(d), len(files), 'requests')
    for f in files:
        raw = open(f, encoding='utf-8').read()
        try: j = json.loads(raw)
        except Exception: print('  ', os.path.basename(f), 'not json'); continue
        if not j.get('tools'): continue
        s = '\n'.join(texts(j))
        heads = sorted(set(h.split('agents-md-compat')[-1] for h in re.findall(r'Contents of (.*?) \(', s) if 'agents-md-compat' in h))
        marks = {}
        for m in re.findall(r'MARKER-[A-Z0-9-]+', s): marks[m] = marks.get(m, 0) + 1
        tr = '"tool_result"' in raw
        err = bool(re.search(r'"is_error":\s*true', raw))
        print('  ', os.path.basename(f), 'tool_result' if tr else 'first', 'ERR' if err else '', heads, marks)
