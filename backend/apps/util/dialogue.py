from fuzzywuzzy import fuzz
from random import choice
from typing import Union, List

from apps.bot.models import Sender
from apps.util.constant import Constant


class Dialogue:
    """Описание сценария диалога с ботом.
    Сценарий диалога на данный момент (написанный лично Тарантино):

                                     /start
                                        │
                          ┌─Да──Объект квадратный?──Нет─┐
                          │                             │
            ┌─Да──У него есть уши?──Нет─┐            Это кот
            │                           │
         Это кот                    Это хлеб

    Модуль работает по "блочному принципу":
        Диалог состоит из блоков. Блоком является обработчик сообщений.
        Каждое полученное сообщение будет проходить через текущий обработчик отправителя.
        В данном случае первым блоком, присваивающийся новым отправителям по умолчанию является "Start".
        Этот обработчик проверяет: если message == "/start" - переход к последующему блоку "Объект квадратный?".
        Если нет - бот будет негодовать.

    Перед обработкой сообщение фильтруется от лишнего мусора и форматируется.
    Также проходится проверка на наличие ошибок путем обработки результата метрики Расстояния Левенштейна
    (через fuzzywuzzy на данный момент) относительно полученной строки и всех имеющихся вариантов ответов.
    Более предпочтительным вариантом является тот, в сравнении с которым редакционная разность является минимальной.
    """

    class BLOCK:
        """Класс, хранящий все описанные блоки.
        Описанные блоки также должны ассоциироваться с пользовательскими этапами.
        Этапы являются неотъемлемой частью модели отправителя, указаны они в `apps.bot.models.Sender.STAGE`.
        """

        class Functional:
            def __init__(self, function):
                """Декоратор, описывающий встроенный функционал.
                """

                self.function = function

            def __call__(self, sender: Sender, message: str) -> str:
                """Описание стандартного функционала.
                """

                # Переопределение отправителя на второй блок при /start
                if message == "/start":
                    sender.set_step(Sender.STAGE.FORM)
                    return Constant.DIALOGUE.BLOCK.FORM
                answer = self.function(sender, message)
                if answer:
                    return answer
                # Если было введено что-то кроме /start - бот будет реагировать на белиберду
                return Dialogue.get_misunderstanding()

        @staticmethod
        @Functional
        def start(sender: Sender, message: str) -> str:
            """Определение начала диалога. Сценарий не меняется относительно алгоритма по-умолчанию.
            """

            pass

        @staticmethod
        @Functional
        def form(sender: Sender, message: str) -> str:
            """Объект квадратный?
            Да - отправляем ответ бота, перенаправляем на вопрос о наличии ушей.
            Нет - ужас. Заканчиваем диалог. Предупреждаем о коте.
            """

            # То что должно выполнится если условие неверное
            def no_function():
                sender.cats += 1
                sender.save()

            return Dialogue.BLOCK.binary(
                sender, message,
                [sender.STAGE.EARS, Constant.DIALOGUE.BLOCK.EARS],       # Да
                [sender.STAGE.END, Constant.DIALOGUE.BLOCK.FINISH_CAT],  # Нет
                no_func=no_function
            )

        @staticmethod
        @Functional
        def ears(sender: Sender, message: str) -> str:
            """У объекта есть уши?
            Да - ужас. Заканчиваем диалог. Предупреждаем о коте.
            Нет - Также заканчиваем диалог, но говорим про хлеб.
            """

            # То что должно выполнится если условие неверное
            def yes_function():
                sender.cats += 1
                sender.save()

            # То что должно выполнится если условие неверное
            def no_function():
                sender.breads += 1
                sender.save()

            return Dialogue.BLOCK.binary(
                sender, message,
                [Sender.STAGE.END, Constant.DIALOGUE.BLOCK.FINISH_CAT],    # Да
                [Sender.STAGE.END, Constant.DIALOGUE.BLOCK.FINISH_BREAD],  # Нет
                yes_func=yes_function, no_func=no_function
            )

        @staticmethod
        @Functional
        def end(sender: Sender, message: str) -> str:
            """Описание конца диалога. Данный случай - определение кота.
            Если пользователь на данном этапе написал белиберду вместо Start,
            то автоматически перенаправляется в начало без команды /start.
            """

            # Даем медаль за определение кота
            sender.cats += 1
            sender.save()

            # Сразу же переопределяем пользователя в начало
            sender.set_step(Sender.STAGE.FORM)
            return Constant.DIALOGUE.BLOCK.RETURN

        @staticmethod
        def binary(
                sender: Sender, message: str, yes: List[Union[str, str]], no: List[Union[str, str]],
                yes_func=None, no_func=None) -> str:
            """Кастомный обработчик вопросов с бинарными вариантами ответами (да/нет).
            """

            # Получаем результат - конвертирование ответа отправителя под булеву
            data = Dialogue.correct_binary(message)
            if data is None:
                # Неясно что вышло
                return Dialogue.get_misunderstanding()
            if data:
                # Ответ был положительным
                if yes_func:
                    yes_func()
                sender.set_step(yes[0])
                return yes[1]
            else:
                # Ответ был отрицательным
                if no_func:
                    no_func()
                sender.set_step(no[0])
                return no[1]

        @staticmethod
        def get_block(sender: Sender):
            """Определение ассоциаций этапов и обработчиков.
            Получение блока исходя из присвоенного отправителю этапа.
            """

            # Ассоциации
            data = {
                sender.STAGE.START: Dialogue.BLOCK.start,
                sender.STAGE.FORM: Dialogue.BLOCK.form,
                sender.STAGE.EARS: Dialogue.BLOCK.ears,
                sender.STAGE.END: Dialogue.BLOCK.end,
            }

            try:
                # Получение текущего обработчика
                return data[sender.step]
            except KeyError:
                # Определение нового обработчика если текущий не существует
                sender.set_step(sender.STAGE.START)
                return data['start']

    @staticmethod
    def get_answer(sender: Sender, message: str) -> str:
        """Получение сообщения от отправителя, обработка ответа.
        """

        # Получаем необходимый блок, запускаем его
        block = Dialogue.BLOCK.get_block(sender)
        return block(sender, message)

    @staticmethod
    def get_misunderstanding() -> str:
        """Получить одну из реакций непонимания бота.
        """

        return choice(Constant.DIALOGUE.ANSWER.WHAT)

    @staticmethod
    def clean_string(string: str) -> str:
        """Очистка и форматирование строки.
        """

        # Удаляем все кроме букв, переводим все в нижний регистр
        return ''.join(ch for ch in string.lower() if ch.isalpha())

    @staticmethod
    def clean_array(array: list[str]) -> list[str]:
        """Очистка массива строк.
        """

        # Все то же самое что и в clean_string, но с массивами строк
        return [Dialogue.clean_string(string) for string in array]

    @staticmethod
    def need_for_correction(message: str, variants: list[str]) -> bool:
        """Функция проверяет, есть ли сообщение в массиве предложенных вариантов.
        Обычно используется перед исправлением опечаток для оптимизации.
        Принимает сообщение, а также варианты для сравнения.
        Возвращает True, если нуждается в исправлении и не найден в массиве, иначе - False.
        """

        # Очистка данных
        message = Dialogue.clean_string(message)
        variants = Dialogue.clean_array(variants)

        # Возвращение инвертированного значения, чтобы соответствовать названию функции
        return message not in variants

    @staticmethod
    def correct(message: str, variants: list[str]) -> str:
        """Поиск очепяток и их исправление.
        Принимает сообщение, а также варианты для сравнения.
        Отдельно проверяется на нужду в исправлении сообщения.
        """

        # Проверка на нужду в исправлении опечаток
        if not Dialogue.need_for_correction(message, variants):
            return message

        # Очистка сообщения
        original_message = message
        message = Dialogue.clean_string(message)

        # Ищем более подходящий вариант
        suitable = [None, 0]  # Сохраняем в формате [строка, процент]
        for index, variant in enumerate(Dialogue.clean_array(variants)):
            # Определение процента совпадений строк
            output = fuzz.ratio(message, variant)

            # Если процент совпадения приемлемый
            if output >= Constant.ACCEPTABLE_EQUIVALENCE_PERCENT:
                # Если процент совпадения больше приемлемого предыдущего
                if suitable[1] < output:
                    # Сохраняем новые данные
                    suitable = [variants[index], output]

        # Возвращение исправленного варианта
        return suitable[0] if suitable[0] else original_message

    @staticmethod
    def correct_binary(message: str) -> Union[bool, None]:
        """Обертка под correct, однако лишь для бинарных вариантов ответа из массивов ANSWER.YES и ANSWER.NO.
        Ответом является результат принадлежности к какой-либо группе.
        Если первый параметр True - является согласием, если False - отрицанием. Если None - то хренью непонятной.
        """

        # Получение и очистка данных
        correct = Dialogue.correct(message, Constant.DIALOGUE.ANSWER.YES + Constant.DIALOGUE.ANSWER.NO)
        message = Dialogue.clean_string(correct)

        # Определение того, к какой группе относится ответ
        if message in Dialogue.clean_array(Constant.DIALOGUE.ANSWER.YES):
            return True
        if message in Dialogue.clean_array(Constant.DIALOGUE.ANSWER.NO):
            return False
        else:
            return None
