# app.py
import streamlit as st
import time
from pipeline import run_research_pipeline

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
    <style>
        /* General */
        body {
            font-family: 'Segoe UI', sans-serif;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .hero-banner h1 {
            color: #e94560;
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .hero-banner p {
            color: #a8b2d8;
            font-size: 1.1rem;
        }

        /* Agent Cards */
        .agent-card {
            background: #1e1e2e;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            border-left: 4px solid #e94560;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: transform 0.2s ease;
        }
        .agent-card:hover {
            transform: translateX(4px);
        }
        .agent-card.active {
            border-left-color: #00d4ff;
            background: #1a2a3a;
        }
        .agent-card.done {
            border-left-color: #00ff88;
        }
        .agent-card h4 {
            margin: 0 0 4px 0;
            color: #cdd6f4;
            font-size: 1rem;
        }
        .agent-card p {
            margin: 0;
            color: #7f849c;
            font-size: 0.85rem;
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: 8px;
        }
        .badge-waiting  { background: #313244; color: #7f849c; }
        .badge-running  { background: #1e3a5f; color: #00d4ff; }
        .badge-done     { background: #1e3b2f; color: #00ff88; }
        .badge-error    { background: #3b1e1e; color: #ff6b6b; }

        /* Section Headers */
        .section-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 24px 0 12px 0;
        }
        .section-header h3 {
            color: #cdd6f4;
            margin: 0;
            font-size: 1.2rem;
        }
        .section-divider {
            flex: 1;
            height: 1px;
            background: linear-gradient(to right, #e94560, transparent);
        }

        /* Result Boxes */
        .result-box {
            background: #1e1e2e;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #313244;
            margin-bottom: 16px;
            max-height: 400px;
            overflow-y: auto;
        }
        .result-box pre {
            color: #cdd6f4;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 0.88rem;
            line-height: 1.6;
        }

        /* Metric Cards */
        .metric-row {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
        }
        .metric-card {
            flex: 1;
            background: #1e1e2e;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            border: 1px solid #313244;
        }
        .metric-card .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #e94560;
        }
        .metric-card .metric-label {
            color: #7f849c;
            font-size: 0.8rem;
            margin-top: 4px;
        }

        /* Sidebar */
        .sidebar-info {
            background: #1e1e2e;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 12px;
            border: 1px solid #313244;
        }
        .sidebar-info h5 {
            color: #e94560;
            margin: 0 0 6px 0;
            font-size: 0.9rem;
        }
        .sidebar-info p {
            color: #a8b2d8;
            font-size: 0.82rem;
            margin: 0;
        }

        /* Spinner override */
        .stSpinner > div {
            border-top-color: #e94560 !important;
        }

        /* Button */
        .stButton > button {
            background: linear-gradient(135deg, #e94560, #c23152);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 32px;
            font-size: 1rem;
            font-weight: 700;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(233, 69, 96, 0.5);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            background: #1e1e2e;
            border-radius: 10px;
            padding: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #7f849c;
            border-radius: 8px;
        }
        .stTabs [aria-selected="true"] {
            background: #e94560 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State Initialisation
# ─────────────────────────────────────────────
def init_session_state():
    defaults = {
        "pipeline_state": None,
        "is_running": False,
        "run_history": [],
        "agent_statuses": {
            "search": "waiting",
            "reader": "waiting",
            "writer": "waiting",
            "critic": "waiting",
        },
        "elapsed_time": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────
def reset_agent_statuses():
    st.session_state.agent_statuses = {
        "search": "waiting",
        "reader": "waiting",
        "writer": "waiting",
        "critic": "waiting",
    }

def badge_html(status: str) -> str:
    labels = {
        "waiting": ("⏳ Waiting",  "badge-waiting"),
        "running": ("⚡ Running",  "badge-running"),
        "done":    ("✅ Done",     "badge-done"),
        "error":   ("❌ Error",    "badge-error"),
    }
    text, cls = labels.get(status, ("⏳ Waiting", "badge-waiting"))
    return f'<span class="status-badge {cls}">{text}</span>'

def agent_card_html(icon, title, description, status):
    state_cls = "active" if status == "running" else ("done" if status == "done" else "")
    return f"""
    <div class="agent-card {state_cls}">
        <h4>{icon} {title} {badge_html(status)}</h4>
        <p>{description}</p>
    </div>
    """

def word_count(text: str) -> int:
    return len(text.split()) if text else 0

def char_count(text: str) -> int:
    return len(text) if text else 0

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Research System")
    st.markdown("---")

    # Agent pipeline overview
    st.markdown("### 🤖 Agent Pipeline")

    agents_info = [
        ("🔍", "Search Agent",  "Finds recent & reliable sources"),
        ("📄", "Reader Agent",  "Scrapes & extracts deep content"),
        ("✍️", "Writer Agent",  "Synthesises a structured report"),
        ("🧐", "Critic Agent",  "Reviews & scores the report"),
    ]

    for icon, name, desc in agents_info:
        status = st.session_state.agent_statuses.get(name.split()[0].lower(), "waiting")
        st.markdown(
            agent_card_html(icon, name, desc, status),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Run history
    st.markdown("### 📚 Run History")
    if st.session_state.run_history:
        for i, entry in enumerate(reversed(st.session_state.run_history[-5:]), 1):
            with st.expander(f"#{len(st.session_state.run_history) - i + 1} · {entry['topic'][:25]}…"):
                st.caption(f"🕐 {entry['time']}s elapsed")
                st.caption(f"📝 {entry['words']} words in report")
    else:
        st.caption("No runs yet.")

    st.markdown("---")
    st.markdown(
        "<div style='color:#7f849c; font-size:0.78rem; text-align:center;'>"
        "Multi-Agent AI Research System<br>Built with LangChain + Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown("""
    <div class="hero-banner">
        <h1>🔬 Multi-Agent AI Research System</h1>
        <p>Powered by autonomous Search · Reader · Writer · Critic agents</p>
    </div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Input Section
# ─────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1])

with col_input:
    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2024",
        label_visibility="collapsed",
    )

with col_btn:
    run_clicked = st.button("🚀 Research", disabled=st.session_state.is_running)

# ─────────────────────────────────────────────
# Example Topics
# ─────────────────────────────────────────────
st.markdown("**💡 Try an example:**")
example_cols = st.columns(4)
examples = [
    "Large Language Models 2025",
    "CRISPR gene editing advances",
    "Renewable energy storage",
    "Autonomous vehicle safety",
]
for col, example in zip(example_cols, examples):
    with col:
        if st.button(f"📌 {example}", key=f"ex_{example}"):
            topic = example
            run_clicked = True

st.markdown("---")

# ─────────────────────────────────────────────
# Pipeline Execution
# ─────────────────────────────────────────────
if run_clicked and topic.strip():
    st.session_state.is_running = True
    reset_agent_statuses()
    st.session_state.pipeline_state = None

    # ── Live status area ──────────────────────
    status_container  = st.container()
    progress_bar      = st.progress(0)
    stage_placeholder = st.empty()

    with status_container:
        st.markdown(f"### 🔎 Researching: *{topic}*")

    pipeline_state = {}
    start_time     = time.time()
    error_occurred = False

    try:
        # ── STAGE 1 · Search ─────────────────
        st.session_state.agent_statuses["search"] = "running"
        stage_placeholder.info("🔍 **Search Agent** is finding relevant sources…")
        progress_bar.progress(10)

        from agents import build_search_agent
        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]
        })
        pipeline_state["search_result"] = search_result["messages"][-1].content
        st.session_state.agent_statuses["search"] = "done"
        progress_bar.progress(30)

        # ── STAGE 2 · Reader ─────────────────
        st.session_state.agent_statuses["reader"] = "running"
        stage_placeholder.info("📄 **Reader Agent** is scraping the best source…")
        progress_bar.progress(40)

        from agents import build_reader_agent
        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [
                (
                    "user",
                    f'Based on the following search result about "{topic}", '
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{pipeline_state['search_result'][:800]}"
                )
            ]
        })
        pipeline_state["scraped_content"] = reader_result["messages"][-1].content
        st.session_state.agent_statuses["reader"] = "done"
        progress_bar.progress(60)

        # ── STAGE 3 · Writer ─────────────────
        st.session_state.agent_statuses["writer"] = "running"
        stage_placeholder.info("✍️ **Writer Agent** is composing the report…")
        progress_bar.progress(70)

        from agents import writer_chain
        research_combined = (
            f"Search Results:\n{pipeline_state['search_result']}\n\n"
            f"Detailed Scraped Content:\n{pipeline_state['scraped_content']}"
        )
        pipeline_state["report"] = writer_chain.invoke({
            "topic":    topic,
            "research": research_combined,
        })
        st.session_state.agent_statuses["writer"] = "done"
        progress_bar.progress(85)

        # ── STAGE 4 · Critic ─────────────────
        st.session_state.agent_statuses["critic"] = "running"
        stage_placeholder.info("🧐 **Critic Agent** is reviewing the report…")

        from agents import critic_chain
        pipeline_state["feedback"] = critic_chain.invoke({
            "report": pipeline_state["report"]
        })
        st.session_state.agent_statuses["critic"] = "done"
        progress_bar.progress(100)

    except Exception as exc:
        error_occurred = True
        stage_placeholder.error(f"❌ Pipeline error: {exc}")
        for agent in st.session_state.agent_statuses:
            if st.session_state.agent_statuses[agent] == "running":
                st.session_state.agent_statuses[agent] = "error"

    finally:
        elapsed = round(time.time() - start_time, 1)
        st.session_state.elapsed_time   = elapsed
        st.session_state.is_running     = False
        st.session_state.pipeline_state = pipeline_state

        if not error_occurred:
            stage_placeholder.success(f"✅ Research completed in **{elapsed}s**!")
            # Save to history
            st.session_state.run_history.append({
                "topic": topic,
                "time":  elapsed,
                "words": word_count(pipeline_state.get("report", "")),
            })

elif run_clicked and not topic.strip():
    st.warning("⚠️ Please enter a research topic before running.")

# ─────────────────────────────────────────────
# Results Section
# ─────────────────────────────────────────────
state = st.session_state.pipeline_state

if state:

    # ── Metrics Row ──────────────────────────
    st.markdown("### 📊 Run Summary")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("⏱️ Elapsed Time",   f"{st.session_state.elapsed_time}s")
    with m2:
        st.metric("📝 Report Words",   word_count(state.get("report", "")))
    with m3:
        st.metric("🔍 Search Length",  f"{char_count(state.get('search_result', ''))} chars")
    with m4:
        st.metric("📄 Scraped Length", f"{char_count(state.get('scraped_content', ''))} chars")

    st.markdown("---")

    # ── Tabbed Results ───────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Final Report",
        "🧐 Critic Feedback",
        "🔍 Search Results",
        "📄 Scraped Content",
    ])

    # ── Tab 1 · Final Report ─────────────────
    with tab1:
        st.markdown(
            "<div class='section-header'>"
            "<h3>📋 Generated Research Report</h3>"
            "<div class='section-divider'></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        report = state.get("report", "No report generated.")
        st.markdown(report)

        # Download button
        st.download_button(
            label="⬇️ Download Report (.md)",
            data=report,
            file_name=f"research_report_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    # ── Tab 2 · Critic Feedback ──────────────
    with tab2:
        st.markdown(
            "<div class='section-header'>"
            "<h3>🧐 Critic Agent Feedback</h3>"
            "<div class='section-divider'></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        feedback = state.get("feedback", "No feedback generated.")
        st.markdown(feedback)

        st.download_button(
            label="⬇️ Download Feedback (.md)",
            data=feedback,
            file_name=f"critic_feedback_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    # ── Tab 3 · Search Results ───────────────
    with tab3:
        st.markdown(
            "<div class='section-header'>"
            "<h3>🔍 Raw Search Results</h3>"
            "<div class='section-divider'></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        search_text = state.get("search_result", "No search results.")
        st.text_area(
            label="Search Output",
            value=search_text,
            height=400,
            label_visibility="collapsed",
        )

    # ── Tab 4 · Scraped Content ──────────────
    with tab4:
        st.markdown(
            "<div class='section-header'>"
            "<h3>📄 Scraped Web Content</h3>"
            "<div class='section-divider'></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        scraped_text = state.get("scraped_content", "No scraped content.")
        st.text_area(
            label="Scraped Content",
            value=scraped_text,
            height=400,
            label_visibility="collapsed",
        )

# ─────────────────────────────────────────────
# Empty State
# ─────────────────────────────────────────────
else:
    st.markdown("""
        <div style="
            text-align: center;
            padding: 60px 20px;
            color: #7f849c;
        ">
            <div style="font-size: 4rem; margin-bottom: 16px;">🔬</div>
            <h3 style="color: #cdd6f4; margin-bottom: 8px;">Ready to Research</h3>
            <p>Enter a topic above and click <strong style="color:#e94560">🚀 Research</strong>
               to start the multi-agent pipeline.</p>
            <br>
            <p style="font-size:0.85rem;">
                The system will automatically run the<br>
                <strong>Search → Reader → Writer → Critic</strong> pipeline
                and present the results here.
            </p>
        </div>
    """, unsafe_allow_html=True)