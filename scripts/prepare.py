"""Prepare source artwork and exact original-file metadata for publication."""
from pathlib import Path
from html.parser import HTMLParser
import urllib.request,urllib.parse,json,hashlib,zipfile,io
R=Path(__file__).resolve().parents[1]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Installing-the-Missing-Middle-public-sources','Accept':'application/vnd.github+json'}),timeout=30) as r:return r.read()
a=json.loads((R/'content/artwork.json').read_text())
if not any(x.get('slug')=='law-and-stewardship' and x.get('path') for x in a):
 class Images(HTMLParser):
  def __init__(self):super().__init__();self.images=[]
  def handle_starttag(self,t,attrs):
   d=dict(attrs)
   if t=='img' and d.get('src') and not any(v in d['src'] for v in ['favicon','logo']):self.images.append(d)
 base='https://raw.githubusercontent.com/auraofintelligence/UNGA81-Luke-Hayes/main/'
 parser=Images();parser.feed(get(base+'intelligence.html').decode())
 item=next((x for x in parser.images if 'intelligence' in x['src']),parser.images[0])
 url=urllib.parse.urljoin(base+'intelligence.html',item['src']);dest='assets/heroes/law-and-stewardship.webp';(R/dest).write_bytes(get(url))
 a=[x for x in a if x['slug']!='law-and-stewardship'];a.append({'slug':'law-and-stewardship','path':dest,'alt':item.get('alt','Personal and civic intelligence concept artwork'),'source_page':'https://auraofintelligence.github.io/UNGA81-Luke-Hayes/intelligence.html','source_image':url,'note':'Concept artwork from the connected source project.'})
 (R/'content/artwork.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
# An exact uploaded original may be inside an existing public source ZIP.
# Inspect only matching-size PDF entries; do not extract or execute archive files.
target=R/'documents/originals/Local Government Funding Inquiry Submission(20261029-080754).pdf'
record=R/'content/archive-source-check.json'
if not target.exists() and not record.exists():
 expected='b28410f92a996e11da47511828230232ecb9a130';checked=[];found=None
 def inspect_zip(data,depth=0):
  if depth>1:return None
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   for entry in z.infolist():
    if entry.file_size==304726 and entry.filename.lower().endswith('.pdf'):
     b=z.read(entry)
     if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected:return b
    if depth==0 and entry.filename.lower().endswith('.zip') and entry.file_size<12000000:
     result=inspect_zip(z.read(entry),1)
     if result:return result
  return None
 repos=['500-Queens-VC-2026','UNGA81-Luke-Hayes','Anglican-Diocese-82-Claytons-Amity','mutual-futures','ready-set-co-op-trust-hub','aura-genesis-geode-atlas','Redlands_discovers_Luke_Hayes','aura-disaster-resilience','open-record-luke-nathan-hayes']
 for repo in repos:
  if found:break
  try:
   tree=json.loads(get(f'https://api.github.com/repos/auraofintelligence/{repo}/git/trees/main?recursive=1'))
   for item in tree.get('tree',[]):
    if item.get('type')!='blob' or not item['path'].lower().endswith('.zip') or item.get('size',99999999)>15000000:continue
    url=f'https://raw.githubusercontent.com/auraofintelligence/{repo}/main/'+urllib.parse.quote(item['path'])
    try:
     b=inspect_zip(get(url));checked.append(url)
     if b:target.write_bytes(b);found=url;break
    except Exception as exc:checked.append({'url':url,'error':str(exc)})
  except Exception as exc:checked.append({'repo':repo,'error':str(exc)})
 record.write_text(json.dumps({'exact_original_found':bool(found),'source':found,'archives_checked':checked},ensure_ascii=False,indent=2)+'\n')
s=json.loads((R/'content/sources.json').read_text())
guides=[
('A Fair Go for the AI Age: Postcode-Level Sovereign Compute','National rationale for shared community compute.'),
('AUKUS Public Inquiry Submission','Wider national capability and public-investment context.'),
('Aura Genesis for Children and Young People in Australian Care','Child and youth learning, care continuity, Verse Box and opportunities for adulthood.'),
('Aura Genesis Geode Development, Edition 3','Genesis, personal models, materials, hub workloads and civic infrastructure; especially page 37.'),
('Aura Teacher Training: 60 Days','Sixty-day learning programme; Days 41–42 directly connect rack deployment and distributed continuity.'),
('Aura of Intelligence for Adaptive Whole-of-Life Support','Dementia, disability, ageing, personal records and changes of care or home.'),
('Aura of Intelligence for Tourism and Domestic Travel','Qualified-self development through travel; operator, volunteer and public-service connections.'),
('Building an Australian Legal RAG System','Legal intelligence design background; the current project direction governs development.'),
('Do Not Put All Our Eggs in One Basket','Distributed infrastructure discussion and carried-forward capital planning assumptions.'),
('Fiji–Australia Vuvale Union Submission','Regional relationships, ownership, workforce and public-purpose development.'),
('Local Government Funding Inquiry Submission','Civic twins, community assets and local-government funding context.'),
('Ocean of Peace Alliance / Veitacini Treaty Submission','Regional cooperation and longer-term shared capability.'),
('Ready SET Co-op: 2026 Strategy Archive','Earlier organisational and workforce design; read with current naming and the non-monetary C-Hour direction.'),
('Global Sensorium: Scientific Models and Debate','Earth-space digital twins, sensor pipelines, simulation, model comparison and community science.')]
for d,(title,note) in zip(s['documents'],guides):
 d['title']=title;d['note']=note;p=R/d['path'];d['available']=p.exists()
 if p.exists():
  b=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['git_blob'];d['bytes']=len(b);d['sha256']=hashlib.sha256(b).hexdigest()
(R/'content/sources.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
(R/'content/source-import-report.json').write_text(json.dumps({'matched':sum(d['available'] for d in s['documents']),'expected':14,'missing':[d['original_name'] for d in s['documents'] if not d['available']]},ensure_ascii=False,indent=2)+'\n')
print('Prepared artwork and',len(guides),'document guides.')
