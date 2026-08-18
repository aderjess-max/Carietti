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

## Publishing plan — two accounts

The article goes out under both names, and the order matters.

**Publish the article from her personal profile, not the Sobrynth page.** Her profile has 5,106
followers, ~345 views/week, and a live engagement history; a 2024-founded company page has none of
that, and LinkedIn throttles page reach besides. The Sobrynth byline is already in the article's
sign-off, so authorship is clear either way. Then the Sobrynth page shares it with its own
commentary — the page gets the asset in its feed without paying the page-reach penalty.

Sequence: personal post first, in the Tue–Thu 7:30–9:00am ET window. Sobrynth's page shares 60–90
minutes later, once the first wave of comments has landed. Any Sobrynth colleagues who reshare
should do it the same day with their own line of commentary — a bare repost carries far less than
a repost with a sentence attached.

## Her personal post

Post natively with cover image B (`assets/cover-sobrynth-B.png`) and put the article URL in the
first comment. Article links suppress reach — her link-share post did 619 impressions against
2,267 for a native image post — so the link never goes in the body.

> A high-performing employee took FMLA leave last year.
>
> Not because she was sick. Because her son was.
>
> He had started struggling with substance use, and overnight she became a care navigator, an insurance expert, a treatment researcher, and a crisis manager — none of which she was trained for, all of which she did on hold with a call center.
>
> She had the leave. What she didn't have was a plan.
>
> Here is the part employers miss. Benefits get built around the person with the diagnosis. But 46% of American adults have a family member or close friend who has been addicted to drugs. In any workforce, the people carrying someone else's crisis outnumber the people currently in treatment — and they never show up in a benefits report. They show up as leave requests, missed deadlines, and resignations coded "personal reasons."
>
> Meanwhile the family, navigating alone, defaults to the most visible level of care rather than the most appropriate one. The health plan absorbs that decision.
>
> I wrote this for Sobrynth, where our peer recovery coaches walk with both people — the employee and the person they love. 24/7, no session limits, and it extends to family.
>
> Link in the comments.

First comment, posted immediately after:

> Guidance Instead of Guesswork — the full piece: [article URL]

## Sobrynth's page post

Same story, institutional voice, no "I." Use cover image A (`assets/cover-sobrynth-A.png`) so the
two posts don't look like duplicates in anyone's feed.

> An employee took FMLA leave last year. Not because she was sick — because her son was.
>
> He had started struggling with substance use. Overnight she became a care navigator, an insurance expert, a treatment researcher, and a crisis manager. She did most of it on hold with a call center.
>
> She had the leave. What she didn't have was a plan.
>
> Most benefits are built around the person with the diagnosis. But 46% of American adults have a family member or close friend who has been addicted to drugs. In any workforce, the people carrying someone else's crisis outnumber the people currently in treatment — and they don't show up in a benefits report. They show up as leave requests, missed deadlines, and resignations coded "personal reasons."
>
> Meanwhile the family, navigating alone, defaults to the most visible level of care rather than the most appropriate one. The health plan absorbs that decision.
>
> Sobrynth's certified peer recovery coaches walk with both — the employee and the person they love. 24/7, confidential, no session limits, and support that extends to family.
>
> Jess Ferretti wrote about what it costs employers when a family has to guess, and what changes when they don't. Link in the comments.

## If the article gets published from the Sobrynth page instead

Then her personal post becomes a reshare with commentary — never a bare repost. Use this:

> I wrote this one for Sobrynth, but I have been carrying the story around a lot longer than that.
>
> The employee in it never had a substance use problem. Her son did. She still ended up as the one who left work, because nothing in her benefits package was built for the person standing next to the person who is struggling.
>
> I have spent the last three years selling mental health and substance use benefits to employers. This is the gap I hear about most and see addressed least. We count the employee in treatment. We don't count the three people rearranging their lives around them.
>
> That is the part Sobrynth actually fills, and it is why I am working with them.

Optional, and entirely her call: one line naming her own recovery would make this the least
fakeable post in the category. It also changes the register from professional to personal, which
is a bigger decision than a single post. Leaving it out costs nothing.

## Mechanics

Tue–Thu, 7:30–9:00am ET. No hashtags. Never edit after posting — it resets distribution. Clear two
hours afterward and reply to every comment inside 90 minutes; early comment velocity drives reach.

**Don't attach a fractional-VP ask to any of these.** It's client content, and the practice
benefit is indirect: it demonstrates category depth to exactly the buyer she sells to. Bolting a
pitch onto the end would cost more credibility than it earns.

**Why the hook works.** LinkedIn truncates at roughly 200 characters. The first three lines land
inside that window and end on "Because her son was" — the reader has to expand to find out what
happened.
