"""Recover exact supplied originals from public source repositories; never substitute editions."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, os, urllib.request, urllib.parse, re, time
ROOT=Path(__file__).resolve().parents[1]
OWNER='auraofintelligence'
FILES=[
('D01','A Fair Go for the AI Age_ Postcode-Level Sovereign Compute as Shared National Infrastructure(20261029-080505).docx','694400948fb1991cf8db3a7608f03af434ffcf49','National infrastructure submission'),
('D02','AUKUS_Public_Inquiry_Submission_Luke_Nathan_Hayes_2026(20261029-080505).docx','fc4dd5a911c01f39528923d2629bacbc6b2cf96a','AUKUS public inquiry submission'),
('D03','Aura_Genesis_Children_and_Teens_Australian_Care(2).docx','5a4f3dab52525c63be52b7554caa1aa8a62a4111','Children and young people in Australian care'),
('D04','Aura_Genesis_Geode_Development_Edition_3(4).pdf','4d362193afda17a5ffe5955901812fddf98ff056','Aura Genesis Geode Development, edition 3'),
('D05','Aura_Teacher_Training_60_Days(7).pdf','65853657f9f1e10b680d11c5475185bfec9d09d3','Aura Teacher Training: 60 Days'),
('D06','Aura_of_Intelligence_Adaptive_Whole_of_Life_Support(2).docx','50dfd1e7453876f76ce78d33a7a9d6d9ae3a146e','Adaptive whole-of-life support'),
('D07','Aura_of_Intelligence_Tourism_and_Domestic_Travel(2).docx','fa0b68cffb3bf36009c30dea04a8f727fa86c520','Tourism and domestic travel'),
('D08','Building an Australian Legal RAG System(20261029-080516).pdf','73ba95dea4085719b8f292e9e6042924666fd3f8','Australian legal intelligence architecture'),
('D09','Do Not Put All Our Eggs in One Basket(9).docx','4f127fe47da66e0823cd755c12ff3412dd143627','Distributed compute discussion paper'),
('D10','Fiji_Australia_Vuvale_Union_Submission_Luke_Nathan_Hayes_2026(20261029-080505).docx','993a79420e2d09781faa943e5858887f1403eac6','Fiji–Australia Vuvale Union submission'),
('D11','Local Government Funding Inquiry Submission(20261029-080754).pdf','b28410f92a996e11da47511828230232ecb9a130','Local government funding submission'),
('D12','Ocean_of_Peace_Alliance_Veitacini_Treaty_Submission_Luke_Nathan_Hayes_2026(20261029-080506).docx','ae5697a50652fd89896d24acc3e7b0424bec223d','Ocean of Peace / Veitacini submission'),
('D13','SETCo 2026 Pitch Plan Revision(20261029-080533).pdf','f7bd8d246ba8483f087d9b83b25b3aebe50630dd','Ready SET strategy archive'),
('D14','Web3 Sensorium for Science Debate(20261029-083308).pdf','2aa8f529e1bddc6bd921766d6653fb9392af5220','Global Sensorium: scientific models and debate')]
LINKS=[
('P01','UNGA81 — A fair go in the age of intelligence','https://auraofintelligence.github.io/UNGA81-Luke-Hayes/','Public-purpose and missing-middle framework'),
('P02','Ready SET Co-op Cultural Intelligence Node','https://auraofintelligence.github.io/ready-set-co-op-cultural-intelligence-node/index.html','A local rack, workloads, shared equipment and learning'),
('P03','Ready SET Co-op Trust Hub','https://auraofintelligence.github.io/ready-set-co-op-trust-hub/','Participation, relationships and shared assets'),
('P04','500 Queens Venture Capital','https://auraofintelligence.github.io/500-Queens-VC-2026/','Women-led enterprise, leadership and investment development'),
('P05','Mutual Futures','https://auraofintelligence.github.io/mutual-futures/','Business succession, ownership, learning and time'),
('P06','Australian Law 2012 and Your Relevance','https://auraofintelligence.github.io/australian-law-2012-lukes-relevance/','Personal and project-specific legal relevance'),
('P07','Australian Legal Engine','https://github.com/auraofintelligence/australian-legal-engine','Source-linked legal intelligence development'),
('P08','Legal Memory Workbench','https://auraofintelligence.github.io/legal-memory-workbench/','Project context and legal research preparation'),
('P09','C-Hour Introduction','https://auraofintelligence.github.io/C-Hour-introduction/','Voluntary contribution and non-monetary reciprocity'),
('P10','P4A','https://p4a.xyz/','Civic development, councils, divisions and electorate twins'),
('P11','Aura Genesis Geode Atlas','https://auraofintelligence.github.io/aura-genesis-geode-atlas/','Genesis, Geode development and teacher learning'),
('P12','Oceania Healthy De-Slop Co-ops','https://auraofintelligence.github.io/Oceania-healthy-de-slop-co-ops/','Locally shaped wellbeing co-operatives'),
('P13','82 Claytons Road Anglican partnership proposal','https://github.com/auraofintelligence/Anglican-Diocese-82-Claytons-Amity','Aged care, longevity and community assets'),
('P14','Installing the Missing Middle — source repository','https://github.com/auraofintelligence/installing-the-missing-middle','This presentation, source register and shared development briefs')]
def get(url):
 headers={'User-Agent':'Installing-the-Missing-Middle-source-check','Accept':'application/vnd.github+json'}
 if url.startswith('https://api.github.com/') and os.getenv('GH_TOKEN'): headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
 for n in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=40) as r:return r.read()
  except Exception:
   if n==2:raise
   time.sleep(n+1)
def api(path):return json.loads(get('https://api.github.com/'+path))
def blobsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def scan(repo):
 try:
  tree=api(f"repos/{OWNER}/{repo['name']}/git/trees/{repo['default_branch']}?recursive=1")
  return repo,tree
 except Exception as e:return repo,{'error':str(e),'tree':[]}
def main():
 (ROOT/'content').mkdir(exist_ok=True); (ROOT/'documents/originals').mkdir(parents=True,exist_ok=True)
 need={x[2]:x for x in FILES if not (ROOT/'documents/originals'/x[1]).exists()}
 found={}; audit=[]
 if need:
  repos=[]
  for page in range(1,10):
   batch=api(f'users/{OWNER}/repos?per_page=100&page={page}')
   repos.extend(batch)
   if len(batch)<100:break
  with ThreadPoolExecutor(max_workers=10) as pool:
   for repo,tree in pool.map(scan,repos):
    if tree.get('error'):audit.append({'repo':repo['name'],'error':tree['error']})
    if tree.get('truncated'):audit.append({'repo':repo['name'],'error':'Tree truncated; not a complete scan'})
    for item in tree.get('tree',[]):
     if item.get('sha') in need and item.get('type')=='blob':
      row=need[item['sha']]; url=f"https://raw.githubusercontent.com/{OWNER}/{repo['name']}/{tree['sha']}/{urllib.parse.quote(item['path'])}"
      try:
       b=get(url)
       if blobsha(b)!=row[2]:raise ValueError('Original hash mismatch')
       (ROOT/'documents/originals'/row[1]).write_bytes(b);found[row[2]]=url
      except Exception as e:audit.append({'repo':repo['name'],'error':str(e)})
 oldpath=ROOT/'content/sources.json'; old={x['id']:x for x in json.loads(oldpath.read_text()).get('documents',[])} if oldpath.exists() else {}
 docs=[]
 for id,name,sha,title in FILES:
  path=ROOT/'documents/originals'/name; exists=path.exists()
  if exists and blobsha(path.read_bytes())!=sha:raise ValueError('Changed original: '+name)
  docs.append({'id':id,'title':title,'original_name':name,'path':'documents/originals/'+name,'git_blob':sha,'sha256':hashlib.sha256(path.read_bytes()).hexdigest() if exists else None,'bytes':path.stat().st_size if exists else None,'available':exists,'source_url':found.get(sha,old.get(id,{}).get('source_url'))})
 (ROOT/'content/sources.json').write_text(json.dumps({'documents':docs,'links':[dict(zip(['id','title','url','purpose'],x)) for x in LINKS]},ensure_ascii=False,indent=2)+'\n')
 (ROOT/'content/source-import-report.json').write_text(json.dumps({'matched':sum(d['available'] for d in docs),'expected':len(docs),'missing':[d['original_name'] for d in docs if not d['available']],'scan_notes':audit},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'matched':sum(d['available'] for d in docs),'expected':len(docs),'missing':[d['original_name'] for d in docs if not d['available']]},indent=2))
if __name__=='__main__':main()
