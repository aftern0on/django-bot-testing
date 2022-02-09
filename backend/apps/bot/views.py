from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot.models import Message as MessageModel
from apps.bot.models import Sender as SenderModel
from apps.util.cat import Cat


class MessageView(APIView):
    """Создание объекта модели сообщения.
    """

    @staticmethod
    def post(request):
        """Отправка нового вопроса и получение ответа. Принимаемые параметры:\n
        user_id (str) - Идентификатор отправителя\n
        message (str) - Сообщение отправителя\n
        Результат: строка с сообщением от бота
        """

        user_id = request.query_params.get('user_id')
        message = request.query_params.get('message')

        if user_id is None or message is None:
            return Response("Отсутствует один или несколько параметров: user_id, message")

        previous = MessageModel.objects.filter(sender__key=user_id).last()
        sender = SenderModel.objects.get_or_create(key=user_id)
        answer = Cat.get_answer(sender[0], message)
        MessageModel(sender=sender[0], text=message, answer=answer, previous=previous).save()
        return Response(answer)


class DataView(APIView):
    """Просмотр данных.
    """

    @staticmethod
    def get(request):
        """Получение данных о съеденном хлебе и котах.\n
        Результат: данные о выборе отправителей в формате {"cats": int, "breads": int}
        """

        cats = 0
        breads = 0
        for sender in SenderModel.objects.all():
            cats += sender.cats
            breads += sender.breads

        return Response({"cats": cats, "breads": breads})


