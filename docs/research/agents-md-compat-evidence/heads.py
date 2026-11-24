import json, glob, re, sys
def texts(o):
    if isinstance(o, dict):
        for v in o.values(): yield from texts(v)
    elif isinstance(o, list):
        for v in o: yield from texts(v)
    elif isinstance(o, str): yield o
f = sorted(glob.glob(f'cap/{sys.argv[1]}/req-*messages*'), key=lambda p: int(re.search(r'req-(\d+)', p).group(1)))[0]
s = '\n'.join(texts(json.load(open(f, encoding='utf-8'))))
print(f); print(re.findall(r'Contents of (.*?) \(', s))
for needle in sys.argv[2:]: print(repr(needle), needle in s)
