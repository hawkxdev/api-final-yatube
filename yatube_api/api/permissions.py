"""Кастомные права доступа."""

from rest_framework import permissions


class AuthorOnlyEditPermission(permissions.BasePermission):
    """Права автора контента."""

    def has_permission(self, request, view):
        """Проверка базовых прав."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка прав объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
