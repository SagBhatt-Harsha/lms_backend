from rest_framework.routers import DefaultRouter
from .views import MobilizationViewSet

router = DefaultRouter()
router.register('', MobilizationViewSet, basename='mobilization')

urlpatterns = router.urls