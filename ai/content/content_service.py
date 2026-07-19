# =========================================================
# THE SERVICE LAYER  —  the AI logic (NO HTTP here)
# =========================================================
# Pattern 2: treat AI as ONE step in a pipeline, never the whole
# thing. The model call sits in the middle, wrapped by validation
# on BOTH sides:
#
#   1. input validation   -> reject bad input BEFORE paying for a call
#   2. AI processing       -> the single, isolated call to the client
#   3. post-processing     -> clean + validate the probabilistic output
#   4. response formatting -> shape a predictable result for the caller

from ai.content.content_client import ContentClient


# ---- DEFAULT WAY (a bare function that only calls the model) ----
# def summarize_post(text):
#     client = ContentClient()
#     return client.generate(text)


# ---- CUSTOMISED WAY (full pipeline with validation on both sides) ----
def summarize_post(text):
    # STAGE 1 — input validation (cheap guard before spending a call)
    if not text or not text.strip():
        raise ValueError("No content was provided to summarize.")
    if len(text.strip()) < 20:
        raise ValueError("Content is too short to summarize.")

    # STAGE 2 — AI processing (the ONE call, hidden behind the client)
    client = ContentClient()
    prompt = _build_prompt(text)
    raw_output = client.generate(prompt)

    # STAGE 3 — post-processing (NEVER trust probabilistic output)
    summary = _clean_output(raw_output)
    if not summary:
        raise ValueError("The AI returned an empty summary.")

    # STAGE 4 — response formatting (a clean, predictable shape)
    return {
        "summary": summary,
        "length": len(summary),
    }


# =========================================================
# Private helpers — small pieces, easy to unit-test on their own
# =========================================================
def _build_prompt(text):
    # The prompt lives in ONE place. Change it here, nowhere else.
    return f"Summarize this blog post in one short paragraph:\n\n{text}"


def _clean_output(raw_output):
    # Sanitize the messy model text: trim spaces + blank lines.
    return raw_output.strip()