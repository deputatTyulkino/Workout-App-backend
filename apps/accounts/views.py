from functools import partial

from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import CreateUserSerializer, LoginSerializer, ResponseAuthSerializer, ProfileSerializer

tags = ['auth']


# Create your views here.
class RegisterAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer

    @extend_schema(
        summary='Регистрация пользователя',
        description='Api для реслизации пользователя с использованием JWT',
        tags=tags,
        responses=ResponseAuthSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        serializer = self.get_serializer(user)
        return Response(
            data={
                'user': serializer.data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    @extend_schema(
        summary='Вход в систему',
        description='Api для входа пользователя в систему',
        tags=tags,
        request=LoginSerializer,
        responses=ResponseAuthSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateProfileAPIView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary='Обновление данных пользователя',
        tags=tags,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Частичное обновление данных пользователя',
        tags=tags,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
