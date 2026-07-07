import streamlit as st
from datetime import datetime


# -----------------------------------------------------
# Initialize History
# -----------------------------------------------------

def initialize_history():
    """
    Create the history list if it doesn't exist.
    """

    if "summary_history" not in st.session_state:
        st.session_state.summary_history = []


# -----------------------------------------------------
# Add New Summary
# -----------------------------------------------------

def add_summary(article, summary):
    """
    Save a generated summary to session history.
    """

    initialize_history()

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "article": article,
        "summary": summary
    }

    # Newest first
    st.session_state.summary_history.insert(0, record)


# -----------------------------------------------------
# Retrieve History
# -----------------------------------------------------

def get_history():
    """
    Return all saved summaries.
    """

    initialize_history()
    return st.session_state.summary_history


# -----------------------------------------------------
# Search History
# -----------------------------------------------------

def search_history(keyword):
    """
    Search summaries and articles by keyword.
    """

    initialize_history()

    keyword = keyword.lower().strip()

    if keyword == "":
        return st.session_state.summary_history

    results = []

    for item in st.session_state.summary_history:

        if (
            keyword in item["article"].lower()
            or
            keyword in item["summary"].lower()
        ):
            results.append(item)

    return results


# -----------------------------------------------------
# Clear History
# -----------------------------------------------------

def clear_history():
    """
    Remove every saved summary.
    """

    initialize_history()

    st.session_state.summary_history = []


# -----------------------------------------------------
# Total Summaries
# -----------------------------------------------------

def total_summaries():

    initialize_history()

    return len(st.session_state.summary_history)