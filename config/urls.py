from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("study.urls")),
]

admin.site.site_header = "Подготовка к экзаменам"
admin.site.site_title = "Управление материалами"
admin.site.index_title = "Предметы и карточки"
