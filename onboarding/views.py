from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trainee
from .serializers import TraineeSerializer
from batches.models import Batch

# Create your views here.

class TraineeViewSet(ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(registered_by=self.request.user)

    # Custom Endpoint: PATCH /api/onboarding/{id}/batch/
    @action(detail=True, methods=['get', 'patch'])
    def batch(self, request, pk=None):
        trainee = self.get_object()

        batch_id = request.data.get('batch')

        if batch_id:
            batch = Batch.objects.get(id=batch_id)

            # VALIDATION
            if batch.domain != trainee.domain:
                return Response({"error": "Domain mismatch"}, status=400)

            if batch.slot != trainee.slot:
                return Response({"error": "Slot mismatch"}, status=400)

            trainee.batch = batch
        else:
            trainee.batch = None

        trainee.save()

        if request.method == 'GET':
            return Response({
                "id": trainee.id,
                "name": trainee.name,
                "batch": {
                    "id": trainee.batch.id,
                    "name": trainee.batch.name
                } if trainee.batch else None
            })
        
        return Response({
            "id": trainee.id,
            "name": trainee.name,
            "batch": {
                "id": trainee.batch.id,
                "name": trainee.batch.name
            } if trainee.batch else None
        })