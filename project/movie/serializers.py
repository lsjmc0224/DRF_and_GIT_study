from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    tag = serializers.SerializerMethodField()

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id', 'name', 'content', 'created_at', 'updated_at', 'comments', 'num']

class MovieListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]
    
    class Meta:
        model = Movie
        fields = ['id', 'name', 'created_at', 'updated_at', 'image', 'comments_cnt', 'tag']
        read_only_fields = ['id','name', 'created_at', 'comments_cnt']
    

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['movie']

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        field = '__all__'
