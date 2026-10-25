import json
d = json.load(open('pcw.json', encoding='utf-8'))
paths = [t['path'] for t in d.get('tree', [])]
print(len(paths))
hits = [p for p in paths if p.endswith('.md') and '2020' in p]
for p in hits:
    print(p)
