from django.urls import path

from . import views

app_name = "study"

urlpatterns = [
    path("", views.subject_list, name="subjects"),
    path("subjects/<slug:slug>/", views.practice, name="practice"),
    path("subjects/<slug:slug>/cards/<slug:card_id>/", views.card_detail, name="card"),
]
