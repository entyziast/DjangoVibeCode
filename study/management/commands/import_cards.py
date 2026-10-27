from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction

from study.importing import load_cards
from study.models import Card, Subject


class Command(BaseCommand):
    help = "Импортирует JSON-карточки целиком, обновляя существующие записи по id."
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            nargs="?",
            default=str(settings.BASE_DIR / "data" / "questions.json"),
            help="Путь к JSON-массиву в UTF-8 (по умолчанию data/questions.json).",
        )
        parser.add_argument(
            "--subject",
            default="operating-systems",
            help="Адрес существующего предмета (по умолчанию operating-systems).",
        )

    def handle(self, *args, **options):
        try:
            records = load_cards(options["path"])
        except (OSError, ValueError, UnicodeError) as exc:
            raise CommandError(f"Импорт отменён до записи в базу: {exc}") from exc

        created_count = 0
        updated_count = 0
        try:
            with transaction.atomic():
                # Serialize imports for this subject until the whole batch commits.
                subject = Subject.objects.select_for_update().get(slug=options["subject"])
                ids = [record["id"] for record in records]
                if Card.objects.filter(pk__in=ids).exclude(subject=subject).exists():
                    raise CommandError(
                        "Импорт отменён: один из id уже принадлежит другому предмету. "
                        "Используйте глобально уникальные идентификаторы."
                    )
                for record in records:
                    defaults = {key: value for key, value in record.items() if key != "id"}
                    _, created = Card.objects.update_or_create(
                        id=record["id"],
                        subject=subject,
                        defaults=defaults,
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
        except Subject.DoesNotExist as exc:
            raise CommandError(
                "Предмет не найден. Примените миграции или создайте предмет в админке."
            ) from exc
        except DatabaseError as exc:
            raise CommandError(
                "Ошибка базы данных: весь импорт отменён. Проверьте подключение и миграции."
            ) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершён. Создано: {created_count}; обновлено: {updated_count}; "
                f"всего обработано: {len(records)}."
            )
        )
