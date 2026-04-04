from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import MobilizationRecord
from .serializers import MobilizationSerializer

# Create your views here.

class MobilizationViewSet(ModelViewSet):
    queryset = MobilizationRecord.objects.all()
    serializer_class = MobilizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        state = self.request.query_params.get('state')

        if state:
            return self.queryset.filter(state=state)

        return self.queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        mobile = request.query_params.get('mobile')

        records = self.queryset.filter(mobile=mobile)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)