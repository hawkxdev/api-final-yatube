"""Кастомные права доступа."""

from typing import Any

from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import APIView


class AuthorOnlyEditPermission(permissions.BasePermission):
    """Права автора контента."""

    def has_permission(self, request: HttpRequest, view: APIView) -> bool:
        """Проверка базовых прав."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self, request: HttpRequest, view: APIView, obj: Any
    ) -> bool:
        """Проверка прав объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
