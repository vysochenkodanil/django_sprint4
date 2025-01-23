from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.conf.urls.static import static
from blog.views import ProfileView

# Обработчики ошибок
handler404 = 'pages.views.page_not_found'  # Ошибка 404
handler500 = 'pages.views.server_error'    # Ошибка 500

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Приложение blog
    path('', include('blog.urls', namespace='blog')),

    # Приложение pages
    path('pages/', include('pages.urls', namespace='pages')),

    # Аутентификация (встроенные представления Django)
    path('accounts/', include('django.contrib.auth.urls')),

    # Регистрация
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),

    # Профиль пользователя
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),

    # Изменение пароля
    # path(
    #     'password_change/',
    #     auth_views.PasswordChangeView.as_view(
    #         template_name='registration/password_change_form.html',
    #         success_url=reverse_lazy('password_change_done'),
    #     ),
    #     name='password_change',
    # ),
    # path(
    #     'password_change/done/',
    #     auth_views.PasswordChangeDoneView.as_view(
    #         template_name='registration/password_change_done.html',
    #     ),
    #     name='password_change_done',
    # ),
    # path('auth/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('auth/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path(
    'auth/password_change/',
    auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',  # Ваш шаблон
        success_url=reverse_lazy('password_change_done'),  # Перенаправление после успешного изменения
    ),
    name='password_change',
    ),
    path(
    'auth/password_change/done/',
    auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html',  # Ваш шаблон
    ),
    name='password_change_done',
    ),

    # Сброс пароля
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

# Подключение медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)