from rest_framework import serializers

from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

        # `summary` / `summary_generated_at` are produced by the AI service,
        # never by the client — mark them read-only so a caller can't POST
        # their own fake summary through the normal CRUD endpoints.
        read_only_fields = ['summary', 'summary_generated_at']
