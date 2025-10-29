from rest_framework import serializers
from .models import Author

class AuthorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "display_name"]
