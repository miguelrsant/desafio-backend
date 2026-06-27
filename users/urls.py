from django.urls import path

from .views import UserCreateView, UserLoginView

urlpatterns = [
    path("register", UserCreateView.as_view()),
    path("login", UserLoginView.as_view())
]
