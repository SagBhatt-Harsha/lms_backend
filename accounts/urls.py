from django.urls import path
from .views import LoginView, MeView, LogoutView

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/me/', MeView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]