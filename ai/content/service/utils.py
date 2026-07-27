# =========================================================
# SHARED SERVICE HELPERS
# =========================================================
# Small, reusable pieces that BOTH services (summarize + generate) depend on.
# Keeping them here — instead of copy-pasting into each service file — is what
# removes duplication while still giving every *service* its own file.
from ..content_client import ContentClient


def validate_text_input(text: str, min_length: int = 20, field_name: str = "Content") -> str:
    """Reject empty/whitespace/too-short input; return the cleaned text."""
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty or whitespace.")

    cleaned_text = text.strip()

    if len(cleaned_text) < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters long.")

    return cleaned_text


def validate_title(title: str, min_length: int = 5) -> str:
    """Title validation is just text validation with a shorter minimum."""
    return validate_text_input(title, min_length, field_name="Title")


def generate_ai_content(prompt: str, system: str = None) -> str:
    """Shared AI execution logic (one client call + output cleaning).

    The ONE place the services reach the client. Both summarize and generate
    call through here, so they always use the SAME ContentClient. The optional
    `system` message is forwarded to the client for callers that need it.
    """
    client = ContentClient()
    result = client.generate(prompt, system=system)

    cleaned_result = result.strip()
    if not cleaned_result:
        raise ValueError("Model output was empty or invalid.")

    return cleaned_result
