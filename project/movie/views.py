from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie
from .serializers import MovieSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET', 'POST'])
def movie_list_create(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        seriailzer = MovieSerializer(movies, many=True)
        return Response(data=seriailzer.data)
    
    if request.method == 'POST':
        seriailzer = MovieSerializer(data=request.data)
        if seriailzer.is_valid(raise_exeption=True):
            seriailzer.save()
            return Response(data=seriailzer.data)