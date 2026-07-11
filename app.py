import json
import streamlit as st

from agents.analytics_agent import AnalyticsAgent
from agents.content_agent import ContentAgent
from agents.optimization_agent import OptimizationAgent
from agents.publisher_agent import PublisherAgent
from agents.review_agent import ReviewAgent


st.set_page_config(page_title="InstaBay Marketing Teammate", page_icon="🏝️", layout="wide")
st.title("🏝️ InstaBay Marketing Teammate")
st.caption("Brand-grounded bilingual creation → quality gate → human approval → safe Meta dry-run → measurement → next batch")

for key, value in {"asset": None, "review": None, "publish": None}.items():
    st.session_state.setdefault(key, value)

create_tab, analytics_tab, integration_tab = st.tabs(["1. Create & approve", "2. Measure & improve", "3. Meta integration"])

with create_tab:
    left, right = st.columns([1, 2])
    with left:
        topic = st.text_input("Creative focus", "sunset by the Red Sea")
        pillar = st.selectbox("Content pillar", ["Beach & Nature", "Wellness", "Sea Adventures", "Dining & Sunset", "Guest Moments"])
        content_type = st.selectbox("Format", ["Reel", "Carousel", "Image"])
        if st.button("Generate bilingual asset", type="primary", use_container_width=True):
            st.session_state.asset = ContentAgent().generate_post(topic, pillar, content_type)
            st.session_state.review = ReviewAgent().review(st.session_state.asset)
            st.session_state.publish = None
    with right:
        asset = st.session_state.asset
        if not asset:
            st.info("Generate an asset to see the bilingual caption, visual brief and quality gate.")
        else:
            st.subheader(f"{asset['content_type']} draft · {asset['pillar']}")
            st.markdown("**English**")
            st.write(asset["caption_en"])
            st.markdown("**العربية**")
            st.write(asset["caption_ar"])
            st.caption(" ".join(asset["hashtags"]))
            st.info(f"Visual brief: {asset['visual_brief']}")
            if asset.get("reel_storyboard"):
                st.markdown("**Reel storyboard (24 seconds)**")
                st.dataframe(asset["reel_storyboard"], use_container_width=True, hide_index=True)
            review = st.session_state.review
            if review["passed"]:
                st.success(f"Automated quality gate passed · Brand {review['brand_consistency_score']}/5 · Arabic {review['arabic_quality_score']}/5")
            else:
                st.error("Quality gate failed: " + "; ".join(review["notes"]))
            approved = st.checkbox("I approve this asset for publishing", help="Nothing can call Meta without this explicit human approval.")
            if st.button("Run Meta publishing dry-run", disabled=not (approved and review["passed"]), use_container_width=True):
                st.session_state.publish = PublisherAgent(dry_run=True).publish(asset, approved=True)
            if st.session_state.publish:
                st.success("No external post was made. The Graph API plan is ready for a human-confirmed live run.")
                st.json(st.session_state.publish["plan"])

with analytics_tab:
    report = AnalyticsAgent().analyze()
    a, b, c = st.columns(3)
    a.metric("Before weighted ER", f"{report['by_batch']['before']}%")
    b.metric("After weighted ER", f"{report['by_batch']['after']}%", f"+{report['uplift_pct']}%")
    c.metric("Best format", report["best_format"])
    st.caption("Synthetic, reproducible challenge dataset. Weighted ER = (likes + comments + 2×saves + 2×shares) / reach × 100.")
    st.dataframe(report["records"], use_container_width=True, hide_index=True)
    st.subheader("Recommended next batch")
    for level, message in OptimizationAgent().suggest(report):
        getattr(st, level)(message)

with integration_tab:
    st.subheader("Live-ready adapter, safe by default")
    st.markdown("The app defaults to a dry-run. A real deployment needs a Meta app, an Instagram Professional account, a linked Facebook Page (for Facebook Login), permissions and a public HTTPS media URL.")
    st.code("META_ACCESS_TOKEN=...\nIG_USER_ID=...\n# call PublisherAgent(dry_run=False).publish(asset, approved=True, media_url='https://...')", language="bash")
    st.markdown("For a Reel the adapter creates a media container, polls its `status_code` until `FINISHED`, then calls `media_publish`. The approval check is enforced in code before either dry-run or live action.")
