from rest_framework.routers import DefaultRouter
from .views import TraineeViewSet

router = DefaultRouter()
router.register('', TraineeViewSet, basename='onboarding')

urlpatterns = router.urls