from django.http import HttpResponse

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer

# Import the AI feature from the SERVICE layer.
# The view knows NOTHING about the model or the client — only the service.
from ai.content.content_service import summarize_post

# 
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

def hello(request):
    return HttpResponse("Hello Django!")


# =========================================================
# WAY 1 — AUTOMATIC (ViewSet + Router)
# One small class gives you list / retrieve / create / update / delete.
# =========================================================
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# =========================================================
# WAY 2 — MANUAL (function-based view)
# More code, but full control: pagination + business rules.
# =========================================================
@api_view(["GET"])
def get_posts(request):
    try:
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 10))
        start = (page - 1) * limit
        end = start + limit

        posts = Post.objects.filter(is_published=True)[start:end]

        serializer = PostSerializer(posts, many=True)
        return Response(
            {"page": page, "limit": limit, "results": serializer.data},
            status=status.HTTP_200_OK,
        )
    except Exception:
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    # GET /blog/posts/manual/?page=1&limit=5


# =========================================================
# AI FEATURE — "summarize a post"  (Session 2 architecture)
# =========================================================
# The view handles HTTP ONLY:
#   - read the request
#   - call the service  (all AI logic lives THERE, not here)
#   - return a response
#
# ---- WRONG WAY (what beginners do — commented out on purpose) ----
# @api_view(["POST"])
# def summarize_post_view(request):
#     text = request.data.get("content", "")
#     client = ContentClient()                 # model call inside the view :(
#     raw = client.generate(text)              # no validation, not reusable,
#     return Response({"summary": raw})        # not testable without the web layer
#
# ---- CUSTOMISED WAY (thin view -> service does the work) ----
@api_view(["POST"])
def summarize_post_view(request):
    text = request.data.get("content", "")
    try:
        result = summarize_post(text)                  # the service pipeline
        return Response(result, status=status.HTTP_200_OK)
    except ValueError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(
#     method="post",
#     operation_summary="Summarize a blog post",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=["content"],
#         properties={
#             "content": openapi.Schema(
#                 type=openapi.TYPE_STRING,
#                 description="The blog post text to summarize (min 20 characters).",
#                 example="Django is a high-level Python web framework that "
#                         "encourages rapid development and clean design.",
#             ),
#         },
#     ),
#     responses={
#         200: openapi.Response(
#             description="Summary generated",
#             schema=openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "summary": openapi.Schema(type=openapi.TYPE_STRING),
#                     "length": openapi.Schema(type=openapi.TYPE_INTEGER),
#                 },
#             ),
#         ),
#         400: openapi.Response(description="Validation error (empty or too-short content)"),
#     },
# )
# @api_view(["POST"])
# def summarize_post_view(request):
#     text = request.data.get("content", "")
#     try:
#         result = summarize_post(text)
#         return Response(result, status=status.HTTP_200_OK)
#     except ValueError as exc:
#         return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)