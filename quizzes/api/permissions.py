from rest_framework.permissions import BasePermission

class IsAdminOrQuizCreator(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        
        return obj.created_by == request.user