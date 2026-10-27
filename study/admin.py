from django.contrib import admin

from .models import Card, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "topic", "question"]
    list_filter = ["subject", "topic"]
    search_fields = ["id", "topic", "question", "answer"]
    list_select_related = ["subject"]

    def get_readonly_fields(self, request, obj=None):
        return ["id"] if obj else []
