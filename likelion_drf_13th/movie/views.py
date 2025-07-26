from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view #데코레이터
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import Movie, Comment, Tag
from .serializers import MovieSerializer, CommentSerializer, TagSerializer, MovieListSerializer

from django.shortcuts import get_object_or_404

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    # serializer_class = MovieSerializer
    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        return MovieSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
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
        movie.tags.clear()
        self.handle_tags(movie)

    def handle_tags(self, movie):
        tags = [words[1:] for words in movie.content.split(' ') if words.startswith('#')]
        for t in tags:
            tag, created = Tag.objects.get_or_create(name=t)
            movie.tags.add(tag)
        movie.save()
    
    @action(methods=['GET'], detail=False)
    def recommend(self, request):
        ran_movie = self.get_queryset().order_by("?").first()
        ran_movie_serializer = MovieListSerializer(ran_movie)
        return Response(ran_movie_serializer.data)
    
    @action(methods=['GET'], detail=True)
    def test(self, request, pk=None):
        test_movie = self.get_object()
        test_movie.click_num+=1
        test_movie.save(update_fields=['click_num'])
        return Response()
# @api_view(['GET', 'POST'])
# def movie_list_create(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(data=serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             content = request.data['content']
#             movie = get_object_or_404(Movie, id = serializer.data['id'])
#             tags = [words[1:] for words in content.split(' ') if words.startswith('#')]
#             for t in tags:
#                 try:
#                     tag = get_object_or_404(Tag, name = t)
#                 except:
#                     tag = Tag(name=t)
#                     tag.save()
#                 movie.tag.add(tag)
#             movie.save()
#         return Response(data=MovieSerializer(movie).data)
        
# @api_view(['GET', 'PATCH', 'DELETE'])
# def movie_detail_update_delete(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)

#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     elif request.method == 'PATCH':
#         serializer = MovieSerializer(instance=movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             movie = get_object_or_404(Movie, id = serializer.data['id'])
#             movie.tag.clear()
#             content = request.data['content']
#             tags = [words[1:] for words in content.split(' ') if words.startswith('#')]
#             for t in tags:
#                 try:
#                     tag = get_object_or_404(Tag, name = t)
#                 except:
#                     tag = Tag(name=t)
#                     tag.save()
#                 movie.tag.add(tag)
#             movie.save() 
#         return Response(data = MovieSerializer(movie).data)
#     elif request.method == 'DELETE':
#         movie.delete()
#         data = {
#             'deleted_movie': movie_id
#         }
#         return Response(data)

#댓글 디테일 조회 수정 삭제   
class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsOwnerOrReadOnly()]
        return []
#영화 게시물에 있는 댓글 목록 조회, 영화 게시물에 댓글 작성
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


# @api_view(['GET', 'POST'])
# def comment_read_create(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     if request.method == 'GET':
#         comments = Comment.objects.filter(movie=movie)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(data=serializer.data)
    
#     if request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(movie=movie)
#         return Response(data=serializer.data)
    
class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    lookup_url_kwarg="tag_name"

    def retrieve(self, request, *args, **kwargs):
        tag_name=kwargs.get("tag_name")
        tags=get_object_or_404(Tag, name=tag_name)
        movies=Movie.objects.filter(tags=tags)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

# @api_view(['GET'])
# def find_tag(request, tags_name):
#     tags = get_object_or_404(Tag, name = tags_name)
#     if request.method == 'GET':
#         movie = Movie.objects.filter(tags__in=[tags])
#         serializer = MovieSerializer(movie, many=True)
#         return Response(data=serializer.data)

