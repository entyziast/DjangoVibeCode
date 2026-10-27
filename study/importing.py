import json
from pathlib import Path

from django.core.exceptions import ValidationError

from .models import Card

CARD_FIELDS = {"id", "topic", "question", "answer", "source_ref"}


def unique_object(pairs):
    """Do not silently discard repeated keys while decoding JSON."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Повторяющееся поле JSON: {key}.")
        result[key] = value
    return result


def load_cards(path):
    """Validate the entire file without database access or text normalization."""
    records = json.loads(
        Path(path).read_text(encoding="utf-8-sig"),
        object_pairs_hook=unique_object,
    )
    if not isinstance(records, list) or not records:
        raise ValueError("Ожидается непустой JSON-массив карточек.")

    seen_ids = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict) or set(record) != CARD_FIELDS:
            raise ValueError(
                f"Карточка {index}: нужны ровно поля id, topic, question, answer, source_ref."
            )
        for field, value in record.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Карточка {index}: поле {field} должно быть непустой строкой.")
            if "\x00" in value:
                raise ValueError(f"Карточка {index}: поле {field} содержит нулевой символ.")
            try:
                value.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ValueError(
                    f"Карточка {index}: поле {field} содержит некорректный Unicode."
                ) from exc

        # Validate field lengths and the ID format, but not database uniqueness:
        # an existing ID is expected on a repeated import.
        try:
            Card(**record).clean_fields(exclude=["subject"])
        except ValidationError as exc:
            raise ValueError(f"Карточка {index}: {'; '.join(exc.messages)}") from exc
        if record["id"] in seen_ids:
            raise ValueError(f"Карточка {index}: повторяющийся id {record['id']}.")
        seen_ids.add(record["id"])

    return records
