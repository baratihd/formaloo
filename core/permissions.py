from constants import messages

from rest_framework.permissions import IsAdminUser


__all__ = ('IsSuperUser',)


class IsSuperUser(IsAdminUser):
    message = messages.ACCESS_DENIED

    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view) and request.user.is_authenticated and request.user.is_superuser
        )
