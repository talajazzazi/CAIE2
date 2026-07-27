# =========================================================
# SERVICE — generate a blog post from a title  (NO HTTP here)
# =========================================================
# Same four-stage pipeline as summarize; the only real differences are the
# validation rule (title length) and the output fields (title + content).
import logging

from .utils import validate_title, generate_ai_content

# Module-level logger (standard library) — NOT configured via settings.py.
logger = logging.getLogger(__name__)


# Max character count for the generated body.
MAX_CONTENT_LENGTH = 500


# The prompt text lives in exactly ONE place. Tone is added only when provided.
def _build_generate_prompt(title: str, tone: str = None) -> str:
    prompt = f"Write a short blog post about: {title}."

    if tone:
        prompt += f" Write it in a {tone} tone."

    prompt += f" Keep the total output under {MAX_CONTENT_LENGTH} characters."
    return prompt


def generate_post(title: str, tone: str = None) -> dict:
    # --- Validation (minimum 5 characters) ---
    cleaned_title = validate_title(title, min_length=5)

    # --- AI (build prompt, call the client once, clean the output) ---
    prompt = _build_generate_prompt(cleaned_title, tone)
    try:
        cleaned_content = generate_ai_content(prompt)
    except Exception:
        # Log the FACT of the failure — never the prompt or the title.
        logger.error("Generate failed: AI service error")
        raise

    # --- Post-processing (hard cap the body at 500 characters) ---
    if len(cleaned_content) > MAX_CONTENT_LENGTH:
        cleaned_content = cleaned_content[:MAX_CONTENT_LENGTH]

    # --- Formatting (a predictable shape) ---
    logger.info("Generate succeeded: status=success, length=%s", len(cleaned_content))
    return {
        "title": cleaned_title,
        "content": cleaned_content,
        "length": len(cleaned_content),
    }
