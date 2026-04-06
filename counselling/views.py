from rest_framework.viewsets import ModelViewSet
from accounts.permissions import RolePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import CounsellingLog
from .serializers import CounsellingSerializer

# Create your views here.

class CounsellingViewSet(ModelViewSet):
    queryset = CounsellingLog.objects.all()
    serializer_class = CounsellingSerializer
    permission_classes = [RolePermission]

    def perform_create(self, serializer):
        '''Logged-in User's id is stored in counselled_by Field.'''
        serializer.save(counselled_by=self.request.user)

    @action(detail=True, methods=['get', 'patch'])
    # Above line tells DRF:“Create a custom route inside this ViewSet”. detail=True means this endpoint works on a Single Object.So, DRF adds {id} to the endpoint. DRF uses function name as URL path.

    def status(self, request, pk=None):
        '''For Custom Patch Operation.
        API Endpoint: PATCH /api/counselling/{id}/status/'''
        instance = self.get_object()

        if request.method == 'GET':
            return Response({
                "id": instance.id,
                "status": instance.status,
                "slot": instance.slot,
                "domain": instance.domain
            })
        
        new_status = request.data.get('status')
        slot = request.data.get('slot')
        domain = request.data.get('domain')

        if not new_status:
            return Response({"error": "Status required"}, status=400)

        # Apply validation logic
        if new_status == "Registered":
            if not slot or not domain:
                return Response(
                    {"error": "Both Slot and Domain required when Registered"},
                    status=400
                )

        instance.status = new_status
        instance.slot = slot
        instance.domain = domain
        instance.save()

        return Response({
            "id": instance.id,
            "status": instance.status,
            "slot": instance.slot,
            "domain": instance.domain
        })