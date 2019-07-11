from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from photologue.models import Gallery, Photo


class Category(MPTTModel):
    """Класс модели категорий сетей"""
    name = models.CharField("Название", max_length=50)
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    template = models.CharField("Шаблон", max_length=500, default="news/post_list.html")
    slug = models.SlugField("url", unique=True, max_length=100, blank=True, null=True)
    active = models.BooleanField("Отображать?", default=True)
    paginated = models.PositiveIntegerField("Количество новостей на странице", default=5)

    class Meta:
        verbose_name = "Категория новостей"
        verbose_name_plural = "Категории новостей"

    def get_absolute_url(self):
        return reverse('list-news', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Tags(models.Model):
    """Класс модели тегов"""
    name = models.CharField("Тег", max_length=50, unique=True)
    slug = models.SlugField("url", unique=True, max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Post(models.Model):
    """Класс модели поста"""
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField("Заголовок", max_length=500)
    subtitle = models.CharField("Под заголовок", max_length=500, blank=True, null=True)
    mini_text = models.TextField("Краткое содержание", max_length=5000)
    text = models.TextField("Полное содержание", max_length=10000000)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    edit_date = models.DateTimeField(
        "Дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,
        blank=True,
        null=True)

    photo = models.ForeignKey(
        Photo,
        verbose_name="Главная фотография",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    gallery = models.ForeignKey(
        Gallery,
        verbose_name="Фотографии",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    tag = models.ManyToManyField(Tags, verbose_name="Тег", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    template = models.CharField("Шаблон", max_length=500, default="news/post_detail.html")
    slug = models.SlugField("url", max_length=500, unique=True)

    published = models.BooleanField("Опубликовать?", default=True)
    viewed = models.IntegerField("Просмотрено", default=0)
    status = models.BooleanField("Для зарегистрированных", default=False)
    background_color = models.CharField(
        "Цвет фона",
        help_text="#000000",
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-published_date"]

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_category_slug(self):
        return self.category.slug

    def get_category_template(self):
        return self.category.template

    def get_category_paginated(self):
        return self.category.paginated

    def get_absolute_url(self):
        return reverse('new-detail', kwargs={'category': self.category.slug, 'post': self.slug})

    def __str__(self):
        return "{}".format(self.title)


class Comments(models.Model):
    """Модель коментариев к новостям"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="Новость", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=2000)
    date = models.DateTimeField("Дата", auto_now_add=True)
    update = models.DateTimeField("Изменен", auto_now=True)
    parent_comment = models.ForeignKey(
        "self",
        verbose_name="Родительский комментарий",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return "{} - {}".format(self.user, self.post)
