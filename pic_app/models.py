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

    class Meta:
        """Вспомогательный класс"""

        app_label = "django_app"
        ordering = ("-date_time", "title")
        verbose_name = "Мем"
        verbose_name_plural = "Мемы"

    def __str__(self):
        if self.is_moderate:
            status = "ОК"
        else:
            status = "НА ПРОВЕРКЕ"
        return f"{status} {self.title} {self.date_time} {self.title}"
#
# class PostComments(models.Model):
#     """
#     CREATE TABLE IF NOT EXISTS post_comments
#     (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title_id INTEGER,
#     author TEXT,
#     text TEXT,
#     datetime TEXT DEFAULT CURRENT_TIMESTAMP
#     )
#     ''')
#     """
#
#     post_id = models.IntegerField("Публикация, к которой комментарий")
#     author = models.CharField("Автор", max_length=200)
#     text = models.TextField("Текст комментария", )
#     date_time = models.DateTimeField("Дата и время создания", default=timezone.now)
#
#     class Meta:
#         app_label = "django_app"
#         ordering = ("-date_time", "post_id")
#         verbose_name = "Комментарий к публикации"
#         verbose_name_plural = "Комментарии к публикациям"
#
#     def __str__(self):
#         return f"{self.post_id} {self.date_time} {self.author}"
#
#
# class PostRatings(models.Model):
#     """
#     CREATE TABLE IF NOT EXISTS post_ratings
#     (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title_id INTEGER,
#     rating INTEGER
#     )
#     """
#
#     author = models.ForeignKey(
#         to=User,
#         on_delete=models.CASCADE  # удаление
#     )
#     post = models.ForeignKey(
#         to=Posts,
#         on_delete=models.CASCADE
#     )
#     status = models.BooleanField(default=False)  # Лайк или дизлайк
#
#     class Meta:
#         app_label = "django_app"
#         ordering = ("-post", "author")
#         verbose_name = "Рейтинг к публикации"
#         verbose_name_plural = "Рейтинги к публикациям"
#
#     def __str__(self):
#         if self.status:
#             like = "ЛАЙК"
#         else:
#             like = "ДИЗЛАЙК"
#         return f"{self.post.title} {self.author.username} {like}"
#
#
#
