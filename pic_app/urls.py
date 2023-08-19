from django.urls import path
from pic_app import views

urlpatterns = [
    path("", views.home, name=""),
    path("register/", views.register, name="register"),
    path("login/", views.login_f, name="login"),
    path('logout/', views.logout_f, name="logout"),

    path("list/", views.list_view, name="list"),
    path("tags/", views.tags, name="tags"),

    path("delete_mem/<str:pk>/", views.delete_mem, name="delete_mem"),

    #
    path("news/list/", views.news_list, name="news_list"),
    path("news/detail/<str:pk>/", views.news_detail, name="news_detail"),
    path("news/comments/create/<str:pk>/", views.news_comments_create, name="news_comments_create"),
    path('rating/change/<str:pk>/<str:status>/', views.rating_change, name="rating_change"),

    path("create/", views.create_mem, name="create_mem"),
    path("valute/", views.valute, name="valute"),
    path("api/valute", views.get_api_valute, name="api_valute")

]