# =========================================================
# AI FEATURE — "summarize a post"  (thin view -> service does the AI work)
# =========================================================
# The view handles HTTP ONLY:
#   - read the request
#   - (for post_id) look up the Post and, after summarizing, persist the result
#   - call the service (all AI logic lives THERE)
#   - return a response
#
# Two modes:
#   * {"post_id": <id>}   -> load that Post, summarize its content, SAVE the
#                            summary + timestamp back onto the Post, return it.
#   * {"content": "..."}  -> ad-hoc summarize of raw text (nothing saved).
import logging

from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

# The view knows NOTHING about the model call — only the model and the service.
from ..models import Post
from ai.content.service import summarize_post

# Module-level logger (standard library) — NOT configured via settings.py.
logger = logging.getLogger(__name__)


# =========================================================
# RATE LIMITING — protect the costly AI endpoint
# =========================================================
# UserRateThrottle caps a logged-in USER; for anonymous callers it falls back
# to the IP address — so this one class covers per-user AND per-IP. It uses the
# 'ai' rate (10/hour) defined in settings.REST_FRAMEWORK.
class SummarizeThrottle(UserRateThrottle):
    scope = "ai"


@api_view(["POST"])
@throttle_classes([SummarizeThrottle])
def summarize_post_view(request):
    post_id = request.data.get("post_id")
    try:
        if post_id is not None:
            # ---- MODE 1: summarize an existing post by id, then persist ----
            # The VIEW owns the DB work (look up + save); the SERVICE only
            # summarizes text and never touches HTTP or the database.
            try:
                post = Post.objects.get(pk=post_id)
            except (Post.DoesNotExist, ValueError, TypeError):
                return Response(
                    {"error": f"No post found with id={post_id!r}."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            result = summarize_post(post.content)   # AI logic lives in the service

            post.summary = result["summary"]
            post.summary_generated_at = timezone.now()
            post.save(update_fields=["summary", "summary_generated_at"])

            # Log the OUTCOME only — status + id, never the content.
            logger.info("Summary saved: status=success, post_id=%s", post.id)

            result["post_id"] = post.id
            result["summary_generated_at"] = post.summary_generated_at
        else:
            # ---- MODE 2: stateless summarize of raw text (nothing saved) ----
            text = request.data.get("content", "")
            result = summarize_post(text)

        return Response(result, status=status.HTTP_200_OK)
    except ValueError as exc:
        # Bad INPUT (empty / too short) -> 400
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
