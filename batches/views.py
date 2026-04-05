from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Batch
from .serializers import BatchSerializer

# Create your views here.

class BatchViewSet(ModelViewSet):
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Batch.objects.all()

        domain = self.request.query_params.get('domain')
        active = self.request.query_params.get('active')

        if domain:
            # POST api/batches/?domain=
            queryset = queryset.filter(domain=domain)

        # end_date >= today → active
        if active:
            # POST api/batches/?active=true/false
            from datetime import date
            today = date.today()

            if active == 'true':
                queryset = queryset.filter(end_date__gte=today)
            elif active == 'false':
                queryset = queryset.filter(end_date__lt=today)

        return queryset