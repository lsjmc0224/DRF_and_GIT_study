from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET', 'POST'])
def movie_list_create(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        
@api_view(['GET', 'PATCH', 'DELETE'])
def movie_detail_update_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        movie.delete()
        data = {
            'deleted_movie':movie_id
        }
        return Response(data)

@api_view(['GET', 'POST'])
def comment_read_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(movie=movie)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie)
        return Response(serializer.data)
