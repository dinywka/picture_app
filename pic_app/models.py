from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Mem(models.Model):
    """Таблица с мемами"""

    author = models.ForeignKey(to=User, max_length=200, on_delete=models.CASCADE)
    title = models.CharField("Наименование", max_length=200, unique=True)
    description = models.TextField("Описание", default="")
    image = models.ImageField("Изображение", upload_to="images/posts")
    date_time = models.DateTimeField("Дата и время создания", default=timezone.now)
    is_moderate = models.BooleanField("Прошёл ли модерацию", default=False)
    likes = models.IntegerField("Лайки", default=0)
    comments = models.IntegerField("Комментарии", default=0)

    class Meta:
        """Вспомогательный класс"""

        app_label = "pic_app"
        ordering = ("-date_time", "title")
        verbose_name = "Мем"
        verbose_name_plural = "Мемы"

    def __str__(self):
        if self.is_moderate:
            status = "ОК"
        else:
            status = "НА ПРОВЕРКЕ"
        return f"{status} {self.title} {self.date_time} {self.title}"
