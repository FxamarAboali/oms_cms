from datetime import datetime

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View

from .models import Category, Post


class AllNews(ListView):
    """Список всех статей"""

    def get_queryset(self):
        post_list = Post.objects.filter(
            lang__slug__icontains=self.kwargs.get('lang'),
            category__active=True,
            published=True,
            published_date__lte=datetime.now())

        if self.request.user.is_authenticated:
            posts = post_list
        else:
            posts = post_list.filter(status=False)

        if posts.exists():
            self.paginate_by = posts.first().get_category_paginated()
            self.template_name = posts.first().get_category_template()
            return posts
        else:
            raise Http404()


class News(ListView):
    """Вывод новостей из конкретной категории"""
    def get_queryset(self):
        post_list = Post.objects.filter(
                lang__slug__icontains=self.kwargs.get('lang'),
                category__slug=self.kwargs.get('slug'),
                category__active=True,
                published=True,
                published_date__lte=datetime.now())
        if self.request.user.is_authenticated:
            posts = post_list
        else:
            posts = post_list.filter(status=False)

        if posts.exists():
            self.paginate_by = posts.first().get_category_paginated()
            self.template_name = posts.first().get_category_template()
            return posts
        else:
            raise Http404()


class PostDetail(View):
    """Вывод полной новости"""
    def get(self, request, lang='ru', category=None, post=None):
        modal = request.GET.get("modal", None)
        new = get_object_or_404(
            Post,
            lang__slug__icontains=lang,
            slug=post,
            category__active=True,
            published=True,
            published_date__lte=datetime.now())
        if new.status and request.user.is_authenticated or not new.status:
            new.viewed += 1
            new.save()
            if modal is None:
                return render(request, new.template, {"post": new})
            else:
                return render(request, 'news/modal-news-uikit.html', {"post": new})
        else:
            raise Http404

