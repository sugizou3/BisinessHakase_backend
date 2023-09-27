from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment,Dictionary,SearchInfo

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        extra_kwargs= {'password': {'write_only': True, 'required':True }}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    class Meta:
        model=Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img','download')
        extra_kwargs = {'userProfile': {'read_only': True}}

class PostSerializer(serializers.ModelSerializer):
    # word = serializers.SerializerMethodField()
    created_on = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    class Meta:
        model = Post
        fields = ('id','userPost', 'main', 'author','booktitle', 'sub', 'good','word','created_on')
        extra_kwargs = {'userPost': {'read_only': True}}

    # def get_word(self, instance):
    #     return instance.get_word()

class CommentSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment','post','created_on')
        extra_kwargs = {'userComment': {'read_only': True}}

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ('id','text')

class SearchInfoSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    class Meta:
        model = SearchInfo
        fields = ('id','user','count','text','created_on')






