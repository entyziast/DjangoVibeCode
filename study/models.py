from django.core.validators import RegexValidator
from django.db import models


class Subject(models.Model):
    name = models.CharField("название", max_length=255)
    slug = models.SlugField("адрес", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self):
        return self.name


class Card(models.Model):
    id = models.CharField(
        "идентификатор",
        primary_key=True,
        max_length=64,
        validators=[
            RegexValidator(
                regex=r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z",
                message="Используйте строчные латинские буквы, цифры и одиночные дефисы между группами.",
            )
        ],
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="cards",
        verbose_name="предмет",
    )
    topic = models.CharField("тема", max_length=255)
    question = models.TextField("вопрос")
    answer = models.TextField("ответ")
    source_ref = models.TextField("ссылка на исходный материал")

    class Meta:
        ordering = ["id"]
        verbose_name = "карточка"
        verbose_name_plural = "карточки"

    def __str__(self):
        return f"{self.id}: {self.question[:80]}"
