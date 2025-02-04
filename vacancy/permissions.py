from rest_framework.permissions import BasePermission

class IsStudentUser(BasePermission):
    """
    Custom permission to allow only students to access the job vacancies.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'STUDENT'