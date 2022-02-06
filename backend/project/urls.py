"""
Конфигурация URL-адреса проекта.
Список "urlpatterns" направляет URL-адреса в views. Дополнительная информация по ссылке:
https://docs.djangoproject.com/en/3.2/topics/http/urls/
Примеры:
    Представления функций:
        1. Импортирование: from my_app import views
        2. Добавление URL-адрес в urlpatterns: path('', views.home, name='home')
    Представления на основе классов:
        1. Импортирование: from other_app.views import Home
        2. Добавление URL-адрес в urlpatterns: path('', Home.as_view(), name='home')
    Включая другую URL-конфигурацию:
        1. Импортирование функции include(): from django.urls import include, path
        2. Добавление URL-адрес в urlpatterns: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/', include('apps.bot.urls'), name='bot'),

    path('admin/', admin.site.urls),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]

