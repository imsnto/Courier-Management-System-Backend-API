from rest_framework import permissions



class IsOrderOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f"Checking permissions for user: {request.user}, order: {obj}")
        return request.user == obj.user or request.user.role == 'ADMIN' or request.user == obj.delivery_man
   