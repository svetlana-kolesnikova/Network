from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """Доступ только для активных сотрудников."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.is_active)
