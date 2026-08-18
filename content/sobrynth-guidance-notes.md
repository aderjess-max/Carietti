# Editor's notes — "Guidance Instead of Guesswork"

Article: `content/sobrynth-guidance-instead-of-guesswork.md`
Cover images: `assets/cover-sobrynth-A.png` (recommended) and `assets/cover-sobrynth-B.png`, both 1200×644.
Sources: `assets/cover-sobrynth-*.html` + `assets/cover-sobrynth.css`, rendered with `python3 assets/shoot-cover.py`.

## Sobrynth brand, pulled from the overview deck

sobrynth.com is unreachable from this environment, so the covers are built from the branding
inside `Sobrynth_Overview_Deck.pptx` — theme colors counted across all 25 slides, plus the logo
art lifted straight out of the deck. Everything lives in `assets/cover-sobrynth.css` as tokens,
so a brand change is a one-line edit.

| Token | Hex | Where it comes from |
|---|---|---|
| `--purple-deep` | `#3A2C73` | deck headline purple |
| `--purple` | `#4F3E93` | primary purple |
| `--purple-mid` | `#58488C` | most-used color in the deck after white |
| `--lilac` | `#E0DAEA` | panel tint |
| `--lilac-light` | `#AFA9EC` | eyebrows on dark |
| `--ink` | `#1F1A2E` | body text |
| `--orange` | `#EC8B3E` | the accent — second most-used color in the deck |
| `--orange-light` | `#FAA95F` | accent on dark |
| `--paper` | `#F4F2EF` | warm off-white ground |
| `--grey` | `#6B6B76` | secondary text |

Logos extracted to `assets/sobrynth/`: `logo-full-color.png` (white background knocked out to
transparent so it sits on the warm paper), `logo-reversed.png` for dark grounds, and
`mark-maze.png`, the standalone labyrinth mark.

Type: the deck uses **Roboto Serif** for display and **Roboto Light** for body. Neither is
installed here, so the renders substitute DejaVu Serif and DejaVu Sans. The CSS names the Roboto
faces first — re-render on a machine with Roboto installed and the covers pick them up with no
other change. They will get slightly narrower, so glance at the line breaks if you do.

The maze mark carries the article: a family navigating treatment is literally in a labyrinth, and
that is already Sobrynth's own metaphor. It's why cover A puts it in its own panel rather than
tucking it in a corner.

## What changed and why

1. **Structure.** Added six section headers. LinkedIn articles are scanned before they're read, and headers let a benefits leader skim to "What it costs the employer" and then go back to the top.
2. **Added the two numbers the piece was missing.** A story alone doesn't move a benefits budget. Now attributed inline: NSC/NORC's ~$8,500 per year per affected person (their calculator counts dependents, which is exactly the article's point), and Pew's 46% of U.S. adults with a family member or close friend who's been addicted. Two is the right number — more turns it into a whitepaper.
3. **"She had the leave. What she didn't have was a plan."** New pivot line, and the hinge the whole article turns on.
4. **Made the search concrete.** "Hold music. A list of facilities she had no way to evaluate and no one to evaluate it with." Specific beats summarized — and "which one just bought the top search result" is a detail every parent who has done this recognizes instantly.
5. **Named the invisible cost.** Added: none of this shows up on a dashboard labeled "substance use" — it shows up as leave, attrition, and a claim nobody saw coming. That reframes the piece from sympathy to a P&L problem.
6. **Sharpened the Sobrynth section** with the specifics from the product: certified peer recovery coaches, lived experience, 24/7, confidential, no session limits, uncapped and extending to loved ones. Added "still on the phone in week eleven, not just week one" — it's what actually differentiates peer support from a directory.
7. **Tightened throughout** — cut the doubled "for employers" framing and the repeated "the goal is" construction, trimmed roughly 15% of the words without losing a beat.
8. **Gave it an ask.** The original just ended. Now it closes with one question a benefits leader can take into their next meeting, then a direct invitation. Direct, not coy.
9. Fixed "Guess Work" → "guesswork" (one word).

## Two things to check before publishing

- **FMLA.** Leave to care for an adult child generally requires that the child be incapable of self-care because of a disability — a nuance a benefits audience may catch. The line as written ("took leave under FMLA") is fine if that's what happened in the real case. If it isn't, "took leave" alone is safer and loses nothing.
- **The client's voice.** The piece says "we" and "our peer recovery coaches." That's correct if it publishes under your byline as Sobrynth's VP of Sales, Fractional, which the sign-off states. Worth a read from Sobrynth's side before it goes up.

## Alternate titles

The current title is the thesis, so it earns its place. If you want to test a sharper one:

- *Her Son Was Struggling. She Was the One Who Left Work.*
- *The Employee Your Benefits Plan Can't See*

## Companion feed post

Article links suppress reach — her link-share post did 619 impressions against 2,267 for a native image post. So don't share the article as a link. Post this natively with cover image B (`assets/cover-sobrynth-B.png`), and put the article URL in the first comment.

> A high-performing employee took FMLA leave last year.
>
> Not because she was sick. Because her college-aged son was.
>
> Overnight she became a care navigator, an insurance expert, a treatment researcher, and a crisis manager — none of which she was trained for, all of which she did on hold with a call center.
>
> She had the leave. What she didn't have was a plan.
>
> Here's what I keep seeing: benefits are built around the person with the diagnosis. But 46% of American adults have a family member or close friend who's been addicted to drugs. In any workforce, the people carrying someone else's crisis outnumber the people currently in treatment — and they never show up in a benefits report. They show up in leave requests and resignations coded "personal reasons."
>
> I wrote about what it costs employers when a family has to guess, and what changes when they don't.

Post Tue–Thu, 7:30–9:00am ET. No hashtags. Clear two hours after and reply to every comment inside 90 minutes.
