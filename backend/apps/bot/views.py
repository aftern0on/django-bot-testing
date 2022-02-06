from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot.models import Message as MessageModel
from apps.bot.models import Write as WriteModel
from apps.util.cat import Cat


class MessageView(APIView):
    """Создание объекта модели сообщения.
    """

    @staticmethod
    def post(request):
        """Отправка нового вопроса и получение ответа. Принимаемые параметры:\n
        user_id (str) - Идентификатор пользователя\n
        message (str) - Сообщение пользователя\n
        Результат: строка с сообщением от бота
        """

        user_id = request.query_params.get('user_id')
        message = request.query_params.get('message')

        if user_id is None or message is None:
            return Response("Отсутствует один или несколько параметров: user_id, message")

        previous = MessageModel.objects.filter(write__key=user_id).last()
        write = WriteModel.objects.get_or_create(key=user_id)
        answer = Cat.get_answer(write[0], message)
        MessageModel(write=write[0], text=message, answer=answer, previous=previous).save()
        return Response(answer)


class DataView(APIView):
    """Просмотр данных.
    """

    @staticmethod
    def get(request):
        """Получение данных о съеденном хлебе и котах.\n
        Результат: данные о выборе пользователей в формате {"cats": int, "breads": int}
        """

        cats = 0
        breads = 0
        for writer in WriteModel.objects.all():
            cats += writer.cats
            breads += writer.breads

        return Response({"cats": cats, "breads": breads})


