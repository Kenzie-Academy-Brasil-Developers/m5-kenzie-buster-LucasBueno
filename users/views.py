from rest_framework.views import APIView, Request, Response, status
from .models import User
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from movies.permissions import IsOwner


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    ...


class OldLoginView2(APIView):
    def post(self, request: Request) -> Response:
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
      
        return Response(
            {"token": serializer.validated_data["refresh"]}, status.HTTP_200_OK
        )


class OldLoginView1(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        #    user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return_refresh = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(
            {"token": return_refresh["refresh"]}, status.HTTP_200_OK
        )
