# Resume

Source of truth for Jess Ferretti's resume.

| File | What it is |
|---|---|
| `resume.md` | Readable source of truth for the copy. Edit here first. |
| `build_resume.js` | Renders the copy into a formatted `.docx` (docx-js). |
| `Jess-Ferretti-Resume.docx` | The deliverable. Editable in Word/Google Docs, ATS-parseable. |
| `Jess-Ferretti-Resume.pdf` | Send-ready PDF, rendered from the `.docx`. |

## Rebuilding

```bash
npm install          # first time only
node build_resume.js
soffice --headless --convert-to pdf --outdir . Jess-Ferretti-Resume.docx
```

Keep `resume.md` and `build_resume.js` in sync by hand — the script does not parse the
markdown, it holds its own copy of the text.

## Design notes

- Letter, 0.5"/0.62" margins, Calibri 9.5pt body. Three pages.
- Accent `#1F8A65` — the brand green `#37B98A` darkened so it stays legible in print and
  passes contrast on white.
- Dates are right-aligned with a real tab stop, not `PositionalTab`: the latter is a
  Word-only feature and renders inline in LibreOffice, Google Docs, and most PDF pipelines.
- Role headers and their descriptors carry `keepNext` so a job title never strands at the
  bottom of a page away from its bullets.

## Copy rules carried over from CLAUDE.md

- The category is always **"digital health"** — never "behavioral health" as a label.
  Depth is proven by naming mental health, substance use, and recovery specifically.
- **Never imply Sobrynth or VIVIO are six-month engagements.** They are open-ended
  contracts. The productized six-month engagement is the offer, described under Carietti.
- Carietti is the operating entity, not a multi-principal firm. Sobrynth and VIVIO sit
  under it as engagements rather than as three parallel jobs.
- No pricing on the resume. A resume is not a rate card.
