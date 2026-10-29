# Installing the Missing Middle

**Community compute. Useful heat. Local ownership.**

A business plan by Luke Nathan Hayes for joint development with Megan and Brad: a national installation business within a federation of people and corporate vehicles.

[Open the website](https://auraofintelligence.github.io/installing-the-missing-middle/) · [Presentation view](https://auraofintelligence.github.io/installing-the-missing-middle/presentation.html) · [PDF plan](https://auraofintelligence.github.io/installing-the-missing-middle/downloads/Installing-the-Missing-Middle-Plan.pdf) · [Editable Word plan](https://auraofintelligence.github.io/installing-the-missing-middle/downloads/Installing-the-Missing-Middle-Plan.docx)

## The proposal

The starting basis is a future population of 30 million and one single-rack node per 10,000 people: 3,000 nodes. All postcodes enter outreach together; installations progress through participating people, facilities, workloads and finance. The programme combines UPS, useful heat, 360/XR installation learning, co-operative ownership, finite investor returns and hardware renewal.

Brad builds the core delivery team through his data-centre industry experience and contacts. Megan develops institutional relationships and commercial arrangements. Luke carries the integrated architecture, applications, federation and progression plans.

## What is included

- Twelve full plan chapters plus presentation view, source library, project connections, downloads, licence and sitemap.
- 17 large uncropped chapter-specific concept heroes, reused with provenance from connected source projects.
- A register of all 14 supplied documents and 14 supplied project/repository links.
- Original downloads, searchable reading copies, extracted source-link records and file hashes.
- Matching PDF, Word and Markdown editions from one manuscript.
- Separate component briefs for Brad, Megan and Luke, a current-direction record, and agent instructions.
- Responsive navigation, previous/next routes, floating return-to-top control, source search and an illustrative capital calculator.

13 of 14 exact supplied originals are mirrored. The complete register identifies the remaining edition awaiting transfer: Local Government Funding Inquiry Submission(20261029-080754).pdf. No different edition has been substituted.

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
