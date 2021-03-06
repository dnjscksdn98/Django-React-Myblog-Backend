from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Post, Author, Category, Comment, UserProfile, PostView

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    previous_post = serializers.SerializerMethodField()
    next_post = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'overview',
            'timestamp',
            'author',
            'thumbnail',
            'category',
            'featured',
            'content',
            'previous_post',
            'next_post',
            'comments',
            'likes',
            'view_count',
            'comment_count'
        ]

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data

    def get_category(self, obj):
        return CategorySerializer(obj.category.all(), many=True).data

    def get_previous_post(self, obj):
        return PostSerializer(obj.previous_post).data

    def get_next_post(self, obj):
        return PostSerializer(obj.next_post).data

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id',
            'user',
            'profile_image'
        ]

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title'
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'timestamp',
            'content'
        ]

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    reading_list = serializers.SerializerMethodField()
    my_posts = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'reading_list',
            'my_posts'
        ]

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_reading_list(self, obj):
        return PostViewSerializer(obj.reading_list.all(), many=True).data

    def get_my_posts(self, obj):
        return PostSerializer(obj.my_posts.all(), many=True).data


class PostViewSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = PostView
        fields = [
            'id',
            'post'
        ]

    def get_post(self, obj):
        return PostSerializer(obj.post).data
