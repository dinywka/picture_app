from django.urls import path
from pic_app import views

urlpatterns = [
    path("", views.home, name=""),
    path("register/", views.register, name="register"),
    path("login/", views.login_f, name="login"),
    path('logout/', views.logout_f, name="logout"),

    path("list/", views.list_view, name="list"),
    path("tags/", views.tags, name="tags"),

    #
    path("list/", views.list_view, name="posts"),
    path("detail/<str:pk>/", views.detail_view, name="post_detail"),
    path("detail/<str:pk>/", views.detail_view, name="post_change"),
    path("detail/<str:pk>/", views.detail_view, name="post_delete"),
    #
    path("detail/<str:pk>/", views.detail_view, name="detail"),
    path("create/", views.create_mem, name="create_mem"),

]