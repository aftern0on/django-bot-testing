"""
Файл конфигурации проекта Django.

Подбробная информация по текущему файлу:
https://docs.djangoproject.com/en/3.2/topics/settings/

Полная документация по settings.py:
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from distutils.util import strtobool
from pathlib import Path
from dotenv import load_dotenv

# Создание пути внутри проекта: BASE_DIR / 'subdir'.
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# Параметры быстрого запуска разработки - не подходят для прода
# Подробная информация: https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: хранить секретный ключ, используемый в производстве, в секрете
SECRET_KEY = os.getenv('SECRET_KEY')

# ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: не запускать с включенной отладкой в рабочей среде
DEBUG = bool(strtobool(os.getenv('DJANGO_DEBUG', default=False)))

# Список всех, кто будет получать уведомления об ошибках кода
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()

# Определение установленных приложений
INSTALLED_APPS = [
    'apps.bot.apps.BotConfig',

    'drf_spectacular',
    'django_filters',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Промежуточное программное обеспечение
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Список IP адресов, имеющие доступ к отладочной информации
INTERNAL_IPS = ['127.0.0.1']

# Путь для импорта Python-модуля с главной конфигурацией URL-ов
ROOT_URLCONF = 'project.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-объект приложения, который будет использовать сервер
WSGI_APPLICATION = 'project.wsgi.application'

# Настройка базы данных
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', default="postgres"),
        'USER': os.getenv('DATABASE_USER', default="postgres"),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', default="postgres"),
        'HOST': os.getenv('DATABASE_HOST', default="database"),
        'PORT': int(os.getenv('DATABASE_PORT', default=5432))
    }
}

# Настройка валидации паролей
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Интернационализация
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static-файлы (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Каталог для работы с файлами
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Тип поля первичного ключа по умолчанию
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.util.pagination.CustomPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Настройка отображения API Django Rest Framework в Swagger
SPECTACULAR_SETTINGS = {
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATION_PARAMETERS': True,
    'COMPONENT_SPLIT_PATCH': False,
    'GENERIC_ADDITIONAL_PROPERTIES': 'dict',
    'SCHEMA_PATH_PREFIX': r'/api/',
}


