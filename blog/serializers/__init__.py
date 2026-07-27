# Re-export so callers keep doing  from .serializers import PostSerializer
from .user import UserSerializer
from .post import PostSerializer
from .category import CategorySerializer
from .comment import CommentSerializer

__all__ = [
    'UserSerializer',
    'PostSerializer',
    'CategorySerializer',
    'CommentSerializer',
]
