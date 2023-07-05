from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    tag = serializers.SerializerMethodField()
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    comments = serializers.SerializerMethodField(read_only=True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'content', 'tag', 'created_at', 'updated_at', 'comments', 'image']

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['movie']

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        field = '__all__'
