from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    get_posts,
    hello,
    summarize_post_view,
    generate_post_view,
)


# ---- WAY 1: the Router auto-builds all CRUD URLs for the ViewSet ----
# It creates:  /blog/posts/   and   /blog/posts/<id>/
router = DefaultRouter()
router.register('posts', PostViewSet)


urlpatterns = [
    path('hello/', hello),               # from Session 1

    # ---- WAY 2: our manual views get their own explicit URLs ----
    # Listed BEFORE the router so they aren't mistaken for /posts/<id>/
    path('posts/manual/', get_posts),

    # ---- AI features ----
    path('posts/summarize/', summarize_post_view),   # summarize raw text OR a post by id
    path('posts/generate/', generate_post_view),     # generate a post body from a title
]

# add the auto-generated router URLs on top of our manual ones
urlpatterns += router.urls