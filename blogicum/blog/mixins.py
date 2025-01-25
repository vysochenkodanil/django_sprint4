from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone

from .models import Post


class PublishedPostsMixin:
    """Миксин для выборки опубликованных постов."""

    def get_published_posts(self):
        """Возвращает опубликованные посты."""
        current_time = timezone.now()
        return Post.objects.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class AuthorCheckMixin(UserPassesTestMixin):
    """Миксин для проверки авторства."""

    def test_func(self):
        """Проверяет, является ли пользователь автором объекта."""
        obj = self.get_object()
        return self.request.user == obj.author

    def handle_no_permission(self):
        """Обрабатывает случай, если пользователь не автор."""
        if isinstance(self.get_object(), Post):
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        raise Http404("Объект не найден или недоступен")
