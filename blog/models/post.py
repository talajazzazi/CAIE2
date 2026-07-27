from django.db import models

from .user import User
from .category import Category


# =========================================================
# POST — the main table, with relationships + AI summary
# =========================================================
class Post(models.Model):
    # ForeignKey = "one-to-many": one user writes many posts.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   # delete a user's posts with the user
        related_name='posts',       # reverse access: user.posts.all()
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # keep the post even if its category is gone
        related_name='posts',
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=150)
    content = models.TextField()
    is_published = models.BooleanField(default=True)   # used by the "hide unpublished" rule
    created_at = models.DateTimeField(auto_now_add=True)

    # ---- AI SUMMARY (summarize-by-id task) ----
    # The summarize-by-id endpoint generates a summary from `content` and saves
    # it back HERE, so the result is persisted in the DB rather than being
    # thrown away after the HTTP response. `blank=True` + a default keep the
    # field optional: a post is valid before it has ever been summarized.
    summary = models.TextField(blank=True, default='')
    summary_generated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
