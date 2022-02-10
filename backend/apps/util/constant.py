class Constant:
    """Проектные константы.
    """

    # Приемлемый процент совпадения строк при поиске ошибок
    ACCEPTABLE_EQUIVALENCE_PERCENT = 50

    class DIALOGUE:
        """Диалоговые сообщения.
        """

        class BLOCK:
            """Блоковые сообщения.
            """

            FORM = "Привет! Я помогу отличить кота от хлеба! Объект перед тобой квадратный?"
            EARS = "У него есть уши?"
            FINISH_CAT = "Это кот, а не хлеб! Не ешь его!"
            FINISH_BREAD = "Это хлеб, а не кот! Ешь его!"
            RETURN = "Давай-ка начнем сначала. Объект перед тобой квадратный?"

        class ANSWER:
            """Варианты ответов.
            """

            YES = ["конечно", "ага", "пожалуй"]
            NO = ["нет, конечно", "ноуп", "найн"]
            WHAT = ["Чего-чего?", "Я тебя не понял, повтори", "Я не расслышал", "Повтори-ка"]
