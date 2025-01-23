from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404

from .models import Category, Post, Comment
from .forms import PostForm, CommentForm, EditProfileForm

User = get_user_model()


class PostListView(ListView):
    """Отображает список опубликованных постов."""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        """Возвращает опубликованные посты с аннотацией количества комментариев."""
        current_time = timezone.now()
        return Post.objects.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class CategoryPostsView(ListView):
    """Отображает список постов в определённой категории."""
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        """Возвращает опубликованные посты в выбранной категории."""
        current_time = timezone.now()
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.objects.filter(
            category=self.category,
            pub_date__lte=current_time,
            is_published=True
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        """Добавляет категорию в контекст."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetailView(DetailView):
    """Отображает детали поста."""
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        """Возвращает пост, если он опубликован или пользователь является автором."""
        post = super().get_object(queryset=queryset)
        current_time = timezone.now()
        if (post.is_published and post.pub_date <= current_time and post.category.is_published) or post.author == self.request.user:
            return post
        raise Http404("Пост не найден или недоступен")

    def get_context_data(self, **kwargs):
        """Добавляет комментарии и форму комментария в контекст."""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('created_at')
        context['form'] = CommentForm()
        context['can_edit'] = self.object.author == self.request.user
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание нового поста."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Устанавливает автора поста и проверяет дату публикации."""
        form.instance.author = self.request.user
        if form.instance.pub_date > timezone.now():
            form.instance.is_published = False
        else:
            form.instance.is_published = True
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправляет на страницу профиля автора после создания поста."""
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование поста."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        """Проверяет, является ли пользователь автором поста."""
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        """Перенаправляет на страницу поста, если пользователь не автор."""
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])

    def get_success_url(self):
        """Перенаправляет на страницу поста после успешного редактирования."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление поста."""
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        """Проверяет, является ли пользователь автором поста."""
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        """Перенаправляет на страницу поста, если пользователь не автор."""
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание нового комментария."""
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html'

    def form_valid(self, form):
        """Устанавливает пост и автора комментария."""
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправляет на страницу поста после создания комментария."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование комментария."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        """Проверяет, является ли пользователь автором комментария."""
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        """Возвращает 404, если пользователь не автор."""
        raise Http404("Комментарий не найден или недоступен")

    def get_success_url(self):
        """Перенаправляет на страницу поста после успешного редактирования."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление комментария."""
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        """Проверяет, является ли пользователь автором комментария."""
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        """Возвращает 404, если пользователь не автор."""
        raise Http404("Комментарий не найден или недоступен")

    def get_success_url(self):
        """Перенаправляет на страницу поста после удаления комментария."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})

    def get_context_data(self, **kwargs):
        """Не передаёт объект формы в контекст для страницы удаления."""
        context = super().get_context_data(**kwargs)
        if '/delete_comment/' in self.request.path:
            context.pop('form', None)
        return context


class ProfileView(DetailView):
    """Отображает профиль пользователя."""
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        """Добавляет посты пользователя в контекст."""
        context = super().get_context_data(**kwargs)
        profile = self.object
        current_time = timezone.now()

        if self.request.user == profile:
            posts = Post.objects.filter(author=profile)
        else:
            posts = Post.objects.filter(
                author=profile,
                pub_date__lte=current_time,
                is_published=True,
                category__is_published=True
            )

        posts = posts.annotate(comment_count=Count('comments')).order_by('-pub_date')
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя."""
    model = User
    form_class = EditProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя для редактирования."""
        return self.request.user

    def get_success_url(self):
        """Перенаправляет на страницу профиля после редактирования."""
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})