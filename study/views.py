from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from .models import Card, Subject


@require_GET
def subject_list(request):
    subjects = Subject.objects.annotate(card_count=Count("cards"))
    return render(request, "study/subject_list.html", {"subjects": subjects})


@never_cache
@require_GET
def practice(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    cards = subject.cards.all()
    current_id = request.GET.get("current", "")
    if current_id:
        try:
            Card._meta.get_field("id").clean(current_id, None)
        except ValidationError:
            return HttpResponseBadRequest("Некорректный идентификатор текущей карточки.")
    card = cards.exclude(pk=current_id).order_by("?").first()
    if card is None:
        # No alternative: show the only card, or an empty state if none exist.
        card = cards.order_by("?").first()
    if card is None:
        return render(request, "study/practice.html", {"subject": subject, "card": None})
    # A stable URL keeps refresh and answer disclosure on the same question.
    return redirect("study:card", slug=subject.slug, card_id=card.pk)


@never_cache
@require_GET
def card_detail(request, slug, card_id):
    subject = get_object_or_404(Subject, slug=slug)
    card = get_object_or_404(Card, subject=subject, pk=card_id)
    return render(
        request,
        "study/practice.html",
        {"subject": subject, "card": card, "card_count": subject.cards.count()},
    )
