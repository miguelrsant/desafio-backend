from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User


class UserService:

    @staticmethod
    def create_user(username: str, password: str):

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        refresh = RefreshToken.for_user(user)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
            },
        }

    @staticmethod
    def login_user(username: str, password: str):

        user = authenticate(username=username, password=password)

        if user is None:
            return None

        refresh = RefreshToken.for_user(user)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
