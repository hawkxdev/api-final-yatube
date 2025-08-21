"""ViewSets для API."""

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets

from posts.models import Group, Post
from .permissions import AuthorOnlyEditPermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOnlyEditPermission,)

    def perform_create(self, serializer):
        """Автоматическая привязка автора."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOnlyEditPermission,)

    def get_queryset(self):
        """Фильтрация по посту."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        """Автоматическая привязка автора и поста."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для подписок."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Только подписки текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Автоматическая привязка пользователя."""
        serializer.save(user=self.request.user)
