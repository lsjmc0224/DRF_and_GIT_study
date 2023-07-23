from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .models import Movie, Comment, Tag
from .serializers import MovieSerializer, CommentSerializer, TagSerializer, MovieListSerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    # serializer_class = MovieSerializer
    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        else: 
            return MovieSerializer
    
    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsAdminUser()]
        return []

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        movie = serializer.instance
        self.handle_tags(movie)

        return Response(serializer.data)
    
    def perform_update(self, serializer):
        movie = serializer.save()
        movie.tag.clear()
        self.handle_tags(movie)

    def handle_tags(self, movie):
        words = movie.content.split(' ')
        tag_list = []
        for w in words:
            if w[0] == '#':
                tag_list.append(w[1:])
        
        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            movie.tag.add(tag)

        movie.save()
    @action(methods=["GET"], detail=False)
    def recommend(self, request):
        ran_movie = self.get_queryset().order_by("?").first()
        ran_movie_serializer = MovieListSerializer(ran_movie)
        return Response(ran_movie_serializer.data)
    
    @action(methods=["GET"], detail=True)
    def test(self, request, pk=None):
        test_movie = self.get_object()
        test_movie.num += 1
        test_movie.save(update_fields=["num"])
        return Response()

class CommentViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

class MovieCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        movie = self.kwargs.get("movie_id")
        queryset = Comment.objects.filter(movie_id=movie)
        return queryset

    # def list(self, request, movie_id=None):
    #     movie = get_object_or_404(Movie, id=movie_id)
    #     queryset = self.filter_queryset(self.get_queryset().filter(movie=movie))
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    def create(self, request, movie_id=None):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie)
        return Response(serializer.data) 

class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    lookup_url_kwarg = "tag_name"

    def retrieve(self, request, *args, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag = get_object_or_404(Tag, name=tag_name)
        movies = Movie.objects.filter(tag=tag)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
