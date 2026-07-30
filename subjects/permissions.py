from rest_framework.permissions import BasePermission

class IsSubjectTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == 'SUPER_ADMIN' or obj.assigned_teacher == request.user
