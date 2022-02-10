from django.contrib import admin

from apps.bot.models import Message, Sender


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Добавление модели сообщения в админ-панель.
    """

    readonly_fields = ['sender', 'previous']


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    """Добавление модели отправителя в админ-панель.
    """

    readonly_fields = ['cats', 'breads']
