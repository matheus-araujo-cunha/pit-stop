from rest_framework import permissions



class IsAdmPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        staff_methods = {
            "GET",
        }
        if request.method in staff_methods:
            return True

        return request.user.is_superuser           
        