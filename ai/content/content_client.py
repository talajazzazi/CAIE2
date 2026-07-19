# =========================================================
# THE CLIENT LAYER  —  the boundary to the outside world
# =========================================================
# This is the ONLY file that talks to the model. Switching the
# provider (stub -> OpenAI) changes THIS file and nothing else —
# the service pipeline and the view don't move at all.
#
# The API key lives in your .env, NEVER in the code:
#   OPENAI_API_KEY=sk-...

from decouple import config
from openai import OpenAI


class ContentClient:
    """Talks to the OpenAI API. The single point of contact with the model."""

    def __init__(self):
        # Read the key from .env via python-decouple (same as settings.py).
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))

    # ---- (real OpenAI call) ----
    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",                     # cheap + good for summaries
            messages=[{"role": "user", "content": prompt}],
        )
        # Return PLAIN TEXT so the service layer stays unchanged.
        return response.choices[0].message.content