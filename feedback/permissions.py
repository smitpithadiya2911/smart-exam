from rest_framework.permissions import BasePermission

class IsFeedbackOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == 'SUPER_ADMIN' or obj.user == request.user
