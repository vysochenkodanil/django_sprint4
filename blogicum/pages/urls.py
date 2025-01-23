from django.urls import path
from django.views.generic import TemplateView

app_name = 'pages'  # Пространство имён для приложения pages

urlpatterns = [
    # Страница "О проекте"
    path(
        'about/',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'
    ),

    # Страница "Правила"
    path(
        'rules/',
        TemplateView.as_view(template_name='pages/rules.html'),
        name='rules'
    ),
]