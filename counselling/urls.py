from rest_framework.routers import DefaultRouter
from .views import CounsellingViewSet

router = DefaultRouter()
router.register('', CounsellingViewSet, basename='counselling')

urlpatterns = router.urls