import os
import time
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/sshleifer/distilbart-cnn-12-6"


def summarize_text(article, summary_length="Medium"):

    token = os.getenv("HF_TOKEN")

    if not token:
        raise Exception(
            "HF_TOKEN is missing from Render Environment Variables."
        )

    article = article.strip()

    if not article:
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

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": article,
        "parameters": {
            "max_new_tokens": max_length,
            "min_new_tokens": min_length,
            "do_sample": False
        }
    }

    start = time.time()

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 401:
            raise Exception(
                "Invalid Hugging Face API token."
            )

        if response.status_code == 403:
            raise Exception(
                "Your Hugging Face token does not have permission to access this model."
            )

        if response.status_code == 429:
            raise Exception(
                "Rate limit exceeded. Please try again later."
            )

        if response.status_code == 503:
            raise Exception(
                "The AI model is loading. Please wait 20–30 seconds and try again."
            )

        if response.status_code != 200:
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise Exception(
                f"Hugging Face API Error ({response.status_code}): {error}"
            )

        result = response.json()

        if (
            not isinstance(result, list)
            or len(result) == 0
            or "summary_text" not in result[0]
        ):
            raise Exception(
                f"Unexpected API response: {result}"
            )

        summary = result[0]["summary_text"]

        processing_time = round(
            time.time() - start,
            2
        )

        return summary, processing_time

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network Error: {e}")


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
            reading_time(original)
            - reading_time(summarized),
            2
        ),
    }