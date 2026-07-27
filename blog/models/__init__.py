# Re-export every model so the rest of the codebase can keep doing
#   from blog.models import Post          (or  from .models import Post)
# exactly as before — the split into per-file modules is invisible to callers.
# Django also needs each model imported HERE so its app registry discovers them.
from .user import User
from .category import Category
from .post import Post
from .comment import Comment
__all__ = ['User', 'Category', 'Post', 'Comment']
