from django.urls import path
from .views import *
from . import views

app_name="movie"
urlpatterns = [
    path('', views.movie_list_create),
]