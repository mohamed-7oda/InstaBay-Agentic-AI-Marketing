# 🏝️ InstaBay Agentic AI Marketing Teammate

An end-to-end, safe-by-default Instagram marketing workflow for the fictional InstaBay Resort & Spa in Hurghada. It plans brand-consistent bilingual content, evaluates it, requires human approval, prepares a Meta Graph API request, measures engagement, and changes the next batch from evidence.

> **Challenge scope and honesty:** this repository uses a deterministic content generator and a synthetic, labelled engagement dataset so the entire loop can be run without credentials or paid services. The Meta adapter is real code but defaults to dry-run; no post is sent to Instagram in the demo.

## Demo in 60 seconds

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test.py
streamlit run app.py
```

The app works without an API key. In the UI: generate a bilingual Reel or post → inspect the automated review → tick the human approval checkbox → run the dry-run → view the synthetic before/after analytics and the recommended next batch.

## Architecture

```text
Brand memory (JSON) → Content agent → deterministic quality gate → HUMAN APPROVAL
                                                                    ↓
Analytics dataset ← Meta Graph adapter (dry-run by default) ← approved asset
       ↓
Optimization agent → next-batch mix, pillar and posting-time recommendation
```

Each hand-off is a structured Python dictionary. This deliberately avoids an elaborate framework: it makes content, review scores, approval state, publish payload and metrics inspectable in a five-to-six-hour prototype.

| Component | Responsibility | Evidence |
|---|---|---|
| `BrandAgent` | Grounds all work in voice, visual rules, pillars, cadence and guardrails | `data/brand_rules.json` |
| `ContentAgent` | Generates bilingual post/Reel assets, including visual brief and storyboard | `agents/content_agent.py` |
| `ReviewAgent` | Checks required fields, Arabic script, hashtag count and Reel storyboard | `agents/review_agent.py` |
| `PublisherAgent` | Blocks unapproved actions and emits a dry-run plan or calls Graph API in explicit live mode | `agents/publisher_agent.py` |
| `AnalyticsAgent` | Calculates weighted engagement rate by batch | `data/engagement.csv` |
| `OptimizationAgent` | Converts observed results into the next content mix | `agents/optimization_agent.py` |

## Brand and sample output

- [One-page brand identity](Docs/InstaBay%20Brand%20Identity.pdf)
- [Bilingual weekly calendar and complete Reel concept](outputs/content_calendar.md)
- [Calendar spreadsheet source](data/content_calendar.csv)

The identity is warm, sensory and relaxed-luxury—made for Egyptian domestic travellers, GCC guests and European explorers. Visuals use natural turquoise water and sunset warmth. Arabic is independently written for a regional audience rather than presented as a literal English translation.

## Benchmark results

The offline dataset contains 5 baseline and 6 improved-batch posts. It is synthetic and reproducible, not represented as live account data.

| Metric | Definition / method | Baseline | Improved batch |
|---|---|---:|---:|
| Brand consistency | 1–5 rubric: voice, pillar, visual brief, hashtag rules and guardrails; `ReviewAgent` regression check | 4.0/5 | 5.0/5 |
| Arabic quality | 1–5 author rubric: natural regional phrasing, Arabic CTA, legibility and brand-voice match; script/CTA are regression-tested | 3.5/5 | 5.0/5 |
| Weighted engagement rate | `(likes + comments + 2×saves + 2×shares) / reach × 100` | 5.10% | 7.51% |
| Optimization uplift | Relative change in mean weighted engagement rate from the included dataset | — | **+47.4%** |
| Efficiency | Template generation on a local machine; no paid API call required | <$0.001 / asset | <$0.001 / asset |
| Latency | Template creation; excludes optional image/video production | <0.1 s / asset | <0.1 s / asset |
| Autonomy | All stages except final external action run unattended | 80% | 80%; human approval remains mandatory |

The uplift is not causal proof. It is a controlled offline simulation designed to demonstrate the feedback-loop mechanics. In production, the agent would collect real `reach`, saves, shares, comments, plays and watch-through data, compare cohorts with sufficient sample size, and only then promote a recommendation.

## Improvement loop

The baseline is weighted toward 17:00 static assets. The simulated improved batch tests a 20:00 Cairo posting window, more short Reels, save-focused bilingual hooks and stronger Wellness/Dining/Sea Adventure coverage. The analytics module finds the result above and proposes a next batch of **3 Reels, 2 carousels and 1 image**, prioritizing the strongest pillar. The `test_feedback_loop_has_positive_measured_uplift` test verifies this result from the checked-in data.

## Meta Graph API integration

`PublisherAgent` implements the official container flow:

1. A human must pass `approved=True`; otherwise the call raises `PermissionError`.
2. Create a media container at `/{ig_user_id}/media` with a public HTTPS `image_url` or `video_url`.
3. For a Reel, poll the container until `status_code=FINISHED`.
4. Publish only then at `/{ig_user_id}/media_publish`.

For a real account, set `META_ACCESS_TOKEN` and `IG_USER_ID`, supply a public media URL, and instantiate `PublisherAgent(dry_run=False)`. This requires a Meta app, an Instagram Professional account, the appropriate permissions and—in the Facebook Login route—a linked Facebook Page. The demo does not bypass platform rules or scrape Instagram. See Meta’s [Instagram API content-publishing documentation](https://developers.facebook.com/docs/instagram-platform/content-publishing/) and its [official API collection](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api?entity=request-23987686-1ff01566-3509-48bd-a0f4-8571a91ccfdf).

## Approach and research note

- **Adopted: explicit plan → act → observe loop.** ReAct motivates interleaving actions with observations rather than producing a one-shot answer; here, analytics updates the next content batch. [Yao et al., 2023](https://arxiv.org/abs/2210.03629)
- **Adopted: human confirmation before an irreversible external action.** The release boundary is separate from content generation and enforced by code, not a prompt.
- **Adopted: component-level evaluation.** Besides task completion, the prototype measures content quality, tool boundary, environment data and outcome movement—a direction reflected in the recent agent-assessment literature. [Akshathala et al., 2025](https://arxiv.org/abs/2512.12791)
- **Rejected: a heavy multi-agent framework and live publishing in the demo.** They add setup and safety risk without improving the evidence in this time-box. Plain Python keeps the state path auditable; the adapter makes a live integration swappable.
- **Cost decision:** generation is template-first and free. An LLM or image/video provider would be introduced only after it improves the measured metric enough to justify its marginal cost.

## Assumptions and trade-offs

- No verified business account or Meta app-review access is available, so publishing and analytics are safely mocked with clearly marked synthetic data.
- Arabic quality is an author rubric and automated regression check, not a claim of a native-speaker panel; production would add a native Arabic reviewer sample.
- The supplied brand/calendar PDFs remain the presentation artifacts; the Markdown calendar is the version-controlled, reviewable source.

## If this were real

I would add OAuth/token lifecycle management, webhook ingestion, durable storage, scheduled approval queues, media hosting/transcoding checks, rate-limit/error handling, audience-segment experiments, native Arabic review and a statistically powered experiment policy. I would also ingest actual Meta Insights rather than use the fixture dataset, then use a holdout and minimum sample threshold before altering the content strategy.

## Submission checklist

- [x] Agentic workflow with persistent, inspectable hand-offs
- [x] One-page brand identity and bilingual one-week calendar
- [x] Full bilingual Reel concept/storyboard
- [x] Human-in-the-loop publishing gate and Graph API adapter
- [x] Engagement analysis and evidence-driven next batch
- [x] Reproducible benchmark and before → after uplift
- [x] Research/approach note, assumptions and production plan
- [ ] Record and add the required 3–5 minute walkthrough video link
