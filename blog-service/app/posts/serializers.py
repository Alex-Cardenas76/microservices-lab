from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorMiniSerializer
from categories.serializers import CategorySerializer

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorMiniSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    excerpt = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "excerpt", "author", "category", "published_at"]

class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorMiniSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "body", "author", "category", "published_at", "views"]
