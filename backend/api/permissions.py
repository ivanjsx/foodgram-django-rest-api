from rest_framework.permissions import (SAFE_METHODS, AllowAny, BasePermission,
                                        IsAuthenticatedOrReadOnly)



class UserViewSetPermission(AllowAny):
    """
    Safe methods are allowed to all users, including anonymous.
    Neither authentication is required to create a user.
    Once created, for further unsafe operations on a user,
    authentication as the django administrator is required.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )



class IsAdminOrReadOnly(BasePermission):
    """
    Safe methods are allowed to all users, including anonymous.
    To perform any unsafe operations,
    authentication as the django administrator is required.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
