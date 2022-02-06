from random import choice
from apps.bot.models import Write
from fuzzywuzzy import fuzz


class Cat:
    answer_yes = ["конечно", "ага", "пожалуй"]
    answer_no = ["нетконечно", "ноуп", "найн"]

    @staticmethod
    def get_answer(write: Write, message: str):
        """Получение ответа от бота.
        """

        # Сброс/начало диалога
        if message == "/start":
            return Cat.set_step(
                write, Write.STEP.STEP_ONE, "Привет! Я могу отличить кота от хлеба! Объект перед тобой квадратный?")

        # Сбрасываем лишние символы, оставляем только буквы, все в нижний регистр
        message = ''.join(ch for ch in message.lower() if ch.isalpha())

        # Ищем ошибки, формируем сообщение о нахождении ошибки если она есть
        message = Cat.find_an_error(message)

        # Находимся на этапе формы
        if write.step == Write.STEP.STEP_ONE:
            # Объект не квадратный
            if message in Cat.answer_no:
                write.cats += 1
                return Cat.set_step(write, Write.STEP.STEP_FINISH, "Это кот, а не хлеб! Не ешь его!")
            # Квадратный
            if message in Cat.answer_yes:
                return Cat.set_step(write, Write.STEP.STEP_TWO, "У него есть уши?")

        # Находимся на этапе ушей
        if write.step == Write.STEP.STEP_TWO:
            # Объект с ушами
            if message in Cat.answer_yes:
                write.cats += 1
                return Cat.set_step(write, Write.STEP.STEP_FINISH, "Это кот, а не хлеб! Не ешь его!")
            # Объект не с ушами, все нормально
            if message in Cat.answer_no:
                write.breads += 1
                return Cat.set_step(write, Write.STEP.STEP_FINISH, "Это хлеб, а не кот! Ешь его!")

        # Если финишная прямая и пользователь что-то еще сказал
        if write.step == Write.STEP.STEP_FINISH:
            return Cat.set_step(write, Write.STEP.STEP_ONE, "Давай-ка начнем сначала. Объект перед тобой квадратный?")

        # Если бот ничего не понял
        return choice(["Чего-чего?", "Повтори-ка!"])

    @staticmethod
    def set_step(write, step, message):
        """Переопределяет текущее положение пользователя в диалоге.
        """

        write.step = step
        write.save()
        return message

    @staticmethod
    def find_an_error(message) -> [bool, str]:
        """Перебор всех вариантов для поиска похожего экземпляра без ошибки.
        Возвращает кортеж: флаг об исправлении сообщения и само сообщение.
        """

        # Если слово уже есть в массивах
        if message in Cat.answer_yes or message in Cat.answer_no:
            return message

        # Итерируем все доступные варианты на поиск очепяток
        last_data = [0, ""]
        for variable in Cat.answer_yes + Cat.answer_no:
            output = fuzz.ratio(message, variable)
            if output > 50 and output > last_data[0]:
                last_data = [output, variable]

        if last_data[0]:
            return last_data[1]

        # Вообще ничего не подходит
        return message

