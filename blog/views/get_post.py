from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Post
from ..serializers import PostSerializer


# =========================================================
# WAY 1 — AUTOMATIC (ViewSet + Router)
# One small class gives you list / retrieve / create / update / delete.
# =========================================================
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# =========================================================
# WAY 2 — MANUAL (function-based view): pagination + business rules.
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
