from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from django.views.generic import ListView, DetailView



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
    # Количество постов на странице
    paginate_by = 10  

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
