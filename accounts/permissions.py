from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        # If not logged in
        if not user or not user.is_authenticated:
            return False

        action = view.action  # list, create, update, destroy etc.

        # ADMIN HAS FULL ACCESS
        if user.role == "admin":
            return True

        # ---------------- MOBILIZATION ----------------
        if view.basename == 'mobilization':
            # view.basename uses basename Attribute of router.register() Method.
            if action in ['list', 'retrieve', 'search']:
                return user.role != "trainee"
            if action == 'create':
                return user.role in ["admin", "mobilizer"]
            if action in ['update', 'partial_update']:
                return user.role in ["admin", "mobilizer"]
            if action == 'destroy':
                return user.role == "admin"

        # ---------------- COUNSELLING ----------------
        if view.basename == 'counselling':
            if action in ['list', 'retrieve']:
                return user.role in ["admin", "counsellor", "teacher"]
            if action == 'create':
                return user.role in ["admin", "counsellor"]
            if action == 'status':  # custom action
                return user.role in ["admin", "counsellor"]
            if action == 'destroy':
                return user.role == "admin"

        # ---------------- TEACHERS ----------------
        if view.basename == 'teacher':
            if action == 'list':
                return user.role in ["admin", "counsellor"]
            if action == 'create':
                return user.role == "admin"
            if action == 'destroy':
                return user.role == "admin"

        # ---------------- BATCHES ----------------
        if view.basename == 'batch':
            if action == 'list':
                return user.role not in ["mobilizer", "trainee"]
            if action in ['create', 'update', 'partial_update']:
                return user.role in ["admin", "counsellor"]
            if action == 'destroy':
                return user.role == "admin"

        # ---------------- ONBOARDING ----------------
        if view.basename == 'onboarding':
            if action in ['list', 'retrieve']:
                return user.role in ["admin", "counsellor", "teacher"]
            if action in ['create', 'update', 'partial_update', 'batch']:
                return user.role in ["admin", "counsellor"]
            if action == 'destroy':
                return user.role == "admin"

        return False