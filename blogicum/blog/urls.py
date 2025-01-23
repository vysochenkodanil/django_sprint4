from django.urls import path
from .views import (
    PostListView,
    CategoryPostsView,
    PostDetailView,
    PostCreateView,
    ProfileView,
    PostUpdateView,
    PostDeleteView,
    EditProfileView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

app_name = 'blog'  # Пространство имён для приложения blog

urlpatterns = [
    # Главная страница со списком постов
    path('', PostListView.as_view(), name='index'),

    # Страница поста
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),

    # Страница постов в категории
    path(
        'category/<slug:category_slug>/',
        CategoryPostsView.as_view(),
        name='category_posts'
    ),

    # Создание нового поста
    path('blog/create/', PostCreateView.as_view(), name='create_post'),

    # Профиль пользователя
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),

    # Редактирование профиля
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),

    # Создание поста (альтернативный путь)
    path('posts/create/', PostCreateView.as_view(), name='post_create'),

    # Редактирование поста
    path(
        'posts/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='edit_post'),

    # Удаление поста
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'),

    # Создание комментария
    path(
        'posts/<int:post_id>/comment/',
        CommentCreateView.as_view(),
        name='add_comment'),

    # Редактирование комментария
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        CommentUpdateView.as_view(),
        name='edit_comment'
    ),

    # Удаление комментария
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment'
    ),
]
