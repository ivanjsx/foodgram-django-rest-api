from rest_framework.permissions import (SAFE_METHODS, AllowAny, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class RecipeViewSetPermission(IsAuthenticatedOrReadOnly):
    """
    Safe methods are allowed to all users, including anonymous.
    To create a recipe, authentication is required.
    Once created, for further unsafe operations on a recipe,
    authentication as the recipe author is required.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
        )


class UserViewSetPermission(AllowAny):
    """
    Safe methods are allowed to all users, including anonymous.
    Neither authentication is required to create a user.
    Once created, for further unsafe operations on a user,
    authentication as the project administrator is required.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class SetOnesPasswordActionPermission(BasePermission):
    """
    Safe methods are disabled at the action level.
    To change any user's password,
    authentication as the project administrator is required.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Safe methods are allowed to all users, including anonymous.
    To perform any unsafe operations,
    authentication as the project administrator is required.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )
