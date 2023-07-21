from django import template
import datetime
from django.contrib.auth.models import User, Group
from pic_app import models
import locale


# Фильтры и тэги (jinja)
# Для изменения отображения данных в шаблоне, для логики внутри шаблонов

# 0. strftime
# 1. Смена округления
# 2. Сменить запятую на точку, и наоборот (разные языки)
# 3. Формат с разделителями (раздение числа при слишком больших значениях)
# 4. Нужно написать тэг, который проверяет группы у пользователя


register = template.Library()


@register.simple_tag(takes_context=True)
def check_user_group(context: str, groups: str = "", cnt=1, c=1) -> bool:
    try:
        user: User = context["request"].user

        # print(groups)       # "Модераторы контента, Модераторы, Модераторы, Привет"
        groups_list = sorted(list(set([x.strip() for x in groups.split(",")])), reverse=False)
        # print(groups_list)  # ['Модераторы', 'Модераторы контента', 'Привет']

        this_user_groups: list[str] = [x.name for x in user.groups.all()]
        # print(this_user_groups)  # ['Модераторы контента', 'Основатели']

        for i in this_user_groups:      # линейная
            # for j in groups_list:     # квадратичная
            #     if i == j:
            #         return True
            if i in groups_list:
                return True
        return False
    except Exception as error:
        print("error simple_tag check_user_group: ", error)
        return False


@register.simple_tag(name='digit_beautify')
def digit_beautify(value):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    return locale.format_string('%.2f', value, grouping=True)



@register.simple_tag(takes_context=True)
def text_upper_case(context: str, text: str):
    try:
        return str(text).upper() + " kokos"
    except Exception as error:
        print("error simple_tag text_upper_case: ", error)
        return ""


@register.filter(name="format_datetime")
def format_datetime(source: datetime.datetime, format: str = ""):  # SIMPLE TAG
    """Преобразует дату в строку в формате datetime"""

    # , tz_hours: float = 6.0
    # source = source + datetime.timedelta(hours=tz_hours)

    match format:  # match-case (switch-case - js/go) - хэширует(запоминает) значения своих кейсов
        case "time":
            return source.strftime("%H:%M:%S")
        case "time1":
            return source.strftime("%H-%M-%S")
        case "date":
            return source.strftime("%d.%m.%Y")
        case "date2":
            return source.strftime("%d.%m.%Y") + "banana"
        case _:
            return source


@register.filter(name="rounding")
def rounding(source: float | int, count_len: int = 0):
    """Округление дробных значений"""
    # try:
    if count_len < 0:
        raise ValueError(f"ERROR count_len = {count_len}")
    elif count_len == 0:
        return int(source)
    else:
        return round(source, count_len)
    # except Exception as e:
    #     print(e)
    #     return source


@register.filter(name="my_slice")
def my_slice(source: str, length: int):
    """"""

    return source[:length]


@register.filter
def capitalize_first_letter(text):
    return text.capitalize()


@register.simple_tag(name="bold_italic")
def bold_italic(text):
    return f"✻{text}✻"