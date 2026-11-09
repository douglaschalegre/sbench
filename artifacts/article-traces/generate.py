"""Generate log-only article figures. Metadata selection is documented in provenance.json."""
from pathlib import Path
import json
import html
import hashlib

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BASE = ROOT / 'runs/20260615T221949Z/entries/community_workshop_replan'
logs = {h: (BASE/h/'r3/stdout.log').read_text().splitlines() for h in ['codex','opencode','bdi']}
manifest = []

def event(h, n):
    manifest.append({'harness':h,'line':n})
    return json.loads(logs[h][n-1])

def format_event(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)

# Retain original JSON structure and values, selecting relevant fields.
c38 = event('codex',38)
c42 = event('codex',42)
codex = format_event({'type':c38['type'],'item':{k:c38['item'][k] for k in ['type','command','aggregated_output','exit_code','status']}})+'\n\n'+format_event(c42)
o31 = event('opencode',31)
o35 = event('opencode',35)
opencode = format_event({'type':o31['type'],'part':{'tool':o31['part']['tool'],'state':{'status':o31['part']['state']['status'],'input':o31['part']['state']['input']}}})+'\n\n'+format_event({'type':o35['type'],'part':{'reason':o35['part']['reason']}})
# Contiguous excerpts, separated only by whitespace. No invented log lines.
bdi_ranges = [(22,28),(37,37),(43,46),(55,57)]
bdi = '\n\n'.join('\n'.join(logs['bdi'][a-1:b]) for a,b in bdi_ranges)
manifest.extend({'harness':'bdi','lines':[a,b]} for a,b in bdi_ranges)
css = '''
+*{box-sizing:border-box}
+body{margin:0;background:#fff;color:#20252c}
+main{padding:30px 36px;background:#fff}
+pre{margin:0;font:17px/1.65 Menlo,Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;tab-size:2}
+.dark{background:#14191f;color:#e5e9ee}
+.dark main{background:#14191f}
+@media(max-width:600px){main{padding:20px}pre{font-size:14px}}
+@media print{main{padding:20px}}
+'''.replace('\n+','\n')
figures = [('01-codex-log',codex,False),('02-opencode-log',opencode,False),('03-bdi-log',bdi,False),('04-bdi-log-dark',bdi,True)]
# Retire the previous editorial figures so the deliverable contains log-only images.
for stem in ['01-trace-excerpts','02-comparison-lanes','03-replanning-closeup','04-termination']:
    for ext in ['html','png','pdf']:
        (OUT/f'{stem}.{ext}').unlink(missing_ok=True)
for name, text, dark in figures:
    doc = '<!doctype html><html><meta charset="utf-8"><style>'+css+'</style><body'+(' class="dark"' if dark else '')+'><main><pre>'+html.escape(text)+'</pre></main></body></html>'
    (OUT/f'{name}.html').write_text(doc)
    (OUT/f'{name}.txt').write_text(text+'\n')
(OUT/'provenance.json').write_text(json.dumps({'sources':{h:{'path':str((BASE/h/'r3/stdout.log').relative_to(ROOT)),'sha256':hashlib.sha256((BASE/h/'r3/stdout.log').read_bytes()).hexdigest()} for h in logs},'selection':manifest,'formatting':'JSON pretty-printed. Codex line 38 and OpenCode events retain selected original fields and hierarchy. Codex line 42 is complete. BDI excerpts are literal contiguous ranges separated by blank lines. No labels or editorial text rendered.'},indent=2))
print('Generated four log-only figures.')
