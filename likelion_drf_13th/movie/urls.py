from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, CommentViewSet, MovieCommentViewSet,TagViewSet
# from .views import *
# from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'movie'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("movies", MovieViewSet)

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", CommentViewSet, basename="comments")

movie_comment_router = routers.SimpleRouter(trailing_slash=False)
movie_comment_router.register("comments", MovieCommentViewSet, basename="comments")

tag_router = routers.SimpleRouter(trailing_slash=False)
tag_router.register("tags", TagViewSet, basename="tags")



urlpatterns = [
    #  path('', views.movie_list_create),
    #  path('<int:movie_id>', views.movie_detail_update_delete),
    # path('<int:movie_id>/comment', views.comment_read_create),
    # path('tags/<str:tags_name>', views.find_tag),
    path("", include(default_router.urls)),
    path("", include(comment_router.urls)),
    path("movies/<int:movie_id>/", include(movie_comment_router.urls)),
    path("", include(tag_router.urls)),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)