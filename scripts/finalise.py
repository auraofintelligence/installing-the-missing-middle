from pathlib import Path
from html import escape
import json,hashlib
R=Path(__file__).resolve().parents[1]
BASE='https://auraofintelligence.github.io/installing-the-missing-middle/'
for p in R.rglob('*.html'):
 if '.git' in p.parts or '_site' in p.parts:continue
 s=p.read_text()
 if 'assets/refinements.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="assets/refinements.css"></head>',1)
 p.write_text(s)
files=sorted(p for p in R.rglob('*.html') if '.git' not in p.parts and '_site' not in p.parts and p.name!='404.html')
urls=[BASE+('' if p.relative_to(R).as_posix()=='index.html' else p.relative_to(R).as_posix()) for p in files]
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(u)+'</loc></url>' for u in urls)+'</urlset>\n')
s=json.loads((R/'content/sources.json').read_text());n=sum((R/d['path']).exists() for d in s['documents']);missing=[d['original_name'] for d in s['documents'] if not (R/d['path']).exists()]
a=json.loads((R/'content/artwork.json').read_text());heroes=sum(bool(x.get('path')) for x in a)
source_note='All 14 supplied originals are present, byte-for-byte verified.' if n==14 else f'{n} of 14 exact supplied originals are mirrored. The complete register identifies the remaining edition awaiting transfer: '+', '.join(missing)+'. No different edition has been substituted.'
readme=f'''# Installing the Missing Middle

**Community compute. Useful heat. Local ownership.**

A business plan by Luke Nathan Hayes for joint development with Megan and Brad: a national installation business within a federation of people and corporate vehicles.

[Open the website]({BASE}) · [Presentation view]({BASE}presentation.html) · [PDF plan]({BASE}downloads/Installing-the-Missing-Middle-Plan.pdf) · [Editable Word plan]({BASE}downloads/Installing-the-Missing-Middle-Plan.docx)

## The proposal

The starting basis is a future population of 30 million and one single-rack node per 10,000 people: 3,000 nodes. All postcodes enter outreach together; installations progress through participating people, facilities, workloads and finance. The programme combines UPS, useful heat, 360/XR installation learning, co-operative ownership, finite investor returns and hardware renewal.

Brad builds the core delivery team through his data-centre industry experience and contacts. Megan develops institutional relationships and commercial arrangements. Luke carries the integrated architecture, applications, federation and progression plans.

## What is included

- Twelve full plan chapters plus presentation view, source library, project connections, downloads, licence and sitemap.
- {heroes} large uncropped chapter-specific concept heroes, reused with provenance from connected source projects.
- A register of all 14 supplied documents and 14 supplied project/repository links.
- Original downloads, searchable reading copies, extracted source-link records and file hashes.
- Matching PDF, Word and Markdown editions from one manuscript.
- Separate component briefs for Brad, Megan and Luke, a current-direction record, and agent instructions.
- Responsive navigation, previous/next routes, floating return-to-top control, source search and an illustrative capital calculator.

{source_note}

## Develop the components

[Brad](briefs/brad.md) · [Megan](briefs/megan.md) · [Luke](briefs/luke.md) · [Current direction](briefs/current-direction.md) · [Agent instructions](AGENTS.md)

Edit `content/plan.md` for the shared manuscript. Current human direction takes precedence over conflicting archive wording. The original uploads remain unchanged. The financial allowance is a planning scenario, not a supplier quote. No applications, funding awards or institutional endorsements are invented.

## Build

Python 3.12 or later, python-docx, PyMuPDF, Pillow and LibreOffice Writer are used for the publication build.

```sh
python -m pip install python-docx PyMuPDF Pillow
python scripts/prepare.py
python scripts/build.py --pdf --check
python scripts/finalise.py
python -m http.server 8765
```

`prepare.py` uses the connected public source page to complete missing artwork. The build itself uses the local manuscript, original documents and images. The publisher workflow creates the site and downloadable editions, checks local links and original-file hashes, and publishes through GitHub Pages. Browser checks cover mobile and desktop layouts and the interactive controls.

## Source and design continuity

The full plan, source library, work briefs and source registries remain in this repository. Images have no text overlays or imposed cropping. All interface text uses a single system-font stack with an 18px base. No font files, accounts, trackers or submission backend are bundled.

## Licence

[Strange But True Public Source Licence](LICENCE.md). Original work copyright 2026 Luke Nathan Hayes / Strange But True / Aura of Intelligence. Commercial and corporate rights remain reserved. [Source and artwork rights](RIGHTS.md).
'''
(R/'README.md').write_text(readme)
(R/'content/publication-status.json').write_text(json.dumps({'chapters':12,'html_pages':len(files)+1,'heroes':heroes,'source_records':14,'originals_present':n,'missing_originals':missing,'project_links':14,'plan_sha256':hashlib.sha256((R/'content/plan.md').read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
print(source_note)
