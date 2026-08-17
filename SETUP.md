# The prospecting agent — setup

A Claude Code skill that researches target companies, scores them against buying signals,
drafts outreach from the playbook, and stages everything in your Gmail drafts for review.

**It never sends.** Every message waits in drafts until you read it and hit send.

---

## Where to run it

Run this **on your own machine**, not in Claude Code on the web. Web sessions get a fresh
container each time, so the Gmail token wouldn't survive between runs and neither would your
pipeline file unless it was committed every session.

```bash
git clone https://github.com/aderjess-max/Carietti.git
cd Carietti
git checkout claude/fractional-vp-sales-plan-bgy5xs
```

Then open the folder with Claude Code (`claude` in that directory, or the desktop app).

---

## Step 1 — Works immediately, no setup

The agent runs right now with zero configuration. Without Gmail credentials it writes each
draft to `pipeline/drafts/` as a `.md` file you can read and an `.eml` file you can open in
any mail client, edit, and send.

Try it:

```
/prospect research Adaptive
```

If that's enough for you, stop here. The Gmail steps below only buy you the convenience of
drafts landing directly in your inbox.

---

## Step 2 — Gmail drafts (about 10 minutes, one time)

### 2a. Install the libraries

```bash
pip install -r requirements.txt
```

### 2b. Create a Google OAuth client

Free, and stays private to you.

1. Go to <https://console.cloud.google.com/>
2. Create a project — name it anything, "Prospecting Agent" is fine
3. Search for **Gmail API** in the top bar, open it, click **Enable**
4. Left menu → **APIs & Services** → **OAuth consent screen**
   - User type: **External**
   - App name, your email for both support and developer contact — that's all that's required
   - On the **Scopes** step, click **Add or remove scopes**, and add
     `https://www.googleapis.com/auth/gmail.compose`
   - On **Test users**, add your own Gmail address
   - Leave it in Testing mode. You never need to publish it.
5. Left menu → **Credentials** → **Create credentials** → **OAuth client ID**
   - Application type: **Desktop app**
   - Create, then **Download JSON**
6. Save that file to `.gmail/credentials.json` in this repo

```bash
mkdir -p .gmail
mv ~/Downloads/client_secret_*.json .gmail/credentials.json
```

### 2c. Authorize

```bash
python3 scripts/gmail_auth.py
```

A browser opens. Google will warn that the app isn't verified — that's expected for a
personal OAuth client. Click **Advanced** → **Go to (your app name)** → allow.

Test it:

```bash
python3 scripts/gmail_draft.py --to you@yourdomain.com \
    --subject "test" --body "it works" --company "Test"
```

Check your Gmail drafts.

---

## A note on the send permission

Google publishes no scope that allows creating a draft but forbids sending. `gmail.compose`
is the narrowest one that can create drafts, and it technically permits sending too.

So the guarantee is enforced in code, not by the scope: `scripts/gmail_draft.py` calls
`users.drafts.create` and has no send path. The skill instructions forbid sending through
any other route. If you want belt and braces, read that file — it's about 120 lines and the
only Gmail write in it is the draft call.

Revoke access any time at <https://myaccount.google.com/permissions>.

---

## Using it

| Command | What happens |
|---|---|
| `/prospect monday` | The full origination block — source, research, draft, report |
| `/prospect source` | Find new targets via the signal search, score, add to pipeline |
| `/prospect research <company>` | Deep research on one company, score it, write the observation |
| `/prospect draft` | Draft every touch that's due, stage as Gmail drafts |
| `/prospect due` | What's due today and this week |
| `/prospect status` | Pipeline report — counts, stalls, missing emails |

The Monday block is the one that matters. Run it at the start of every week and the rest
takes care of itself.

### Running it directly

The Python scripts work on their own if you'd rather not go through Claude:

```bash
python3 scripts/pipeline.py due --days 7
python3 scripts/pipeline.py status
python3 scripts/pipeline.py list --status hot
```

---

## Files

```
.claude/skills/prospect/
  SKILL.md              the agent's instructions
  references/
    signals.md          the six buying signals and the scoring rubric
    plays.md            the five plays, both vertical variants each
    voice.md            writing rules, the kill list, the self-check
scripts/
  pipeline.py           target and touch state — stdlib only
  gmail_draft.py        draft staging, no send path
  gmail_auth.py         one-time OAuth
pipeline/
  targets.csv           your pipeline, opens in Excel
  touches.csv           every touch logged, for channel attribution
  drafts/               fallback drafts when Gmail isn't configured (gitignored)
CLAUDE.md               practice context — pricing, positioning, decisions
```

`pipeline/targets.csv` is a plain CSV. Open it in Excel, edit it by hand, add contacts you
sourced yourself — the agent reads whatever's there.

---

## What to watch

**Verify the observation.** The agent is instructed never to claim a signal it hasn't seen,
and to flag anything it couldn't confirm. Read the "Why now" line in each report — if it says
a company is hiring AEs, that posting should be real. A false opening line is the one mistake
that permanently costs you a future buyer.

**Contact emails.** The agent will flag inferred addresses rather than guessing silently.
Confirm those before sending.

**Refresh the domain lines quarterly.** The specific observations in `plays.md` are what make
these messages land. Update them from live engagements — the version that works in month nine
should reference something you learned in month six.
