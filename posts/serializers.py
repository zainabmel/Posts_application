#This file used to convert python objects to JSON

from rest_framework import serializers
from .models import Post
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_name', 'content', 'created_at', 'updated_at']

