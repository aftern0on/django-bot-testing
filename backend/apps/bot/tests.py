from django.test import TestCase
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.bot.models import Write, Message


class MessageTestCase(TestCase):
    def setUp(self) -> None:
        self.bread_eater_line = (
            ("first", "/start"),
            ("first", "ага"),
            ("first", "ноуп")
        )
        self.cat_eater_line = (
            ("second", "/start"),
            ("second", "нет, конечно")
        )
        self.cat_eater_answer_multi_case_line = (
            ("third", "/start"),
            ("third", "АгА!!111!111!!"),
            ("third", "_____ПоЖАлуй!!")
        )
        self.switch_to_start_line = (
            ("fourth", "/start"),
            ("fourth", "пожалуй"),
            ("fourth", "/start"),
            ("fourth", "ноуп")
        )
        self.write_with_typos = (
            ("fifth", "/start"),
            ("fifth", "агга конечн"),
            ("fifth", "нааайн")
        )

    def test_get_data(self):
        """Получаем данные ответов пользователей.
        """

        print()
        print("[bot/data] Получаем текущие данные об ответах пользователей")
        answer = self.client.get("/api/bot/data/")
        self.assertEqual(answer.status_code, 200)
        print(f"[bot/data]     {answer.data}")
        print()

        print("[bot/data] Создаем пользователя, съевшего 2 кота и 5 хлеба")
        Write(key="bread_lover", cats=2, breads=5).save()
        answer = self.client.get("/api/bot/data/")
        self.assertEqual(answer.status_code, 200)
        print(f"[bot/data]     {answer.data}")
        print()

        print("[bot/data] Создаем пользователя, съевшего 7 котов и 9 хлеба")
        Write(key="cat_lover", cats=7, breads=9).save()
        answer = self.client.get("/api/bot/data/")
        self.assertEqual(answer.status_code, 200)
        print(f"[bot/data]     {answer.data}")
        print()
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    def test_get_answers(self):
        """Отвечаем на вопросы бота, записываем сообщения.
        """

        print()
        print("[bot/question] Проверка реакции на ответы боту")
        print("[bot/question] Создаем пользователя first, едим хлеб")
        self.run_line(self.bread_eater_line)

        print("[bot/question] Создаем пользователя second, едим кота")
        self.run_line(self.cat_eater_line)

        print("[bot/question] Создаем пользователя third, отвечаем мусорным текстом")
        self.run_line(self.cat_eater_answer_multi_case_line)

        print("[bot/question] Создаем пользователя fourth, сбрасываем диалог через /start")
        self.run_line(self.switch_to_start_line)

        print("[bot/question] Пишем с ошибками")
        self.run_line(self.write_with_typos)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    def run_line(self, request_line):
        """Проверка ветки диалога с ботом.
        """

        for request_data in request_line:
            answer = MessageTestCase.send_answer(self, request_data)
            self.assertEqual(answer.status_code, 200)
            print(f'[bot/question]     {request_data[1]}: {answer.data}')
        print()

    def send_answer(self, request_data) -> Response:
        """Формирование ответа.
        """

        return self.client.post(f'/api/bot/question/?user_id={request_data[0]}&message={request_data[1]}')

