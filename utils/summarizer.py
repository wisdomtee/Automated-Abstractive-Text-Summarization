import os
import time
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)


def summarize_text(article, summary_length="Medium"):

    if not article.strip():
        return "", 0

    if summary_length == "Short":
        max_length = 60
        min_length = 20

    elif summary_length == "Medium":
        max_length = 120
        min_length = 40

    else:
        max_length = 180
        min_length = 70

    start = time.time()

    result = client.summarization(
        article,
        model="sshleifer/distilbart-cnn-12-6",
        max_length=max_length,
        min_length=min_length,
    )

    processing_time = round(time.time() - start, 2)

    return result.summary_text, processing_time


def word_count(text):
    return len(text.split())


def reading_time(words):
    return round(words / 200, 2)


def compression(original_words, summary_words):

    if original_words == 0:
        return 0

    return round(
        ((original_words - summary_words) / original_words) * 100,
        1
    )


def generate_statistics(article, summary):

    original = word_count(article)
    summarized = word_count(summary)

    return {
        "original_words": original,
        "summary_words": summarized,
        "compression": compression(original, summarized),
        "original_reading_time": reading_time(original),
        "summary_reading_time": reading_time(summarized),
        "time_saved": round(
            reading_time(original) - reading_time(summarized),
            2
        ),
    }