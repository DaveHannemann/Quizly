from rest_framework.permissions import BasePermission

class IsAdminOrQuizCreator(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin
        if request.user and request.user.is_staff:
            return True
        
        # Allow access if the user is the creator of the quiz
        return obj.created_by == request.user