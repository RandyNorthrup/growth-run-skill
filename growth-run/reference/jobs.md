# Gig hunt check-in

**Rules:**
- $0 budget: never buy credits, Connects or memberships.
- No cold email.
- The owner approves every contract or deposit.
- Bids and applications claim only verified work and dates.
- The portfolio link goes to the owner's existing site. Never create site content; repos are read-only.

## LinkedIn (main free channel)
- **Search without logging in:**
  1. Run `python li_search.py "<keywords>" "f_JT=C&sortBy=R&f_TPR=r86400"`.
     - The defaults are remote (`f_WT=2`), Easy Apply (`f_AL=true`), US and the past week.
     - `f_JT=C` restricts to contract jobs. Leave it out for full-time.
     - `sortBy=R` (relevance) respects keywords. `sortBy=DD` mostly ignores them and returns the same pool of about 100 jobs.
  2. Run `python li_detail.py <id>…` for the title, company, type, seniority, applicant count and full description. It writes `details.json`.
- **Score the fit (1–5)** against the stack, seniority, rate and location. Skip AI-training gigs that pay under the rate floor, thin postings, and hybrid roles outside the owner's area.
- **Easy Apply** (logged in): Next, then Review, then scroll down. Uncheck "Follow company", then Submit. Use the web-focused resume the owner approved.
  - On screening questions, use only the facts in the profile; give city and state, never a street address.
  - If a question needs information you don't have, stop and ask.
- Log each application to the owner's pipeline: date, source, title, URL, rate, type, fit, action, status, next step, follow-up date and notes.
- **Follow up** about 6 days after applying if there's no response, and only inside the platform's messaging.

## Other free channels
- **Hacker News "Who wants to be hired?"** opens monthly, on about the 1st weekday. Post one SEEKING WORK comment: location/remote, stack, 3–4 real projects with links, the portfolio, and the owner's public contact email.
- **Contra:** free tier with 0% commission. Fill out the profile: rate band, a bio of 400 characters or fewer, links, time zone, and 3–4 work pieces.
  - A work piece needs at least one Tool.
  - The "Add work" dialog has no reachable file input. Paste the image instead: run `python clipimage.py <img>`, then press Ctrl+V in the dialog.
  - Escape leaves a Draft tile behind; delete it through its "..." menu.
  - ID and wallet verification are the owner's.
- **Upwork:** if the free Connects are gone, run it inbound-only. Use Project Catalog listings (free) and accept client invites. Never buy Connects.
- **Reddit r/forhire:** needs account age and karma. Don't karma-farm; skip it if the account doesn't qualify.
- **Craigslist gigs:** mostly spam or under $25/hr. Skip.

## Check-in routine
1. Look in Gmail and the platform inboxes for replies. Flag anything needing the owner's answer.
2. Run new searches, especially the newest postings, and apply to fits of 4 or more.
3. Update the pipeline and the run-state memory: what was applied to, what was skipped and why, and the next check date.
4. Report the applications, any replies, and the questions for the owner.
