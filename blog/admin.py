from django.contrib import admin

from .models import User, Category, Post, Comment


# ---- CUSTOMIZED WAY (control how the model is displayed) ----
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'is_published')


# Our User is a PLAIN model (no passwords/permissions), so a normal
# ModelAdmin fits — NOT the auth UserAdmin.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'is_active', 'created_at')
    search_fields = ('name', 'phone_number')
    list_filter = ('is_active', 'created_at')


admin.site.register(Category)
admin.site.register(Comment)
