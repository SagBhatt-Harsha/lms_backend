from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import UserSerializer

# Create your views here.

class LoginView(APIView):
    """
    POST /api/auth/login/
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })

class MeView(APIView):
    """
    GET /api/auth/me/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class LogoutView(APIView):
    """
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"})

