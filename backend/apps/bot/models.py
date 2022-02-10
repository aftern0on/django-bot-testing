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

    class STAGE:
        """Этап отправителя в диалоге с ботом.
        Этап определяет обработчик, которым будет пользоваться бот при реагировании на ответ.
        """

        START = 'start'          # Начальный этап
        FORM = 'form'            # Этап выяснения формы объекта
        EARS = 'ears'            # Этап выяснения наличия у объекта ушей
        END = 'end'      # Конец диалога
        CHOICES = [
            (START, 'Старт'),
            (FORM, 'Форма объекта'),
            (EARS, 'Наличие у объекта ушей'),
            (END, 'Конец диалога')
        ]

    key = models.CharField(verbose_name="Ручной идентификатор", max_length=64)
    step = models.CharField(
        verbose_name="На каком этапе диалога", max_length=128,
        choices=STAGE.CHOICES, default=STAGE.START)
    cats = models.IntegerField(verbose_name="Количество съеденных котов", default=0)
    breads = models.IntegerField(verbose_name="Количество съеденного хлеба", default=0)

    class Meta:
        verbose_name = "Отправитель"
        verbose_name_plural = "Отправители"
        ordering = ["key", "id"]

    def set_step(self, step):
        """Переопределение этапа в диалоге.
        """

        self.step = step
        self.save()

    def __str__(self):
        return f"{self.key}"

