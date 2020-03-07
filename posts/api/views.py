from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from django.contrib.auth.models import User
from posts.models import Post, Comment
from .serializers import PostSerializer


class PostsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentView(APIView):
    def post(self, request, *args, **kwargs):
        comment = request.data.get('comment', None)
        post_id = request.data.get('blogId')

        if comment is None:
            return Response({'message': 'Invalid comment received.'}, status=HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            raise Http404('This page does not exist.')

        new_comment = Comment(
            user=request.user,
            content=comment,
            post=post
        )
        new_comment.save()

        post.comments.add(new_comment)
        post.save()

        return Response({'message': 'Successfully submitted a comment.'}, status=HTTP_200_OK)