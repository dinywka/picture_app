from django.urls import path
from pic_app import views

urlpatterns = [
    path("", views.home, name=""),
    path("register/", views.register, name="register"),
    path("login/", views.login_f, name="login"),
    path('logout/', views.logout_f, name="logout")
]