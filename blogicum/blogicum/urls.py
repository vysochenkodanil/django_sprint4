from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from blog.views import ProfileView
from django.contrib.auth.forms import UserChangeForm
# Ошибка 404
handler404 = 'pages.views.page_not_found'
# Ошибка 500
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/', 
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),

    # # Редактирование профиля
    # path('edit_profile/', auth_views.PasswordChangeView.as_view(
    #     template_name='blog/profile.html',
    #     form_class=UserChangeForm,
    #     success_url=reverse_lazy('pages:homepage'),
    # ), name='edit_profile'),

    # Изменение пароля
    # path('password_change/', auth_views.PasswordChangeView.as_view(
    #     template_name='registration/password_change_form.html',
    #     success_url=reverse_lazy('blog:password_change_done'),
    # ), name='password_change'),

    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='registration/password_change_done.html',
    # ), name='password_change_done'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',  # Шаблон для формы изменения пароля
            success_url=reverse_lazy('password_change_done'),  # Перенаправление после успешного изменения пароля
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html',  # Ваш шаблон
        ),
        name='password_change_done',
    ),
]