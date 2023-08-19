from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from pic_app import utils
from django.urls import reverse
import random
import re
from pic_app import models
import requests
from bs4 import BeautifulSoup

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
        return redirect(reverse("list"))
    else:
        raise ValueError("Invalid method")


def delete_mem(request, pk: str):
    """Удаление мема."""

    if request.method == "GET":
        mem = models.Mem.objects.get(id=int(pk))  # SQL
        mem.delete()
        return redirect(reverse("list"))
    else:
        raise ValueError("Invalid method")


def tags(request):
    memes = [
        {
            "id": x,
            "title": f"Наименование {x}",
            "description": {"data1": {"price": random.randint(1, 1000000) + random.random()}}

        }
        for x in range(1, 20 + 1)
    ]
    return render(request, "picture_app/tags.html", {"memes": memes})



def news_list(request):
    """Возврат списка новостей."""

    search = request.POST.get("search", "")
    news = utils.CustomCache.caching(key="news_list", timeout=2,
                                     lambda_func=lambda: models.News.objects.all().filter(is_ban=False).filter(
                                         title__icontains=search))
    current_page = utils.CustomPaginator.paginate(object_list=news, limit=3, request=request)
    return render(request, "picture_app/news_list.html", context={"current_page": current_page, "search": search})


def news_detail(request, pk):
    """Возврат новости."""

    new = utils.CustomCache.caching(key="news_detail_" + str(pk), timeout=5,
                                    lambda_func=lambda: models.News.objects.get(id=int(pk)))
    comments = utils.CustomCache.caching(key="comments_news_detail_" + str(pk), timeout=1,
                                         lambda_func=lambda: models.NewsComments.objects.filter(news=new))
    current_page = utils.CustomPaginator.paginate(object_list=comments, limit=3, request=request)

    post_rating_objs = models.NewsRatings.objects.all().filter(post=new)
    rating = post_rating_objs.filter(status=True).count() - post_rating_objs.filter(status=False).count()
    count_r = post_rating_objs.count()

    return render(request, "picture_app/news_detail.html", context=
    {"new": new, "current_page": current_page, "rating": {"rating": rating, "count_r": count_r}
     })


def news_comments_create(request, pk):
    """Создание комментария."""

    if request.method != "POST":
        raise Exception("Invalid method")

    news = models.News.objects.get(id=int(pk))
    user = request.user
    text = request.POST.get("text", "")
    models.NewsComments.objects.create(news=news, author=user, text=text)

    return redirect(reverse('news_detail', args=(pk,)))


def rating_change(request, pk, status):
    """Создаёт рейтинг к новости"""

    if request.method == "GET":
        post_obj = models.News.objects.get(id=int(pk))
        author_obj = request.user
        status = True if int(status) == 1 else False
        post_rating_objs = models.NewsRatings.objects.filter(post=post_obj, author=author_obj)
        if len(post_rating_objs) <= 0:
            models.NewsRatings.objects.create(post=post_obj, author=author_obj, status=status)
        else:
            post_rating_obj = post_rating_objs[0]
            if (status is True and post_rating_obj.status is True) or \
                    (status is False and post_rating_obj.status is False):
                post_rating_obj.delete()
            else:
                post_rating_obj.status = status
                post_rating_obj.save()
        return redirect(reverse('news_detail', args=[pk]))
    else:
        raise Exception("Method not allowed!")


def valute(request):
    #выводить на страницу курс валют: доллар, юань, рубль
    url = "https://kase.kz/ru/currency/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    kzt_usd = get_valute(soup, "#USDKZT")
    kzt_cny = get_valute(soup, "#CNYKZT")
    kzt_rub = get_valute(soup, "#RUBKZT")
    return HttpResponse(f"KZT TO USD = {kzt_usd}, CNY TO KZT = {kzt_cny}, RUB TO KZT = {kzt_rub}")

def get_valute(soup, href):
    usd = soup.find_all('a', href=href)
    currency = list(filter(lambda x: len(x) > 1, usd[0].text.split(' ')))[1].strip()
    return currency

def get_api_valute(request):
    data = {
        "USD": 450,
        "RUB": 4.5,
        "CNY": 64,
    }
    return JsonResponse(data)


