import streamlit as st

from agents.content_agent import ContentAgent
from agents.analytics_agent import AnalyticsAgent
from agents.optimization_agent import OptimizationAgent

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="InstaBay AI Marketing Assistant",
    page_icon="🏝️",
    layout="wide",
)

st.title("🏝️ InstaBay AI Marketing Assistant")
st.write("Generate, review, analyze, and optimize Instagram content using AI Agents.")
st.divider()


# -------------------------
# Cached Agents
# -------------------------
# Agents are stateless/expensive-ish to construct, so build them once per
# session instead of on every rerun.

@st.cache_resource
def get_content_agent() -> ContentAgent:
    return ContentAgent()


@st.cache_resource
def get_analytics_agent() -> AnalyticsAgent:
    return AnalyticsAgent()


@st.cache_resource
def get_optimization_agent() -> OptimizationAgent:
    return OptimizationAgent()


# -------------------------
# Session State
# -------------------------
# "status" tracks where the current post is in its lifecycle:
#   None -> "draft" -> "published" / "rejected"
# Keeping analytics/report in session_state (rather than only inside the
# button's `if` block) means they survive reruns triggered by other widgets.

defaults = {
    "post": None,
    "status": None,
    "report": None,
    "history": [],  # list of {"post": str, "status": str}
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


def reset_post_state():
    st.session_state.post = None
    st.session_state.status = None
    st.session_state.report = None


# -------------------------
# Sidebar: history + reset
# -------------------------

with st.sidebar:
    st.header("Session")
    if st.button("🔄 Start New Post", use_container_width=True):
        reset_post_state()
        st.rerun()

    st.divider()
    st.subheader("History")
    if not st.session_state.history:
        st.caption("No posts generated yet this session.")
    else:
        for i, item in enumerate(reversed(st.session_state.history), start=1):
            icon = "✅" if item["status"] == "published" else "❌"
            with st.expander(f"{icon} Post {len(st.session_state.history) - i + 1}"):
                st.write(item["post"])


# -------------------------
# Generate Content
# -------------------------

content_agent = get_content_agent()

generate_disabled = st.session_state.status == "published"
if st.button(
    "✨ Generate Instagram Post",
    disabled=generate_disabled,
    help="Approve, reject, or start a new post to generate again."
    if generate_disabled
    else None,
):
    with st.spinner("Generating content..."):
        try:
            st.session_state.post = content_agent.generate_post()
            st.session_state.status = "draft"
            st.session_state.report = None
        except Exception as e:
            st.error(f"Couldn't generate a post right now: {e}")

# -------------------------
# Display Generated Post
# -------------------------

if st.session_state.post:
    st.subheader("📄 Generated Post")

    edited_post = st.text_area(
        "Post content",
        st.session_state.post,
        height=350,
        label_visibility="collapsed",
        disabled=st.session_state.status != "draft",
    )
    # Keep edits made before approval.
    if st.session_state.status == "draft":
        st.session_state.post = edited_post

    if st.session_state.status == "draft":
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Approve & Publish", use_container_width=True):
                st.session_state.status = "published"
                st.session_state.history.append(
                    {"post": st.session_state.post, "status": "published"}
                )
                st.rerun()

        with col2:
            if st.button("❌ Reject", use_container_width=True):
                st.session_state.status = "rejected"
                st.session_state.history.append(
                    {"post": st.session_state.post, "status": "rejected"}
                )
                st.rerun()

    elif st.session_state.status == "published":
        st.success("Post published successfully! (Mock)")

        if st.session_state.report is None:
            with st.spinner("Analyzing performance..."):
                try:
                    st.session_state.report = get_analytics_agent().analyze()
                except Exception as e:
                    st.error(f"Analytics failed: {e}")

        report = st.session_state.report
        if report:
            st.divider()
            st.subheader("📊 Analytics")

            m1, m2, m3 = st.columns(3)
            m1.metric("Average Likes", f"{report['average_likes']:.0f}")
            m2.metric("Average Reach", f"{report['average_reach']:.0f}")
            m3.metric("Best Performing Content", report["best_post"])

            st.divider()
            st.subheader("💡 Optimization")

            try:
                optimizer = get_optimization_agent()
                suggestions = optimizer.suggest(report)
            except AttributeError:
                # Fallback if OptimizationAgent has no `suggest` method yet.
                suggestions = []
                if report["best_post"] == "Reel":
                    suggestions.append(
                        ("success", "Increase Reel content from 2 to 4 posts per week.")
                    )
                if report["average_likes"] > 250:
                    suggestions.append(
                        ("info", "Continue using luxury and beach-focused content.")
                    )
                else:
                    suggestions.append(
                        ("warning", "Test new content styles and posting times.")
                    )

            if not suggestions:
                st.caption("No specific optimizations to suggest right now.")
            else:
                for level, message in suggestions:
                    getattr(st, level)(message)

    elif st.session_state.status == "rejected":
        st.warning("Post rejected. Generate a new one when you're ready.")