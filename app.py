import os
import streamlit as st

from utils.file_reader import extract_text

from utils.summarizer import (
    summarize_text,
    generate_statistics
)

from utils.charts import (
    word_count_chart,
    compression_chart,
    reading_time_chart
)

from utils.history import (
    initialize_history,
    add_summary,
    get_history,
    search_history,
    clear_history,
    total_summaries
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------

css_path = os.path.join(
    "style",
    "style.css"
)

if os.path.exists(css_path):

    with open(css_path) as css:

        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# INITIALIZE SESSION
# ---------------------------------------------------

initialize_history()

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "article" not in st.session_state:
    st.session_state.article = ""

if "stats" not in st.session_state:
    st.session_state.stats = None

if "processing_time" not in st.session_state:
    st.session_state.processing_time = 0

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("⚙️ Settings")

    summary_length = st.selectbox(
        "Summary Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=[
            "txt",
            "pdf",
            "docx"
        ]
    )

    st.divider()

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=False
    )

    st.divider()

    st.metric(
        "Summaries Created",
        total_summaries()
    )

    st.divider()

    if st.button("🗑️ Clear History"):

        clear_history()

        st.success("History cleared.")

# ---------------------------------------------------
# DARK MODE
# ---------------------------------------------------

if dark_mode:

    st.markdown("""
    <style>

    .main{

        background:#0F172A;
        color:white;

    }

    h1,h2,h3,h4,p{

        color:white;

    }

    div[data-testid="metric-container"]{

        background:#1E293B;
        color:white;

    }

    </style>
    """,
    unsafe_allow_html=True)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""

<div class="hero">

<h1>📰 AI Text Summarizer</h1>

<p>

Generate concise summaries from long
documents using Facebook's
BART Transformer model.

</p>

</div>

""",
unsafe_allow_html=True)

# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------

left, right = st.columns(2)

# ---------------------------------------------------
# LEFT PANEL
# ---------------------------------------------------

with left:

    st.subheader("📄 Original Document")

    if uploaded_file is not None:

        try:

            st.session_state.article = extract_text(
                uploaded_file
            )

            st.success(
                "Document loaded successfully."
            )

        except Exception as e:

            st.error(str(e))

    article = st.text_area(

        "Article",

        value=st.session_state.article,

        height=420,

        placeholder="Paste an article or upload a document..."

    )

    st.session_state.article = article

    generate = st.button(
        "🚀 Generate Summary"
    )

# ---------------------------------------------------
# RIGHT PANEL
# ---------------------------------------------------

with right:

    st.subheader("📑 Generated Summary")

    summary_box = st.empty()
    # ---------------------------------------------------
# GENERATE SUMMARY
# ---------------------------------------------------

if generate:

    if article.strip() == "":

        st.warning("Please enter or upload an article.")

    else:

        try:

            with st.spinner("🤖 AI is generating your summary..."):

                summary, processing_time = summarize_text(
                    article,
                    summary_length
                )

                st.session_state.summary = summary

                st.session_state.processing_time = processing_time

                st.session_state.stats = generate_statistics(
                    article,
                    summary
                )

                add_summary(
                    article,
                    summary
                )

        except Exception as e:

            st.error(f"An error occurred: {e}")
# ---------------------------------------------------
# DISPLAY SUMMARY
# ---------------------------------------------------

if (
    st.session_state.summary != ""
    and st.session_state.stats is not None
):

    summary = st.session_state.summary
    stats = st.session_state.stats
    processing_time = st.session_state.processing_time

    summary_box.success(summary)

    st.divider()

    st.subheader("📊 Summary Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📄 Original Words",
        stats["original_words"]
    )

    c2.metric(
        "📝 Summary Words",
        stats["summary_words"]
    )

    c3.metric(
        "📉 Compression",
        f'{stats["compression"]}%'
    )

    c4.metric(
        "⏱ Processing Time",
        f"{processing_time:.2f}s"
    )

    st.divider()

    c5, c6 = st.columns(2)

    c5.metric(
        "📖 Original Reading Time",
        f'{stats["original_reading_time"]} min'
    )

    c6.metric(
        "💡 Time Saved",
        f'{stats["time_saved"]} min'
    )

    st.divider()

    st.download_button(
        "📥 Download Summary",
        data=summary,
        file_name="summary.txt",
        mime="text/plain"
    )

    st.text_area(
        "📋 Copy Summary",
        value=summary,
        height=180
    )

    st.divider()

    st.subheader("📈 Analytics")

    chart1, chart2 = st.columns(2)

    with chart1:

        fig = word_count_chart(
            stats["original_words"],
            stats["summary_words"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with chart2:

        fig = compression_chart(
            stats["compression"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    fig = reading_time_chart(
        stats["original_reading_time"],
        stats["summary_reading_time"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with chart2:

        fig = compression_chart(

            stats["compression"]

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    fig = reading_time_chart(

        stats["original_reading_time"],

        stats["summary_reading_time"]

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )