# Resume

Source of truth for Jess Ferretti's resume.

## Two variants

Both build from the same record. They differ only in the intro and the market framing —
the experience, awards, and education are identical.

| Variant | File | Use it for |
|---|---|---|
| **Digital health** | `Jess-Ferretti-Resume` | The practice. The one to lead with. |
| **General** | `Jess-Ferretti-Resume-General` | Roles and industries outside digital health. |

What actually swaps: the tagline, the opening two paragraphs, the recovery paragraph, the
Carietti descriptor, the Ferrandino closing bullet, and the Where I Sell rows. All six live
in the `VARIANTS` table at the top of `build_resume.js` — add a variant by adding a key.

The general cut leads on the shape of the sale (long-cycle, multi-stakeholder, built from
nothing or run at scale) rather than the category, and widens Where I Sell to the full
industry set — automotive, manufacturing, retail and CPG, facilities and construction —
which is real history the digital health cut deliberately suppresses.

## Files

| File | What it is |
|---|---|
| `resume.md` | Readable source of truth for the copy. Edit here first. |
| `build_resume.js` | Renders both variants into formatted `.docx` files (docx-js). |
| `Jess-Ferretti-Resume.docx` / `.pdf` | Digital health cut. |
| `Jess-Ferretti-Resume-General.docx` / `.pdf` | General cut. |

## Rebuilding

```bash
npm install          # first time only
node build_resume.js # writes both .docx files
soffice --headless --convert-to pdf --outdir . Jess-Ferretti-Resume.docx
soffice --headless --convert-to pdf --outdir . Jess-Ferretti-Resume-General.docx
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
- **Do not put the productized offer structure on the resume.** The six-month fixed term,
  the three-slot ceiling, the terminal-deliverable gate and the $2–10M ICP band are real
  and they stay in `CLAUDE.md`, the SOW and the sales conversation — but on the resume they
  read as a product spec that lets a reader disqualify themselves before replying. Her call,
  2026-09-02: be fluid about what she takes on to start. The resume describes capability and
  a range of engagement shapes; the structure gets introduced once there is a conversation.
