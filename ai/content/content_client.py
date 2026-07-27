# =========================================================
# THE CLIENT LAYER  —  the boundary to the outside world
# =========================================================
# This is the ONLY file that talks to the model. Switching the provider
# (e.g. OpenAI -> another vendor) changes THIS file and nothing else — the
# service pipeline and the views never move.
#
# Secure key management:
# The API key is a CREDENTIAL. It lives in .env, is loaded ONCE in
# settings.py, and is READ from there here. We never touch the environment
# directly and we NEVER hardcode the key.

from django.conf import settings          # read the key/model from ONE place
from openai import OpenAI


class ContentClient:
    """Talks to the OpenAI API. The single point of contact with the model."""

    def __init__(self):
        # ---- BAD WAY — NEVER do this ----
        # self.client = OpenAI(api_key="sk-1234567890abcdef")  # hardcoded -> leaks
        #
        # ---- GOOD WAY — settings.py loads it from .env, we just read settings ----
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, prompt, system=None):
        """Send a prompt to the model and return its reply as PLAIN TEXT.

        A SYSTEM message (when provided) sets firm boundaries the user text
        cannot override. It stays OPTIONAL so the client remains generic and
        reusable across services. Returning a plain string keeps the service
        layer independent of the provider's response objects — swap the vendor
        and callers don't change.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,   # a small, cheap chat model is fine here
            messages=messages,
        )
        return response.choices[0].message.content
