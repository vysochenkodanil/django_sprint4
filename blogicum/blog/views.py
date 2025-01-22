from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Category, Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import EditProfileForm
from django.contrib.auth.models import User
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Comment
from .forms import CommentForm
from django.db.models import Count


User = get_user_model()

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html' 

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.post_id})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html' # Используем существующий шаблон
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.post_id})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.pub_date > timezone.now():
            form.instance.is_published = False
        else:
            form.instance.is_published = True
        return super().form_valid(form)    

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = None  # Убедитесь, что форма не передаётся для удаления
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'  # Шаблон для редактирования поста
    pk_url_kwarg = 'post_id'  # Имя параметра URL для идентификатора поста

    def get_success_url(self):
        # Перенаправляем на страницу отредактированной публикации
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.pk})

    def test_func(self):
        # Проверяем, является ли пользователь автором публикации
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        # Если пользователь не автор, перенаправляем на страницу поста
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user  # Редактируем текущего пользователя

    def get_success_url(self):
        # Динамически формируем success_url с username текущего пользователя
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})
    
class ProfileContextMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object  # Получаем объект пользователя
        posts = Post.objects.filter(author=profile).order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(posts, 10)  # 10 постов на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        return context
    

class ProfileView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        current_time = timezone.now()
        posts = Post.objects.filter(
            author=profile,
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        current_time = timezone.now()
        return Post.objects.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')

class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        current_time = timezone.now()
        queryset = Post.objects.select_related('category', 'location', 'author')
        post = get_object_or_404(
            queryset,
            pk=self.kwargs['post_id'],
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем форму для комментариев в контекст
        context['form'] = CommentForm()
        # Добавляем список комментариев в контекст
        context['comments'] = self.object.comments.all()
        return context
