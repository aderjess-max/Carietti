# Fractional VP of Sales Practice — Working Context

Persistent context for building and iterating on this practice. Update as facts change.

## Goal

**$400K collected revenue in year one** from a solo fractional VP of Sales practice.

## Operator profile

- 23 years sales experience; quotas carried up to **$12M**
- Verticals: digital healthcare, B2B SaaS, automotive, commercial construction
- Based on **Long Island, NY**. Works **fully remote** — national reach, NY metro is the beachhead not the boundary
- Currently holds **two 1099 fractional engagements** (open-ended, full-time-ish framing)
- Starting the new practice model **week of 2026-08-16**

## Financial parameters

| | |
|---|---|
| Bridge income (current 1099 work) | ~$12.5K/mo |
| Personal income floor | ~$17.5K/mo |
| Current monthly gap | ~$5K short |
| Bridge time load | 10–20 hrs/week ≈ 1 slot |
| Bridge exit terms | At-will, can stop anytime |

## The offer

**6-month engagements**, 3 concurrent slots maximum.

Deliverables: ICP + segmentation, full sales narrative/pitch, email templates, outreach cadences,
sales process + stages, tech stack selection and implementation, CRM stood up and live,
enablement/ramp plan, and finally **hiring their VP of Sales** (the successor).

### Pricing (locked)

| Tier | Total | Rate | For |
|---|---|---|---|
| Foundation | $72K | $12K/mo | Pre-A, under ~$2M |
| **Founder to Team** (core) | **$96K** | **$16K/mo** | $2–10M — the target deal |
| Scale Engine | $120K | $20K/mo | $10M+, multi-segment |

Raise to $84K / $102K / $120–135K at month 9.

### Payment terms

**40 / 30 / 30** — 40% at signature (non-refundable), 30% at month-3 artifact gate,
30% at terminal deliverable (default: VP offer accepted). Every SOW gets a **date ceiling**
on the final trigger: "VP hired, or month 7, whichever comes first."

### Back-end levers

- **VP placement fee**: 20% of first-year base, $35K floor (~$40–50K typical). Half on offer acceptance, half at day 90. **Disclose in the MSA.**
- **Post-engagement advisory**: $4,500/mo, 6-month minimum ($27K). Coach the VP placed.
- **Equity**: 0.25–0.5% for ≤20% of cash fee. Seed only. **One slot at a time, maximum.**

## Key decisions made

1. **Price is not the constraint — pipeline is.** $400K ÷ 3 slots ÷ 12 mo = $11,111/slot/mo, below the $11,732 market average. At a realistic 70% year-one utilization the required rate is $16K/mo.
2. **Do not discount the first client.** The bridge income removes the cash pressure that normally forces it. Buy proof with *scope* (sell Foundation at $72K) — never with rate.
3. **Bridge exit is a condition, not a date: give notice the week client two signs.** Two engagements ≈ 1.8× floor and capacity is spent. Holding longer trades a $96K slot for $12.5K/mo.
4. **Build the reusable asset library in months 1–2**, while the bridge covers the floor and the calendar is open. It is the load-bearing element that makes 3 concurrent engagements survivable.
5. **Lead with two verticals: digital health + commercial construction / contech.** Not four. ~9,000 fractional sales leaders in US/Canada, overwhelmingly SaaS-generalist — generic positioning gets rate-compared to $10K/mo marketplace operators. Remote work makes vertical depth *more* important, not less.
6. **The wedge**: *"I'm hired to make myself unnecessary in six months. The last thing I deliver is the person who replaces me."* Market average engagement is 9.7 months and drifts; a defined exit is the differentiator.

## Revenue model (year one)

| Scenario | Signed | Bridge | Retainer | Placements | Advisory | Collected |
|---|---|---|---|---|---|---|
| Floor (bridge to M10) | 3 | $125K | $202K | $40K | $9K | **$376K** |
| Base (bridge to M8) | 4 | $100K | $271K | $40K | $14K | **$425K** |
| Target (bridge to M6) | 5 | $75K | $371K | $80K | $27K | **$553K** |

Bridge and signings move inversely — the bridge occupies a slot.

## Origination math

150 targeted conversations → 50 qualified calls → 15 proposals → **5 signed**.
≈ 13 conversations and 4 qualified calls per month. ~25 outbound actions/week.

Channel targets: VC/PE platform partners 2–3 deals · warm network 1–2 · recruiter referral swap 1 · vertical communities 1 · marketplaces as gap-filler.

## Top risks

1. **Holding the bridge past the trigger** — most likely way this underperforms
2. **Origination stops during delivery** — month 4 is the danger point
3. The $5K gap tempting an early cheap deal
4. Three concurrent tactical builds without the asset library
5. Placement fee read as a conflict (mitigate: disclose in MSA)
6. Slow client hiring holding the final 30% (mitigate: date ceiling)

## Artifacts

- **Strategy, research and pricing**: https://claude.ai/code/artifact/7985cfd3-122f-446a-af21-4bae3f71694c
- **Launch playbook, plays and target list**: https://claude.ai/code/artifact/5cbaaef2-2819-4942-bb24-1626ba17de2a (`launch-playbook.html`)

## The prospecting agent

A Claude Code skill at `.claude/skills/prospect/` that sources targets, scores them against
buying signals, drafts outreach from the plays, and stages Gmail drafts for human review.
**It never sends.** Setup and usage in `SETUP.md`.

- `/prospect monday` — the full weekly origination block
- `/prospect source` · `/prospect research <company>` · `/prospect draft` · `/prospect due` · `/prospect status`

State lives in `pipeline/targets.csv` and `pipeline/touches.csv` (plain CSV, Excel-friendly).
Run it on a local machine, not a web session — the Gmail token and pipeline need to persist.

Keep `references/plays.md` fresh: the domain-specific observations are what make the messages
land, and they should be refreshed quarterly from live engagements.

## Working agreement

- Branch: `claude/fractional-vp-sales-plan-bgy5xs`
- Keep artifacts updated in place (same URLs) rather than publishing new ones
- Update this file whenever pricing, positioning, capacity, or financial parameters change
- Log signed clients, prices actually achieved, and channel attribution as they happen — the model above should be re-cut against real data, not left as forecast
