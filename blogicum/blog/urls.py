from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostListView, CategoryPostsView, PostDetailView, PostCreateView, ProfileView, PostUpdateView, PostDeleteView
from .views import EditProfileView 
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView
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
    path('posts/<int:post_id>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='delete_post'),
    
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', CommentDeleteView.as_view(), name='delete_comment'),
]