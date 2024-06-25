from rest_framework import permissions


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    """
    Пермишен, который разрешает доступ на просмотр всем пользователям,
    но разрешает изменение только авторам, модераторам и администраторам.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
