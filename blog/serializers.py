from rest_framework import serializers

from .models import Post, Category, Comment, User


# =========================================================
# USER SERIALIZER — for the User model
# =========================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        # ---- DEFAULT WAY: safe here because a User has no password ----
        fields = '__all__'

        # ---- CUSTOMISED WAY: or list exactly the fields you want ----
        # fields = ['id', 'name', 'phone_number', 'is_active', 'created_at']


# =========================================================
# POST SERIALIZER — two ways to choose the fields
# =========================================================
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

        # ---- CUSTOMISED WAY: list exactly the fields you want ----
        # fields = ['id', 'title', 'content', 'author',
        #           'category', 'is_published', 'created_at']


# The other models use the same simple pattern.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'