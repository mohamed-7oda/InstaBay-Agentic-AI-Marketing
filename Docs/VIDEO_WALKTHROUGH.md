# 3–5 minute walkthrough script

## 0:00–0:30 — Problem and outcome

“This is InstaBay, a safe-by-default agentic Instagram marketing teammate for a fictional Red Sea resort in Hurghada. The objective was not to make a generic caption generator: it has to define the brand, create natural Arabic and English content, require approval before publishing, measure performance and improve the next batch.”

Show the README architecture diagram.

## 0:30–1:15 — Why this architecture

“I chose six small, inspectable components instead of a heavyweight multi-agent framework. Brand memory grounds the content. The content agent creates a structured asset. The review agent checks quality. A human is the release gate. The publisher is an isolated Graph API adapter. Analytics and optimization close the loop. Every hand-off is visible as a Python dictionary, which makes the workflow easy to debug and defend.”

Show `data/brand_rules.json` and `agents/planner_agent.py`.

## 1:15–2:15 — Content and Arabic

“The brand is relaxed-luxury: turquoise water, warm sunset and unhurried moments. I use English and Arabic as separate copy, not a literal translation. Here is a generated 24-second Reel. It includes the hook, visual direction, bilingual on-screen text, an audio direction, captions and a CTA. The review gate verifies required fields, Arabic-script coverage, a reasonable hashtag count and the Reel storyboard.”

Run `streamlit run app.py`. Generate a Reel in the first tab and point out the English, Arabic, storyboard and review score.

## 2:15–3:00 — Safe publishing

“Publishing is deliberately dry-run by default. The app will not even build an action until the reviewer ticks explicit human approval. The dry-run displays the exact Graph API sequence. In live mode, the adapter creates a media container, polls until it is finished, then calls `media_publish`. Credentials and a public media URL are required, so the challenge demo cannot accidentally publish an external post.”

Tick approval and run the dry-run. Show the generated plan in the third tab or the JSON panel.

## 3:00–3:45 — Measurement and improvement

“To make the loop reproducible without account access, I include a clearly labelled synthetic dataset. The baseline has mostly 17:00 static posts. The improved batch tests a 20:00 Cairo window, more Reels and save-focused bilingual hooks. Weighted engagement rate rises from 5.10% to 7.51%, a 47.4% simulated uplift. The optimizer recommends the next mix: three Reels, two carousels and one image.”

Show the analytics tab and `data/engagement.csv`.

## 3:45–4:30 — Rigor, trade-offs and next steps

“The README distinguishes fact from simulation and includes the quality, Arabic, efficiency, autonomy and uplift metrics. I chose a free template-first generator to keep the prototype reproducible and low-cost. For production I would add real Meta Insights/webhooks, media hosting and validation, token lifecycle management, experiment holdouts and native Arabic review. The unit tests validate the bilingual Reel gate, the approval block and the positive feedback-loop calculation.”

Finish by running `python test.py` and show the passing tests.
