import time
import streamlit as st
from transformers import pipeline


# -----------------------------------------------------
# Load Model (Cached)
# -----------------------------------------------------

@st.cache_resource
def load_model():
    """
    Load the summarization pipeline only once.
    """

    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

    return summarizer


# -----------------------------------------------------
# Generate Summary
# -----------------------------------------------------

def summarize_text(article, summary_length="Medium"):
    """
    Generate a summary using DistilBART.
    """

    summarizer = load_model()

    article = article.strip()

    if not article:
        return "", 0

    if summary_length == "Short":
        max_len = 60
        min_len = 20

    elif summary_length == "Medium":
        max_len = 120
        min_len = 40

    else:
        max_len = 180
        min_len = 70

    start_time = time.time()

    summary = summarizer(
        article,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        truncation=True
    )[0]["summary_text"]

    processing_time = round(
        time.time() - start_time,
        2
    )

    return summary, processing_time


# -----------------------------------------------------
# Word Count
# -----------------------------------------------------

def word_count(text):
    return len(text.split())


# -----------------------------------------------------
# Reading Time
# -----------------------------------------------------

def reading_time(words):
    """
    Average reading speed:
    200 words per minute
    """

    return round(words / 200, 2)


# -----------------------------------------------------
# Compression Percentage
# -----------------------------------------------------

def compression(original_words, summary_words):

    if original_words == 0:
        return 0

    return round(
        ((original_words - summary_words) / original_words) * 100,
        1
    )


# -----------------------------------------------------
# Statistics
# -----------------------------------------------------

def generate_statistics(article, summary):
    """
    Return useful summary statistics.
    """

    original_words = word_count(article)

    summary_words = word_count(summary)

    stats = {

        "original_words": original_words,

        "summary_words": summary_words,

        "compression": compression(
            original_words,
            summary_words
        ),

        "original_reading_time":
            reading_time(original_words),

        "summary_reading_time":
            reading_time(summary_words),

        "time_saved":
            round(
                reading_time(original_words)
                -
                reading_time(summary_words),
                2
            )

    }

    return stats