from django.urls import path
from . import views

urlpatterns = [
    path("user/register", views.UserRegister.as_view()),
    path("user/login", views.UserLogin.as_view()),
    path("user/logout", views.UserLogout.as_view()),
    path("user/edit/password", views.UserPasswordChange.as_view()),
    path("user/edit/image", views.UploadUserImage.as_view()),
]
