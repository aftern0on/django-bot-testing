from django.contrib import admin

from apps.bot.models import Message, Write


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Добавление сообщения в админ-панель.
    """

    readonly_fields = ['write', 'previous']


@admin.register(Write)
class WriteAdmin(admin.ModelAdmin):
    """Добавление пользователя в админ-панель.
    """

    readonly_fields = ['key', 'cats', 'breads']
