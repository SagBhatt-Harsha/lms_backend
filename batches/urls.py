from rest_framework.routers import DefaultRouter
from .views import BatchViewSet

router = DefaultRouter()
router.register('', BatchViewSet, basename='batch')

urlpatterns = router.urls