from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
import re
from pic_app import models

# Create your views here.
def home(request):
    return render(request,'picture_app/home.html')

def register(request):
    if request.method == "GET":
        return render(request, "picture_app/register.html")
    elif request.method == "POST":
        email = request.POST.get("email", None)  # Admin1@gmail.com
        password = request.POST.get("password", None)  # Admin1@gmail.com
        if (
                re.match(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", email) is None
        ):
            return render(
                request,
                "picture_app/register.html",
                {"error": "Некорректный формат email или пароль"},
            )
        try:
            User.objects.create(
                username=email,
                password=make_password(password),
                email=email,
            )
        except Exception as error:
            return render(
                request,
                "picture_app/register.html",
                {"error": str(error)},
            )
        return render(request, "picture_app/list.html")
    else:
        raise ValueError("Invalid method")


def login_f(request):
    if request.method == "GET":
        return render(request, "picture_app/login.html", {})
    elif request.method == "POST":
        email = request.POST.get('email')  # user@gmail.com
        password = request.POST.get('password')  # Qwerty!123

        # В первый раз, ты "предъявляешь" логин и пароль, система генерирует тебе токен на 15 минут, и следующие 15 минут "предъявляя" этот токен,
        # ты доказываешь что ты это ты. Система "автоматически" обновляет токен по истечению времени.

        # 1. конфиденциальность - пароль отправляется единожды.
        # 2. брутфорс сильно ослажняется.

        user = authenticate(request, username=email,
                            password=password)  # пытается, взять из базы этого пользователя с этим паролем

        # 1       -> (хэш-функция) -> й3ащшаasdgfsdf124р12141431
        # Qwerty1!-> (хэш-функция) -> й3ащшар32щ1р43124р12141431
        # Qwerty! -> (хэш-функция) -> й3ащшар32щ1р43124р12542153
        if user is None:
            raise Exception("ДАННЫЕ ДЛЯ ВХОДА НЕПРАВИЛЬНЫЕ!")
        else:
            login(request, user)  # сохраняет токен в кукесы(cookies)
            return render(request, "picture_app/list.html")
    else:
        raise Exception("Method not allowed!")


def logout_f(request: HttpRequest) -> HttpResponse:
    """Выход из аккаунта"""
    logout(request)
    return redirect(reverse('login'))


def list_view(request: HttpRequest) -> HttpResponse:
    """_view"""

    memes = models.Mem.objects.all()

    return render(request, "picture_app/list.html", {"images": memes})


def detail_view(request: HttpRequest, pk: str) -> HttpResponse:
    """_view"""
    return redirect(reverse("login"))


# def create_view(request: HttpRequest, pk: str) -> HttpResponse:
#     """_view"""
#     return redirect(reverse("login"))


def create_mem(request):
    """Создание нового мема."""

    if request.method == "GET":
        return render(request, "picture_app/create_mem.html")
    elif request.method == "POST":
        title = request.POST.get("title", None)
        avatar = request.FILES.get("avatar", None)
        models.Mem.objects.create(author=request.user, title=title, description="", image=avatar)  # SQL
        return redirect(reverse("list"))
    else:
        raise ValueError("Invalid method")



def update_mem(request, pk: str):
    """Обновление существующего мема."""

    if request.method == "GET":
        mem = models.Mem.objects.get(id=int(pk))  # SQL
        mem.title = mem.title[::-1]
        # mem.is_moderate = False
        mem.save()
        return redirect(reverse("list_memes"))
    else:
        raise ValueError("Invalid method")


def delete_mem(request, pk: str):
    """Удаление мема."""

    if request.method == "GET":
        mem = models.Mem.objects.get(id=int(pk))  # SQL
        mem.delete()
        return redirect(reverse("list_memes"))
    else:
        raise ValueError("Invalid method")