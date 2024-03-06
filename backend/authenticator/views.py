from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer,
    UserImageSerializer,
)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.
@permission_classes([AllowAny])
class UserRegister(APIView):
    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return JsonResponse(serialized_data.data, status=201)


@permission_classes([AllowAny])
class UserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.token, created = Token.objects.get_or_create(user=user)
        response = UserLoginSerializer(user)
        return JsonResponse(response.data, status=200)


@permission_classes([IsAuthenticated])
class UserLogout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse({}, status=204, safe=False)


@permission_classes([IsAuthenticated])
class UserPasswordChange(APIView):
    def get_object(self):
        return self.request.user

    def patch(self, request):
        user = self.get_object()
        serializer = UserPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data["password"]):
            return JsonResponse(
                {"password": "Incorrect password"}, status=400, safe=False
            )
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return JsonResponse({}, status=204, safe=False)


@permission_classes([IsAuthenticated])
class UploadUserImage(APIView):
    def patch(self, request):
        serialized_data = UserImageSerializer(instance=request.user, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return JsonResponse(serialized_data.data, safe=False)
