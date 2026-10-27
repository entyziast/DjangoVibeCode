import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="название")),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="адрес")),
            ],
            options={
                "verbose_name": "предмет",
                "verbose_name_plural": "предметы",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                ("id", models.CharField(
                    max_length=64,
                    primary_key=True,
                    serialize=False,
                    validators=[django.core.validators.RegexValidator(
                        message="Используйте строчные латинские буквы, цифры и одиночные дефисы между группами.",
                        regex=r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z",
                    )],
                    verbose_name="идентификатор",
                )),
                ("topic", models.CharField(max_length=255, verbose_name="тема")),
                ("question", models.TextField(verbose_name="вопрос")),
                ("answer", models.TextField(verbose_name="ответ")),
                ("source_ref", models.TextField(verbose_name="ссылка на исходный материал")),
                ("subject", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="cards",
                    to="study.subject",
                    verbose_name="предмет",
                )),
            ],
            options={
                "verbose_name": "карточка",
                "verbose_name_plural": "карточки",
                "ordering": ["id"],
            },
        ),
    ]
