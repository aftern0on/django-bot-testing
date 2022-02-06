from django.urls import path, include, re_path
from rest_framework import routers
from apps.bot.views import MessageView, DataView

urlpatterns = [
    path(r'bot/question/', MessageView.as_view()),
    path(r'bot/data/', DataView.as_view())
]

