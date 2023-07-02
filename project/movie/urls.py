from django.urls import path
from .views import *
from . import views

app_name="movie"
urlpatterns = [
    path('', views.movie_list_create),
    path('<int:movie_id>', views.movie_detail_update_delete),
    path('<int:movie_id>/comment', views.comment_read_create),
]