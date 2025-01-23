from django.shortcuts import render


def page_not_found(request, exception):
    """Обработчик для ошибки 404 (страница не найдена)."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Обработчик для ошибки 403 (CSRF-защита)."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Обработчик для ошибки 500 (ошибка сервера)."""
    return render(request, 'pages/500.html', status=500)
