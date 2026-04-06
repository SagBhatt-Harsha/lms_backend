from rest_framework.viewsets import ModelViewSet
from accounts.permissions import RolePermission

from .models import Teacher
from .serializers import TeacherSerializer

# Create your views here.

class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [RolePermission]

    def get_queryset(self):
        # This Method Overrides Default queryset.
        # For api endpoint: GET /api/teachers/?domain=
        queryset = Teacher.objects.all()

        # Filter by Domain
        domain = self.request.query_params.get('domain')

        if domain:
            queryset = queryset.filter(domain=domain)

        return queryset
