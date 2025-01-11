from django.urls import path

from .views import PostListView, CategoryPostsView, PostDetailView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'category/<slug:category_slug>/',
        CategoryPostsView.as_view(),
        name='category_posts'
    ),
]
