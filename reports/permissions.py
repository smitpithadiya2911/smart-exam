from rest_framework.permissions import BasePermission

class IsReportAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role in ['SUPER_ADMIN', 'TEACHER'] or request.user.is_superuser)
