from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Category, Post
from django.views.generic import ListView, DetailView, CreateView
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import EditProfileForm  # Импортируем кастомную форму
from django.contrib.auth.models import User



User = get_user_model()

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
    model = User  # Модель, с которой работает представление
    template_name = 'blog/profile.html'  # Шаблон для отображения
    context_object_name = 'profile'  # Имя объекта в контексте шаблона
    slug_field = 'username'  # Поле для поиска пользователя
    slug_url_kwarg = 'username'  # Имя параметра URL

    def get_context_data(self, **kwargs):
        # Получаем контекст от родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем объект пользователя
        profile = self.object
        # Получаем публикации пользователя (если у вас есть модель Post)
        posts = Post.objects.filter(author=profile).order_by('-created_at')
        # Пагинация
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Добавляем публикации в контекст
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
        ).order_by('-pub_date')

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
        ).order_by('-pub_date')

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
        return get_object_or_404(
            Post,
            pk=self.kwargs['post_id'],
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        )

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        # Присваиваем автора, чтобы не просрать
        form.instance.author = self.request.user
        return super().form_valid(form)