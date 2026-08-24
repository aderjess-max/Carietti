# The weekly signal searches

Run these every Monday. They generate the target list; a static list of names goes stale in
six weeks. Target **15 qualified companies per week**, discard anything scoring under 40.

## Search 1 — the primary (outranks the rest combined)

Companies hiring AEs or SDRs with **no** VP Sales / Head of Sales / CRO in place.

**LinkedIn Sales Navigator** — save these as a lead search:
- Industry: Hospitals and Health Care, Wellness and Fitness Services, Software Development
- Headcount: 11–50, 51–200
- Keywords in company: `digital health` OR `behavioral health` OR `telehealth` OR
  `employee benefits` OR `care navigation` OR `population health` OR `virtual care`
- Then for each hit, run a people search on that company for `VP Sales` OR `Head of Sales`
  OR `Chief Revenue` OR `CRO`. **No result is the signal.**

**Job boards** — same filter, checked weekly:
- Wellfound: search `Account Executive` + Healthcare + Seed/Series A
- Built In NYC / Built In: Healthtech, Sales, 11–200 employees
- YC job board: filter Healthcare, roles tagged Sales
- Paraform, Rippling Jobs, Ashby-hosted boards

## Search 2 — stale leadership req

`VP of Sales` or `Head of Sales` roles at digital health companies, posted more than 60 days
ago or re-posted. LinkedIn shows posting age. A req they can't fill means you're the bridge.

## Search 3 — funding window

Series A raised **9–24 months ago**. Under 9 is too early, over 30 usually means resolved
or stalled.

- Rock Health quarterly funding reports and their weekly digest
- Fierce Healthcare digital health funding coverage
- Behavioral Health Business — the best source for the mental health and SUD segment
- MedCity News, AlleyWatch for NYC
- Crunchbase or Tracxn saved search if you buy one

## Search 4 — the people signals

- **First sales hire departed inside 18 months** — LinkedIn tenure check on company alumni
- **Founder still listed on the demo or contact page** — check the company's own site
- **New segment or geography announced** in the last six months — press releases, company
  LinkedIn posts

## Adjacent target class worth its own pass

**Companies selling into employers and health plans** that aren't strictly digital health —
benefits navigation, specialty pharmacy, care management, financial wellbeing. Same buyer,
same committee, same procurement cycle, and your BI WORLDWIDE and VIVIO experience covers it
directly. Thin competition from fractional sales leaders who only know SaaS.

## Scoring

Use the rubric in `.claude/skills/prospect/references/signals.md`. Anything 40+ goes into
`pipeline/targets.csv` via `python3 scripts/pipeline.py add`. Under 40 gets discarded without
sentiment — a thin list worked hard beats a fat list worked never.
