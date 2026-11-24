import json, glob, re, os, sys

def texts(o):
    if isinstance(o, dict):
        for v in o.values(): yield from texts(v)
    elif isinstance(o, list):
        for v in o: yield from texts(v)
    elif isinstance(o, str):
        yield o

root, prefix = sys.argv[1], sys.argv[2]
for d in sorted(glob.glob(os.path.join(root, 'cap', prefix + '*'))):
    files = sorted(glob.glob(os.path.join(d, 'req-*messages*.json')), key=lambda p: int(re.search(r'req-(\d+)', p).group(1)))
    if not files:
        print(os.path.basename(d), 'NO REQUEST'); continue
    s = '\n'.join(texts(json.load(open(files[0], encoding='utf-8'))))
    heads = [h.split('agents-md-compat')[1] for h in re.findall(r'Contents of (.*?) \(', s) if 'agents-md-compat' in h]
    marks = {}
    for m in re.findall(r'MARKER-[A-Z0-9-]+', s): marks[m] = marks.get(m, 0) + 1
    print(f"{os.path.basename(d):8} files={heads}  markers={marks}")
