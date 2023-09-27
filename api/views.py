from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment,Dictionary
from .serializers import UserSerializer, PostSerializer, ProfileSerializer, CommentSerializer
from rest_framework import permissions
from gensim import models
from rest_framework.decorators import action
from rest_framework.response import Response 
from rest_framework import status
from .search import getImportantWords,passDictionary

class IsActiveOrReadOnly(permissions.BasePermission):
    """アカウント取得者以外読み取り専用"""

    def has_permission(self, request, view):
        """GET, HEAD, OPTIONS は常に許可"""
        if request.method in permissions.SAFE_METHODS:
            return True

        # アカウント取得者のみすべて許可
        return request.user.is_active



class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsActiveOrReadOnly] 

    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)

    
    




class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsActiveOrReadOnly]
    

    def perform_create(self, serializer):
        netdata = self.request.data
        data = netdata.copy()
        text = data["main"]+" "+data['sub']+" "+data['author']+" "+data['booktitle']
        words = getImportantWords(text=text,wordBoolean=False)
        word_ids = passDictionary(words)
        serializer.save(userPost=self.request.user,word=word_ids)
    
    
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsActiveOrReadOnly,)


class PostRetrieveView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsActiveOrReadOnly,)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsActiveOrReadOnly] 

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)



class SearchListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Post.objects.all()
        # dictionary = Dictionary.objects.all()
        # print(dictionary)
        main = self.request.query_params.get('main', None)
        if main:
            words = getImportantWords(text=main,wordBoolean=False)
            word_ids = passDictionary(words)

            for id in word_ids:
                queryset = queryset.filter(word__in=[id])

        return queryset
    









