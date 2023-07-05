from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="movie"
urlpatterns = [
    path('', views.movie_list_create),
    path('<int:movie_id>', views.movie_detail_update_delete),
    path('<int:movie_id>/comment', views.comment_read_create),
    path('tags/<tag_name>', views.find_tag),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)