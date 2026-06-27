from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import CreateUserSerializer, LoginUserSerializer
from .services import UserService


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = CreateUserSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = UserService.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "message": "User created successfully.",
                "data": result,
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = UserService.login_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if result is None:
            return Response(
                {
                    "message": "Invalid username or password.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {
                "message": "Login successful.",
                "data": result,
            },
            status=status.HTTP_200_OK,
        )
