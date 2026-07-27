# =========================================================
# AI FEATURE — "generate a post from a title"  (thin view -> service)
# =========================================================
# HTTP ONLY: read the title (and optional tone), call the service, return it.
# All prompt building / validation lives in the service, never here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ai.content.service import generate_post


@api_view(["POST"])
def generate_post_view(request):
    title = request.data.get("title", "")
    tone = request.data.get("tone")   # optional
    try:
        result = generate_post(title, tone)
        return Response(result, status=status.HTTP_200_OK)
    except ValueError as exc:
        # Bad INPUT (empty / too short title) -> 400
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
