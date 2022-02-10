from django.test import TestCase
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.bot.models import Sender, Message
from apps.util.constant import Constant


class MessageTestCase(TestCase):
    def setUp(self) -> None:
        """Массивы тестовых диалоговых линий. Также указаны ожидаемые ответы от бота для получения оценки результатов.
        """

        self.bread_eater_line = (
            ("first", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("first", "ага", Constant.DIALOGUE.BLOCK.EARS),
            ("first", "ноуп", Constant.DIALOGUE.BLOCK.FINISH_BREAD)
        )
        self.cat_eater_line = (
            ("second", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("second", "нет, конечно", Constant.DIALOGUE.BLOCK.FINISH_CAT)
        )
        self.cat_eater_answer_multi_case_line = (
            ("third", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("third", "АгА!!111!111!!", Constant.DIALOGUE.BLOCK.EARS),
            ("third", "_____ПоЖАлуй!!", Constant.DIALOGUE.BLOCK.FINISH_CAT)
        )
        self.switch_to_start_line = (
            ("fourth", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("fourth", "пожалуй", Constant.DIALOGUE.BLOCK.EARS),
            ("fourth", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("fourth", "ноуп", Constant.DIALOGUE.BLOCK.FINISH_CAT)
        )
        self.write_with_typos = (
            ("fifth", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("fifth", "агга конечн", Constant.DIALOGUE.BLOCK.EARS),
            ("fifth", "нааайн", Constant.DIALOGUE.BLOCK.FINISH_BREAD)
        )
        self.bot_will_start_all_over_again = (
            ("sixth", "/start", Constant.DIALOGUE.BLOCK.FORM),
            ("sixth", "ага", Constant.DIALOGUE.BLOCK.EARS),
            ("sixth", "ноуп", Constant.DIALOGUE.BLOCK.FINISH_BREAD),
            ("sixth", "ыпрып", Constant.DIALOGUE.BLOCK.RETURN),
            ("sixth", "нет, конечно", Constant.DIALOGUE.BLOCK.FINISH_CAT)
        )

    def test_get_data(self):
        """Получаем данные ответов отправителей.
        """

        print()
        print("[bot/data] [*] Получаем текущие данные об ответах отправителей")
        answer = self.client.get("/api/bot/data/")
        mark = '[+]' if answer.data['cats'] == 0 and answer.data['breads'] == 0 else '[_]'
        print(f"[bot/data]     {mark} {answer.data}")
        print()

        print("[bot/data] [*] Создаем отправителя, съевшего 2 кота и 5 хлеба")
        Sender(key="bread_lover", cats=2, breads=5).save()
        answer = self.client.get("/api/bot/data/")
        mark = '[+]' if answer.data['cats'] == 2 and answer.data['breads'] == 5 else '[_]'
        print(f"[bot/data]     {mark} {answer.data}")
        print()

        print("[bot/data] [*] Создаем отправителя, съевшего 7 котов и 9 хлеба")
        Sender(key="cat_lover", cats=7, breads=9).save()
        answer = self.client.get("/api/bot/data/")
        mark = '[+]' if answer.data['cats'] == 9 and answer.data['breads'] == 14 else '[_]'
        print(f"[bot/data]     {mark} {answer.data}")
        print()

        print("[bot/data] [*] Удалим живодера, съевшего 7 котов, добавим отправителя, съевших 17 хлеба")
        Sender.objects.get(key="cat_lover").delete()
        Sender(key="massive_bread_lover", cats=0, breads=17).save()
        answer = self.client.get("/api/bot/data/")
        mark = '[+]' if answer.data['cats'] == 2 and answer.data['breads'] == 22 else '[_]'
        print(f"[bot/data]     {mark} {answer.data}")

        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    def test_get_answers(self):
        """Отвечаем на вопросы бота, записываем сообщения.
        """

        print()
        print("[bot/question] Проверка реакции на ответы боту")
        print("[bot/question] [*] Кушаем хлеб")
        self.run_line(self.bread_eater_line)

        print("[bot/question] [*] Кушаем кота")
        self.run_line(self.cat_eater_line)

        print("[bot/question] [*] Кушаем кота, но с мусорным текстом")
        self.run_line(self.cat_eater_answer_multi_case_line)

        print("[bot/question] [*] Сбрасываем диалог через /start")
        self.run_line(self.switch_to_start_line)

        print("[bot/question] [*] Кушаем хлеб, но делаем это с ошибками")
        self.run_line(self.write_with_typos)

        print("[bot/question] [*] Вынуждаем бота начать диалог снова")
        self.run_line(self.bot_will_start_all_over_again)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    def run_line(self, request_line):
        """Проверка ветки диалога с ботом.
        """

        for request_data in request_line:
            answer = MessageTestCase.send_answer(self, request_data)
            mark = '[+]' if request_data[2] == answer.data else '[_]'
            print(f'[bot/question]     {mark} {request_data[1]}: {answer.data}')
        print()

    def send_answer(self, request_data) -> Response:
        """Формирование ответа.
        """

        return self.client.post(f'/api/bot/question/?user_id={request_data[0]}&message={request_data[1]}')

