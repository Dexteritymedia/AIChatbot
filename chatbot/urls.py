from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("sign-up/", views.RegisterView.as_view(), name='register'),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("chat/<int:session_id>", views.chatbot_page, name="chatbot_page"),
]
