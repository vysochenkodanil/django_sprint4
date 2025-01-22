from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from blog.views import ProfileView
from django.conf import settings
from django.conf.urls.static import static
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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)