from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment
from .serializers import UserSerializer, PostSerializer, ProfileSerializer, CommentSerializer
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """管理者以外読み取り専用"""

    def has_permission(self, request, view):
        """GET, HEAD, OPTIONS は常に許可"""
        if request.method in permissions.SAFE_METHODS:
            return True

        # 管理者のみすべて許可
        return request.user.is_superuser



class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [IsAdminOrReadOnly] 

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
    
    

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrReadOnly,)


class PostRetrieveView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrReadOnly,)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly] 

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)








