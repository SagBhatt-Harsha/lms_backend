from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mobilization.models import MobilizationRecord
from counselling.models import CounsellingLog
from onboarding.models import Trainee
from batches.models import Batch

from django.db.models import Count
from datetime import date

# Create your views here.

class DashboardMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # TOTAL COUNTS

        total_mobilized = MobilizationRecord.objects.count()

        total_counselled = CounsellingLog.objects.count()

        total_registered = CounsellingLog.objects.filter(
            status="Registered"
        ).count()

        total_onboarded = Trainee.objects.count()

        # GENDER DISTRIBUTION (FROM MOBILIZATION)

        gender_data = MobilizationRecord.objects.values('gender').annotate(
            count=Count('id')
        )

        gender_distribution = {
            item['gender']: item['count'] for item in gender_data
        }

        # COUNSELLING STATUS BREAKDOWN

        status_data = CounsellingLog.objects.values('status').annotate(
            count=Count('id')
        )

        counselling_status_breakdown = {
            item['status']: item['count'] for item in status_data
        }

        # BATCH STATUS

        today = date.today()

        active_batches = Batch.objects.filter(
            end_date__gte=today
        ).count()

        closed_batches = Batch.objects.filter(
            end_date__lt=today
        ).count()

        # RECENT MOBILIZATIONS (LAST 5)

        recent_records = MobilizationRecord.objects.order_by('-date')[:5]

        recent_mobilizations = [
            {
                "id": record.id,
                "name": record.name,
                "mobile": record.mobile,
                "state": record.state,
                "date": record.date
            }
            for record in recent_records
        ]

        # FINAL RESPONSE

        return Response({
            "total_mobilized": total_mobilized,
            "total_counselled": total_counselled,
            "total_registered": total_registered,
            "total_onboarded": total_onboarded,
            "gender_distribution": gender_distribution,
            "counselling_status_breakdown": counselling_status_breakdown,
            "active_batches": active_batches,
            "closed_batches": closed_batches,
            "recent_mobilizations": recent_mobilizations
        })