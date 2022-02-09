from django.db import models


class Message(models.Model):
    """Модель сообщения и ответ бота на него.
    """

    sender = models.ForeignKey(verbose_name="Отправитель", on_delete=models.CASCADE, to="Sender")
    text = models.CharField(verbose_name="Текст сообщения", max_length=255)
    answer = models.CharField(verbose_name="Ответ на сообщение", max_length=255)
    previous = models.ForeignKey(verbose_name="Предыдущее сообщение", on_delete=models.CASCADE, to='Message',
                                 null=True, blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["sender", "id"]

    def __str__(self):
        return f"{self.sender}: {self.text}"


class Sender(models.Model):
    """Модель записи отправителя.
    """

    class STEP:
        STEP_ONE = 'one'
        STEP_TWO = 'two'
        STEP_FINISH = 'finish'
        CHOICES = [
            (STEP_TWO, 'Первый шаг'),
            (STEP_TWO, 'Второй шаг'),
            (STEP_FINISH, 'Финиш')]

    key = models.CharField(verbose_name="Ручной идентификатор отправителя", max_length=64)
    step = models.CharField(verbose_name="Какой опрос проходит отправитель", choices=STEP.CHOICES, max_length=64)
    cats = models.IntegerField(verbose_name="Количество съеденных котов", default=0)
    breads = models.IntegerField(verbose_name="Количество съеденного хлеба", default=0)

    class Meta:
        verbose_name = "Отправитель"
        verbose_name_plural = "Отправители"
        ordering = ["key", "id"]

    def __str__(self):
        return f"{self.key}"

