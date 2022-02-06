from django.db import models


class Message(models.Model):
    """Модель сообщения и ответ бота на него.
    """

    write = models.ForeignKey(verbose_name="Пользователь", on_delete=models.CASCADE, to="Write")
    text = models.CharField(verbose_name="Текст сообщения", max_length=255)
    answer = models.CharField(verbose_name="Ответ на сообщение", max_length=255)
    previous = models.ForeignKey(verbose_name="Предыдущее сообщение", on_delete=models.CASCADE, to='Message',
                                 null=True, blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["write", "id"]

    def __str__(self):
        return f"{self.write}: {self.text}"


class Write(models.Model):
    """Модель записи пользователя.
    """

    class STEP:
        STEP_ONE = 'one'
        STEP_TWO = 'two'
        STEP_FINISH = 'finish'
        CHOICES = [
            (STEP_TWO, 'Первый шаг'),
            (STEP_TWO, 'Второй шаг'),
            (STEP_FINISH, 'Финиш')]

    key = models.CharField(verbose_name="Ручной идентификатор пользователя", max_length=64)
    step = models.CharField(verbose_name="Какой опрос проходит пользователь", choices=STEP.CHOICES, max_length=64)
    cats = models.IntegerField(verbose_name="Количество съеденных котов", default=0)
    breads = models.IntegerField(verbose_name="Количество съеденного хлеба", default=0)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["key", "id"]

    def __str__(self):
        return f"{self.key}"

