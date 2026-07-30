from rest_framework.permissions import BasePermission

class IsExamCreatorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == 'SUPER_ADMIN' or obj.created_by == request.user
