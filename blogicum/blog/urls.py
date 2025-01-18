from django.urls import path
from .views import PostListView, CategoryPostsView, PostDetailView, PostCreateView
from .views import profile


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'category/<slug:category_slug>/',
        CategoryPostsView.as_view(),
        name='category_posts'
    ),
    path('blog/create/', PostCreateView.as_view(), name='create_post'),
    path('profile/<str:username>/', profile, name='profile'),
    
]
