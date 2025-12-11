from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission personnalisée:
    - Admin peut tout faire
    - User peut voir/modifier uniquement ses tickets
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin a tous les droits
        if request.user.role == 'admin':
            return True
        
        # User peut voir ses propres tickets
        return obj.created_by == request.user

class IsAdmin(permissions.BasePermission):
    """
    Seulement les admins
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

## 📂 Vérifiez votre structure
