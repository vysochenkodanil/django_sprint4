from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostListView, CategoryPostsView, PostDetailView, PostCreateView, ProfileView, PostUpdateView, PostDeleteView
from .views import EditProfileView 

app_name = 'blog'  # Пространство имён для приложения blog

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'category/<slug:category_slug>/',
        CategoryPostsView.as_view(),
        name='category_posts'
    ),
    path('blog/create/', PostCreateView.as_view(), name='create_post'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]