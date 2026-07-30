from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.permissions import BasePermission

def role_required(allowed_roles):
    """
    Decorator for views to enforce user role restrictions.
    allowed_roles: list or tuple of role strings e.g. ['SUPER_ADMIN', 'TEACHER']
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('login')
            if request.user.role not in allowed_roles and not request.user.is_superuser:
                messages.error(request, "Access denied. You do not have permission to view this resource.")
                raise PermissionDenied("You do not have permission to perform this action.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'SUPER_ADMIN' or request.user.is_superuser)

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'TEACHER' or request.user.is_superuser)

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'STUDENT' or request.user.is_superuser)
